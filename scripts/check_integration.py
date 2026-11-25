"""Validate version metadata, translations and Python documentation without HA imports."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# Temporary, immutable test-documentation baseline. Remove when #39 is closed.
LEGACY_TEST_REF = "87305adc947945263d8f4e405bea4e25153fa223"
VERSION = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(alpha|beta|rc)\.([1-9][0-9]*))?"
)
HA_VERSION = re.compile(r"20[0-9]{2}\.(?:[1-9]|1[0-2])\.(?:0|[1-9][0-9]*)")
PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z_0-9]*)\}")


def read_object(path: Path) -> dict:
    """Read a JSON object; reject other top-level types."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: expected a JSON object")
    return value


def valid_version(value: object) -> bool:
    """Accept the project's canonical HA-compatible SemVer subset."""
    return isinstance(value, str) and VERSION.fullmatch(value) is not None


def version_key(value: str) -> tuple[int, int, int, int, int]:
    """Order canonical versions, with stable after all prereleases."""
    match = VERSION.fullmatch(value)
    if match is None:
        raise ValueError("invalid integration version")
    major, minor, patch, stage, serial = match.groups()
    return (
        int(major),
        int(minor),
        int(patch),
        {"alpha": 0, "beta": 1, "rc": 2, None: 3}[stage],
        int(serial or 0),
    )


def metadata_errors(
    root: Path, release_tag: str | None = None, previous_version: str | None = None
) -> list[str]:
    """Check integration packaging and, when requested, release invariants."""
    errors = []
    manifests = sorted((root / "custom_components").glob("*/manifest.json"))
    if len(manifests) != 1:
        return ["Expected exactly one integration manifest in the HACS repository."]
    path = manifests[0]
    manifest = read_object(path)
    hacs = read_object(root / "hacs.json")
    domain = path.parent.name
    version = manifest.get("version")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", domain) or manifest.get("domain") != domain:
        errors.append("Manifest domain must match the integration directory.")
    if not valid_version(version):
        errors.append("manifest.version must use canonical SemVer (see standard).")
    minimum = hacs.get("homeassistant")
    if not isinstance(minimum, str) or not HA_VERSION.fullmatch(minimum):
        errors.append("hacs.homeassistant must declare a canonical HA Core version.")
    if hacs.get("zip_release") is True and hacs.get("filename") != f"{domain}.zip":
        errors.append("HACS ZIP filename must match the integration domain.")
    if hacs.get("content_in_root") is not False:
        errors.append(
            "HACS integration files must be under custom_components/<domain>."
        )
    if release_tag is not None:
        if not valid_version(release_tag) or release_tag != version:
            errors.append("Release tag must equal manifest.version exactly.")
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        if f"## [{release_tag}]" not in changelog.splitlines():
            errors.append("Changelog must contain the exact release-version heading.")
    if previous_version is not None:
        if not valid_version(previous_version) or not valid_version(version):
            errors.append("Current and previous versions must be valid SemVer.")
        elif version_key(version) <= version_key(previous_version):
            errors.append("The integration version must increase for a new release.")
    return errors


def translation_shape(value: object, path: tuple[str, ...] = ()) -> dict:
    """Return leaf keys, value types and placeholder multiplicities."""
    if isinstance(value, dict):
        result = {}
        for key, child in value.items():
            result.update(translation_shape(child, (*path, key)))
        return result
    placeholders = (
        tuple(sorted(PLACEHOLDER.findall(value))) if isinstance(value, str) else ()
    )
    return {path: (type(value).__name__, placeholders)}


def translation_errors(root: Path) -> list[str]:
    """Require locale keys and formatting placeholders to match strings.json."""
    errors = []
    for manifest in sorted((root / "custom_components").glob("*/manifest.json")):
        directory = manifest.parent
        strings = directory / "strings.json"
        translations = sorted((directory / "translations").glob("*.json"))
        if not strings.exists() and not translations:
            continue
        if not strings.exists() or not translations:
            errors.append(f"{directory.name}: missing strings.json or translations.")
            continue
        expected = translation_shape(read_object(strings))
        for locale in translations:
            actual = translation_shape(read_object(locale))
            errors.extend(
                f"{locale.name}: translation mismatch at {'.'.join(key)}"
                for key in sorted(expected.keys() | actual.keys())
                if expected.get(key) != actual.get(key)
            )
    return errors


def undocumented(source: str) -> list[tuple[str, str, int]]:
    """Find undocumented definitions, including private and nested functions.

    The fingerprint ignores line positions but includes the definition body.
    Consequently unchanged legacy test definitions can be recognized without
    allowing changed or newly created undocumented definitions.
    """
    tree = ast.parse(source)
    result = []

    def visit(node: ast.AST, scope: tuple[str, ...] = ()) -> None:
        """Walk AST definitions and retain their qualified names."""
        if isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            if not isinstance(node, ast.Module):
                scope = (*scope, node.name)
            name = ".".join(scope) or "<module>"
            if node.body and not (ast.get_docstring(node) or "").strip():
                fingerprint = hashlib.sha256(ast.dump(node).encode()).hexdigest()
                result.append((name, fingerprint, getattr(node, "lineno", 1)))
        for child in ast.iter_child_nodes(node):
            visit(child, scope)

    visit(tree)
    return result


def legacy_source(root: Path, ref: str, path: str) -> str | None:
    """Read an immutable Git baseline file; new files have no grandfathering."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def documentation_errors(root: Path, legacy_ref: str | None) -> tuple[list[str], int]:
    """Reject every runtime/tooling gap and every new/changed test gap."""
    errors = []
    grandfathered = 0
    if legacy_ref is not None:
        subprocess.run(
            ["git", "cat-file", "-e", f"{legacy_ref}^{{commit}}"],
            cwd=root,
            capture_output=True,
            check=True,
        )
    for folder in ("custom_components", "scripts", "tests"):
        for path in sorted((root / folder).rglob("*.py")):
            relative = path.relative_to(root).as_posix()
            missing = undocumented(path.read_text(encoding="utf-8"))
            if not missing:
                continue
            baseline = (
                legacy_source(root, legacy_ref, relative)
                if folder == "tests" and legacy_ref
                else None
            )
            allowed = (
                Counter((name, digest) for name, digest, _ in undocumented(baseline))
                if baseline is not None
                else Counter()
            )
            for name, digest, line in missing:
                if allowed[(name, digest)]:
                    allowed[(name, digest)] -= 1
                    grandfathered += 1
                else:
                    errors.append(f"{relative}:{line}: missing docstring: {name}")
    return errors, grandfathered


def main() -> int:
    """Run all policy checks and return nonzero for any failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-tag", help="Validate a proposed exact release tag.")
    parser.add_argument(
        "--previous-version", help="Require a strictly newer integration version."
    )
    parser.add_argument(
        "--strict-tests", action="store_true", help="Reject legacy test gaps as well."
    )
    args = parser.parse_args()
    try:
        errors = metadata_errors(ROOT, args.release_tag, args.previous_version)
        errors.extend(translation_errors(ROOT))
        doc_errors, legacy_count = documentation_errors(
            ROOT, None if args.strict_tests else LEGACY_TEST_REF
        )
        errors.extend(doc_errors)
    except (
        OSError,
        TypeError,
        ValueError,
        SyntaxError,
        subprocess.CalledProcessError,
    ) as err:
        sys.stderr.write(
            f"Engineering policy check failed: {type(err).__name__}: {err}\n"
        )
        return 1
    for error in errors:
        sys.stderr.write(f"{error}\n")
    if errors:
        return 1
    sys.stdout.write(
        f"PASS: metadata, translations, production/tooling docstrings; "
        f"{legacy_count} unchanged legacy test documentation gaps (#39).\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
