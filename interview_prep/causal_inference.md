# Causal Inference

## Core objects

- Unit `i`: the entity of interest, such as a user, artist, geo, or campaign cell
- Treatment `W_i`: `1` if treated, `0` if control
- Potential outcomes:
  - `Y_i(1)`: outcome under treatment
  - `Y_i(0)`: outcome under control
- Observed outcome:
  - `Y_i = W_i Y_i(1) + (1 - W_i) Y_i(0)`

## Estimands

- Individual treatment effect: `Y_i(1) - Y_i(0)`
- Average treatment effect (ATE): `E[Y(1) - Y(0)]`
- Average treatment effect on the treated (ATT): `E[Y(1) - Y(0) | W = 1]`
- Conditional average treatment effect (CATE): `E[Y(1) - Y(0) | X]`

## Core assumptions

### Consistency

If unit `i` receives treatment `w`, then the observed outcome equals the potential outcome under `w`.

### Ignorability / unconfoundedness

`(Y_i(0), Y_i(1))` is independent of `W_i` given `X_i`

Plain meaning: after conditioning on observed covariates `X`, treatment assignment is independent of the potential outcomes.

### Positivity / overlap

`0 < Pr(W_i = 1 | X_i = x) < 1`

Plain meaning: for any relevant covariate profile, there is some chance of treatment and some chance of control.

### SUTVA

- No hidden versions of treatment
- One unit's outcome is not affected by another unit's treatment

This can fail in marketing when users influence each other or channels interact.

## Interpretation bridge

Under consistency and ignorability:

- `Pr(Y(w) | X) = Pr(Y_obs | X, W = w)`
- `E[Y(w) | X] = E[Y_obs | X, W = w]`

Interpretation: within a covariate slice `X`, observed outcomes among units that got `w` can stand in for the potential outcomes under `w`.

## DAG vocabulary

### Confounder

A common cause of treatment and outcome.

`X -> W` and `X -> Y`

Usually adjust for confounders.

### Mediator

On the causal path from treatment to outcome.

`W -> M -> Y`

Adjusting for mediators changes the estimand.

### Collider

A common effect of two variables.

`A -> C <- B`

Do not condition on colliders unless you have a specific reason and understand the induced bias.

## Common designs and tools

- Outcome regression
- Matching
- Propensity score methods
- Inverse probability weighting
- Doubly robust estimation
- Difference-in-differences
- Instrumental variables
- Regression discontinuity
- Synthetic control

## Failure modes to watch

- Omitted variable bias
- Selection bias
- Collider bias
- Post-treatment adjustment
- Poor overlap / extreme propensity scores
- Interference between units
- Bad estimand definition

## Interview prompts

- What is the estimand?
- Why is this causal question identifiable?
- What assumptions are required?
- Which variables should you adjust for, and which should you not?
- What would make your estimate biased?
- What would you do if randomization is impossible?

## Amazon Music framing

Useful examples:

- Incremental effect of a marketing campaign on trial starts
- Effect of a playlist recommendation treatment on listening hours
- Impact of a retention offer on churn
- Geo-level lift from an artist promotion campaign
