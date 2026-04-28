"""Amazon Music exact randomization-inference practice problem.

Problem:
Amazon Music runs a small pilot of a win-back campaign and randomizes
households into:
    - control: no campaign
    - treatment: received the campaign

For each household we observe whether they started a trial in the next 14 days:
    - 1: started a trial
    - 0: did not start a trial

Goal:
Given two small binary lists, compute an exact randomization-inference p-value
instead of a Monte Carlo approximation.

Null and alternative:
- H0: sharp null of no treatment effect for any unit
- H1: treatment and control differ in conversion

Statistic:
Use signed lift:
    conversion_rate(treatment) - conversion_rate(control)

Task:
Use exact randomization inference to compute a two-sided p-value.

Exact randomization procedure:
1. Compute the observed lift from the original treatment and control lists.
2. Pool all observed outcomes from treatment and control into one combined list.
3. Enumerate every possible reassignment of treatment labels that preserves the
   original treatment-group size.
4. For each reassignment:
   - assign the chosen indices to a fake treatment group
   - assign the remaining indices to a fake control group
   - compute the lift for that reassignment
5. Use the full randomization null distribution to compute the exact two-sided
   p-value:
   proportion of null lifts whose absolute value is greater than or equal to
   the observed absolute lift.

Important note:
- Because outcomes can repeat, enumerate assignments using unit indices,
  not just distinct outcome values.
- Exact enumeration is only practical for small samples, which is why this
  practice problem uses a tiny pilot.

Required outputs:
1. control conversion rate
2. treatment conversion rate
3. observed lift
4. total number of possible assignments considered
5. exact two-sided randomization-inference p-value

Suggested clarifications:
- Why is this "exact"?
  Because you evaluate every assignment consistent with the original design,
  rather than approximating with random draws.
- Why use combinations?
  Choosing which units are labeled treatment completely determines the
  reassignment under a fixed treatment-group size.
- What changes compared with randomization_example0?
  There you approximated the null with many random permutations; here you
  enumerate the full null distribution.

Use standard-library-only Python. No pandas, numpy, or scipy.
"""


# TODO:
# 1. Define conversion_rate(outcomes).
# 2. Define absolute_lift(treatment, control) or a signed-lift function.
# 3. Pool treatment and control outcomes into one list.
# 4. Enumerate all treatment index sets of size len(treatment).
# 5. For each treatment index set:
#    - assign the selected indices to treatment
#    - assign the remaining indices to control
#    - compute the signed lift
# 6. Compute the exact two-sided p-value as:
#    count of null lifts with abs(lift) >= abs(observed_lift)
#    divided by total number of assignments.


from random import Random
import math
from itertools import combinations

class exactPvalues():
    
    def __init__(self,treatment, control, seed=42):
        self.treatment = treatment
        self.control = control
        self.pooled = self.treatment + self.control
        self.treatment_label = [1 for x in self.treatment] + [0 for x in self.control]
        self.rng = Random(seed)
        
    
    def compute_statistic(self,treatment, control):
        treat_conversion = sum(treatment)/len(treatment)
        control_conversion = sum(control)/len(control)
        return treat_conversion - control_conversion
    
    def compute_permutations(self):
        perm_stat_array = []
        total_permutations = math.factorial(len(self.pooled))/(math.factorial(len(self.treatment))*math.factorial(len(self.pooled)-len(self.treatment)))
        print("Total permutation to test: % s" % total_permutations)
        for treat_idx in combinations(range(len(self.pooled)),len(self.treatment)):
            treatment_outcomes = [self.pooled[x] for x in treat_idx]
            control_outcomes = [self.pooled[x] for x in range(len(self.pooled)) if x not in treat_idx]
            perm_stat = self.compute_statistic(treatment=treatment_outcomes,control=control_outcomes)
            perm_stat_array.append(perm_stat)
        return perm_stat_array
    
    def compute_exact_pvalue_two_sided(self):
        observed_stat = self.compute_statistic(self.treatment,self.control)
        perm_stat_array = self.compute_permutations()
        pvalue = (sum((1 if abs(x) >= abs(observed_stat) else 0 for x in perm_stat_array)))/(len(perm_stat_array))
        return pvalue
    
    def compute_exact_pvalue_one_sided(self):
        observed_stat = self.compute_statistic(self.treatment,self.control)
        perm_stat_array = self.compute_permutations()
        pvalue = (sum((1 if x >= observed_stat else 0 for x in perm_stat_array)))/(len(perm_stat_array))
        return pvalue

        

def main():
    # Keep the sample small so exact enumeration is feasible.
    control = [0, 0, 1, 0, 0, 0, 1, 0]
    treatment = [1, 1, 1, 1, 0, 0, 1, 1]
    control = [0, 0, 1, 0]
    treatment = [1, 1, 1, 1]

    print(__doc__)
    print()
    print("Sample sizes")
    print(f"  control households:   {len(control)}")
    print(f"  treatment households: {len(treatment)}")
    print(f"  total households:     {len(control) + len(treatment)}")
    print()
    print("Hint")
    print("  Use itertools.combinations over unit indices, not over outcome values.")
    permutation_test = exactPvalues(treatment,control,seed=42)
    pvalue = permutation_test.compute_exact_pvalue_two_sided()
    print("Pvalue: %s" % pvalue)


if __name__ == "__main__":
    main()
