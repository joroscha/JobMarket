import random as rnd

class MinDraws:

    def __init__(self,freq_dict):
        self.frequ_dict = freq_dict
        self.population = []
        for key, value in self.frequ_dict.items():
            self.population.extend([key]*value)
        self.unique_labels = self.frequ_dict.keys()
        self.unque_labels_length = len(self.unique_labels)

    def get_min_number_draws(self,with_replacement=True):
        num_iterations = 0
        unique_labels_sampled = set()
        if with_replacement:
            while len(unique_labels_sampled) <  self.unque_labels_length:
                index = int(rnd.random()*len(self.population))
                value = self.population[index]
                unique_labels_sampled.add(value)
                num_iterations += 1
        else:
            population_copy = self.population.copy()
            while len(unique_labels_sampled) <  self.unque_labels_length:
                index = int(rnd.random()*len(population_copy))
                value = population_copy[index]
                unique_labels_sampled.add(value)
                population_copy.pop(index)
                num_iterations += 1
        return num_iterations  
            

    def get_expected_number_draws(self,with_replacement=True, iterations=10000):
        iterations_sum = 0
        for _ in range(iterations):
            iterations_sum += self.get_min_number_draws(with_replacement)
        return iterations_sum/iterations

def main():
    freq_dict = {'artist_a': 20
                 ,'artist_b': 15
                 ,'artist_c':10
                 ,'aritst_d':5}
    sampling = MinDraws(freq_dict)
    expected_minimum_draws = sampling.get_expected_number_draws(with_replacement=True,iterations=10000)
    print("The expected number is: %s" % expected_minimum_draws)

if __name__ == "__main__":
    main()



