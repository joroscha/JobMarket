"""Amazon Music randomization inference practice problem.

Problem:
Amazon Music runs a win-back campaign and randomizes households into:
    - control: no campaign
    - treatment: received the campaign

For each household we observe whether they started a trial in the next 14 days:
    - 1: started a trial
    - 0: did not start a trial

Goal:
Given two binary lists, test whether the campaign changed conversion using
randomization inference.

Null and alternative:
- H0: sharp null of no treatment effect for any unit
- H1: treatment and control differ in conversion

Statistic:
Use signed lift:
    conversion_rate(treatment) - conversion_rate(control)

Task:
Use randomization inference to compute a two-sided p-value.

Randomization inference procedure:
1. Compute the observed lift from the original treatment and control lists.
2. Pool all observed outcomes from treatment and control into one combined list.
3. On each randomization iteration:
   - randomly assign len(treatment) outcomes to a fake treatment group
     without replacement
   - assign the remaining outcomes to a fake control group
   - compute the lift for that reassignment
4. Use the randomization null distribution to compute the two-sided p-value:
   proportion of null lifts whose absolute value is greater than or equal to
   the observed absolute lift.

Required outputs:
1. control conversion rate
2. treatment conversion rate
3. observed lift
4. two-sided randomization-inference p-value

Suggested clarifications:
- Why shuffle assignment instead of resampling with replacement?
  Because randomization inference conditions on the observed sample and varies
  only the treatment assignment.
- Why sample without replacement?
  Because each observed unit must appear exactly once in each reassignment.
- What changes compared with bootstrap p-values?
  Bootstrap resamples observations; randomization inference reshuffles treatment
  assignment under the null.

Use standard-library-only Python. No pandas, numpy, or scipy.
"""


# TODO:
# 1. Define conversion_rate(outcomes).
# 2. Define absolute_lift(treatment, control).
# 3. Pool treatment and control outcomes into one list.
# 4. On each iteration:
#    - randomly select len(treatment) outcomes without replacement for treatment
#    - assign the remaining outcomes to control
#    - compute the signed lift
# 5. Compute the two-sided p-value as:
#    proportion of null lifts with absolute value >= observed absolute lift.


from random import Random
import math

class randomizationInf():

    def __init__(self, control, treatment,seed=7):
        self.control = control
        self.treatment= treatment
        self.pooled = self.control + self.treatment
        self.rng = Random(seed)

    def compute_statistic(self,treatment,control):
        treat_rate = sum(treatment)/len(treatment)
        control_rate = sum(control)/len(control)
        return treat_rate - control_rate
    
    def single_draw(self):
        sample_labels = self.rng.sample(self.pooled,len(self.pooled))
        treat_sample = sample_labels[0:len(self.treatment)]
        control_sample = sample_labels[len(self.treatment):]
        diff_statistic = self.compute_statistic(treat_sample,control_sample)
        return diff_statistic

    def get_sample_array(self,iterations=10000):
        stat_array = []
        for _ in range(iterations):
            stat_array.append(self.single_draw())
        return stat_array

    def compute_randomization_two_sided_test(self,iterations=10000):
        stat_array = self.get_sample_array(iterations)
        observed_statistic = self.compute_statistic(self.treatment,self.control)
        pvalue = (sum((1 if abs(x)>=abs(observed_statistic) else 0 for x in stat_array))+1)/(len(stat_array)+1)
        return pvalue
    
    def compute_randomization_one_sided_test(self,iterations=10000):
        stat_array = self.get_sample_array(iterations)
        observed_statistic = self.compute_statistic(self.treatment,self.control)
        pvalue = (sum((1 if x>=observed_statistic else 0 for x in stat_array))+1)/(len(stat_array)+1)
        return pvalue


def main():
    control = [
        0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
    ]
    treatment = [
        0, 1, 0, 1, 0, 1, 1, 0, 0, 1,
        0, 1, 0, 0, 1, 0, 1, 0, 1, 0,
    ]

    print(__doc__)
    print()
    print("Sample sizes")
    print(f"  control households:   {len(control)}")
    print(f"  treatment households: {len(treatment)}")

    sampling = randomizationInf(control=control, treatment=treatment,seed=7)
    pvalue = sampling.compute_randomization_two_sided_test(iterations=10000)
    print("P value is %s: " % pvalue)


if __name__ == "__main__":
    main()
