# Agent instructions — pasqualaw.com

This repo is the source for [pasqualaw.com](https://pasqualaw.com), the website of Meghan Pasqua, LLC — a Dalton, Georgia law office. Static site built with [Zola](https://www.getzola.org) (custom templates, no theme), deployed to GitHub Pages via `.github/workflows/deploy.yml`.

## Reading the site as an agent

Don't scrape the HTML — the site publishes agent-friendly surfaces:

- `https://pasqualaw.com/llms.txt` — site index
- `https://pasqualaw.com/llms-full.txt` — full site in one file
- Every page has a markdown twin: `/index.md`, `/about.md`, `/location.md`, `/contact.md`, `/privacy-policy.md`, `/disclaimer.md`
- `/.well-known/ard.json` and `/.well-known/agent-skills/index.json` — machine-readable catalogs

## Working on the codebase

- Content lives in `content/*.md` (Zola TOML front matter). Pages set `description` and `updated` — keep `updated` current when editing a page; it feeds `<lastmod>` in the sitemap.
- Note: the About, Contact, and homepage bodies live mostly in `templates/` (`page.html`, `index.html`), not in `content/`. The twin generator falls back to extracting text from the rendered HTML when a content file is thin.
- `templates/base.html` carries the JSON-LD (`LegalService`, `Person`, `Service` nodes, `WebSite`), Open Graph tags, canonical link, and markdown-alternate links.
- `templates/robots.txt` and `templates/sitemap.xml` override Zola's defaults — robots welcomes answer-engine and user-triggered agents and opts out of training-only crawlers; the sitemap emits `<lastmod>` from `updated`.
- `scripts/generate_md_twins.py` runs in CI after `zola build` and generates the markdown twins, `llms-full.txt`, and the agent-skills index (with a fresh SKILL.md sha256 digest) into `public/`. If you add a content page, it gets a twin automatically.
- `static/skills/pasqualaw-site/SKILL.md` is the published agent skill; if you edit it, the digest regenerates in CI — never hand-edit `.well-known/agent-skills/index.json`.
- `public/` is build output committed for convenience — never edit it by hand; run `zola build` (plus the twin script) to regenerate.

## Constraints

- Never remove or weaken the AI-accessibility surfaces above.
- All pages must keep: canonical link, `og:type`, `og:image`, per-page `description`.
- Site content is legal-adjacent — never fabricate credentials, practice areas, or client claims. The site intentionally states that its content is not legal advice; preserve the disclaimer and privacy pages.
- Conventional, descriptive commits.
