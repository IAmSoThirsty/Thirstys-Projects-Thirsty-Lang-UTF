# Ship Plan — Thirsty-Lang: GitHub, PyPI, Docs, Polish, Grammar

## Goal
Complete all 5 shipping steps to make Thirsty-Lang ready for public release.

## Subtasks

### 1. GitHub Setup & Push
- `git init` in project root
- Fix ALL fake URLs in `pyproject.toml`: `Homepage`, `Source`, `Bug Tracker` → point to correct repo `https://github.com/IAmSoThirsty/Thirstys-Projects-Thirsty-Lang-UTF`
- Fix ALL fake URLs in `README.md`: remove "(URL TBD once repo is created)" comment, use real repo URL
- Create `.gitignore` (Python standard: `__pycache__/`, `*.pyc`, `dist/`, `*.egg-info/`, `.venv/`, `.env`)
- Generate SSH key pair at `~/.ssh/id_ed25519` (non-interactive, no passphrase)
- Print the **public key** for the user to add to GitHub
- Stage all files, commit with message "Initial commit — Thirsty-Lang UTF 6-tier governance language"
- Add remote `origin git@github.com:IAmSoThirsty/Thirstys-Projects-Thirsty-Lang-UTF.git`
- **Do NOT push yet** — wait for user to add SSH key. Print instructions.

### 2. PyPI Build Preparation
- Install `build` and `twine`
- Update `pyproject.toml` version to `0.1.0` (already set, verify)
- Verify the package name `thirsty-lang` is valid (no name conflict check)
- Build: `python -m build` — produce sdist + wheel in `dist/`
- Print instructions: "To publish: `twine upload dist/*` — requires PyPI API token. Get one at https://pypi.org/manage/account/token/"
- Do NOT actually upload — that needs user's PyPI token.

### 3. Documentation Generation
- Generate full HTML docs from source using `pdoc` (pure Python, no config needed)
  - Command: `pdoc --html --output-dir docs --force src/utf/`
- Create `docs/index.html` as a landing page linking to all module docs
- Create `docs/LANGUAGE_SPEC.md` — a human-readable reference doc covering:
  - All 6 tiers with descriptions
  - Keywords and syntax reference
  - CLI commands reference
  - License info

### 4. Low-Priority Polish Items
- **REPL state persistence**: The REPL is inline in `src/utf/thirsty_lang/cli.py` (in `cmd_repl`). Fix so `interpreter.env` persists across REPL lines (currently each line is evaluated separately — the env is created fresh or not shared). Check how `_execute_source` works — ensure the `Environment` is shared across lines. Add `.clear` command to reset env.
- **TokenType.IN**: Add `IN = "in"` to `TokenType` enum in `src/utf/thirsty_lang/token.py`. Add `"in"` to `KEYWORDS` dict. Fix `_parse_refill_stmt` in `parser.py` to remove the `hasattr(TokenType, "IN")` guard and use `TokenType.IN` directly.
- **Pipe block syntax `|>`**: Currently `|>` only works as infix operator producing `PipeExpr`. Check if hello.thirsty was simplified because of this. Add block-level support: `|>` at the start of a line in a block context redirects the entire block result through the pipe. This may be a parser change in `_parse_statement` or `_parse_expression` to handle `|>` as statement-starting pipe.

### 5. Formal BNF Grammar
- Write `docs/GRAMMAR.md` with complete BNF/EBNF grammar for Thirsty-Lang (Tier 1)
- Cover: program structure, statements, expressions, literals, patterns, types, modules
- Use standard BNF notation with clear non-terminal names
- Include all keywords and operators
- Add notes on whitespace, comments, and tokenization rules

## Deliverables
| File | Description |
|------|-------------|
| `.gitignore` | Python-standard gitignore |
| `~/.ssh/id_ed25519.pub` | SSH public key (user adds to GitHub) |
| `dist/thirsty_lang-0.1.0.tar.gz` | Source distribution |
| `dist/thirsty_lang-0.1.0-py3-none-any.whl` | Wheel distribution |
| `docs/index.html` | Main docs landing page |
| `docs/LANGUAGE_SPEC.md` | Language reference |
| `docs/GRAMMAR.md` | Formal BNF grammar |
| Updated `pyproject.toml` | Correct URLs |
| Updated `README.md` | Correct repo instructions |
| Updated `src/utf/thirsty_lang/cli.py` | Fixed REPL state persistence |
| Updated `src/utf/thirsty_lang/token.py` | Added TokenType.IN |
| Updated `src/utf/thirsty_lang/parser.py` | Fixed for-loop parsing + pipe block support |

## User Handoff Required
1. **SSH key**: User adds printed public key to GitHub → then I can `git push`
2. **PyPI token**: User provides PyPI API token → then I can `twine upload dist/*`