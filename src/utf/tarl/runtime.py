"""
T.A.R.L. Runtime — LRU-cached, parallel policy evaluation.

Phase 2 additions:
  register_source(name, provider) — bind a live data provider to
  source:name references in policy conditions. provider may be a
  static list/set or a zero-arg callable returning a list/set.
"""
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from typing import Optional

from utf.tarl.spec import (
    TarlVerdict, TarlDecision, TarlPolicy, TarlRule, DEFAULT_DENY,
)
from utf.tarl.core import SafeExpr, PolicyParser


class LRUCache:
    """Simple LRU cache with maximum size."""

    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self._cache = OrderedDict()

    def get(self, key: str) -> Optional[TarlDecision]:
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, value: TarlDecision):
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > self.maxsize:
            self._cache.popitem(last=False)

    def invalidate(self, key: str):
        self._cache.pop(key, None)

    def clear(self):
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)


class TarlRuntime:
    """
    TARL policy runtime:
    - LRU decision cache (128 entries)
    - ThreadPoolExecutor for parallel rule evaluation
    - Adaptive ordering (most-frequently-matched rules evaluated first)
    - Dynamic source registry for source:name condition references
    """

    def __init__(
        self,
        policy: Optional[TarlPolicy] = None,
        max_workers: int = 4,
    ):
        self.policy = policy or TarlPolicy()
        self.cache = LRUCache(maxsize=128)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._hit_counts: dict = {}
        self._sources: dict = {}

    # ── Source registry ───────────────────────────────────────────────────────

    def register_source(
        self, name: str, provider
    ) -> "TarlRuntime":
        """
        Bind a data provider to source:<name> condition references.

        provider — a list/set (static) or a zero-arg callable that
                   returns a list/set each time it is called.
        Returns self for chaining.
        """
        self._sources[name] = provider
        return self

    def _inject_sources(self, context: dict) -> dict:
        """Resolve all registered sources and inject into a context copy."""
        if not self._sources:
            return context
        ctx = dict(context)
        for name, provider in self._sources.items():
            try:
                value = provider() if callable(provider) else provider
            except Exception:
                value = []
            ctx[f"source:{name}"] = value
        return ctx

    # ── Policy management ─────────────────────────────────────────────────────

    def set_policy(self, new_policy: TarlPolicy):
        """Replace the active policy and reset the cache and hit counts."""
        self.policy = new_policy
        self.cache.clear()
        self._hit_counts = {
            i: 0 for i in range(len(new_policy.rules))
        }

    # ── Evaluation ────────────────────────────────────────────────────────────

    def evaluate(
        self,
        context: dict,
        policy_text: Optional[str] = None,
    ) -> TarlDecision:
        """
        Evaluate the active policy (or policy_text if supplied) against
        context. Sources are resolved before evaluation. Returns the
        first matching rule's verdict, or DEFAULT_DENY.
        """
        ctx = self._inject_sources(context)
        cache_key = str(sorted(ctx.items()))

        if policy_text is not None:
            policy = PolicyParser.parse(policy_text)
        else:
            policy = self.policy

        if not policy.rules:
            return DEFAULT_DENY

        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        ordered_indices = sorted(
            range(len(policy.rules)),
            key=lambda i: self._hit_counts.get(i, 0),
            reverse=True,
        )

        futures_by_idx = {}
        for idx in ordered_indices:
            rule = policy.rules[idx]
            future = self.executor.submit(
                self._evaluate_rule, rule, ctx
            )
            futures_by_idx[idx] = (future, rule)

        results = {}
        for idx, (future, rule) in futures_by_idx.items():
            try:
                matched, decision = future.result()
                results[idx] = (matched, decision, rule)
            except Exception:
                results[idx] = (
                    False,
                    TarlDecision(
                        verdict=TarlVerdict.DENY,
                        reason="Evaluation error",
                    ),
                    rule,
                )

        for idx in ordered_indices:
            matched, decision, rule = results[idx]
            if matched:
                self._hit_counts[idx] = (
                    self._hit_counts.get(idx, 0) + 1
                )
                result = TarlDecision(
                    verdict=decision.verdict,
                    reason=decision.reason or f"Rule matched: {rule}",
                    rule_index=idx,
                    matched_rule=str(rule),
                )
                self.cache.put(cache_key, result)
                return result

        self.cache.put(cache_key, DEFAULT_DENY)
        return DEFAULT_DENY

    def _evaluate_rule(
        self, rule: TarlRule, context: dict
    ) -> tuple:
        """Evaluate one rule. Returns (matched, TarlDecision)."""
        try:
            tokens = PolicyParser._tokenize(rule.condition)
            matched = SafeExpr.evaluate(tokens, context)
            if matched:
                return True, TarlDecision(
                    verdict=rule.verdict,
                    reason=f"Condition '{rule.condition}' matched",
                )
            return False, TarlDecision(
                verdict=rule.verdict,
                reason="Condition did not match",
            )
        except Exception as exc:
            return False, TarlDecision(
                verdict=rule.verdict,
                reason=f"Evaluation error: {exc}",
            )

    def shutdown(self):
        """Clean up the thread pool."""
        self.executor.shutdown(wait=False)
