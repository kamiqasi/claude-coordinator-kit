#!/usr/bin/env python3
"""Checks the kit: python3 tests/check_kit.py (standard library only; exit 1 on any failure).

- every skill (and the setup example) has frontmatter with name, description and
  disable-model-invocation: true;
- names are unique and match their folders;
- every skill tells the reader to read the setup file;
- every `setup.<key>` a skill uses is defined in the setup example's YAML block;
- every relative link in a skill (../<skill>/SKILL.md) and in docs/ (HTML and CSS) resolves within the repo;
- the site has no <script>, animates only with a prefers-reduced-motion rule that stills the hero scene, has the scene's
  windows, folder and carrier birds, and ships any font with its licence;
- the plugin and marketplace manifests are JSON and agree on the plugin's name and version;
- the kit has exactly the EXPECTED skills below, and the README table, the site's cards and the marketplace
  description each name every one of them.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SETUP = ROOT / "coordinator-setup.example" / "SKILL.md"
SETUP_PATHS = (".claude/skills/coordinator-setup/SKILL.md", "~/.claude/skills/coordinator-setup/SKILL.md")
EXPECTED = ("send", "inbox", "review-pr", "merged", "next", "wip", "while-we-wait", "walkthrough", "handoff")
KEY_USE = re.compile(r"`setup\.([a-z_]+(?:\.[a-z_]+)*)`")

checks = 0
failures: list[str] = []


def check(ok: bool, what: str) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(what)


def frontmatter(path: Path) -> dict[str, str] | None:
    """The `key: value` lines between the opening and closing `---`; None if there are none."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    out = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def yaml_keys(text: str) -> set[str]:
    """Dotted key paths from the first ```yaml block, by indentation (mappings only; enough for this file)."""
    m = re.search(r"```yaml\n(.*?)```", text, re.S)
    if not m:
        return set()
    keys, stack = set(), []  # stack of (indent, key)
    for line in m.group(1).splitlines():
        km = re.match(r"^(\s*)([a-z_]+):(?:\s|$)", line)
        if not km:
            continue
        indent = len(km.group(1))
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, km.group(2)))
        keys.add(".".join(k for _, k in stack))
        # inline mapping, e.g. weights: {impact: 3, urgency: 2}
        inline = re.search(r":\s*\{(.*)\}\s*(#.*)?$", line)
        if inline:
            for sub in re.findall(r"([a-z_]+)\s*:", inline.group(1)):
                keys.add(".".join(k for _, k in stack) + "." + sub)
    return keys


def skill_files() -> list[Path]:
    return sorted(SKILLS.glob("*/SKILL.md"))


def check_skills() -> None:
    files = skill_files()
    check(len(files) > 0, "skills/: no skills found")
    names: dict[str, Path] = {}
    for path in files + [SETUP]:
        rel = path.relative_to(ROOT)
        fm = frontmatter(path)
        check(fm is not None, f"{rel}: no frontmatter")
        if fm is None:
            continue
        for key in ("name", "description"):
            check(bool(fm.get(key)), f"{rel}: frontmatter lacks {key}")
        check(fm.get("disable-model-invocation") == "true", f"{rel}: needs disable-model-invocation: true")
        name = fm.get("name", "")
        expected = "coordinator-setup" if path == SETUP else path.parent.name
        check(name == expected, f"{rel}: name {name!r} doesn't match its folder ({expected!r})")
        check(name not in names, f"{rel}: name {name!r} also used by {names.get(name)}")
        names[name] = rel
        check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) is not None, f"{rel}: name {name!r} isn't kebab-case")
    check("coordinator-setup" not in [p.parent.name for p in files],
          "skills/coordinator-setup: the filled-in setup file must not ship in skills/")


def check_setup_refs() -> None:
    defined = yaml_keys(SETUP.read_text(encoding="utf-8"))
    check(len(defined) > 10, "coordinator-setup.example: no YAML keys found")
    for path in skill_files():
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        check(all(p in text for p in SETUP_PATHS), f"{rel}: doesn't tell the reader to read the setup file")
        for key in sorted(set(KEY_USE.findall(text))):
            check(key in defined, f"{rel}: uses setup.{key}, which the setup example doesn't define")


def check_skill_links() -> None:
    for path in skill_files():
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"`(\.\./[a-z0-9-]+/SKILL\.md)`", text):
            check((path.parent / target).resolve().is_file(),
                  f"{path.relative_to(ROOT)}: {target} doesn't resolve")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "script":
            self.scripts += 1
        for attr in ("href", "src"):
            if a.get(attr):
                self.refs.append(a[attr])


def check_docs() -> None:
    pages = sorted((ROOT / "docs").glob("*.html"))
    check(bool(pages), "docs/: no HTML pages")
    for page in pages:
        rel = page.relative_to(ROOT)
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        check(parser.scripts == 0, f"{rel}: has a <script> (the site is HTML and CSS only)")
        for ref in parser.refs:
            parts = urlsplit(ref)
            if parts.scheme in ("http", "https", "mailto"):
                check(parts.scheme != "http", f"{rel}: {ref} isn't https")
                continue
            if ref.startswith("#"):
                check(ref[1:] in parser.ids, f"{rel}: anchor {ref} has no target")
                continue
            if ref.startswith("url(") or ref.startswith("data:"):
                continue
            target = (page.parent / parts.path).resolve()
            check(target.is_file() and ROOT in target.parents, f"{rel}: {ref} doesn't resolve within the repo")
    css = ROOT / "docs" / "style.css"
    if css.is_file():
        text = css.read_text(encoding="utf-8")
        check("@import" not in text and not re.search(r"url\(\s*['\"]?https?:", text),
              "docs/style.css: loads something from outside the repo")
        check("prefers-color-scheme: dark" in text, "docs/style.css: no dark scheme")
        if "animation" in text:
            check("prefers-reduced-motion: reduce" in text, "docs/style.css: animates without a prefers-reduced-motion rule")
            at = text.find("prefers-reduced-motion: reduce")
            block = text[at:at + 600] if at >= 0 else ""
            check(".scene *" in block and "animation: none" in block,
                  "docs/style.css: the reduced-motion rule doesn't switch off every animation in the hero scene")
        for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)", text):
            if ref.startswith("data:"):
                continue
            target = (css.parent / ref).resolve()
            check(target.is_file() and ROOT in target.parents, f"docs/style.css: {ref} doesn't resolve within the repo")
    fonts = sorted((ROOT / "docs" / "fonts").glob("*.woff2")) + sorted((ROOT / "docs" / "fonts").glob("*.ttf"))
    if fonts:
        licences = [p for p in (ROOT / "docs" / "fonts").iterdir() if p.name.upper().startswith(("OFL", "LICENSE"))]
        check(bool(licences), "docs/fonts/: a font without its licence file next to it")


def check_manifests() -> None:
    try:
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        check(False, f".claude-plugin: {e}")
        return
    check(bool(plugin.get("name")), "plugin.json: no name")
    check(not plugin.get("name", "").startswith("claude-"), "plugin.json: names starting claude- are refused")
    for key in ("name", "owner", "plugins"):
        check(key in market, f"marketplace.json: no {key}")
    entries = market.get("plugins") or []
    check(any(e.get("name") == plugin.get("name") and e.get("source") in ("./", ".") for e in entries),
          "marketplace.json: doesn't list this repo's plugin with source ./")
    check(all(e.get("version") == plugin.get("version") for e in entries if e.get("name") == plugin.get("name")),
          "marketplace.json and plugin.json disagree on the version")


def check_commands() -> None:
    names = sorted(p.parent.name for p in skill_files())
    check(names == sorted(EXPECTED), f"skills/: expected {sorted(EXPECTED)}, found {names}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| `/([a-z-]+)` \|", readme, re.M)
    check(sorted(rows) == sorted(EXPECTED), f"README.md: the commands table lists {rows}")
    words = {9: "nine"}
    count = words.get(len(EXPECTED), str(len(EXPECTED)))
    check(f"{count} skills" in readme, f"README.md: doesn't say {count} skills")
    site = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    cards = re.findall(r"<li><h3><code>/([a-z-]+)</code></h3>", site)
    for part in ('class="scene"', 'class="win win-coord"', 'class="win win-work"', 'class="cote"', 'class="bird fly-a"', 'class="bird fly-b"'):
        check(part in site, f"docs/index.html: the hero scene lacks {part}")
    check(sorted(cards) == sorted(EXPECTED), f"docs/index.html: the cards are {cards}")
    check(f"{count.capitalize()} commands</h2>" in site, f"docs/index.html: the heading doesn't say {count.capitalize()} commands")
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    desc = " ".join(e.get("description", "") for e in market.get("plugins", []))
    missing = [n for n in EXPECTED if f"/{n}" not in desc]
    check(not missing and desc.lower().startswith(count), f"marketplace.json: description misses {missing} or the count")


def main() -> int:
    check_skills()
    check_commands()
    check_setup_refs()
    check_skill_links()
    check_docs()
    check_manifests()
    for f in failures:
        print("FAIL", f)
    print(f"check_kit: {'OK' if not failures else 'FAILED'} ({checks} checks, {len(failures)} failed)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
