"""Generate markdown twins, llms-full.txt, and the agent-skills index into the build output.

Run after `zola build`: python3 scripts/generate_md_twins.py content/ public/
"""

import hashlib
import json
import re
import sys
from pathlib import Path

BASE_URL = "https://pasqualaw.com"
SKILL_REL = "skills/pasqualaw-site/SKILL.md"

HTML_TAG = re.compile(r"<[^>]+>")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n?", text, re.DOTALL)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        kv = re.match(r'^(\w+)\s*=\s*"?([^"]*)"?\s*$', line)
        if kv:
            meta[kv.group(1)] = kv.group(2)
    return meta, text[match.end():]


def build_twin(meta: dict[str, str], body: str, canonical: str) -> str:
    title = meta.get("title", "Meghan Pasqua | Attorney at Law")
    description = meta.get("description", "")
    front = f'---\ntitle: "{title}"\ndescription: "{description}"\ncanonical: "{canonical}"\n---\n'
    return f"{front}\n# {title}\n\n{body}\n"


def extract_rendered_text(out_dir: Path, slug: str) -> str:
    """Fallback for pages built mostly in templates: extract text from rendered HTML."""
    html_path = out_dir / ("index.html" if slug == "index" else f"{slug}/index.html")
    if not html_path.exists():
        return ""
    html = html_path.read_text(encoding="utf-8")
    match = re.search(r"<main>(.*?)</main>", html, re.DOTALL)
    if not match:
        return ""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", match.group(1), flags=re.DOTALL)
    text = re.sub(r"<svg[^>]*>.*?</svg>", "", text, flags=re.DOTALL)
    text = HTML_TAG.sub(" ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def main(content_dir: Path, out_dir: Path) -> None:
    twins: list[str] = []
    for src in sorted(content_dir.glob("*.md")):
        meta, body = parse_front_matter(src.read_text(encoding="utf-8"))
        slug = "index" if src.stem == "_index" else meta.get("path", src.stem)
        canonical = f"{BASE_URL}/" if slug == "index" else f"{BASE_URL}/{slug}/"
        cleaned = HTML_TAG.sub("", body).strip()
        if len(cleaned) < 300:
            cleaned = extract_rendered_text(out_dir, slug) or cleaned
        twin = build_twin(meta, cleaned, canonical)
        (out_dir / f"{slug}.md").write_text(twin, encoding="utf-8")
        twins.append(twin)
        print(f"wrote {slug}.md")
    (out_dir / "llms-full.txt").write_text("\n\n---\n\n".join(twins), encoding="utf-8")
    print("wrote llms-full.txt")
    write_skills_index(out_dir)


def write_skills_index(out_dir: Path) -> None:
    """Write /.well-known/agent-skills/index.json (v0.2.0) with a fresh SKILL.md digest."""
    digest = hashlib.sha256((out_dir / SKILL_REL).read_bytes()).hexdigest()
    index = {
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "version": "0.2.0",
        "provider": {"name": "Meghan Pasqua, LLC", "url": BASE_URL},
        "skills": [
            {
                "id": "urn:air:pasqualaw.com:skill:site",
                "name": "pasqualaw-site",
                "description": (
                    "Read, cite, and contact the law office of Meghan Pasqua via pasqualaw.com — "
                    "practice areas, credentials, location, and contact info, all available as markdown."
                ),
                "type": "skill-md",
                "url": f"{BASE_URL}/{SKILL_REL}",
                "digest": f"sha256:{digest}",
            }
        ],
    }
    dest = out_dir / ".well-known/agent-skills/index.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print("wrote .well-known/agent-skills/index.json")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
