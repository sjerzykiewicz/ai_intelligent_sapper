import random


class Genom:
    def __init__(self) -> None:
        # none, landmine, claymore, hcb
        self.possible_genes = "NNLNNLNCNCNHNNN"
        self.target_chromosome = "NNNLNNNCNNNHNNNHNNNNLNNNCNNNHNNNLNN" + \
                                 "HNNNNLNNNCNNNLNNNHNNNNCNNNLNNNHNNNL" + \
                                 "NHNNNLLHNNNNNNNNNNNHNNNNNCNNNNCNNNL" + \
                                 "NHHNCNNNNNLNNNNNNNNNNNCLHNLNNNNNNNN" + \
                                 "CNLNNNNNNNNNNNHNHNNLNHNNNNCNNLNNNNN" + \
                                 "NHNNNHNNNNLNNNHCNNNNNNLNNLNCNNNNNNN" + \
                                 "NNNLNNNCNNNHNNNHNNNNLNNNCNNNHNNNLNN" + \
                                 "HNNNNLNNNCNNNLNNNHNNNNCNNNLNNNHNNNL" + \
                                 "NHNNNLLHNNNNNNNNNNNHNNNNNCNNNNCNNNL" + \
                                 "NHHNCNNNNNLNNNNNNNNNNNCLHNLNNNNNNNN" + \
                                 "CNLNNNNNNNNNNNHNHNNLNHNNNNCNNLNNNNN" + \
                                 "NHNNNHNNNNLNNNHCNNNNNNLNNLNCNNNNNNN" + \
                                 "NNNLNNNCNNNHNNNHNNNNLNNNCNNNHNNNLNN" + \
                                 "HNNNNLNNNCNNNLNNNHNNNNCNNNLNNNHNNNL" + \
                                 "NHNNNLLHNNNNNNNNNNNHNNNNNCNNNNCNNNL" + \
                                 "NHHNCNNNNNLNNNNNNNNNNNCLHNLNNNNNNNN" + \
                                 "CNLNNNNNNNNNNNHNHNNLNHNNNNCNNLNNNNN" + \
                                 "NHNNNHNNNNLNNNHCNNNNNNLNNLNCNNNNNNN" + \
                                 "NNNLNNNCNNNHNNNHNNNNLNNNCNNNHNNNLNN" + \
                                 "HNNNNLNNNCNNNLNNNHNNNNCNNNLNNNHNNNL" + \
                                 "NHNNNLLHNNNNNNNNNNNHNNNNNCNNNNCNNNL"
        self.population_size = 70

    def get_random_gene(self) -> str:
        return random.choice(self.possible_genes)

    def get_random_chromosome(self) -> str:
        return "".join([self.get_random_gene() for _ in range(len(self.target_chromosome))])

    def get_random_population(self) -> list:
        return [Individual(self.get_random_chromosome()) for _ in range(self.population_size)]


class Individual(Genom):
    def __init__(self, chromosome: str) -> None:
        super().__init__()
        self.chromosome = chromosome
        self.fitness = self.calc_fitness()

    def calc_fitness(self) -> None:
        fitness = 0
        for gene, target_gene in zip(self.chromosome, self.target_chromosome):
            fitness += gene == target_gene
        return fitness
    
    def mate(self, other):
        new_chromosome = []
        for gene1, gene2 in zip(self.chromosome, other.chromosome):
            probability = random.random()
            if probability < 0.45:
                new_chromosome.append(gene1)
            elif probability < 0.9:
                new_chromosome.append(gene2)
            else:
                new_chromosome.append(self.get_random_gene())

        return Individual("".join(new_chromosome))


def generate_bomb_placement():
    generation = 0

    population = sorted(Genom().get_random_population(), key=lambda individual: individual.fitness, reverse=True)
    while population[0].fitness < len(population[0].target_chromosome) and generation < 3000:
        if generation % 50 == 0:
            print(f"Generation: {generation}\tBest fitness: {population[0].fitness}")
        new_population = population[:5]
        for _ in range(population[0].population_size - 5):
            parent1 = random.choice(population[:15])
            parent2 = random.choice(population[:15])
            new_population.append(parent1.mate(parent2))
        population = sorted(new_population, key=lambda individual: individual.fitness, reverse=True)
        generation += 1

    print(f"Generation: {generation}\tBest fitness: {population[0].fitness}")
    return population[0].chromosome
