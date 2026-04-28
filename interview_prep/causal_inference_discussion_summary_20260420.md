# Causal Inference Discussion Summary

This note summarizes our discussion with an emphasis on interview-ready intuition, especially for Amazon Music and marketing measurement settings.

## 1. Difference-in-Differences

Difference-in-differences (`DiD`) is a causal inference method commonly used in observational or quasi-experimental settings. It estimates treatment effects by comparing the change in the treated group to the change in the control group.

The canonical 2x2 estimator is:

```text
DiD = (Y_T,post - Y_T,pre) - (Y_C,post - Y_C,pre)
```

Equivalent interpretation:

```text
DiD = (Y_T,post - Y_C,post) - (Y_T,pre - Y_C,pre)
```

### Classical intuition

The more classical way to think about DiD is:

1. Take the before/after difference within each group.
2. Compare those changes across treated and control.

Under that interpretation:

- The first difference over time removes time-invariant group differences.
- The second difference across groups removes shocks common to both groups over time.

### Amazon Music example

Suppose some DMAs receive a geo-targeted Amazon Music campaign and others do not. If treated DMAs increase streams by 25 and control DMAs increase by 10 over the same period, the estimated treatment effect is 15.

### Key assumption: parallel trends

Absent treatment, the treated group would have followed the same trend in untreated outcomes as the control group.

Important nuance:

- Parallel trends is about trends in untreated potential outcomes.
- It does not require equal levels.
- It is fundamentally untestable because the treated group's untreated post-treatment path is never observed.

What we can do instead:

- Inspect pre-trends.
- Run placebo or falsification tests.
- Use institutional knowledge to defend the design.

## 2. Event Studies

An event study is a DiD extension that replaces one post-treatment indicator with a set of relative-time indicators.

Relative time is:

```text
event time = calendar time - treatment start time
```

So:

- `-2` means two periods before treatment
- `-1` is often the omitted reference period
- `0` is treatment period
- `+2` means two periods after treatment

### Typical specification

```text
Y_it = alpha_i + lambda_t + sum_k beta_k * 1{t - T_i = k} + error_it
```

with one event-time indicator omitted, usually `k = -1`.

### Interpretation of leads and lags

If `-1` is the reference period, each coefficient compares the treated-control gap at event time `k` to the treated-control gap at event time `-1`.

For example:

```text
beta_k = (treated-control gap at k) - (treated-control gap at -1)
```

So if `beta_-2 = 0`, that means the treated-control gap two periods before treatment is the same as the treated-control gap one period before treatment.

### What leads do

Leads are the pre-treatment coefficients.

They help assess whether treated and control groups were evolving similarly before treatment.

If lead coefficients are close to zero:

- that supports the absence of differential pre-trends
- but does not prove parallel trends

### What lags do

Lags are the treatment-period and post-treatment coefficients.

They show whether the treatment effect is:

- immediate
- delayed
- ramping up
- fading out
- persistent

### Interview-ready summary

Event studies are useful for:

- checking pre-trends
- studying dynamic treatment effects
- visualizing treatment timing and persistence

## 3. Placebo and Falsification Tests

Placebo tests ask:

```text
If I pretend treatment happened when or where it did not, do I still estimate an effect?
```

If yes, that weakens the causal story.

### Useful placebo ideas in Amazon Music

- Fake treatment dates in the pre-period
- Fake treated DMAs
- Future-treated DMAs treated early as a placebo
- Untargeted artists or genres as placebo outcomes
- User segments that should not respond
- Random reassignment or permutation tests

### What placebo tests do and do not do

- Passing them adds credibility.
- Failing them is a red flag.
- Passing them still does not prove identification.

## 4. Inference in DiD: Clustering and Block Bootstrap

In many DiD applications, treatment varies at a group level, such as DMA or state, while outcomes may be observed at a more granular level, such as user or store.

This creates two problems:

- observations within a group are correlated
- observations within a group are serially correlated over time

If we ignore that and use naive standard errors, we overstate precision and overreject the null.

### Clustering

Cluster at the level of treatment assignment.

Examples:

- User-level outcomes with DMA-level randomization -> cluster by DMA
- Store-level outcomes with state-level policy treatment -> cluster by state

Why:

- units inside the same DMA share treatment assignment
- they may share local shocks
- repeated outcomes inside the same DMA are correlated over time

### User clustering vs DMA clustering

If treatment is randomized at the DMA level and users are nested within DMAs:

- clustering by DMA is usually the right default
- clustering by user alone is not enough

Why user clustering alone fails:

- it captures within-user serial correlation
- but misses correlation across different users in the same treated DMA

### Block bootstrap

With block bootstrap, resample clusters with replacement.

For a DMA-level Amazon Music campaign:

1. Sample treated DMAs with replacement.
2. Sample control DMAs with replacement.
3. Recompute the DiD estimate.
4. Repeat many times.
5. Compute the sample variance of the bootstrap estimates.

Bootstrap variance:

```text
Var_boot = [1 / (B - 1)] * sum_b (tau_b* - mean_boot)^2
```

Bootstrap standard error:

```text
SE_boot = sqrt(Var_boot)
```

### Small number of clusters

When the number of clusters is small, ordinary clustered standard errors can still be unreliable.

Possible remedies:

- wild cluster bootstrap
- randomization inference
- careful robustness checks

## 5. Triple Differences

Triple differences (`DDD`) add one more comparison group to remove one more layer of confounding.

The core idea:

- DiD removes common time shocks across treated and control units.
- DDD can additionally remove shocks that differ across subgroups within units.

### Amazon Music example

Suppose:

- treated DMAs receive a rock campaign
- control DMAs do not
- a local festival affects all music listening in treated DMAs

A plain DiD on rock streams is biased upward because it captures:

- campaign effect
- local festival effect

Now define a within-DMA comparison group:

- treated content group: rock
- untreated comparison group: country

Then DDD is:

```text
[(Rock - Country)_treated,post - (Rock - Country)_treated,pre]
- [(Rock - Country)_control,post - (Rock - Country)_control,pre]
```

### What each comparison removes

- `Rock - Country` within a DMA helps remove DMA-specific music shocks, like the festival, if they affect both genres similarly.
- Comparing treated vs control DMAs removes general rock-vs-country trends that would have happened anyway.

### Important nuance

Sometimes the within-DMA comparison group alone is enough, but only under a stronger assumption that the subgroup gap would otherwise have stayed stable. DDD is useful when that gap might also be changing in untreated markets.

### DDD identifying assumption

Absent treatment, the subgroup gap would have evolved similarly in treated and control units.

In the example:

- the `rock minus country` gap in treated DMAs would have evolved like the `rock minus country` gap in control DMAs absent the campaign

## 6. Staggered Treatment and TWFE Problems

With staggered adoption, different units receive treatment at different times.

Example:

- Seattle gets the campaign in week 4
- Atlanta in week 6
- Boston in week 8

### Why naive TWFE breaks

A vanilla two-way fixed effects (`TWFE`) regression may compare:

- newly treated units
to
- already treated units

Those are bad controls.

### Why heterogeneity matters

Problems become serious when treatment effects are heterogeneous:

- across DMAs
- across cohorts
- over event time

Then TWFE becomes a weighted average of many comparisons, including contaminated ones.

Those implicit weights can be:

- hard to interpret
- negative
- sign-reversing in extreme cases

### When vanilla staggered TWFE is relatively safe

The clean practical case is:

- treatment effects are homogeneous across units
- treatment effects are constant over time since treatment
- no anticipation

In practice, these conditions are often unrealistic in marketing settings.

## 7. Typical Fixes for Staggered Adoption

The main principle is:

- avoid using already treated units as controls

### Callaway and Sant'Anna

This estimator builds `ATT(g,t)`:

- effect for cohort `g`
- in calendar period `t`

Controls:

- never-treated units
- not-yet-treated units at time `t`

Good when you want:

- cohort-time effects
- overall ATT summaries
- a transparent modern DiD framework

### Sun and Abraham

This is mainly an event-study solution for staggered treatment timing.

Key idea:

- estimate effects in event time
- compare treated cohorts to valid controls in the same calendar period
- avoid already-treated units as controls

Important nuance:

- Sun-Abraham works in event time
- but the actual comparisons are made in calendar time

Good when you want:

- clean leads and lags
- dynamic effects
- pre-trend checks under staggered adoption

### Core difference between Callaway-Sant'Anna and Sun-Abraham

- Callaway-Sant'Anna is organized around cohort and calendar time
- Sun-Abraham is organized around event time

Both avoid comparing newly treated units to already treated units.

### Borusyak, Jaravel, and Spiess

This is an imputation-style approach.

Idea:

1. Estimate untreated outcome paths using untreated observations.
2. Impute missing untreated outcomes for treated units after treatment.
3. Compare observed outcomes to imputed untreated outcomes.

Good when you want:

- an intuitive counterfactual construction
- a flexible staggered adoption estimator

### Stacked DiD

Build many cleaner cohort-specific 2x2-style studies and stack them.

Good when you want:

- a pragmatic implementation
- a design that is easier to explain operationally

## 8. Matrix Completion for Panel Data

Matrix completion is a way to estimate missing counterfactual outcomes in panel data by exploiting low-rank structure.

Think of the panel as a matrix:

- rows = units, such as DMAs
- columns = time periods
- cells = outcomes, such as streams

Once a unit is treated, its untreated post-treatment outcomes are missing. Matrix completion tries to reconstruct those missing cells using the structure in the observed data.

### Intuition

Panel outcomes are often driven by a few latent factors, such as:

- national demand
- seasonality
- genre cycles
- DMA-specific demand intensity

If those latent patterns explain most of the matrix, missing untreated outcomes can be imputed.

### Why use it

- richer structure than simple DiD
- useful when low-rank latent factors seem plausible
- a flexible alternative to more restrictive panel methods

### Caveat

It is not assumption-free. It replaces simple DiD structure with stronger assumptions about latent low-rank panel structure.

## 9. Interview-Ready Reminders

- Always define the estimand first.
- Explain what the comparison group is and why it is credible.
- State the identifying assumptions clearly.
- Say what would break the design.
- Distinguish association from causation.
- For DiD, mention pre-trends, placebos, anticipation, spillovers, and inference.
- For staggered adoption, explicitly say you would avoid naive TWFE if treatment effects may be heterogeneous.

## 10. Compact Takeaways

- DiD compares changes, not levels.
- Parallel trends is untestable, but pre-trends and placebos provide supporting evidence.
- Event studies help assess pre-trends and dynamic effects.
- Cluster at the level of treatment assignment.
- Triple differences add a within-unit comparison to remove one more source of confounding.
- Staggered TWFE is often problematic in practice because treatment effects are rarely constant and homogeneous.
- Modern fixes include Callaway-Sant'Anna, Sun-Abraham, BJS, and stacked DiD.
- Matrix completion uses latent structure to impute missing untreated outcomes in panel data.
