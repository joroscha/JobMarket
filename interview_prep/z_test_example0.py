"""Amazon Music conversion-lift z-test example.

Problem:
Amazon Music tests a new win-back campaign and observes conversions in
treatment and control.

Goal:
Write a small function that computes:
- control conversion rate
- treatment conversion rate
- absolute lift
- pooled-rate standard error under the null
- z-statistic
- p-value

Use only the Python standard library.
"""

import math


def normal_cdf(x):
    """Standard normal CDF using the error function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def conversion_lift_z_test(
    control_conversions,
    control_total,
    treatment_conversions,
    treatment_total,
    alternative="two-sided",
):
    """Compute a two-sample z-test for difference in conversion rates.

    alternative:
    - "two-sided": p_treatment != p_control
    - "greater": p_treatment > p_control
    - "less": p_treatment < p_control
    """
    if control_total <= 0 or treatment_total <= 0:
        raise ValueError("Group totals must be greater than zero")

    if not (0 <= control_conversions <= control_total):
        raise ValueError("Control conversions must be between 0 and control_total")

    if not (0 <= treatment_conversions <= treatment_total):
        raise ValueError("Treatment conversions must be between 0 and treatment_total")

    if alternative not in {"two-sided", "greater", "less"}:
        raise ValueError("alternative must be 'two-sided', 'greater', or 'less'")

    control_rate = control_conversions / control_total
    treatment_rate = treatment_conversions / treatment_total
    lift = treatment_rate - control_rate

    pooled_rate = (control_conversions + treatment_conversions) / (
        control_total + treatment_total
    )

    standard_error = math.sqrt(
        pooled_rate
        * (1.0 - pooled_rate)
        * ((1.0 / control_total) + (1.0 / treatment_total))
    )
    
    if standard_error == 0:
        raise ValueError("Standard error is zero; z-statistic is undefined")

    z_stat = lift / standard_error

    if alternative == "two-sided":
        p_value = 2.0 * (1.0 - normal_cdf(abs(z_stat)))
    elif alternative == "greater":
        p_value = 1.0 - normal_cdf(z_stat)
    else:
        p_value = normal_cdf(z_stat)

    return {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "lift": lift,
        "pooled_rate": pooled_rate,
        "standard_error": standard_error,
        "z_stat": z_stat,
        "p_value": p_value,
    }


def main():
    summary = conversion_lift_z_test(
        control_conversions=100,
        control_total=1000,
        treatment_conversions=120,
        treatment_total=1000,
        alternative="two-sided",
    )
    print(summary)


if __name__ == "__main__":
    main()
