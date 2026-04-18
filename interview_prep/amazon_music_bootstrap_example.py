"""Minimal bootstrap example for an Amazon Music interview-style question.

Problem:
Amazon Music runs a win-back campaign and randomizes households into:
    - control: no campaign
    - treatment: received the campaign

For each household we observe whether they started a trial in the next 14 days.
Estimate:
    1. observed conversion rates
    2. absolute lift
    3. a bootstrap confidence interval for that lift
"""

from random import Random


def conversion_rate(outcomes):
    if not outcomes:
        raise ValueError("outcomes must be non-empty")
    return sum(outcomes) / len(outcomes)


def absolute_lift(treatment, control):
    return conversion_rate(treatment) - conversion_rate(control)


def bootstrap_sample(values, rng):
    sample = []
    for _ in range(len(values)):
        index = rng.randrange(len(values))
        sample.append(values[index])
    return sample


def percentile(sorted_values, p):
    if not sorted_values:
        raise ValueError("sorted_values must be non-empty")
    if p < 0 or p > 1:
        raise ValueError("p must be between 0 and 1")
    index = int(p * (len(sorted_values) - 1))
    return sorted_values[index]


def bootstrap_metric(treatment, control, metric_fn, iterations=10000, confidence=0.95, seed=7):
    if not treatment or not control:
        raise ValueError("treatment and control must both be non-empty")
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    rng = Random(seed)
    observed = metric_fn(treatment, control)

    estimates = []
    for _ in range(iterations):
        treatment_resample = bootstrap_sample(treatment, rng)
        control_resample = bootstrap_sample(control, rng)
        estimate = metric_fn(treatment_resample, control_resample)
        estimates.append(estimate)

    estimates.sort()
    alpha = 1.0 - confidence
    low = percentile(estimates, alpha / 2.0)
    high = percentile(estimates, 1.0 - alpha / 2.0)

    return observed, low, high


def format_percent(value):
    return f"{100 * value:.2f}%"


def main():
    control = [
        0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    ]
    treatment = [
        0, 1, 0, 1, 0, 1, 1, 0, 0, 1,
        0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
    ]

    observed, low, high = bootstrap_metric(treatment, control, absolute_lift)

    print("Observed rates")
    print(f"  control conversion:   {format_percent(conversion_rate(control))}")
    print(f"  treatment conversion: {format_percent(conversion_rate(treatment))}")
    print()
    print("Bootstrap results")
    print(f"  absolute lift: {format_percent(observed)}")
    print(f"  95% CI: ({format_percent(low)}, {format_percent(high)})")


if __name__ == "__main__":
    main()
