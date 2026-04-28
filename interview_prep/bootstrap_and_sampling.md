# Bootstrap And Sampling Notes

## Mental Map
- `Sampling / Monte Carlo`: simulate draws from a known or assumed process to estimate an expectation, probability, or stopping time.
- `Bootstrap`: resample from the observed data to estimate uncertainty for a statistic like lift or difference in means.
- `Bootstrap p-value`: build a null bootstrap distribution, then ask how extreme the observed statistic is under that null.
- `Randomization inference`: keep outcomes fixed and reshuffle treatment assignment to quantify assignment uncertainty under the sharp null.
- `Exact randomization inference`: enumerate all valid assignments instead of approximating with random permutations.

## When To Use What
- Use `Monte Carlo` when the question is: `What happens on average under this random process?`
- Use `bootstrap SE / CI` when the question is: `How uncertain is my estimated metric from observed data?`
- Use `bootstrap p-values` when you need a hypothesis test and the analytic null distribution is awkward or unavailable.
- Use `randomization inference` for randomized experiments when you want a p-value tied directly to the assignment mechanism.
- Use `exact randomization inference` only when the sample is small enough that all assignments are feasible to enumerate.

## With vs Without Replacement
- Decision rule: `Does one draw change the next draw's distribution?`
- With replacement:
  - one draw does not remove mass from future draws
  - use for ongoing streams like impressions or arrivals
  - Python: `random.choices(..., k=n)`
- Without replacement:
  - one draw changes what remains
  - use for fixed finite pools or assignment reshuffling
  - Python: `random.sample(..., k=n)`
- Randomization inference uses `without replacement` because each observed unit appears exactly once in each reassignment.
- Bootstrap uses `with replacement` because it resamples from the empirical distribution of the observed sample.

## Representing The Population
- Expanded list:
  - `{"a": 2, "b": 1}` -> `["a", "a", "b"]`
  - easiest baseline for interviews
  - can be memory-heavy when counts are large
- Counts-only representation:
  - keep `label -> count`
  - stronger follow-up when asked not to materialize the population
  - requires weighted sampling logic

## Useful Code Patterns
- Weighted sampling with replacement:
  - `random.choices(labels, weights=counts, k=n)`
- Sampling without replacement from counts:
  - `random.sample(labels, counts=counts, k=n)`
- Manual cumulative-mass sampling:
  - draw `u = randrange(total_count)`
  - walk cumulative counts until the interval contains `u`
- Permuting all units without replacement:
  - `rng.sample(pooled, len(pooled))`
- Counting exceedances explicitly:
  - `sum(1 if condition else 0 for x in values)`
- Counting exceedances with a filter:
  - `sum(1 for x in values if condition)`

## Monte Carlo Simulation
- Standard workflow:
  - define one simulation run
  - compute the statistic on that run
  - repeat `B` times
  - average or summarize the outputs
- Common examples:
  - expected number of unique labels after `n` draws
  - probability a rare label appears at least once
  - expected draws until all labels appear
- If `Y_1, ..., Y_B` are the simulation outputs:
  - `mean_hat = average(Y_b)`
  - `sample_sd = sqrt(sum((Y_b - mean_hat)^2) / (B - 1))`
  - `mc_se = sample_sd / sqrt(B)`
- Key distinction:
  - `sample_sd` = spread of single simulation outcomes
  - `mc_se` = uncertainty in the estimated mean because `B` is finite

## Monte Carlo Confidence Intervals
- Use these when your final estimator is the average of many simulation runs.
- Approximate `95%` CI for the Monte Carlo mean:
  - `mean_hat +/- 1.96 * mc_se`
- This is what you used in the unique-label simulation problem.
- Do not confuse `mc_se` with the spread of the simulation outputs themselves.

## How Many Simulations Are Enough
- There is no universal number.
- Practical checkpoints:
  - `100`, `500`, `1000`, `5000`, `10000`
  - or doubling batches: `1000`, `2000`, `4000`, `8000`
- What to check:
  - running mean stability
  - whether `mc_se` is small enough for the decision you care about
  - whether the estimate changes materially as `B` increases
- Rule of thumb:
  - Monte Carlo uncertainty shrinks like `1 / sqrt(B)`
  - to cut `mc_se` in half, you need about `4x` more iterations

## Bootstrap SE And CI
- Bootstrap setup:
  - resample from the observed sample with replacement
  - recompute the estimator each time
  - store all bootstrap estimates
- For treatment/control lift:
  - resample treatment within treatment
  - resample control within control
  - recompute `lift = rate_treat - rate_control`
- If `theta_1*, ..., theta_B*` are bootstrap estimates:
  - `mean_boot = average(theta_b*)`
  - `bootstrap_se = sqrt(sum((theta_b* - mean_boot)^2) / (B - 1))`
- Percentile bootstrap `95%` CI:
  - sort bootstrap estimates
  - `low = sorted_values[int(0.025 * (B - 1))]`
  - `high = sorted_values[int(0.975 * (B - 1))]`
- Important distinction from Monte Carlo:
  - bootstrap SE is the SD of the bootstrap estimates
  - you do `not` divide by `sqrt(B)` because the goal is the sampling distribution of the estimator itself

## Bootstrap P-Values
- Goal:
  - test a null hypothesis using a bootstrap null distribution
- For a pooled null bootstrap in a treatment/control problem:
  - pool treatment and control outcomes together
  - sample `n_treat` and `n_control` with replacement from the pooled outcomes
  - recompute the statistic each time
- Two-sided p-value:
  - `count = sum(1 if abs(x) >= abs(obs) else 0 for x in null_stats)`
  - `p = (count + 1) / (B + 1)`
- One-sided upper-tail p-value:
  - `count = sum(1 if x >= obs else 0 for x in null_stats)`
  - `p = (count + 1) / (B + 1)`
- For simple randomized experiments, bootstrap p-values are often less natural than randomization inference.

## Randomization Inference
- Question:
  - `Could this observed effect arise purely from treatment assignment randomness under the sharp null?`
- Sharp null:
  - `Y_i(1) = Y_i(0)` for every unit
- Procedure:
  - keep observed outcomes fixed
  - reshuffle assignment without replacement, preserving group sizes
  - recompute the statistic each time
- Two-sided RI p-value:
  - `count = sum(1 if abs(x) >= abs(obs) else 0 for x in null_stats)`
  - `p = (count + 1) / (B + 1)`
- One-sided RI p-value:
  - `count = sum(1 if x >= obs else 0 for x in null_stats)`
  - `p = (count + 1) / (B + 1)`
- Clean coding pattern:
  - `perm = rng.sample(pooled, len(pooled))`
  - `fake_treat = perm[:n_treat]`
  - `fake_control = perm[n_treat:]`

## Exact Randomization Inference
- Use when the sample is small.
- Enumerate every valid treatment assignment that preserves the original treatment-group size.
- Important detail:
  - enumerate `unit indices`, not just unique outcome values, because repeated outcomes correspond to different units
- Standard tool:
  - `itertools.combinations(range(total_n), n_treat)`
- Exact p-value:
  - `count / total_assignments`
  - or include the observed stat explicitly if you want the same correction style
- This is exact because you evaluate the full null distribution instead of approximating it with random draws.

## One-Sided vs Two-Sided
- One-sided:
  - use when the alternative is directional and pre-specified
  - example: `treatment increases conversion`
  - compare `x >= obs`
- Two-sided:
  - default when you care about any change in either direction
  - compare `abs(x) >= abs(obs)`
- In interviews:
  - say you would default to two-sided unless the business question clearly specifies direction in advance

## Core Distinctions To Remember
- `Monte Carlo`:
  - resample from a modeled process
  - target is usually an expectation or probability
- `Bootstrap`:
  - resample observations from the sample
  - target is uncertainty of an estimator
- `Randomization inference`:
  - reshuffle treatment assignment
  - target is a null distribution under the experimental design
- `KS test`:
  - asks whether the full distributions differ
  - not just whether the means differ

## Practical Theory To Remember
- Counts act like probability mass.
- With replacement:
  - probabilities stay fixed across draws
- Without replacement:
  - probabilities change after each draw because remaining mass changes
- `random.random()` returns a float in `[0.0, 1.0)`
- `randrange(total)` returns an integer in `[0, total)`
- `int(random() * total)` is correct for mapping to `[0, total)`
- In percentile code, use `len(values) - 1` because the last valid index is `B - 1`
- In sample variance code, use `B - 1` because of the degrees-of-freedom correction, not because of Python indexing

## Common Mistakes
- Mixing up `random.sample` and `random.choices`
- Forgetting that `list.extend(...)` mutates in place and returns `None`
- Mixing up `sample_sd` and `mc_se`
- Dividing bootstrap SE by `sqrt(B)` when you should not
- Using a normal-approximation CI when the prompt asks for a percentile bootstrap CI
- Forgetting to preserve group sizes in bootstrap or randomization procedures
- Calling a Monte Carlo approximation an `exact` p-value
- Forgetting that two-sided tests should compare absolute values
- Not matching the written hypothesis to the actual code path

## Likely Interview Follow-Ups
- Is this with or without replacement?
- What exactly is random here: the sample, the assignment, or the data-generating process?
- Is this a one-sided or two-sided question?
- Why is this bootstrap and not randomization inference?
- Why is this Monte Carlo and not bootstrap?
- How many iterations are enough?
- How would you quantify uncertainty?
- Can you do it without expanding the population?
- Can you do it using only `random.random()` or `randrange()`?
- What edge cases would you handle?
- What is the complexity of your approach?

## Related Practice Files
- `sampling_example0.py`
  - Monte Carlo simulation for expected unique labels
- `sampling_example_1.py`
  - expanded-list implementation for stopping-time style simulation
- `sampling_example_2.py`
  - counts-only solution using high-level sampling helpers
- `sampling_example_3.py`
  - counts-only solution using manual cumulative-count sampling
- `bootstrap_example0.py`
  - bootstrap SE and percentile CI for lift
- `bootstrap_example1.py`
  - bootstrap null distribution and p-values
- `randomization_example0.py`
  - Monte Carlo randomization-inference p-values
- `randomization_example1.py`
  - exact randomization inference by enumerating assignments
- `amazon_music_bootstrap_example.py`
  - solved bootstrap reference example
