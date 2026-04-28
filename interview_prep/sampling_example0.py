"""Amazon Music simulation practice problem.

Problem:
You are given a dictionary mapping labels to frequencies, for example:

    {
        "pop": 50,
        "hip_hop": 30,
        "jazz": 20,
    }

This represents a population with repeated labels according to the frequencies.

Goal:
Estimate the expected number of unique labels observed after drawing `n` items
at random, using simulation.
"""

import random as rnd
import math

class LabelSampling:
    def __init__(self,freqDict):
        if len(freqDict)==0:
            raise ValueError("Frequencey Dictionary is empty")
        self.freqDict = freqDict
        self.freq_array = []
        for key,value in freqDict.items():
            if value < 0:
                raise ValueError("Dictionary contains negative frequencies")
            self.freq_array.extend([key]*value)
        if len(self.freq_array) == 0:
            raise ValueError("Values of dictionary are 0")

    
    def single_draw(self,n,with_replacement=True):
        #if using a expanded array from dictionary
        if with_replacement:
            #choices is with replacement (keep choosing again from the same)
            sample_draw = rnd.choices(self.freq_array,k=n)
        else:
            #sample (sampling from a population)
            sample_draw = rnd.sample(self.freq_array,k=n)
        nunique_values = len(set(sample_draw))
        return nunique_values

    def compute_iterations(self,n,with_replacement=True,iterations=10000):
        if n < 0:
            raise ValueError("N has to be >= 0")
        if (n > len(self.freq_array)) and (with_replacement==False):
            raise ValueError("Without replacement can't take n > population size")
        if (iterations <= 0):
            raise ValueError("Iterations has to be > 0")
        
        total_sum = 0
        nunique_array = []
        for i in range(iterations):
            tmp_value = self.single_draw(n,with_replacement)
            nunique_array.append(tmp_value)
            total_sum += tmp_value
            if ((i+1) % 1000==0):
                running_mean = total_sum/(i+1)
                print("Running Mean at %s: %s" % (i+1,running_mean))
        mean_estimate = total_sum/iterations
        sample_var= sum([(x-mean_estimate)**2 for x in nunique_array])/(len(nunique_array)-1)
        sample_std_dev = math.sqrt(sample_var)
        mc_se = sample_std_dev/math.sqrt(iterations)
        ci_lower = mean_estimate - 1.96*mc_se
        ci_upper = mean_estimate + 1.96*mc_se

        return mean_estimate,mc_se,ci_lower,ci_upper


def main():
    freqDict = {'pop':50
                ,'hip_hop':20
                ,'jazz':10
                ,'rock':40
                ,'country':15
                ,'rap':45}
    
    sampling = LabelSampling(freqDict)
    n=10
    mean_estimate,mc_se,ci_lower,ci_upper = sampling.compute_iterations(n,with_replacement=True,iterations=10000)
    print("Expected unique labels: %s; MC SE: %s; 95%% CI (%s,%s)" % (mean_estimate,mc_se,ci_lower,ci_upper))

if __name__=='__main__':
    main()
