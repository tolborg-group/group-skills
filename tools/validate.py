#!/usr/bin/env python3
"""Check the marketplace, plugin manifests and skills for common mistakes.

Standard library only, so it runs anywhere with Python 3.
Exit code is non-zero if any error is found.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# A "!" directly followed by a backtick runs a shell command when the skill
# loads, even inside code blocks. Flag it so it is never added by accident.
INJECTION_RE = re.compile(r"!`")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load_json(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        err(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as e:
        err(f"{path.relative_to(ROOT)}: invalid JSON ({e})")
    return None


def frontmatter(text):
    """Return top-level `key: value` pairs from YAML frontmatter, or None.

    Handles plain one-line values, block scalars (`key: >` / `key: |`) and
    values continued on indented lines. Not a full YAML parser.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields, key = {}, None
    for line in text[4:end].splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if re.match(r"^[>|][+-]?$", value):
                value = ""  # block scalar: the text is on the following lines
            fields[key] = value
        elif key and line[:1] in (" ", "\t") and line.strip():
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return {k: v.strip("\"'") for k, v in fields.items()}


def check_skill(skill_md):
    rel = skill_md.relative_to(ROOT)
    text = skill_md.read_text()
    fm = frontmatter(text)
    if fm is None:
        err(f"{rel}: missing or malformed frontmatter")
        return
    name = fm.get("name")
    if not name:
        err(f"{rel}: frontmatter has no 'name'")
    elif name != skill_md.parent.name:
        err(f"{rel}: name '{name}' must match folder '{skill_md.parent.name}'")
    elif not NAME_RE.match(name):
        err(f"{rel}: name '{name}' should be lowercase-with-hyphens")
    desc = fm.get("description", "")
    if not desc:
        err(f"{rel}: frontmatter has no 'description'")
    elif len(desc) > 1024:
        err(f"{rel}: description is over 1024 characters")
    elif len(desc) < 40:
        warn(f"{rel}: description is very short; say what it does and when to use it")
    for i, line in enumerate(text.splitlines(), 1):
        if INJECTION_RE.search(line) and "validate: allow-injection" not in text:
            warn(f"{rel}:{i}: '!' followed by a backtick runs a command when the "
                 "skill loads. If intended, add the comment "
                 "<!-- validate: allow-injection --> to the skill.")
    lines = text.count("\n")
    if lines > 500:
        warn(f"{rel}: {lines} lines; consider moving detail into reference files")


def main():
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if market is None:
        return
    for field in ("name", "owner", "plugins"):
        if field not in market:
            err(f"marketplace.json: missing '{field}'")

    listed = set()
    for p in market.get("plugins", []):
        pname, source = p.get("name"), p.get("source")
        if not pname or not source:
            err(f"marketplace.json: plugin entry needs 'name' and 'source': {p}")
            continue
        listed.add(pname)
        if not isinstance(source, str):
            continue  # external plugin (github/git source); nothing local to check
        pdir = (ROOT / source).resolve()
        if not pdir.is_dir():
            err(f"marketplace.json: source for '{pname}' not found: {source}")
            continue
        manifest = load_json(pdir / ".claude-plugin" / "plugin.json")
        if manifest and manifest.get("name") != pname:
            err(f"{pdir.relative_to(ROOT)}: plugin.json name "
                f"'{manifest.get('name')}' != marketplace name '{pname}'")
        skills = sorted((pdir / "skills").glob("*/SKILL.md"))
        if not skills:
            warn(f"plugin '{pname}' has no skills yet")
        for s in skills:
            check_skill(s)

    plugins_dir = ROOT / "plugins"
    if plugins_dir.is_dir():
        for d in sorted(plugins_dir.iterdir()):
            if d.is_dir() and d.name not in listed:
                err(f"plugins/{d.name} exists but is not listed in marketplace.json")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error:   {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
    sys.exit(1 if errors else 0)
