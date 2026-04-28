"""Amazon Music sampling practice problem.

Problem:
You are given a small frequency-table dataset for Amazon Music labels.
Each row represents one label and its observed count in the dataset.

Goal:
Starting from the dataset, estimate the expected number of draws needed
to observe all unique labels at least once.

Sampling setup:
- Build the frequency map from the dataset.
- Treat the dataset as the empirical population.
- On each simulation run, repeatedly draw rows at random until every unique
  label has been seen at least once.
- Support both:
  - sampling with replacement
  - sampling without replacement

Return:
- expected number of draws across many simulation runs

Guidance:
1. Extract the `label` and `count` columns from the dataset.
2. Build a frequency dictionary like `label -> count`.
3. Simulate one run of repeated sampling until all labels are observed.
4. Repeat many times and average the stopping time.

Suggested follow-ups:
- What changes if the dataset is large and you do not want to expand the
  population into a long list?
- How would you compute a Monte Carlo standard error for the estimate?
- How would the answer differ with vs without replacement?
"""

import pandas as pd
from random import Random

class SamplingExample4():
    
    def __init__(self,df_data, seed=7):
        self.df_data = df_data.copy()
        self.population_size = self.df_data.count.sum()
        self.labels = self.df_data.label.to_list()
        self.counts = self.df_data.count.to_list()
        self.freqDict = dict(zip(self.labels,self.counts))
        self.rng = Random(seed)
        pass
    
    def single_draw(self,with_replacement=True):
        unique_labels_sampled = 0
        unique_labels_set = set()
        population_size = self.population_size
        freqDict = self.freqDict.copy()
        while len(unique_labels_set) < len(self.labels):
            if with_replacement:
              #if i can't use randrange, only rand:
              rnd_idx = int(self.rng.random()*(self.population_size))
              rnd_idx = self.rng.randrange(population_size)
              unique_labels_sampled += 1
              cumulative_count = 0
              for label,counts in freqDict.items():
                  cumulative_count += counts
                  if rnd_idx < cumulative_count:
                      unique_labels_set.add(label)
                      break
            else:
              rnd_idx = self.rng.randrange(population_size)
              population_size += -1
              unique_labels_sampled += 1
              cumulative_count = 0
              for label,counts in freqDict.items():
                  cumulative_count += counts
                  if rnd_idx < cumulative_count:
                      unique_labels_set.add(label)
                      freqDict[label] += -1
                      break                
        return unique_labels_sampled
    
    def compute_expectation(self,with_replacement=True,iterations=10000):
        running_sum = 0
        for i in range(iterations):
            running_sum += self.single_draw(with_replacement)
        return running_sum/iterations     


def main():
    pass

if __name__ == '__main__':
    main()
        
