"""
T.A.R.L. Specification Types

Verdict lattice:  DENY ≺ ESCALATE ≺ ALLOW
Restrictive meet: a ∧ b = min(a, b)   — DENY beats all
Permissive join:  a ∨ b = max(a, b)   — ALLOW beats all
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

# Safety ordering: DENY=0 < ESCALATE=1 < ALLOW=2
_VERDICT_RANK: dict = {}


class TarlVerdict(str, Enum):
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    ALLOW = "ALLOW"

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, TarlVerdict):
            return NotImplemented
        return _VERDICT_RANK[self] < _VERDICT_RANK[other]

    def __le__(self, other: object) -> bool:
        if not isinstance(other, TarlVerdict):
            return NotImplemented
        return _VERDICT_RANK[self] <= _VERDICT_RANK[other]

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, TarlVerdict):
            return NotImplemented
        return _VERDICT_RANK[self] > _VERDICT_RANK[other]

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, TarlVerdict):
            return NotImplemented
        return _VERDICT_RANK[self] >= _VERDICT_RANK[other]

    @staticmethod
    def meet(a: "TarlVerdict", b: "TarlVerdict") -> "TarlVerdict":
        """Restrictive composition (∧): min in safety ordering."""
        return a if _VERDICT_RANK[a] <= _VERDICT_RANK[b] else b

    @staticmethod
    def join(a: "TarlVerdict", b: "TarlVerdict") -> "TarlVerdict":
        """Permissive composition (∨): max in safety ordering."""
        return a if _VERDICT_RANK[a] >= _VERDICT_RANK[b] else b


# Populate rank table after enum is defined
_VERDICT_RANK.update({
    TarlVerdict.DENY:     0,
    TarlVerdict.ESCALATE: 1,
    TarlVerdict.ALLOW:    2,
})


class CompositionOp(str, Enum):
    """How a child policy composes with its parent."""
    EXTENDS = "EXTENDS"
    RESTRICTS = "RESTRICTS"

    def __str__(self) -> str:
        return self.value


class SetOp(str, Enum):
    """How policies in a policy_set group are combined."""
    UNION = "UNION"
    INTERSECT = "INTERSECT"
    MAJORITY = "MAJORITY"

    def __str__(self) -> str:
        return self.value


@dataclass
class TarlPolicyRef:
    """A reference to another policy in a composition directive."""
    name: str
    alias: Optional[str] = None
    is_file: bool = False


@dataclass
class TarlRule:
    """A single `when <condition> => VERDICT` rule."""
    condition: str
    verdict: TarlVerdict
    source_line: int = 0

    def __str__(self) -> str:
        return f"when {self.condition} => {self.verdict.value}"


@dataclass
class TarlPolicy:
    """Ordered decision function: P = [r₁, r₂, ..., rₙ] over context space."""
    rules: List[TarlRule] = field(default_factory=list)
    source: str = ""
    name: str = "unnamed"
    # Phase 2: composition
    parent: Optional[str] = None
    composition: Optional[CompositionOp] = None
    includes: List[TarlPolicyRef] = field(default_factory=list)
    has_stop: bool = False
    # Phase 5 stubs: temporal versioning
    version: Optional[str] = None
    supersedes: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    on_expiry: Optional[TarlVerdict] = None

    def __str__(self) -> str:
        header = f"policy {self.name}"
        if self.composition and self.parent:
            header += f" {self.composition.value} {self.parent}"
        if self.version:
            header += f" v{self.version}"
        lines = [f"{header}:"]
        for ref in self.includes:
            alias_part = f" AS {ref.alias}" if ref.alias else ""
            if ref.is_file:
                lines.append(f'  INCLUDE "{ref.name}"{alias_part}')
            else:
                lines.append(f"  INCLUDE {ref.name}{alias_part}")
        for r in self.rules:
            lines.append(f"  {r}")
        if self.has_stop:
            lines.append("  STOP")
        return "\n".join(lines)


@dataclass
class TarlDecision:
    """Result of evaluating a T.A.R.L. policy against a context."""
    verdict: TarlVerdict
    reason: str = ""
    rule_index: int = -1
    matched_rule: Optional[str] = None

    def __str__(self) -> str:
        return f"[{self.verdict.value}] {self.reason}"


@dataclass
class TarlPolicySet:
    """
    A named composition of multiple policies evaluated with set operators.

    groups: list of (SetOp, [policy_name, ...])
    Each group produces a verdict via its operator.
    The final verdict is the meet (∧) of all group verdicts.
    """
    name: str
    groups: List[Tuple[SetOp, List[str]]] = field(default_factory=list)
    default_verdict: TarlVerdict = TarlVerdict.DENY
    source: str = ""

    def __str__(self) -> str:
        lines = [f"policy_set {self.name}:"]
        for op, names in self.groups:
            lines.append(f"  combine {op.value} [{', '.join(names)}]")
        lines.append(f"  default: {self.default_verdict.value}")
        return "\n".join(lines)


# Ground state. Nothing crosses without an explicit ALLOW.
DEFAULT_DENY = TarlDecision(
    verdict=TarlVerdict.DENY,
    reason="default-deny: no rule matched",
    rule_index=-1,
    matched_rule=None,
)
