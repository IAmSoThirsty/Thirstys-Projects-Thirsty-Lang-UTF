# Thirsty-Lang & UTF — Complete Implementation Plan
## Universal Thirsty Family — 6-Tier Language Stack

## Goal
Build the complete Thirsty-Lang / UTF programming language family from scratch based on the canonical v1.3 reference spec — a 6-tier governance-first language stack with Thirsty-Lang, Thirst of Gods, T.A.R.L., Shadow Thirst, TSCG, and TSCG-B.

## Research Summary
The canonical reference document provides exhaustive specifications for all 6 tiers. No additional research needed — all keywords, syntax, types, error codes, file formats, and architectural patterns are fully specified. The reference confirms:
- 41 Python source files, ~7,037 LOC in the reference implementation
- 6 canonical tiers with full keyword tables, type system specs, and API surfaces
- All E-code error registry (E001-E900)
- All 9 TSCG symbols with opcodes
- TSCG-B binary frame format (44-byte minimum)
- Shadow Thirst with 6 analyzers
- TARL with 8 subsystems, bytecode VM, LLVM backend
- Governance model with Triumvirate, Iron Path, PSIA
- CLI with 15+ subcommands

## Approach
Build bottom-up: Tier 1 (Thirsty-Lang) → Tier 2 (Thirst of Gods) → Tier 3 (T.A.R.L.) → Tier 4 (Shadow Thirst) → Tier 5 (TSCG) → Tier 6 (TSCG-B), then cross-cutting layers (governance, CLI, docs, tests). Each tier is fully self-contained and adds to the previous.

## Subtasks

### Phase 1: Project Foundation + Thirsty-Lang Core (Tier 1)
1. **Project structure** — Create src/utf/ package layout with all subdirectories, __init__.py files, pyproject.toml, README.md
2. **Token definitions** — Implement src/utf/thirsty_lang/token.py with all TokenType enum values (drink, pour, sip, thirsty, hydrated, glass, fountain, refill, etc.) and KEYWORDS dict mapping keyword strings to TokenTypes. Include ALL keywords from the spec (core, security, Thirst of Gods, policy, Shadow Thirst). Add multi-char operators (-> pipe, `\ > `, `\ \ `).
3. **Lexer** — Implement src/utf/thirsty_lang/lexer.py with full tokenization: identifiers, keywords, strings (single/double quotes, escape sequences), numbers (int/float), operators, delimiters, comments (// and /* */), source span tracking (line/column). Error handling for unterminated strings (E002) and unrecognized characters (E001).
4. **AST definitions** — Implement src/utf/thirsty_lang/ast.py with ALL AST node types: Program, ModuleHeader, FunctionDecl (glass), ClassDecl (fountain), VariableDecl (drink), BinaryOp, UnaryOp, If (thirsty/hydrated), While/For (refill), Return, Pour, Sip, Import, Assign, Literal (Int, Float, String, Bool), Identifier, Block, PipeExpr, GuardExpr (thirst/quench), SecurityBlock (shield), SanitizeExpr, ArmorExpr, DetectBlock, MorphDef, DefendStrat, EnumDecl, StructDecl, InterfaceDecl, GovernedFunctionDecl, Spillage/Cleanup/Throw, CascadeCall, NewExpr, FloodExpr, DripExpr, EvaporateExpr, CondenseExpr, ErrorLiteral, QuenchedLiteral. Span tracking on ALL nodes.
5. **Parser** — Implement src/utf/thirsty_lang/parser.py with recursive descent parser. Parse all AST node types. Module header support (module + mode core/governed). Expression parsing with precedence (lowest to highest: assignment, pipe, guard, logical, comparison, additive, multiplicative, unary, primary). Multi-error recovery with structured diagnostics and "did you mean?" suggestions.
6. **Type system** — Implement src/utf/thirsty_lang/typesys.py with all types: Int, Float, Bool, String, Void, Any, Error, Quenched[T], Reservoir[T], Task[T], Result[T,E], Governed[T]. Type widening rules (Int→Float, all→Any). Enum types with exhaustive matching. Struct types with field validation.
7. **Type checker** — Implement src/utf/thirsty_lang/checker.py with lexical scoping, duplicate binding detection (E010), unknown identifier detection with nearest-match suggestion within edit distance 3 (E011), immutable assignment guard (E020), type mismatch checking (E021-E024), call arity validation (E030), pipe type compatibility, governance annotation validation (E050). Enum exhaustiveness checking. Interface implementation verification. Statement reachability analysis.
8. **Interpreter** — Implement src/utf/thirsty_lang/interpreter.py with tree-walking evaluation. Environment with scoped variable storage. All expression evaluation types. Control flow (if/hydrated, refill loops). Function calls with argument binding. True tail-call optimization. Module header mode dispatch (core vs governed). Governance enforcement (_enforce_governance). Spillage/cleanup/throw for error handling. Async cascade glass with ThreadPoolExecutor. Reservoir operations (size, push, pop, get, flood). Quenched[T] operations (condense, evaporate). Pipe operator evaluation. Security keyword stubs (shield, sanitize, armor, morph, detect, defend).
9. **Error codes** — Implement src/utf/thirsty_lang/diagnostics.py with complete ERROR_CODES registry (E001-E901), DiagnosticBundle for multi-error reporting, formatted output with caret markers and source spans.

### Phase 2: CLI + Module System + Package Manager
10. **CLI** — Implement src/utf/thirsty_lang/cli.py with all subcommands: run (--trace, --thirst-level, --authority, --demo), repl (interactive), fmt (AST-based formatting), new (scaffold project), build (--target llvm-ir|llvm-obj|llvm-exe|llvm-asm|llvm-jit|js|wasm-pyodide, --emit-manifest), govern (annotation report + auto .tarl), add/audit/lock (package management), doctor (project health check), lsp (stdio mode), docs (generate HTML).
11. **Module system** — Implement src/utf/thirsty_lang/module_system.py with module caching on first import, search path (relative to importing file's directory), 15 stdlib namespaces: thirst::time (now, epoch_ms), thirst::crypto (sha256, sign, hmac, random_bytes, uuid4), thirst::reservoir (size, push, pop, get, flood), thirst::fs (read_file, write_file, exists, list_dir, mkdir, remove), thirst::path (join, dirname, basename, extension, absolute, relative), thirst::json (parse, stringify, get, set), thirst::http (get, post, put, delete), thirst::env (get, set, all), thirst::process (run, exit, args, pid), thirst::log (info, warn, error, debug), thirst::test (assert_eq, assert_ne, assert_true, assert_raises, describe, it), thirst::collections (map, filter, reduce, sort, unique, flatten, zip), thirst::net (tcp_connect, tcp_listen, udp_send), thirst::sqlite (connect, query, execute, close), thirst::yaml (parse, dump), thirst::toml (parse, dump). Plus 16 global builtins: length, contains, split, abs, min, max, push, pop, size, get, flood, condense, evaporate, strain, transmute, distill.
12. **Package manager** — Implement src/utf/thirsty_lang/package_manager.py with thirsty.toml metadata parsing, thirsty.lock with SHA-256 per dependency, add/audit/lock operations.
13. **Formatter** — Implement src/utf/thirsty_lang/formatter.py with AST-based pretty-printer producing canonical formatted output.

### Phase 3: T.A.R.L. (Tier 3)
14. **TARL core** — Implement src/utf/tarl/core.py with policy parser (regex-based), SafeExpr sandboxed evaluator (only safe AST node types allowed), evaluate() returning ALLOW/DENY/ESCALATE with default DENY. Policy rules: when <expr> => VERDICT; evaluated in order, first match wins.
15. **TarlRuntime** — Implement tarl/runtime.py with policy caching (LRU, 128 entries), parallel evaluation (ThreadPoolExecutor), adaptive policy ordering, evaluate(context) -> TarlDecision with verdict + reason fields.
16. **TarlSpec** — Implement tarl/spec.py with TarlVerdict enum (ALLOW, DENY, ESCALATE), TarlDecision dataclass, TarlPolicy dataclass.
17. **TARL CLI** — Implement src/utf/tarl/cli.py with command-line policy evaluation.

### Phase 4: Shadow Thirst (Tier 4)
18. **Shadow Thirst core** — Implement src/utf/shadow_thirst/core.py with mutation parser (validated_canonical blocks with shadow/invariant/canonical sections), ShadowModule AST, promote/reject flow. 6 analyzers: PlaneIsolationAnalyzer (shadow doesn't write canonical state), DeterminismAnalyzer (no now/rand/random), ResourceEstimator (CPU ≤ 1000ms, memory ≤ 256MB), PuritySpringAnalyzer (invariant blocks pure), MemoryEvaporationAnalyzer (peak ≤ 256MB), CanonicalConvergenceAnalyzer (shadow and canonical converge). Critical failures block promotion. Replay hash (SHA-256). Mermaid flowchart visualization.
19. **Plugin system** — Implement plugin loader scanning plugins/*.py for analyze_plugin(module) functions.
20. **Shadow CLI** — Implement src/utf/shadow_thirst/cli.py with check and visualize commands.

### Phase 5: TSCG + TSCG-B (Tiers 5 & 6)
21. **TSCG core** — Implement src/utf/tscg/core.py with 9 core symbols (COG, DNT, SHD, INV, CAP, QRM, COM, ANC, RFX) plus extended set (SAFE, ING, LED, MUT, SEL, QRM_LINEAR, QRM_STATIC). Parser for pipeline (->), AND-combine (^), OR-combine (||) operators. AST nodes (Symbol, Pipeline, Combine). canonical() normalization. checksum() for SHA-256. Validation of recognized symbols.
22. **TSCG CLI** — Implement src/utf/tscg/cli.py.
23. **TSCG-B core** — Implement src/utf/tscg_b/core.py with binary frame format: magic TSGB (4 bytes), version (1), flags (1), payload length (2), payload (N), CRC32 (4), SHA-256 (32). opcode table matching TSCG symbols. pack_text() encoding, unpack_frame() decoding with CRC32 + SHA-256 verification. StreamDecoder class with buffered multi-frame decoding and magic-byte resynchronization.
24. **TSCG-B CLI** — Implement src/utf/tscg_b/cli.py.

### Phase 6: Governance Integration + Advanced Features
25. **Governance enforcement** — Wire governance into interpreter: mode governed activates TARL policy gate before function execution and Shadow Thirst gate before mutation commits. requires clause annotation checking (AuthorityClass.AC1-AC5, AuditTrail.Immutable, HumanAppealWindow[Nd]). Auto TARL policy generation via thirsty govern.
26. **Governance manifest** — Implement --emit-manifest build output with TSCG-B frame (base64), policy_hash, capability_manifest, governance_proof with iron_path_run_id.
27. **Iron Path** — Implement governance/iron_path.py with sovereign execution loop: load pipeline YAML, verify config snapshot cryptographically, execute each stage with role signature + policy state binding, SHA-256 artifact hash, immutable JSONL audit log, compliance bundle export, audit trail integrity verification.
28. **Sovereign Runtime** — Implement governance/sovereign_runtime.py with cryptographic signing, config snapshot creation/verification, policy state hash-binding, append-only audit log writes, compliance bundle export.
29. **Triumvirate** — Implement governance/triumvirate_server.py (FastAPI, port 8001) with 3 pillars: Galahad (ethics, 13 harm patterns), Cerberus (security, 20 threat patterns), CodexDeus (constitutional, 12 violation patterns + FourLaws). POST /intent, GET /audit, GET /fourlaws, POST /chimera/verdict, POST /chimera/canary endpoints. Unanimous ALLOW required.
30. **PSIA** — Implement src/psia/ with 7-stage pipeline: PreScreenGate → Ingestion → Schema Validation → Classification → Shadow Simulation (4 invariant checks) → Governance (Triumvirate submission) → Canonical Log (append-only hash-chained JSONL) → Seal (Merkle tree + Ed25519). 6 plane data models (RawFrame through SealedFrame). FastAPI gateway on port 8002.
31. **LLVM backend** — Implement src/utf/tarl/compiler/frontend.py and llvm_backend.py using llvmlite. Support targets: llvm-ir, llvm-obj, llvm-exe, llvm-asm, llvm-jit.
32. **LSP server** — Implement src/utf/thirsty_lang/lsp_server.py with stdio and TCP modes (port 9898). TextDocumentSync, completion, diagnostics, hover support.
33. **Package registry** — Implement src/utf/thirsty_lang/registry_server.py (FastAPI, port 9000) with publish/search/yank/download endpoints.
34. **Docs generator** — Implement src/utf/thirsty_lang/docs_generator.py with static HTML site generation, sidebar TOC, search index, syntax highlighting, responsive dark CSS.

### Phase 7: Examples + Tests + Verification
35. **Examples** — Create all examples from the spec: hello.thirsty, policy.tarl, promote.shadowthirst, gods.thirstofgods, namespace_imports.thirsty, flavor.thirsty, context.json. Create governed_agent_runner showcase app with module/mode header, Governed[T] returns, requires annotations, multi-namespace imports.
36. **Tests** — Write comprehensive test suite: test_thirsty_lang.py (lexer, parser, checker, interpreter, CLI), test_tarl.py, test_shadow_thirst.py, test_tscg.py, test_tscg_b.py, test_thirsty_flavor.py.
37. **Conformance** — Implement conformance test runner framework.
38. **Integration verification** — End-to-end test: write .thirsty file → lex → parse → check → interpret → output. Round-trip TSCG-B encoding/decoding. Shadow Thirst promote/reject. TARL policy evaluation. All examples must execute and produce correct output.

## Deliverables
| File Path | Description |
|-----------|-------------|
| src/utf/thirsty_lang/token.py | Token definitions (all keywords) |
| src/utf/thirsty_lang/lexer.py | Tokenizer with span tracking |
| src/utf/thirsty_lang/ast.py | All AST node definitions |
| src/utf/thirsty_lang/parser.py | Recursive descent parser |
| src/utf/thirsty_lang/typesys.py | Type system implementation |
| src/utf/thirsty_lang/checker.py | Type checker + semantic analysis |
| src/utf/thirsty_lang/interpreter.py | Tree-walking interpreter |
| src/utf/thirsty_lang/cli.py | Full CLI with 15+ subcommands |
| src/utf/thirsty_lang/module_system.py | 15-namespace stdlib + imports |
| src/utf/thirsty_lang/package_manager.py | thirsty.toml + thirsty.lock |
| src/utf/thirsty_lang/diagnostics.py | Error code registry |
| src/utf/thirsty_lang/formatter.py | AST-based code formatter |
| src/utf/thirsty_lang/lsp_server.py | LSP protocol server |
| src/utf/thirsty_lang/registry_server.py | Package registry |
| src/utf/thirsty_lang/docs_generator.py | Docs site generator |
| src/utf/tarl/core.py | T.A.R.L. policy engine |
| src/utf/tarl/cli.py | TARL CLI |
| src/utf/shadow_thirst/core.py | Shadow Thirst mutation engine |
| src/utf/shadow_thirst/cli.py | Shadow Thirst CLI |
| src/utf/tscg/core.py | TSCG symbolic grammar |
| src/utf/tscg/cli.py | TSCG CLI |
| src/utf/tscg_b/core.py | TSCG-B binary protocol |
| src/utf/tscg_b/cli.py | TSCG-B CLI |
| tarl/runtime.py | TarlRuntime policy evaluation |
| tarl/spec.py | TarlVerdict + TarlDecision |
| governance/iron_path.py | Iron Path sovereign executor |
| governance/sovereign_runtime.py | Cryptographic runtime |
| governance/triumvirate_server.py | 3-pillar governance server |
| src/psia/core.py | 7-stage PSIA pipeline |
| src/utf/examples/* | Example .thirsty, .tarl, .shadowthirst files |
| src/utf/tests/* | Comprehensive test suite |
| pyproject.toml | Package metadata |
| README.md | Project documentation |

## Evaluation Criteria
- All 6 tiers build and run without import errors
- Hello world .thirsty program executes correctly: `python -m src.utf.thirsty_lang hello.thirsty` → "hello, thirsty world"
- All keyword tokens from spec parse correctly
- T.A.R.L. policy evaluates ALLOW/DENY/ESCALATE correctly
- Shadow Thirst promote/reject flow works with 6 analyzers
- TSCG expressions parse, canonicalize, and checksum correctly
- TSCG-B frames pack/unpack with CRC32+SHA256 verification
- Module import system resolves stdlib namespaces
- Type checker catches E010-E050 errors
- CLI subcommands (run/repl/fmt/build/govern) all functional
- Test suite passes

## Notes
- Python 3.11+ required (tomllib)
- Standard library only for core — no third-party runtime dependencies
- Async uses concurrent.futures (stdlib)
- LLVM backend requires llvmlite (optional)
- All water-metaphor keywords implemented exactly per spec
- Governance gates: TARL policy → Shadow Thirst → Constitutional enforcement → Canonical commit
- Default = DENY at every governance gate