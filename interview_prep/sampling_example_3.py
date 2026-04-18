import random as rnd
import statistics
import math

class UniqueLabels():

    def __init__(self,freqDict):
        self.freqDict = freqDict
        self.population_size = sum(self.freqDict.values())
    
    def get_unique_count_sample(self,n,with_replacement=True):
        unique_labels = set()
        if with_replacement:
            for _ in range(n):
                #index = int(rnd.random()*(self.population_size-1))
                index = rnd.randrange(self.population_size)
                cummulative_count = 0
                for key,value in self.freqDict.items():
                    cummulative_count += value
                    if index < cummulative_count:
                        unique_labels.add(key)
                        break
        else:
            wr_dict = self.freqDict.copy()
            for _ in range(n):
                wr_dict_size = sum(wr_dict.values())
                index = rnd.randrange(wr_dict_size)
                cummulative_count = 0
                for key,value in wr_dict.items():
                    cummulative_count += value
                    if index < cummulative_count:
                        unique_labels.add(key)
                        wr_dict[key] -= 1
                        break
        return len(unique_labels)

    def estimate_unique_label_count(self,n,with_replacement=True, iterations=10000):
        if n <= 0:
            raise ValueError("Invalid n")
        if self.population_size == 0:
            raise ValueError("No frequencies greater than 0")
        if (n > self.population_size) and (with_replacement==False):
            raise ValueError("N cannot exceed population size when sampling without replacement")
        total_sum = 0
        unique_counts = list()
        for _ in range(iterations):
            tmp_count = self.get_unique_count_sample(n,with_replacement)
            total_sum += tmp_count
            unique_counts.append(tmp_count)
        empirical_stdev = statistics.stdev(unique_counts)
        mc_stderror = statistics.stdev(unique_counts)/math.sqrt(iterations)
        return (total_sum/iterations, empirical_stdev, mc_stderror)
        

def main():
    freqDict = {'a':20
                ,'b':10
                ,'c':5
                ,'d':5
                ,'f':3
    }
    n=10
    sampling = UniqueLabels(freqDict)
    ex_count, ev, mc = sampling.estimate_unique_label_count(n,True)
    print("expected count: %s" % ex_count)

if __name__=="__main__":
    main()
