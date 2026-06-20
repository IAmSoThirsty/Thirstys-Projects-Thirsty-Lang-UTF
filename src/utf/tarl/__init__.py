"""T.A.R.L. — Thirsty's Active Resistance Language"""
from utf.tarl.spec import TarlVerdict, TarlDecision, TarlPolicy, TarlRule, DEFAULT_DENY
from utf.tarl.runtime import TarlRuntime

__all__ = [
    "TarlVerdict",
    "TarlDecision",
    "TarlPolicy",
    "TarlRule",
    "DEFAULT_DENY",
    "TarlRuntime",
]
