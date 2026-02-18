# Changelog

## [1.3.0] - 2026-02-18
### Added
- Setup section: documents all 4 key lookup locations with examples (env var, config.json, .env)
- Step 0 in Usage: agent checks for KEY_MISSING before proceeding, then tells user exactly how to configure in plain language (3 options with code examples)

## [1.2.0] - 2026-02-18
### Added
- Explicit language selection: `--language` flag (required) on `generate.py`
- Supported languages: zh, en, ja, ko, fr, de, es
- SKILL.md mandates asking the user for language choice before every generation — no defaulting, no inferring
- Language label printed in script output

## [1.1.0] - 2026-02-17
### Added
- skill.yml with display_name, attribution, triggers, permissions
- README.md
- Configuration section (GLM_API_KEY via TOOLS.md)
- Agent owner declaration
- Success criteria and edge cases
- Attribution to original author ViffyGwaanl
### Fixed
- Script now also checks ~/.openclaw/config.json for API key

## [1.0.0] - 2026-02-01
### Added
- Initial release by ViffyGwaanl
- generate.py with full GLM-Image API support
