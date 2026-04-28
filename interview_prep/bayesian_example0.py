"""Amazon Music Beta-Binomial posterior simulation practice.

Problem:
Amazon Music runs a win-back email experiment to restart free trials.
You observe:
    - control: number of eligible users and number of conversions
    - treatment: number of eligible users and number of conversions

Goal:
Using a Beta-Binomial model, simulate the posterior distribution of:
    - control conversion rate
    - treatment conversion rate
    - lift = treatment rate - control rate

Then report:
1. posterior mean control rate
2. posterior mean treatment rate
3. posterior mean lift
4. posterior probability that treatment beats control
5. 95% credible interval for lift

Model:
- Prior:
    p_control ~ Beta(a, b)
    p_treatment ~ Beta(a, b)
- Likelihood:
    y_control | p_control ~ Binomial(n_control, p_control)
    y_treatment | p_treatment ~ Binomial(n_treatment, p_treatment)
- Posterior:
    p_control | data ~ Beta(a + y_control, b + n_control - y_control)
    p_treatment | data ~ Beta(a + y_treatment, b + n_treatment - y_treatment)

Simulation task:
1. Compute posterior Beta parameters for each arm.
2. Draw many samples from each posterior using random.betavariate(...).
3. Compute lift on each draw.
4. Summarize the simulated posterior.

Use only the Python standard library.
"""

import random as rnd


class BetaBinomialPosterior:

    def __init__(
        self,
        control_conversions,
        control_total,
        treatment_conversions,
        treatment_total,
        prior_a=1,
        prior_b=1,
        seed=7,
    ):
        self.control_conversions = control_conversions
        self.control_total = control_total
        self.treatment_conversions = treatment_conversions
        self.treatment_total = treatment_total
        self.prior_a = prior_a
        self.prior_b = prior_b
        self.rng = rnd.Random(seed)

    # TODO:
    # 1. Implement posterior_params(conversions, total).
    # 2. Implement simulate_lift_posterior(num_draws=10000).
    # 3. Implement summarize_posterior(num_draws=10000) returning:
    #    - posterior_mean_control
    #    - posterior_mean_treatment
    #    - posterior_mean_lift
    #    - prob_treatment_beats_control
    #    - ci_low
    #    - ci_high
    pass

    def posterior_params(self, conversions,totals):
        alpha = self.prior_a + conversions
        beta = self.prior_b + (totals - conversions)
        return alpha, beta
        

    def simulate_lift_posterior(self,iterations = 10000):
        alpha_t, beta_t = self.posterior_params(self.treatment_conversions, self.treatment_total)
        alpha_c, beta_c = self.posterior_params(self.control_conversions, self.control_total)
        array_lifts = []
        for _ in range(iterations):
            sample_control = self.rng.betavariate(alpha_c,beta_c)
            sample_treat = self.rng.betavariate(alpha_t,beta_t)
            sample_lift = sample_treat - sample_control
            array_lifts.append(sample_lift)
        return array_lifts

    def summarize_posterior(self,iterations = 10000):
        alpha_t, beta_t = self.posterior_params(self.treatment_conversions, self.treatment_total)
        alpha_c, beta_c = self.posterior_params(self.control_conversions, self.control_total)
        posterior_mean_treatment = alpha_t/(alpha_t + beta_t)
        posterior_mean_control = alpha_c/(alpha_c + beta_c)
        array_lifts = self.simulate_lift_posterior(iterations)
        posterior_mean_lift = sum(array_lifts)/len(array_lifts)
        prob_treatment_beats_control = sum(1 if x > 0 else 0 for x in array_lifts)/len(array_lifts)
        sorted_array_lifts = sorted(array_lifts)
        ci_low = sorted_array_lifts[int(0.025*(len(sorted_array_lifts)-1))]
        ci_high = sorted_array_lifts[int(0.975*(len(sorted_array_lifts)-1))]

        return posterior_mean_control, posterior_mean_treatment, posterior_mean_lift, prob_treatment_beats_control, ci_low, ci_high

    


def main():
    control_total = 1000
    control_conversions = 80
    treatment_total = 1000
    treatment_conversions = 110

    # Example usage after implementation:
    # model = BetaBinomialPosterior(
    #     control_conversions=control_conversions,
    #     control_total=control_total,
    #     treatment_conversions=treatment_conversions,
    #     treatment_total=treatment_total,
    #     prior_a=1,
    #     prior_b=1,
    #     seed=7,
    # )
    # print(model.summarize_posterior(num_draws=10000))

    print("Control: %s / %s" % (control_conversions, control_total))
    print("Treatment: %s / %s" % (treatment_conversions, treatment_total))
    print("Implement BetaBinomialPosterior to simulate the posterior lift.")


if __name__ == "__main__":
    main()
