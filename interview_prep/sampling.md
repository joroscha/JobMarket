# Sampling Notes

## What This Problem Family Is
- Weighted sampling from a discrete distribution.
- Estimating the expected number of unique labels after `n` draws.
- Estimating probabilities of events like `P(at least one rare label)`.
- Estimating stopping times like draws needed until all labels appear.
- These are often simulation questions with coding, edge-case, and interpretation follow-ups.

## With vs Without Replacement
- Decision rule: `Does one draw change the next draw's distribution?`
- With replacement:
  - Use when draws come from an ongoing distribution.
  - One draw does not remove mass from future draws.
  - Good for impressions, listens, or arrivals over time.
- Without replacement:
  - Use when sampling from a fixed finite pool.
  - Each draw consumes one unit and changes the remaining distribution.
  - Good for a frozen inventory or a fixed batch of items.
- Amazon Music examples:
  - Future impressions from a stable genre mix: with replacement.
  - Sampling from a fixed daily inventory of impression slots: without replacement.

## Representing the Population
- Expanded list:
  - Example: `{"a": 2, "b": 1}` -> `["a", "a", "b"]`
  - Easiest to reason about and code.
  - Higher memory cost when counts are large.
- Counts-only representation:
  - Keep `label -> count`.
  - Better when counts are large.
  - Requires weighted sampling logic instead of direct list sampling.
- What to remember:
  - Expanded list is fine as a first solution.
  - Counts-only is a strong follow-up when asked not to materialize the population.

## Sampling Methods
- High-level helpers:
  - `random.choices(labels, weights=counts, k=n)` -> with replacement.
  - `random.sample(labels, counts=counts, k=n)` -> without replacement.
- Manual cumulative-count sampling:
  - Let counts define intervals over total mass.
  - Example:
    - `a` covers `[0, 20)`
    - `b` covers `[20, 30)`
    - `c` covers `[30, 35)`
  - Draw an integer in `[0, total_count)`.
  - Walk cumulative counts and return the interval containing the draw.
- Inverse transform sampling:
  - Discrete version of sampling from a CDF.
  - The cumulative-count method above is inverse transform sampling.
- Without replacement using counts:
  - Copy the counts dictionary.
  - Sample from current cumulative mass.
  - Decrement the chosen label count by 1.
  - Repeat with the updated counts.

## Monte Carlo Simulation
- Monte Carlo = use repeated random draws to estimate a quantity.
- Your examples are Monte Carlo because they:
  - simulate random samples,
  - compute a statistic on each run,
  - average across runs.
- Standard workflow:
  - define one simulation run,
  - compute the quantity of interest,
  - repeat `B` times,
  - summarize with a mean or probability.
- Examples:
  - expected unique labels after `n` draws,
  - probability of at least one jazz impression,
  - expected draws until all labels appear,
  - bootstrap estimates of lift.

## Uncertainty
- There are two layers.

### Process Variability
- The simulated outcome itself varies across runs.
- Example:
  - one run gives `3` unique labels,
  - another gives `4`.
- Measure it with the empirical standard deviation of the simulation outputs.
- In code:
  - `statistics.stdev(unique_counts)`

### Monte Carlo Estimator Variability
- The estimated mean from `B` runs is itself noisy because `B` is finite.
- If `Y_1, ..., Y_B` are the simulation outputs:
  - `mean_hat = average(Y_b)`
  - `empirical_sd = stdev(Y_b)`
  - `mc_se = empirical_sd / sqrt(B)`
- What to remember:
  - process variability is the spread of outcomes,
  - Monte Carlo uncertainty is the uncertainty in the estimated mean.
- More simulations reduce Monte Carlo uncertainty, not process variability.

## When To Stop / How Many Simulations Are Enough
- There is no universal number.
- Start with something reasonable like `1,000`, `5,000`, or `10,000`.
- Check convergence:
  - compare estimates across larger batches,
  - check whether the running mean stabilizes,
  - check whether the Monte Carlo standard error is small enough.
- Rule of thumb:
  - Monte Carlo uncertainty shrinks like `1 / sqrt(B)`.
  - To cut Monte Carlo error in half, you need about `4x` more simulations.
- You usually need more runs when:
  - the event is rare,
  - label frequencies are highly imbalanced,
  - the stopping-time distribution is wide,
  - you need tighter numerical precision.
- Interview phrasing:
  - `I'd start with around 10,000 runs, then check stability by increasing the number of simulations and seeing whether the estimate and Monte Carlo standard error materially change.`

## Practical Theory To Remember
- Counts act like probability mass.
- With replacement:
  - probabilities stay fixed across draws.
- Without replacement:
  - probabilities change after each draw because remaining mass changes.
- Inverse transform sampling:
  - sample a uniform draw from total mass,
  - map it into the cumulative intervals,
  - return the interval's label.
- `random.random()` returns a float in `[0.0, 1.0)`.
- `randrange(total)` returns an integer in `[0, total)`.
- If using `int(random() * total)`, multiply by `total`, not `total - 1`.
- In percentile code, use `len(values) - 1` only when the percentile input can equal `1`.

## Likely Interview Follow-Ups
- Is this with or without replacement?
- Do you want a probability, an expected value, or a stopping time?
- Can you do it without expanding the population?
- Can you do it using only `random.random()` or `randrange()`?
- What edge cases would you handle?
- How many simulations are enough?
- How would you quantify uncertainty?
- What is the complexity of your approach?
- How would you test this?
- What does this mean in an Amazon Music or marketing setting?

## Business Interpretation Prompts
- If labels are genres, what is the expected diversity after `n` impressions?
- If a label is rare, what is the probability that a user sees it at least once?
- If labels represent campaign exposures, are draws from a stable stream or a fixed batch?
- If households are the unit, does one sampled unit affect the next unit's probabilities?

## Common Mistakes
- Off-by-one indexing:
  - `int(random() * total)` is correct for `[0, total)`.
- Using `sample` when you need `choices`, or the reverse.
- Using `=+` instead of `+=`.
- Mixing up variance and standard deviation.
- Calling process standard deviation estimator uncertainty.
- Clamping `n` for with-replacement sampling when large `n` is valid.
- Forgetting that `statistics.stdev` needs at least 2 values.
- Failing to guard `n > total_count` in the without-replacement case.

## Related Practice Files
- `sampling_example_1.py`
  - expanded-list implementation for stopping-time style simulation.
- `sampling_example_2.py`
  - counts-only solution using high-level sampling helpers.
- `sampling_example_3.py`
  - counts-only solution using manual cumulative-count sampling.
- `amazon_music_bootstrap_example.py`
  - bootstrap as a resampling-based Monte Carlo method with uncertainty estimation.
