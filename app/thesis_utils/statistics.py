"""Statistical comparison helpers used by thesis analysis notebooks."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.metrics import f1_score


def holm_adjust(p_values: Sequence[float]) -> np.ndarray:
    """Apply Holm-Bonferroni correction while preserving input order."""

    p_values = np.asarray(p_values, dtype=float)
    count = len(p_values)

    if count == 0:
        return np.array([], dtype=float)

    order = np.argsort(p_values)
    adjusted = np.empty(count, dtype=float)
    running_max = 0.0

    for rank, idx in enumerate(order):
        corrected = min(1.0, (count - rank) * p_values[idx])
        running_max = max(running_max, corrected)
        adjusted[idx] = running_max

    return adjusted


def percentile_ci(values: Sequence[float], ci_level: float = 0.95) -> tuple[float, float]:
    """Return percentile confidence interval bounds."""

    values = np.asarray(values, dtype=float)
    alpha = 1.0 - ci_level
    return (
        float(np.quantile(values, alpha / 2)),
        float(np.quantile(values, 1 - alpha / 2)),
    )


def binomial_exact_two_sided(k: int, n: int) -> float:
    """Exact two-sided binomial p-value with a small dependency-free fallback."""

    if n == 0:
        return 1.0

    try:
        from scipy.stats import binomtest

        return float(binomtest(int(k), int(n), p=0.5, alternative="two-sided").pvalue)
    except Exception:
        k = int(k)
        n = int(n)
        p0 = 0.5 ** n
        probabilities = [p0]

        for i in range(n):
            probabilities.append(probabilities[-1] * (n - i) / (i + 1))

        observed = probabilities[k]
        return float(min(1.0, sum(p for p in probabilities if p <= observed + 1e-15)))


def mcnemar_test(correct_a: Sequence[bool], correct_b: Sequence[bool]) -> dict[str, float | int | str]:
    """Run exact or continuity-corrected McNemar on paired correctness arrays."""

    correct_a = np.asarray(correct_a, dtype=bool)
    correct_b = np.asarray(correct_b, dtype=bool)

    b = int(np.sum(correct_a & ~correct_b))
    c = int(np.sum(~correct_a & correct_b))
    discordant = b + c

    if discordant == 0:
        return {
            "b_a_correct_b_wrong": b,
            "c_a_wrong_b_correct": c,
            "discordant": discordant,
            "method": "no_discordance",
            "statistic": 0.0,
            "p_value": 1.0,
        }

    if discordant < 25:
        return {
            "b_a_correct_b_wrong": b,
            "c_a_wrong_b_correct": c,
            "discordant": discordant,
            "method": "exact_binomial",
            "statistic": float(min(b, c)),
            "p_value": binomial_exact_two_sided(min(b, c), discordant),
        }

    try:
        from scipy.stats import chi2

        statistic = (abs(b - c) - 1) ** 2 / discordant
        p_value = float(chi2.sf(statistic, df=1))
    except Exception:
        statistic = float("nan")
        p_value = float("nan")

    return {
        "b_a_correct_b_wrong": b,
        "c_a_wrong_b_correct": c,
        "discordant": discordant,
        "method": "chi_square_continuity_corrected",
        "statistic": float(statistic),
        "p_value": p_value,
    }


def paired_bootstrap_macro_f1(
    gold,
    pred_a,
    pred_b,
    *,
    labels: Sequence[str],
    n_bootstrap: int = 5000,
    random_state: int = 42,
    ci_level: float = 0.95,
) -> dict[str, float | bool]:
    """Estimate paired Macro-F1 difference and its percentile interval."""

    gold = np.asarray(gold)
    pred_a = np.asarray(pred_a)
    pred_b = np.asarray(pred_b)
    sample_count = len(gold)
    rng = np.random.default_rng(random_state)

    observed_a = f1_score(gold, pred_a, labels=labels, average="macro", zero_division=0)
    observed_b = f1_score(gold, pred_b, labels=labels, average="macro", zero_division=0)
    boot_diff = np.empty(n_bootstrap, dtype=float)

    for idx in range(n_bootstrap):
        sample_idx = rng.integers(0, sample_count, size=sample_count)
        boot_diff[idx] = (
            f1_score(gold[sample_idx], pred_a[sample_idx], labels=labels, average="macro", zero_division=0)
            - f1_score(gold[sample_idx], pred_b[sample_idx], labels=labels, average="macro", zero_division=0)
        )

    low, high = percentile_ci(boot_diff, ci_level)
    p_boot = 2 * min(np.mean(boot_diff <= 0), np.mean(boot_diff >= 0))

    return {
        "f1_macro_a": float(observed_a),
        "f1_macro_b": float(observed_b),
        "f1_macro_diff_a_minus_b": float(observed_a - observed_b),
        "diff_ci_low": low,
        "diff_ci_high": high,
        "diff_ci_excludes_zero": bool(low > 0 or high < 0),
        "bootstrap_two_sided_p_approx": min(float(p_boot), 1.0),
    }
