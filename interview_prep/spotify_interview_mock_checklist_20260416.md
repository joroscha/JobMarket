# Spotify Interview Mock Checklist

## Core Answer Structure

- Clarify the goal first: what decision are we trying to support?
- Identify the unit of analysis: user, session, order, email, or experiment unit.
- State assumptions explicitly when the prompt is incomplete.
- Explain validation steps, not just the final answer.
- End with a practical recommendation.

## SQL / Data Manipulation

- Be comfortable with `GROUP BY`, `HAVING`, `CASE WHEN`, and joins.
- Be ready for window functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, cumulative sums.
- Use CTEs when the logic is easier to read step by step.
- Always check the grain of the data before writing the query.
- Ask whether a join can duplicate rows.
- Decide carefully between `COUNT(*)`, `COUNT(col)`, and `COUNT(DISTINCT ...)`.
- Check how nulls affect the result.
- Be explicit about whether filtering happens before or after aggregation.
- Mention how you would validate the output: row counts, unique IDs, totals, spot checks.

## Pandas / Python

- Favor readable transformations over clever shortcuts.
- Explain whether each step is filtering, aggregating, reshaping, or joining.
- Be fluent with `groupby`, `agg`, `transform`, `merge`, `concat`, `rank`, `sort_values`, `drop_duplicates`, `isna`, `notna`, `melt`, `pivot`, and `pivot_table`.
- Remember indexing pitfalls: `series.iloc[1]` is positional, `series[1]` may be label-based.
- When using a function, be clear on mutation vs reassignment.
- Sanity-check outputs with counts and small manual examples.

## Statistics

- Define a p-value correctly: probability, under the null, of observing a result at least as extreme as the one obtained.
- Define a confidence interval correctly: over repeated sampling, about 95% of 95% confidence intervals would contain the true parameter.
- Be ready to explain Type I error, Type II error, power, and MDE.
- Know the CLT and how it justifies approximate normal inference for sample means and large-sample tests.
- Be able to explain variance, covariance, expected value, and standard error in plain language.
- Know when to use a z-test versus a t-test.

## Experimentation

- State the primary metric first, then secondary metrics and guardrails.
- Confirm that the analysis unit matches the randomization unit.
- Distinguish statistical significance from practical significance.
- Be ready to discuss sample ratio mismatch, peeking, novelty effects, seasonality, interference, and multiple testing.
- For binary outcomes like conversion, know the difference-in-proportions setup.
- Know that `OLS(y ~ treatment)` with a binary outcome and intercept gives the treatment-control difference in means.
- Mention robust standard errors for binary outcomes or heteroskedastic settings.
- When interpreting results, talk about effect size, uncertainty, and business impact together.

## Probability

- Bayes' rule:
  \[
  P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}
  \]
  Think of it both as a probability identity and as a Bayesian updating rule: posterior = likelihood times prior, normalized by evidence.
- Law of total probability:
  \[
  P(B)=\sum_i P(B \mid A_i)P(A_i)
  \]
  Useful for aggregating over customer segments or user states.
- PMF vs PDF vs CDF:
  - PMF for discrete random variables: `P(X = x)`
  - PDF for continuous random variables: `f(x)`, where probabilities come from areas
  - CDF for either type: `F(x) = P(X <= x)`
- For continuous variables:
  \[
  F(x)=\int_{-\infty}^{x} f(t)\,dt
  \]
  The CDF is the accumulated area under the PDF up to `x`.
- Joint, marginal, and conditional:
  - joint: behavior of two variables together
  - marginal: one variable after summing/integrating out the other
  - conditional: one variable given the other
  - key identity:
    \[
    P(X,Y)=P(Y \mid X)P(X)
    \]
- Bernoulli:
  - one binary trial
  - `P(X = 1) = p`, `P(X = 0) = 1 - p`
  - mean `p`, variance `p(1-p)`
- Binomial:
  - number of successes in `n` independent Bernoulli trials with common success probability `p`
  - PMF:
    \[
    P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}
    \]
  - use for signup/conversion counts across exposed users
- Poisson:
  - count of events in a fixed interval
  - PMF:
    \[
    P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!}
    \]
  - use PMF for exactly `k`, CDF for at most `k`, and `1 - CDF(k)` for more than `k`
- Exponential:
  - waiting time to the next event with constant hazard/rate
  - PDF:
    \[
    f(x)=\lambda e^{-\lambda x}, \quad x \ge 0
    \]
  - useful as a first-pass waiting-time model; Cox is often more realistic for product time-to-event data
- Uniform on `[a,b]`:
  - PDF:
    \[
    f(x)=\frac{1}{b-a}
    \]
  - mean `(a+b)/2`, variance `(b-a)^2 / 12`
- Normal:
  - PDF:
    \[
    f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)
    \]
  - central for inference because many estimators are approximately normal by the CLT
- Counting rules:
  - permutations when order matters:
    \[
    \frac{n!}{(n-k)!}
    \]
  - combinations when order does not matter:
    \[
    \binom{n}{k}=\frac{n!}{k!(n-k)!}
    \]
  - if each of `n` trials has `k` possible outcomes, total ordered sequences are `k^n`
  - multinomial counting with repeated category counts:
    \[
    \frac{n!}{x_1!x_2!\cdots x_k!}
    \]
- Multinomial:
  - generalization of the binomial to more than two categories
  - PMF:
    \[
    P(X_1=x_1,\dots,X_k=x_k)=\frac{n!}{x_1!\cdots x_k!}p_1^{x_1}\cdots p_k^{x_k}
    \]
- Markov chains:
  - next state depends only on the current state, not the full past
  - stationary distribution `\pi` satisfies:
    \[
    \pi P = \pi
    \]
  - useful for modeling long-run behavior across user states

## ML Discussion

- Be ready for practical ML, not only theory.
- Know overfitting, bias-variance tradeoff, train/validation/test split, class imbalance, precision, recall, ROC-AUC, calibration, and leakage.
- Tie model evaluation back to the business objective.
- Be clear about what type of mistake is more costly.
- Distinguish offline model metrics from online or product success metrics.

## Strong Phrases To Use

- “Let me clarify the unit of observation before I compute the metric.”
- “I want to make sure this join does not duplicate users.”
- “I would validate the denominator before interpreting the rate.”
- “The result may be statistically significant, but I also want to check if it is practically meaningful.”
- “Before launch, I would review guardrails and downstream effects.”

## Questions To Ask Them

- What metrics matter most for this team?
- How much of the work is experimentation versus exploratory analytics versus modeling?
- What does success look like in the first six months?
- How are decisions typically made from experiment results?

## Last-Minute Reminders

- Optimize for clarity, structure, and judgment.
- Talk through your assumptions.
- If stuck, go back to grain, denominator, and validation.
- Keep answers practical, not purely academic.
