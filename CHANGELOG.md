# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) ·
versioning: [SemVer](https://semver.org/).

> Add an entry under `[Unreleased]` with every feature/fix. On release, move them
> into a dated, versioned section.

## [Unreleased]

### Added
- Initial golden-path scaffold (Inspector, tiered CI, playbook, doc tiers).
- "Agreed work → tracking issue → PRs link back" traceability pattern, woven through PLAYBOOK §9, CONTRIBUTING, and the PR template.
- GROWTH.md, the going-to-market chapter: a landing page search can read, store listings as code, store search, screenshots and store art, ratings without buying them, attribution, developer identity, positioning, and hearing from users. Summarised as PLAYBOOK §10, with checklist lines.
- scripts/store-ranks.py: an App Store search-rank baseline from a JSON config, appended to a doc as a dated table (Apple publishes that API for programmatic use, while Google Play is left to its Console, because Play has no search API and its robots.txt disallows automated search reads).
