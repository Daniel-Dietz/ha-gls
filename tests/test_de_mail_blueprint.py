"""Exercise the actual Germany mail blueprint templates with HA rendering."""

from pathlib import Path
from types import SimpleNamespace

from homeassistant.helpers.template import Template
import pytest
import yaml


class _BlueprintLoader(yaml.SafeLoader):
    """Resolve blueprint input references to their input names for inspection."""


_BlueprintLoader.add_constructor(
    "!input", lambda loader, node: loader.construct_scalar(node)
)


@pytest.fixture
def blueprint():
    """Load the shipped automation, including the actual Jinja templates."""
    path = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "blueprints"
        / "gls_de_mail_tracking.yaml"
    )
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_BlueprintLoader)


def _variables(sender="dispatch@example.test", postcode="01234", **message):
    """Supply synthetic IMAP event variables and explicit blueprint inputs."""
    return {
        "trigger": SimpleNamespace(
            event=SimpleNamespace(data={"sender": sender, **message})
        ),
        "allowed_senders": " DISPATCH@example.test ",
        "postal_code": postcode,
    }


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        (
            {"text": "Paketnummer: 01234567890\nTrack-ID: zx90abcd"},
            ["01234567890", "ZX90ABCD"],
        ),
        (
            {
                "subject": "GLS Paketnummer: 012345678901",
                "text": (
                    "https://www.gls-pakete.de/reach-sendungsverfolgung"
                    "?match=012345678901&other=value"
                ),
            },
            ["012345678901"],
        ),
        (
            {"text": "https://gls-pakete.de/sendungsverfolgung?match=ZX90ABCD"},
            ["ZX90ABCD"],
        ),
        (
            {"text": "https://gls-group.com/GROUP/en/parcel-tracking?match=ZX90ABCD"},
            ["ZX90ABCD"],
        ),
        (
            {"text": "Order 01234567890\nTelefon: 012345678901\nTrack-ID: ABCDEFGH"},
            [],
        ),
        ({"text": "Track-ID: 12345678\nPaketnummer: 012345678901234"}, []),
        (
            {
                "text": (
                    "https://gls-pakete.de.example.test/sendungsverfolgung"
                    "?match=01234567890"
                )
            },
            [],
        ),
        ({"text": "Paketnummer: 01234567890%31\nTrack-ID: ZX90ABCD_more"}, []),
        ({"text": None, "subject": None}, []),
    ],
)
async def test_tracking_codes(hass, blueprint, message, expected):
    """Only explicit labels or recognized tracking links produce codes."""
    template = blueprint["actions"][0]["variables"]["tracking_codes"]
    assert Template(template, hass).async_render(_variables(**message)) == expected


@pytest.mark.parametrize(
    ("sender", "postcode", "allowed"),
    [
        ("dispatch@example.test", "01234", True),
        (" DISPATCH@example.test ", "01234", True),
        ("dispatch@example.test.evil", "01234", False),
        ("", "01234", False),
        (None, "01234", False),
        ("dispatch@example.test", "1234", False),
        ("dispatch@example.test", "123456", False),
        ("dispatch@example.test", "1234X", False),
        ("dispatch@example.test", 12345, False),
    ],
)
async def test_sender_and_postcode_gate(hass, blueprint, sender, postcode, allowed):
    """Fail closed unless the sender and German postcode match."""
    template = blueprint["conditions"][0]["value_template"]
    assert Template(template, hass).async_render(_variables(sender, postcode)) is allowed


def test_event_scope_and_service(blueprint):
    """Only new events from the selected IMAP folder reach the GLS service."""
    trigger = blueprint["triggers"][0]
    assert trigger["event_type"] == "imap_content"
    assert trigger["event_data"] == {
        "username": "mailbox",
        "folder": "folder",
        "initial": True,
    }
    action = blueprint["actions"][1]["repeat"]["sequence"][0]
    assert action["action"] == "gls.track_parcel"
    assert action["data"] == {
        "tracking_code": "{{ repeat.item }}",
        "postal_code": "postal_code",
    }
    assert blueprint["trace"]["stored_traces"] == 0
