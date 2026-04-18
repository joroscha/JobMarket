# Bayesian

## Core idea

Bayesian inference updates beliefs about unknown quantities using observed data.

`posterior proportional to likelihood x prior`

## Building blocks

- Prior: belief before seeing current data
- Likelihood: probability of observed data under parameter values
- Posterior: updated belief after combining prior and data
- Posterior predictive distribution: distribution of future data given current evidence

## Useful contrasts with frequentist inference

### Bayesian

- Parameters are treated as uncertain
- Probability statements about parameters are allowed
- Credible intervals have a direct probabilistic interpretation

### Frequentist

- Parameters are fixed
- Randomness comes from repeated sampling
- Confidence intervals are about long-run procedure coverage

## Core examples

### Beta-Binomial

Useful for conversion-rate problems.

- Prior: `p ~ Beta(a, b)`
- Data: `y | p ~ Binomial(n, p)`
- Posterior: `p | y ~ Beta(a + y, b + n - y)`

### Normal-Normal

Useful for means with Gaussian assumptions.

## Bayesian A/B testing

Questions you can answer:

- What is the posterior probability that treatment beats control?
- What is the posterior distribution of the lift?
- What is the expected loss if we launch the worse option?

## Hierarchical models

Use when estimating many related effects:

- geos
- artist segments
- customer cohorts
- campaign cells

Why they matter:

- partial pooling
- shrinkage of noisy group estimates
- better estimates for sparse groups

## Interview-level use cases

- Small-sample experiments
- Geo experiments with noisy regional effects
- Borrowing strength across markets or artists
- Decision-making when a hard p-value threshold is not ideal

## Concepts to explain clearly

- Prior sensitivity
- Credible interval vs confidence interval
- Why shrinkage is useful
- Why Bayesian methods can be more natural for business decisions
- Why Bayesian results still depend on modeling assumptions

## Common cautions

- Bad priors can distort results
- Posterior probabilities are not magic if the model is wrong
- Bayesian methods do not remove selection bias
- You still need a valid design or strong identification assumptions

## Marketing examples

- Estimate campaign lift by geo with partial pooling across regions
- Compute posterior probability that a new campaign beats current targeting
- Estimate subscription conversion lift in sparse user segments

## Interview prompts

- Explain Bayes theorem in plain English
- When would you prefer Bayesian A/B testing?
- What is a credible interval?
- Why would a hierarchical model help in geo lift measurement?
