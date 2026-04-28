"""Amazon Music bootstrap p-value practice problem.

Problem:
Amazon Music runs a win-back campaign and randomizes households into:
    - control: no campaign
    - treatment: received the campaign

For each household we observe whether they started a trial in the next 14 days:
    - 1: started a trial
    - 0: did not start a trial

Goal:
Given two binary lists, test whether the campaign changed conversion.

Null and alternative:
- H0: treatment and control come from the same conversion distribution
- H1: treatment and control have different conversion distributions

Statistic:
Use signed lift:
    conversion_rate(treatment) - conversion_rate(control)

Task:
Use a pooled bootstrap null distribution to compute a two-sided p-value.

Bootstrap null procedure:
1. Compute the observed lift from the original treatment and control lists.
2. Pool all outcomes from treatment and control into one combined list.
3. On each bootstrap iteration:
   - sample len(treatment) observations with replacement from the pooled list
     to create a bootstrap treatment group
   - sample len(control) observations with replacement from the pooled list
     to create a bootstrap control group
   - compute the bootstrap lift
4. Use the bootstrap null distribution to compute the two-sided p-value:
   proportion of bootstrap lifts whose absolute value is greater than or equal to
   the observed absolute lift.

Required outputs:
1. control conversion rate
2. treatment conversion rate
3. observed lift
4. two-sided bootstrap p-value

Suggested clarifications:
- Why pool the data under the null?
  Under H0, treatment and control are assumed to come from the same distribution.
- Why sample with replacement?
  This is a bootstrap null distribution rather than a permutation test.
- What changes compared with bootstrap_example0?
  There you estimated uncertainty around lift; here you test a null hypothesis.

Use standard-library-only Python. No pandas, numpy, or scipy.
"""


# TODO:
# 1. Define conversion_rate(outcomes).
# 2. Define absolute_lift(treatment, control).
# 3. Write a pooled bootstrap resample function for the null distribution.
# 4. On each iteration, draw:
#    - len(treatment) bootstrap observations for treatment
#    - len(control) bootstrap observations for control
# 5. Compute the bootstrap null lift on each iteration.
# 6. Compute the two-sided p-value as:
#    proportion of bootstrap null lifts with absolute value >= observed absolute lift.

from random import Random
import math

class BoostrapPvalues():
    def __init__(self,control,treatment,seed=7):
        self.control = control
        self.treatment = treatment
        self.pooled = self.control + self.treatment
        self.rng = Random(seed)

    def compute_statistic(self,treatment,control):
        treat_conversion = sum(treatment)/len(treatment)
        control_conversion = sum(control)/len(control)
        return treat_conversion - control_conversion        
        

    def single_draw_statistic(self):
        treat_sample = self.rng.choices(self.pooled,k=len(self.treatment))
        control_sample = self.rng.choices(self.pooled,k=len(self.control))
        diff_statitic = self.compute_statistic(treat_sample,control_sample)
        return diff_statitic
    
    def generate_statistics(self,iterations=10000):
        stat_array = []
        for _ in range(iterations):
            stat_array.append(self.single_draw_statistic())
        return stat_array
    
    def two_sided_test(self,iterations=10000):
        stat_array = self.generate_statistics(iterations)
        obs_statistic = self.compute_statistic(self.treatment,self.control)
        pval = (sum((1 if abs(x)>= abs(obs_statistic) else 0 for x in stat_array))+1)/(len(stat_array)+1)
        return pval
        

    
def main():
    control = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 0, 0, 0, 1, 1, 0,
    ]
    treatment = [
        0, 1, 0, 1, 0, 1, 1, 0, 0, 1,
        0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
    ]

    sampling = BoostrapPvalues(control=control,treatment=treatment,seed=7)    
    pval = sampling.two_sided_test(iterations=10000)
    print("P value is %s" % pval)
    
if __name__ == '__main__':
    main()
