# Thirsty-Lang

**A governance-first programming language family designed to make Red Hat and Black Hat attack patterns structurally harder through water-metaphor syntax where every keyword has an instrumental security effect.**

## Overview

Thirsty-Lang (Universal Thirsty Family — UTF) is a 6-tier governance-first language stack. Each tier adds progressive capabilities while maintaining default-DENY governance at every gate. The language is designed for secure, auditable, and policy-bound execution across Human-Human, Human-AI, AI-Human, and AI-AI collaboration paradigms.

```
# From the project root:
pip install -e .
thirsty run hello.thirsty
```

## Quick Start

```thirsty
module hello: core

glass greet(name) {
    return "hello, " + name + "!"
}

drink main = greet("thirsty world")
pour main
```

```
$ thirsty run hello.thirsty
hello, thirsty world!
```

### Starting a REPL

```bash
$ thirsty repl
Thirsty-Lang REPL (mode: core)
>>> drink x = 42
>>> pour x
42
```

### Building to JavaScript

```bash
$ thirsty build hello.thirsty --target js
Built: hello.js
```

## Governance Thesis

**Default DENY at every governance gate.**

Every tier of Thirsty-Lang enforces a default-deny posture: code cannot execute, data cannot flow, and mutations cannot commit unless explicitly authorized by the governing tier. This principle applies at every level — from variable assignment in Tier 1 to sovereign execution in Tier 6.

## The 6-Tier Family

### Tier 1: Thirsty-Lang
The base language with water-metaphor syntax. Features include functional programming via `glass` (functions), variables via `drink`/`mut`, pipe operators (`|>`), guarded expressions (`thirst`/`quench`), and core control flow (`thirsty`/`hydrated` for if/else, `refill` for loops). Includes built-in module system with 15 stdlib namespaces (`thirst::time`, `thirst::crypto`, `thirst::json`, etc.).

### Tier 2: Thirst of Gods
Adds object-oriented programming (`fountain`/`glass`), async execution (`cascade`/`await`), and structured error handling (`spillage`/`cleanup`/`throw`). Validates deity-level contracts: fountains must have init methods, cascades must have error-aware consumers, spillage blocks must have at least one handler.

### Tier 3: T.A.R.L. (Thirsty's Active Resistance Language)
A policy-as-code engine with TarlVerdict (ALLOW/DENY/ESCALATE) and default-DENY. Policies are evaluated in order with first-match-wins semantics. Includes LRU-cached runtime evaluation and adaptive policy ordering.

### Tier 4: Shadow Thirst
Mutation analysis and invariant verification. Code is structured into `shadow`/`invariant`/`canonical` blocks with 6 built-in analyzers: Plane Isolation, Determinism, Resource Estimation, Purity Spring, Memory Evaporation, and Canonical Convergence. Critical failures block promotion.

### Tier 5: TSCG (Thirsty Symbolic Constraint Grammar)
Symbolic security expressions with 9 core symbols (COG, DNT, SHD, INV, CAP, QRM, COM, ANC, RFX). Supports pipeline (`->`), AND-combine (`^`), and OR-combine (`||`) operators with SHA-256 canonicalization.

### Tier 6: TSCG-B (Thirsty Symbolic Constraint Grammar — Binary)
Binary frame protocol with magic bytes (`TSGB`), CRC32 integrity, and SHA-256 verification. Stream decoder with automatic resynchronization for multi-frame transport.

## Build and Install from Source

```bash
# Clone the repository
git clone https://github.com/IAmSoThirsty/Thirstys-Projects-Thirsty-Lang-UTF.git
cd Thirstys-Projects-Thirsty-Lang-UTF

# Install in development mode
pip install -e .

# Run a file
thirsty run hello.thirsty

# Start the REPL
thirsty repl
```

## Documentation

Full documentation is available in the [docs](docs/index.html) directory.

## License

Copyright 2026 Thirsty's Projects LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

**Thirsty's Projects LLC** — Building governance-first infrastructure for secure, auditable execution.