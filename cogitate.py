# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# cogitate.py
#
# Cogitate-style preregistration + process predictors of
# the collaboration gap (v0.19.0, deep-think upgrade #9,
# report.md section 9 rank 9 — the last unbuilt item).
#
# Sources (report.md sections 3 and 8):
#   - Cogitate Consortium, "Adversarial testing of
#     global neuronal workspace and integrated
#     information theories of consciousness", Nature
#     642:133-142, 2025, DOI 10.1038/s41586-025-08888-1
#     (preregistered adversarial collaboration, n=256;
#     posterior-synchrony analogue vs broadcast analogue:
#     sustained posterior synchronisation was absent,
#     onset ignition observed, offset ignition largely
#     absent — both theories substantially challenged).
#     The bridge imports the METHOD (adversarial
#     preregistration, predictions scored before looking
#     at results), not any one theory's content.
#   - Woolley et al., "Evidence for a collective
#     intelligence factor in the performance of human
#     groups", Science 330:686-688, 2010 (c-factor:
#     mean social sensitivity and equal turn-taking
#     predict group performance; NOT mean/max member
#     IQ; replication contested — leading hypothesis,
#     not established fact).
#
# The construction (fixed before the pilot; see
# docs/preregistration-v0.19.0.md):
#   - The run is the standard design-B collaboration
#     run (N=4, 10 generations, 200 samples per
#     generation) from empathy_field.run_collaboration,
#     whose per-generation rows carry the process
#     variables additively (v0.19.0): "d_per_agent"
#     (per-agent D), "r_mean" (mean pairwise R that
#     generation), "r_posterior_mean" (mean pairwise R
#     within the "posterior" subset = agents {0, 1} by
#     index, fixed before looking).
#   - Per (sigma, seed) run:
#       gap_bits: pooled H_collab - H_isolated.
#       mean_R: mean pairwise R over all generations
#         and pairs (mean social sensitivity analogue).
#       mean_D, max_D: mean / max of per-agent D over
#         all generations (individual-ability analogues).
#       var_D: variance of per-agent D across members,
#         averaged over generations; the equality
#         predictor is -var_D (higher = more equal
#         turn-taking).
#       post_R_sustained: mean over generations of
#         r_posterior_mean (posterior-synchrony
#         analogue); its minimum over generations is
#         recorded as a diagnostic, not gated.
#       broadcast: min(onset, offset), onset = r_mean
#         at generation 0, offset = r_mean at the
#         final generation (ignition at BOTH ends,
#         the GNWT analogue).
#   - Per-seed Pearsons are computed across the sigma
#     grid within each seed (n = number of sigma values).
#   - Sigma grid: te.SIGMA_GRID, which has SEVEN values
#     [0.0, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0] — so the
#     pooled regression in (lxiii) runs over 28 runs
#     (7 sigma x 4 seeds), not 20. The "5 sigma" in the
#     task brief assumed a 5-value grid; the grid as it
#     exists in the code is authoritative.
#
# Frozen bars (from the calibration pilot on seeds 42
# and 7 only — see docs/preregistration-v0.19.0.md):
#   (lx)  MARGIN_LX = 0.10 (calibration worst
#         sub-margin 0.1252, seed 42, mean_R - mean_D).
#   (lxi) BAR_LXI = 0.70 (calibration worst
#         Pearson(gap, -var_D) = 0.7566, seed 7).
#   (lxii) BAR_LXII = 0.80 (calibration worst
#         max(post, broadcast) = 0.8657, seed 7);
#         MARGIN_LXII = 1.00 (calibration worst
#         |post - broadcast| = 1.7568, seed 7).
#   (lxiii) MARGIN_LXIII = 0.05 (calibration pooled
#         R^2 difference 0.1024 over 14 runs).
#
# Everything here is synthetic / classical: the agents
# are noisy copies of a uniform thought, D and R are
# defined overlaps, and no claim measures
# consciousness, resonance in a brain, or any theory
# of consciousness in a human. No Phi (IIT) is
# imported as a consciousness measure anywhere.

import math

import numpy as np

import empathy_field as ef
import thought_entanglement as te

CALIBRATION_SEEDS = (42, 7)
EVALUATION_SEEDS = (1234, 2026)
ALL_SEEDS = CALIBRATION_SEEDS + EVALUATION_SEEDS

POSTERIOR_INDICES = (0, 1)

MARGIN_LX = 0.10
BAR_LXI = 0.70
BAR_LXII = 0.80
MARGIN_LXII = 1.00
MARGIN_LXIII = 0.05


def pearson(xs, ys):
    """Pearson r, or None if degenerate (n < 2 or zero variance).

    A degenerate comparison is a failed sub-check with a
    reason, never a pass — see the claim verdicts.
    """
    xs = [float(x) for x in xs]
    ys = [float(y) for y in ys]
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0.0 or syy <= 0.0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


def run_predictors(sigma, seed, n_agents=4, generations=10,
                   n_samples=200, design="B"):
    """One design-B collaboration run + its process predictors.

    The predictors come from the collaborating arm's
    per-generation rows (the process that produces the
    gap); the isolated arm's rows are not used.
    """
    result = ef.run_collaboration(
        design=design, n_agents=n_agents, sigma=sigma,
        generations=generations, n_samples=n_samples, seed=seed)
    rows = result["collaborating"]["rows"]
    r_means = [r["r_mean"] for r in rows]
    post = [r["r_posterior_mean"] for r in rows]
    d_gens = [r["d_per_agent"] for r in rows]
    d_all = [d for ds in d_gens for d in ds]
    mean_d = sum(d_all) / len(d_all)
    var_ds = []
    for ds in d_gens:
        m = sum(ds) / len(ds)
        var_ds.append(sum((d - m) ** 2 for d in ds) / len(ds))
    return {
        "sigma": float(sigma),
        "seed": int(seed),
        "gap_bits": float(result["gap_bits"]),
        "mean_R": float(sum(r_means) / len(r_means)),
        "mean_D": float(mean_d),
        "max_D": float(max(d_all)),
        "var_D": float(sum(var_ds) / len(var_ds)),
        "neg_var_D": float(-sum(var_ds) / len(var_ds)),
        "post_R_sustained": float(sum(post) / len(post)),
        "post_R_min": float(min(post)),
        "broadcast": float(min(r_means[0], r_means[-1])),
        "onset_R": float(r_means[0]),
        "offset_R": float(r_means[-1]),
    }


def seed_sweep(seed, sigmas=None, **kwargs):
    """One run per sigma on the grid, for one seed."""
    return [run_predictors(s, seed, **kwargs)
            for s in (te.SIGMA_GRID if sigmas is None else sigmas)]


def per_seed_correlations(runs):
    """The six per-seed Pearsons across the sigma grid.

    Returns None for a correlation whose inputs are
    degenerate on this seed.
    """
    gap = [r["gap_bits"] for r in runs]
    return {
        "mean_R": pearson(gap, [r["mean_R"] for r in runs]),
        "mean_D": pearson(gap, [r["mean_D"] for r in runs]),
        "max_D": pearson(gap, [r["max_D"] for r in runs]),
        "neg_var_D": pearson(gap, [r["neg_var_D"] for r in runs]),
        "post": pearson(gap, [r["post_R_sustained"] for r in runs]),
        "broadcast": pearson(gap, [r["broadcast"] for r in runs]),
    }


def _subcheck(value, bar, name):
    """One gated comparison: (ok, detail). None fails."""
    if value is None:
        return False, "%s degenerate (zero variance)" % name
    return bool(value >= bar), "%s = %.4f (bar %.2f)" % (name, value, bar)


def claim_lx(corrs_by_seed):
    """(lx) Mean sensitivity beats individual D, every seed.

    Pearson(gap, mean_R) - Pearson(gap, max_D) >= margin
    AND Pearson(gap, mean_R) - Pearson(gap, mean_D) >= margin.
    """
    per_seed = {}
    overall = True
    for seed, c in corrs_by_seed.items():
        checks = {}
        for other in ("max_D", "mean_D"):
            if c["mean_R"] is None or c[other] is None:
                checks[other] = (False, "degenerate (zero variance)")
            else:
                diff = c["mean_R"] - c[other]
                checks[other] = (
                    bool(diff >= MARGIN_LX),
                    "mean_R - %s = %.4f (margin %.2f)"
                    % (other, diff, MARGIN_LX))
        ok = all(v[0] for v in checks.values())
        per_seed[seed] = {"pass": ok, "checks": checks}
        overall = overall and ok
    return {"claim": "lx", "pass": overall, "per_seed": per_seed}


def claim_lxi(corrs_by_seed):
    """(lxi) Turn-taking equality predicts the gap, every seed.

    Pearson(gap, -var_D) >= bar AND
    Pearson(gap, -var_D) > Pearson(gap, max_D).
    """
    per_seed = {}
    overall = True
    for seed, c in corrs_by_seed.items():
        ok_bar, detail_bar = _subcheck(c["neg_var_D"], BAR_LXI,
                                       "r(gap, -var_D)")
        if c["neg_var_D"] is None or c["max_D"] is None:
            ok_beats = False
            detail_beats = "degenerate (zero variance)"
        else:
            diff = c["neg_var_D"] - c["max_D"]
            ok_beats = bool(diff > 0.0)
            detail_beats = ("r(-var_D) - r(max_D) = %.4f"
                            % diff)
        ok = ok_bar and ok_beats
        per_seed[seed] = {"pass": ok,
                          "bar": (ok_bar, detail_bar),
                          "beats_max_D": (ok_beats, detail_beats)}
        overall = overall and ok
    return {"claim": "lxi", "pass": overall, "per_seed": per_seed}


def claim_lxii(corrs_by_seed):
    """(lxii) Posterior vs broadcast: separable, one predicts.

    max(r(post), r(broadcast)) >= bar AND
    |r(post) - r(broadcast)| >= margin, every seed.
    No direction presupposed — the winner is reported.
    """
    per_seed = {}
    overall = True
    for seed, c in corrs_by_seed.items():
        if c["post"] is None or c["broadcast"] is None:
            ok_best = False
            detail_best = "degenerate (zero variance)"
            ok_sep = False
            detail_sep = "degenerate (zero variance)"
            winner = None
        else:
            best = max(c["post"], c["broadcast"])
            winner = ("posterior" if c["post"] >= c["broadcast"]
                      else "broadcast")
            ok_best = bool(best >= BAR_LXII)
            detail_best = ("max(r) = %.4f (%s; bar %.2f)"
                           % (best, winner, BAR_LXII))
            sep = abs(c["post"] - c["broadcast"])
            ok_sep = bool(sep >= MARGIN_LXII)
            detail_sep = ("|r(post) - r(bcast)| = %.4f "
                          "(margin %.2f)" % (sep, MARGIN_LXII))
        ok = ok_best and ok_sep
        per_seed[seed] = {"pass": ok,
                          "winner": winner,
                          "best": (ok_best, detail_best),
                          "separation": (ok_sep, detail_sep)}
        overall = overall and ok
    return {"claim": "lxii", "pass": overall, "per_seed": per_seed}


def _r2(y, columns):
    """OLS R^2 of y on the given predictor columns + intercept."""
    y = np.asarray(y, dtype=float)
    x = np.column_stack([np.ones(len(y))]
                        + [np.asarray(c, dtype=float)
                           for c in columns])
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0.0:
        return None
    return 1.0 - ss_res / ss_tot


def _adjusted_r2(r2, n, k):
    """Adjusted R^2 (diagnostic: penalises extra predictors)."""
    if r2 is None or n - k - 1 <= 0:
        return None
    return 1.0 - (1.0 - r2) * (n - 1) / (n - k - 1)


def claim_lxiii(all_runs):
    """(lxiii) Pooled regression over all runs.

    R^2(gap ~ mean_R + (-var_D)) exceeds R^2(gap ~ max_D)
    by >= margin. Adjusted R^2 is reported as a
    diagnostic (the two-predictor model carries an extra
    parameter) and is not gated.
    """
    y = [r["gap_bits"] for r in all_runs]
    n = len(all_runs)
    r2_two = _r2(y, [[r["mean_R"] for r in all_runs],
                     [r["neg_var_D"] for r in all_runs]])
    r2_one = _r2(y, [[r["max_D"] for r in all_runs]])
    if r2_two is None or r2_one is None:
        return {"claim": "lxiii", "pass": False, "n_runs": n,
                "detail": "degenerate (zero variance in gap)"}
    diff = r2_two - r2_one
    return {
        "claim": "lxiii",
        "pass": bool(diff >= MARGIN_LXIII),
        "n_runs": n,
        "r2_two": r2_two,
        "r2_one": r2_one,
        "difference": diff,
        "margin": MARGIN_LXIII,
        "adj_r2_two": _adjusted_r2(r2_two, n, 2),
        "adj_r2_one": _adjusted_r2(r2_one, n, 1),
        "adj_difference": (_adjusted_r2(r2_two, n, 2)
                           - _adjusted_r2(r2_one, n, 1)),
        "detail": ("R^2(two) = %.4f, R^2(one) = %.4f, "
                   "difference = %.4f (margin %.2f)"
                   % (r2_two, r2_one, diff, MARGIN_LXIII)),
    }


def evaluate_claims(seeds=ALL_SEEDS, sigmas=None, **kwargs):
    """Full evaluation: per-seed sweeps + verdicts (lx)-(lxiii)."""
    runs_by_seed = {}
    for seed in seeds:
        runs_by_seed[seed] = seed_sweep(seed, sigmas=sigmas, **kwargs)
    corrs = {seed: per_seed_correlations(runs)
             for seed, runs in runs_by_seed.items()}
    all_runs = [r for seed in seeds for r in runs_by_seed[seed]]
    return {
        "runs_by_seed": runs_by_seed,
        "correlations": corrs,
        "lx": claim_lx(corrs),
        "lxi": claim_lxi(corrs),
        "lxii": claim_lxii(corrs),
        "lxiii": claim_lxiii(all_runs),
    }


def main():
    verdict = evaluate_claims()
    for seed in ALL_SEEDS:
        c = verdict["correlations"][seed]
        print("seed %d: r(mean_R)=%.4f r(mean_D)=%.4f r(max_D)=%.4f "
              "r(-var_D)=%.4f r(post)=%.4f r(bcast)=%.4f"
              % (seed, c["mean_R"], c["mean_D"], c["max_D"],
                 c["neg_var_D"], c["post"], c["broadcast"]))
    for key in ("lx", "lxi", "lxii", "lxiii"):
        v = verdict[key]
        print("(%s) %s" % (key, "PASS" if v["pass"] else "FAIL"))
    print("(lxiii) %s" % verdict["lxiii"]["detail"])


if __name__ == "__main__":
    main()
