"""
Shadow Thirst Core — Mutation Parser, Analyzers, and Promotion Flow
Parses mutation definitions and runs 6 analyzers to determine PROMOTE/REJECT.
"""
import re
import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


class AnalysisLevel:
    CRITICAL = "critical"
    NON_CRITICAL = "non-critical"


@dataclass
class AnalysisResult:
    analyzer: str
    passed: bool
    level: str = AnalysisLevel.CRITICAL
    message: str = ""

    @property
    def name(self):
        return self.analyzer

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} [{self.level}] {self.analyzer}: {self.message}"


@dataclass
class ShadowModule:
    """Parsed shadow thirst mutation."""
    name: str
    shadow_code: str = ""
    invariant_code: str = ""
    canonical_code: str = ""
    source: str = ""

    def replay_hash(self) -> str:
        return hashlib.sha256(self.source.encode('utf-8')).hexdigest()


class MutationParser:
    """Parses mutation definitions from source text."""

    MUTATION_RE = re.compile(
        r'mutation\s+(\w+)\s*\{\s*'
        r'validated_canonical\s*\{'
        r'(.*)\}'
        r'\s*\}',
        re.DOTALL
    )

    BLOCK_RE = re.compile(
        r'(shadow|invariant|canonical)\s*\{'
        r'(.*?)\}',
        re.DOTALL
    )

    @classmethod
    def parse(cls, text: str) -> ShadowModule:
        """Parse mutation source text into a ShadowModule."""
        text = text.strip()
        mut_match = cls.MUTATION_RE.search(text)
        if not mut_match:
            raise ValueError("No valid mutation definition found")

        name = mut_match.group(1)
        validated_canonical_body = mut_match.group(2)

        module = ShadowModule(name=name, source=text)
        shadow_code = ""
        invariant_code = ""
        canonical_code = ""

        for block_match in cls.BLOCK_RE.finditer(validated_canonical_body):
            block_type = block_match.group(1).strip()
            block_content = block_match.group(2).strip()

            if block_type == 'shadow':
                shadow_code = block_content
                module.shadow_code = shadow_code
            elif block_type == 'invariant':
                invariant_code = block_content
                module.invariant_code = invariant_code
            elif block_type == 'canonical':
                canonical_code = block_content
                module.canonical_code = canonical_code

        # Also try parsing without the nested validated_canonical wrapper
        if not shadow_code and not invariant_code and not canonical_code:
            direct_blocks = cls.BLOCK_RE.finditer(text[len(f"mutation {name}"):])
            for block_match in direct_blocks:
                block_type = block_match.group(1).strip()
                block_content = block_match.group(2).strip()
                if block_type == 'shadow':
                    module.shadow_code = block_content
                elif block_type == 'invariant':
                    module.invariant_code = block_content
                elif block_type == 'canonical':
                    module.canonical_code = block_content

        return module


# --- Analyzers ---

class PlaneIsolationAnalyzer:
    """Ensures shadow doesn't write to canonical state."""

    WRITE_KEYWORDS = {'assign', 'set', 'write', '=', 'store', 'put', 'push', 'pop'}

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        critical_state_writes = 0
        for keyword in self.WRITE_KEYWORDS:
            if keyword in module.shadow_code.lower():
                critical_state_writes += 1

        # Specific checks: shadow should not contain 'canonical.' or 'canonical_state'
        if 'canonical.' in module.shadow_code or 'canonical_state' in module.shadow_code:
            return AnalysisResult(
                analyzer="PlaneIsolation",
                passed=False,
                level=AnalysisLevel.CRITICAL,
                message="Shadow block writes to canonical state"
            )

        return AnalysisResult(
            analyzer="PlaneIsolation",
            passed=True,
            level=AnalysisLevel.CRITICAL,
            message="Shadow block properly isolated from canonical state"
        )


class DeterminismAnalyzer:
    """Ensures shadow block contains no non-deterministic operations."""

    NON_DETERMINISTIC = {'now', 'rand', 'random', 'time', 'uuid', 'date', 'clock'}

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        found_ops = []
        for op in self.NON_DETERMINISTIC:
            if op in module.shadow_code.lower():
                found_ops.append(op)

        if found_ops:
            return AnalysisResult(
                analyzer="Determinism",
                passed=False,
                level=AnalysisLevel.CRITICAL,
                message=f"Non-deterministic operations found: {', '.join(found_ops)}"
            )

        return AnalysisResult(
            analyzer="Determinism",
            passed=True,
            level=AnalysisLevel.NON_CRITICAL,
            message="Shadow block is deterministic"
        )


class ResourceEstimator:
    """Estimates CPU and memory usage of shadow block."""

    CPU_LIMIT_MS = 1000
    MEMORY_LIMIT_BYTES = 256 * 1024 * 1024  # 256MB

    CPU_WEIGHTS = {
        'for': 10, 'while': 20, 'sort': 50, 'map': 5, 'filter': 5,
        'reduce': 10, 'recursion': 50, 'loop': 15
    }

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        code = module.shadow_code.lower()
        estimated_cpu = 0
        estimated_memory = len(code) * 2  # rough estimate per char

        for keyword, weight in self.CPU_WEIGHTS.items():
            count = code.count(keyword)
            estimated_cpu += count * weight

        # Base cost
        estimated_cpu += len(code.split('\n')) * 5

        issues = []
        if estimated_cpu > self.CPU_LIMIT_MS:
            issues.append(f"CPU estimate {estimated_cpu}ms exceeds {self.CPU_LIMIT_MS}ms limit")
        if estimated_memory > self.MEMORY_LIMIT_BYTES:
            issues.append(f"Memory estimate {estimated_memory} bytes exceeds {self.MEMORY_LIMIT_BYTES} bytes limit")

        if issues:
            return AnalysisResult(
                analyzer="ResourceEstimator",
                passed=False,
                level=AnalysisLevel.CRITICAL if estimated_cpu > self.CPU_LIMIT_MS else AnalysisLevel.NON_CRITICAL,
                message="; ".join(issues)
            )

        return AnalysisResult(
            analyzer="ResourceEstimator",
            passed=True,
            level=AnalysisLevel.CRITICAL,
            message=f"Resources within limits (CPU: ~{estimated_cpu}ms, Mem: ~{estimated_memory} bytes)"
        )


class PuritySpringAnalyzer:
    """Ensures invariant blocks are pure expressions."""

    IMPURE_KEYWORDS = {'print', 'write', 'read', 'input', 'open', 'exec', 'eval', 'import'}

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        if not module.invariant_code:
            return AnalysisResult(
                analyzer="PuritySpring",
                passed=True,
                level=AnalysisLevel.CRITICAL,
                message="No invariant block to check"
            )

        code = module.invariant_code.lower()
        found_impure = []
        for kw in self.IMPURE_KEYWORDS:
            if kw in code:
                found_impure.append(kw)

        if found_impure:
            return AnalysisResult(
                analyzer="PuritySpring",
                passed=False,
                level=AnalysisLevel.CRITICAL,
                message=f"Impure operations in invariant: {', '.join(found_impure)}"
            )

        return AnalysisResult(
            analyzer="PuritySpring",
            passed=True,
            level=AnalysisLevel.CRITICAL,
            message="Invariant block is pure"
        )


class MemoryEvaporationAnalyzer:
    """Estimates peak memory usage of shadow block."""

    PEAK_LIMIT = 256 * 1024 * 1024  # 256MB

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        code = module.shadow_code
        estimated_peak = len(code) * 4  # rough estimation

        # Weight by structures that create allocations
        allocations = 0
        allocations += code.count('new') * 1000
        allocations += code.count('list') * 500
        allocations += code.count('map') * 500
        allocations += code.count('string') * 200
        allocations += code.count('reservoir') * 2000

        estimated_peak += allocations

        if estimated_peak > self.PEAK_LIMIT:
            return AnalysisResult(
                analyzer="MemoryEvaporation",
                passed=False,
                level=AnalysisLevel.NON_CRITICAL,
                message=f"Estimated peak memory {estimated_peak} bytes exceeds {self.PEAK_LIMIT} bytes limit"
            )

        return AnalysisResult(
            analyzer="MemoryEvaporation",
            passed=True,
            level=AnalysisLevel.NON_CRITICAL,
            message=f"Peak memory within limits (~{estimated_peak} bytes)"
        )


class CanonicalConvergenceAnalyzer:
    """Ensures shadow and canonical blocks produce equivalent results."""

    def analyze(self, module: ShadowModule) -> AnalysisResult:
        if not module.shadow_code or not module.canonical_code:
            return AnalysisResult(
                analyzer="CanonicalConvergence",
                passed=False,
                level=AnalysisLevel.CRITICAL,
                message="Both shadow and canonical blocks must be present"
            )

        # Check for structural convergence (both blocks exist and similar structure)
        shadow_lines = [l.strip() for l in module.shadow_code.split('\n') if l.strip()]
        canonical_lines = [l.strip() for l in module.canonical_code.split('\n') if l.strip()]

        if len(shadow_lines) == 0 or len(canonical_lines) == 0:
            return AnalysisResult(
                analyzer="CanonicalConvergence",
                passed=False,
                level=AnalysisLevel.CRITICAL,
                message="Shadow or canonical block is empty"
            )

        # Convergence check: Both should have similar structure
        shadow_return_count = module.shadow_code.count('return')
        canonical_return_count = module.canonical_code.count('return')

        if shadow_return_count != canonical_return_count:
            return AnalysisResult(
                analyzer="CanonicalConvergence",
                passed=False,
                level=AnalysisLevel.NON_CRITICAL,
                message=f"Shadow ({shadow_return_count} returns) and canonical ({canonical_return_count} returns) may not converge"
            )

        # Check output type consistency
        shadow_ops = set(re.findall(r'\b[a-z_]+\b', module.shadow_code.lower()))
        canonical_ops = set(re.findall(r'\b[a-z_]+\b', module.canonical_code.lower()))
        overlap = shadow_ops & canonical_ops

        if len(overlap) < max(1, min(len(shadow_ops), len(canonical_ops)) * 0.3):
            return AnalysisResult(
                analyzer="CanonicalConvergence",
                passed=False,
                level=AnalysisLevel.NON_CRITICAL,
                message="Shadow and canonical blocks use very different operations — possible divergence"
            )

        return AnalysisResult(
            analyzer="CanonicalConvergence",
            passed=True,
            level=AnalysisLevel.CRITICAL,
            message="Shadow and canonical blocks converge"
        )


class PromotionEngine:
    """Executes the promote/reject flow based on analyzer results."""

    def __init__(self):
        self.analyzers = [
            ("PlaneIsolation", PlaneIsolationAnalyzer()),
            ("Determinism", DeterminismAnalyzer()),
            ("ResourceEstimation", ResourceEstimator()),
            ("PuritySpring", PuritySpringAnalyzer()),
            ("MemoryEvaporation", MemoryEvaporationAnalyzer()),
            ("CanonicalConvergence", CanonicalConvergenceAnalyzer()),
        ]

    def evaluate(self, module: ShadowModule) -> Tuple[str, List[AnalysisResult]]:
        """
        Evaluate a mutation module. Returns (verdict, results).
        Verdict is one of: PROMOTE, REJECT, FLAGGED
        """
        results = []

        for name, analyzer in self.analyzers:
            try:
                result = analyzer.analyze(module)
                results.append(result)
            except Exception as e:
                results.append(AnalysisResult(
                    analyzer=name,
                    passed=False,
                    level=AnalysisLevel.CRITICAL,
                    message=f"Analysis error: {e}"
                ))

        # Determine verdict
        critical_failures = [r for r in results if not r.passed and r.level == AnalysisLevel.CRITICAL]
        non_critical_failures = [r for r in results if not r.passed and r.level == AnalysisLevel.NON_CRITICAL]

        if critical_failures:
            verdict = "REJECT"
        elif non_critical_failures:
            verdict = "FLAGGED"
        else:
            verdict = "PROMOTE"

        return verdict, results

    @staticmethod
    def generate_mermaid(module: ShadowModule, verdict: str = "PROMOTE", results: List[AnalysisResult] = None) -> str:
        if results is None:
            results = []
        """Generate a Mermaid flowchart visualization of the promotion flow."""
        lines = ["```mermaid", "flowchart TD"]
        lines.append(f"    M[\"Mutation: {module.name}\"]")

        for i, (name, _) in enumerate([
            ("PlaneIsolationAnalyzer", None),
            ("DeterminismAnalyzer", None),
            ("ResourceEstimator", None),
            ("PuritySpringAnalyzer", None),
            ("MemoryEvaporationAnalyzer", None),
            ("CanonicalConvergenceAnalyzer", None),
        ]):
            r = results[i] if i < len(results) else AnalysisResult(analyzer=name, passed=True)
            status = "✅" if r.passed else "❌"
            lines.append(f"    A{i}[\"{status} {name}\"]")

            if i == 0:
                lines.append(f"    M --> A{i}")
            else:
                lines.append(f"    A{i - 1} --> A{i}")

        lines.append(f"    V[\"Verdict: {verdict}\"]")
        lines.append(f"    A{min(5, len(results) - 1)} --> V")

        if verdict == "PROMOTE":
            lines.append(f"    V --> P[\"🚀 PROMOTE\"]")
        elif verdict == "REJECT":
            lines.append(f"    V --> R[\"❌ REJECT\"]")
        else:
            lines.append(f"    V --> F[\"⚠️ FLAGGED\"]")

        lines.append("```")
        return "\n".join(lines)