# Experimentation

## Why experiments matter

Randomization breaks the link between treatment assignment and potential outcomes, so treated and control groups are comparable in expectation.

## Basic setup

- Treatment group
- Control group
- Randomization unit
- Analysis unit
- Primary metric
- Secondary metrics
- Guardrail metrics

## Design questions

### What is the unit of randomization?

Choose the unit that matches how the treatment is delivered and where spillovers are manageable.

Examples:

- User-level randomization
- Session-level randomization
- Geo-level randomization
- Artist or campaign-cell randomization

### What metric are you trying to move?

Examples:

- Trial starts
- Paid subscriptions
- Listening hours
- Retention
- Churn
- Revenue per user

### What are the guardrails?

Examples:

- Ad load
- App latency
- Cancellation rate
- Customer complaints
- Artist engagement quality

## Core statistical concepts

- Null and alternative hypotheses
- Type I and Type II error
- Power
- Minimum detectable effect (MDE)
- Confidence intervals
- p-values
- Variance reduction
- Multiple testing
- Sequential testing / peeking

## Practical threats

- Sample ratio mismatch
- Noncompliance
- Attrition
- Novelty effects
- Interference / spillovers
- Delayed treatment effects
- Logging bugs
- Metric definition drift

## Design choices interviewers care about

- How to randomize
- How long to run the test
- Whether the MDE is business-relevant
- Whether the chosen metric reflects causal value
- How to deal with contamination
- Whether long-term effects differ from short-term lift

## Common experiment types

- Standard A/B test
- Holdout test
- Cluster-randomized experiment
- Switchback design
- Geo experiment
- Staggered rollout

## Null result interpretation

Ask:

- Was the test powered for the effect size that matters?
- Was implementation correct?
- Was the metric too noisy?
- Was the treatment too weak?
- Are there heterogeneous effects hidden in the average?
- Did the test run long enough to capture lagged impact?

## Marketing-specific cases

- Campaign incrementality using holdouts
- Geo experiment for artist promotion
- Measuring cannibalization across channels
- Estimating incremental paid subscriptions from a new campaign
- Testing different retention offers

## Interview prompts

- How would you design an experiment for this feature or campaign?
- What is the randomization unit and why?
- What could invalidate the result?
- How would you choose sample size?
- What do you do if the result is directionally positive but not significant?
