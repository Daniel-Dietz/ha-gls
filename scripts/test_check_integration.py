"""Regression tests for the standalone repository policy checker."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.check_integration import (
    metadata_errors,
    translation_shape,
    undocumented,
    valid_version,
    version_key,
)


class PolicyTests(unittest.TestCase):
    """Exercise metadata, version ordering and nested definition detection."""

    def test_version_syntax(self) -> None:
        """Reject prefixed, incomplete or noncanonical version strings."""
        for value in ("2.0.1", "2.1.0-beta.1", "3.0.0-rc.2"):
            assert valid_version(value)
        for value in ("v2.0.1", "2.01.0", "2.0", "2.0.1-beta.0", None):
            assert not valid_version(value)

    def test_version_ordering(self) -> None:
        """Stable versions and subsequent majors sort after prereleases."""
        versions = ["2.0.1-alpha.1", "2.0.1-beta.2", "2.0.1-rc.1", "2.0.1", "3.0.0"]
        assert sorted(versions, key=version_key) == versions

    def test_nested_and_async_definitions(self) -> None:
        """Find undocumented private and nested methods, not empty modules."""
        code = '"""Module."""\nclass A:\n    """Class."""\n    async def _run(self):\n        def inner():\n            return 1\n        return inner()\n'
        assert [name for name, _, _ in undocumented(code)] == ["A._run", "A._run.inner"]
        assert undocumented("") == []

    def test_fingerprint_tracks_changed_code(self) -> None:
        """An existing undocumented definition cannot change under the baseline."""
        original = '"""Module."""\ndef f():\n    return 1\n'
        shifted = "\n" + original
        changed = original.replace("return 1", "return 2")
        assert undocumented(original)[0][1] == undocumented(shifted)[0][1]
        assert undocumented(original)[0][1] != undocumented(changed)[0][1]

    def test_translation_placeholders(self) -> None:
        """Allow translated text but detect missing or repeated placeholders."""
        original = {"message": "Hello {name}"}
        assert translation_shape(original) == translation_shape(
            {"message": "Hallo {name}"}
        )
        assert translation_shape(original) != translation_shape(
            {"message": "Hallo {name} {name}"}
        )
        assert translation_shape(original) != translation_shape({"message": "Hallo"})

    def test_release_metadata(self) -> None:
        """Enforce tag, changelog, increasing version, and HACS compatibility."""
        with TemporaryDirectory() as directory:
            root = Path(directory)
            component = root / "custom_components" / "sample"
            component.mkdir(parents=True)
            (component / "manifest.json").write_text(
                json.dumps({"domain": "sample", "version": "2.0.1"})
            )
            (root / "hacs.json").write_text(
                json.dumps(
                    {
                        "homeassistant": "2025.12.0",
                        "zip_release": True,
                        "filename": "sample.zip",
                        "content_in_root": False,
                    }
                )
            )
            (root / "CHANGELOG.md").write_text("## [2.0.1]\n")
            assert metadata_errors(root, "2.0.1", "2.0.0") == []
            assert metadata_errors(root, "v2.0.1", "2.0.0")
            assert metadata_errors(root, "2.0.1", "2.0.1")
            assert metadata_errors(root, "2.0.2", "2.0.0")


if __name__ == "__main__":
    unittest.main()
