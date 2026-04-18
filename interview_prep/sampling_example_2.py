import random as rnd
#Estimate the number of unique labels after sampling n labels at random

class UniqueLabelsNotExpanding():

    def __init__(self,freqDist):
        self.freqDist = freqDist.copy()
        self.labels_population = list(self.freqDist.keys())
        self.label_counts = list(self.freqDist.values())

    def get_unique_labels_single(self,n,with_replacement=True):
        #we will use the weights to sample
        if with_replacement == True:
            label_sample = rnd.choices(population=self.labels_population,
                                       weights=self.label_counts,
                                       k=n)
        else:
            label_sample = rnd.sample(population=self.labels_population,
                                      counts=self.label_counts,
                                      k=n)
        unique_labels_sample = set(label_sample)
        return len(unique_labels_sample)        

    def get_expected_unique_labels(self,n,with_replacement=True, iterations=10000):
        total_sum = 0
        for _ in range(iterations):
            total_sum += self.get_unique_labels_single(n=n,with_replacement=with_replacement)
        return total_sum/iterations     

def main():
    freq_dict = {'id_a':20
                 ,'id_b':10
                 ,'id_c':15
                 ,'id_d':25}
    sampling = UniqueLabelsNotExpanding(freq_dict)
    n=5
    expected_count = sampling.get_expected_unique_labels(n=n,with_replacement=False)
    print("Expected count is %s" % expected_count)    

if __name__ == "__main__":
    main()

