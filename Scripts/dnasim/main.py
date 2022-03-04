import copy
import strand_error_sim
import os

class Simulator:
    """
    Class variables:
    :var self.total_error_rates: Dictionary of the total error rates used in the simulation, as provided in error_rates
        parameter.
    :var self.base_error_rates: Error rates corresponding to each base, as passed.
    :var self.long_deletion_length_rates: Based on (excluding single base deletion):
        https://www.biorxiv.org/content/biorxiv/early/2019/11/13/840231/F12.large.jpg?width=800&height=600&carousel=1
    """
    def __init__(self, total_error_rates, base_error_rates, long_deletion_length_rates):
        """
        @param total_error_rates: Dictionary of the total error rates used in the simulation.
            Example of a dictionary:
            {'d': 0.1, 'i': 0.2, 's': 0.1, 'ld': 0.6}
            NOTE: Dictionary can be passed with values as strings, as the constructor can to parse them to floats.
        @param base_error_rates: Dictionary of dictionaries for each base.
            Example:
            {   'A': {'s': 0.1, 'i': 0.2, 'pi': 0.1, 'd': 0.05, 'ld': 0.6},
                'T': {...},
                'C': {...},
                'G': {...}
            }
        """
        self.total_error_rates = total_error_rates
        self.base_error_rates = base_error_rates
        self.long_deletion_length_rates = long_deletion_length_rates

    def simulate_strand(self, original_strand, num_copies):
        # for each strand, do the simulation on a copy of it num_copies (the generated number of copies) times:
        output_strands = []
        for j in range(num_copies):

            # duplicate strand to create a working (output) strand:
            output_strand = copy.deepcopy(original_strand)

            # create a strand simulator for it:
            strand_error_simulator = strand_error_sim.StrandErrorSimulation(self.total_error_rates,
                                                                            self.base_error_rates,
                                                                            self.long_deletion_length_rates,
                                                                            output_strand)
            # simulate 
            output_strand = strand_error_simulator.simulate_errors_on_strand()

            output_strands.append(output_strand)
        
        return output_strands
    
    def simulate_strands(self, original_strands, num_copies):
        return [self.simulate_strand(s, num_copies) for s in original_strands]

if __name__ == '__main__':
    total_error_rates = {
        'd': 0.05,
        'i': 0.05,
        's': 0.05,
        'ld': 0.0033104220650884975,
    }
    
    base_error_rates = {
        'A': {
            'pi': 0.05,
            'i': 0.05,
            's': 0.05,
            'd': 0.05,
            'ld': 0.003110456472280425,
        },
        'G': {
            'pi': 0.05,
            'i': 0.05,
            's': 0.05,
            'd': 0.05,
            'ld': 0.003931135429009549
        },
        'C': {
            'pi': 0.05,
            'i': 0.05,
            's': 0.05,
            'd': 0.05,
            'ld': 0.0033067584089939467
        },
        'T': {
            'pi': 0.05,
            'i': 0.05,
            's': 0.05,
            'd': 0.05,
            'ld': 0.002907934758532013,
        }
    }

    long_deletion_length_rates = {2: 84,
                                  3: 13,
                                  4: 1.8,
                                  5: 0.2,
                                  6: 0.02}

    sim = Simulator(total_error_rates, base_error_rates, long_deletion_length_rates)

    file_path = os.path.dirname(__file__)
    if file_path != "":
        os.chdir(file_path)

    refs_file = open('../../Data/microsoft-real/Centers.txt', 'r')
    original_strands = [line.strip() for line in refs_file.readlines()]

    i = 0
    output_f = open('../../Data/cov10/nanopore-p15-uniform/clusters.txt', 'w')
    strand_cov = 10
    for strand in original_strands:
        output_f.write(f'{strand_cov}\n')
        for s in sim.simulate_strand(strand, strand_cov):
            output_f.write(s + '\n')
        i += 1
