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

Clarify / decide:
- Are draws with replacement or without replacement?
- What should happen if `n` is larger than the total population size?
- What should happen if input frequencies are empty, zero, or negative?

Suggested structure:
- a class with `__init__`
- one method for a single simulation
- one method for repeated simulations and averaging

What to practice:
- requirement clarification
- class design
- simulation logic
- sampling with and without replacement
- counting unique labels
- edge cases
- naming and clean structure
"""

# TODO:
# 1. Define the class.
# 2. Decide what to store in __init__.
# 3. Write a method to simulate one draw process.
# 4. Write a method to estimate the expected number of unique labels.
# 5. Think about edge cases and invalid inputs.

import random as rnd

class LabelSampler:

    def __init__(self, freq_dic):
        self.freq_dic = freq_dic.copy()
        self.population = []

        #this will create the list that we need
        for label, freq in self.freq_dic.items():
            self.population.extend([label]*freq)

    def single_draw(self,n, with_replacement=True):
        if with_replacement:
            new_sample = rnd.choices(self.population,k=n)
        else:
            new_sample = rnd.sample(self.population,k=n)
        new_sample_set = set(new_sample)    
        return len(new_sample_set)

    def expected_number_labels(self,n, with_replacement=True,iterations=10000):
        label_counts = 0
        for _ in range(iterations):
            label_counts += self.single_draw(n,with_replacement)
        return label_counts/iterations            

def main():
    freq_dic = {'artist_a':10
                ,'artist_b':20
                ,'artist_c':30
                ,'artist_d':5}
    n=10
    sampler = LabelSampler(freq_dic)
    expected_counts = sampler.expected_number_labels(n, with_replacement=True,iterations=10000)
    print("We get: %s" % expected_counts)

if __name__ == "__main__":
    main()






