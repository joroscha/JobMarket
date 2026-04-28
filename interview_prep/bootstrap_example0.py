"""Amazon Music bootstrap practice problem.

Problem:
Amazon Music runs a win-back campaign and randomizes households into:
    - control: no campaign
    - treatment: received the campaign

For each household we observe whether they started a trial in the next 14 days:
    - 1: started a trial
    - 0: did not start a trial

Goal:
Given two binary lists, estimate campaign lift with bootstrap resampling.

Required outputs:
1. control conversion rate
2. treatment conversion rate
3. observed absolute lift
4. bootstrap standard error
5. percentile bootstrap 95% confidence interval
6. a short stakeholder-facing interpretation

Clarify / decide:
- What exactly is being resampled?
  Resample households within treatment and control separately.
- Why resample groups separately?
  The bootstrap should preserve each group's sample size and empirical distribution.
- What lift should you estimate?
  Use absolute lift: treatment conversion rate minus control conversion rate.
- What inputs are valid?
  Non-empty binary lists and a positive number of bootstrap iterations.

Hint path:
1. Implement the observed metric first.
2. Write one bootstrap resample function.
3. On each bootstrap iteration, resample treatment and control separately.
4. Recompute the lift on each bootstrap resample.
5. Store all bootstrap lift estimates.
6. Compute the bootstrap standard error from that empirical distribution.
7. Sort the bootstrap estimates and extract percentile bounds.
8. Explain the result in plain English for a marketing stakeholder.

Suggested edge cases:
- empty treatment or control
- non-binary values
- non-positive iteration count
- invalid confidence level
- deterministic behavior with a fixed seed
- equal treatment and control performance
- treatment stronger than control

Use standard-library-only Python. No pandas, numpy, or scipy.
"""

from random import Random
import math


# TODO:
# 1. Validate that treatment and control are non-empty binary lists.
# 2. Implement conversion_rate(outcomes).
# 3. Implement absolute_lift(treatment, control).
# 4. Implement bootstrap_sample(values, rng) using same-length sampling with replacement.
# 5. Implement bootstrap_lift_distribution(...) and store every bootstrap lift estimate.
# 6. In summarize_bootstrap(...), compute:
#    - control_rate
#    - treatment_rate
#    - observed_lift
#    - bootstrap_se
#    - ci_low
#    - ci_high
# 7. After computing the summary, explain it in one sentence for a marketing stakeholder.


def conversion_rate(outcomes):
    """Return the mean of a binary outcome list."""
    return sum(outcomes)/len(outcomes)

def absolute_lift(treatment, control):
    """Return treatment conversion rate minus control conversion rate."""
    return conversion_rate(treatment) - conversion_rate(control)


def bootstrap_sample(values, rng):
    """Return a same-length bootstrap resample drawn with replacement."""
    random_sample = rng.choices(values,k=len(values))
    return random_sample


def bootstrap_lift_distribution(treatment, control, iterations=10000, seed=7):
    """Return a list of bootstrap lift estimates."""
    rng = Random(seed)
    lift_array = []
    for _ in range(iterations):
        treat_sample = bootstrap_sample(treatment, rng)
        control_sample = bootstrap_sample(control, rng)
        abs_lift = absolute_lift(treat_sample, control_sample)
        lift_array.append(abs_lift)
    return lift_array


def summarize_bootstrap(treatment, control, iterations=10000, confidence=0.95, seed=7):
    """Return a summary dictionary with these keys:

    - control_rate
    - treatment_rate
    - observed_lift
    - bootstrap_se
    - ci_low
    - ci_high
    """
    treatment_rate = conversion_rate(treatment)
    control_rate = conversion_rate(control)
    observed_lift = absolute_lift(treatment, control)
    lift_array = bootstrap_lift_distribution(treatment, control, iterations=iterations, seed=seed)
    sample_mean = sum(lift_array)/len(lift_array)
    #to compute boostrapped Standard Errors:
    sample_variance = sum((x-sample_mean)**2 for x in lift_array)/(len(lift_array)-1)
    sample_standard_dev = math.sqrt(sample_variance)
    bootstrap_se = sample_standard_dev
    sorted_list = sorted(lift_array)
    ci_low = sorted_list[int(0.025*(len(sorted_list)-1))]
    ci_high = sorted_list[int(0.975*(len(sorted_list)-1))]
    sol_dic = {
        'control_rate':control_rate,
        'treatment_rate':treatment_rate,
        'observed_lift':observed_lift,
        'bootstrap_se':bootstrap_se,
        'ci_low':ci_low,
        'ci_high':ci_high
    }
    return sol_dic
    

    

def main():
    control = [
        0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    ]
    treatment = [
        0, 1, 0, 1, 0, 1, 1, 0, 0, 1,
        0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
    ]

    print(summarize_bootstrap(treatment, control, iterations=10000, confidence=0.95, seed=7))
    print("Bootstrap practice prompt")
    print("Implement the TODO functions above, then try:")
    print("  summary = summarize_bootstrap(treatment, control, iterations=10000, seed=7)")
    print("  print(summary)")
    print()
    print("Sample sizes")
    print(f"  control households:   {len(control)}")
    print(f"  treatment households: {len(treatment)}")
    print()
    print("Follow-up")
    print("  After printing the summary, explain the result in one sentence for a marketing stakeholder.")


if __name__ == "__main__":
    main()
