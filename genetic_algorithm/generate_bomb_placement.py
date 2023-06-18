import random


class Genom:
    def __init__(self) -> None:
        # none, landmine, claymore, hcb
        self.possible_genes = ["N", "L", "C", "H"]
        self.possible_genes_weights = [500, 50, 30, 20]
        self.population_size = 70

    def get_random_gene(self) -> str:
        return random.choices(
            self.possible_genes, weights=self.possible_genes_weights, k=1
        )[0]

    def get_random_chromosome(self) -> str:
        return "".join([self.get_random_gene() for _ in range(35 * 21)])

    def get_random_population(self) -> list:
        return [
            Individual(self.get_random_chromosome())
            for _ in range(self.population_size)
        ]


class Individual(Genom):
    def __init__(self, chromosome: str) -> None:
        super().__init__()
        self.chromosome = chromosome
        self.fitness = self.calc_fitness()

    def calc_fitness(self) -> None:
        fitness = 0
        gene = [["" for _ in range(35)] for _ in range(21)]

        for i, g in enumerate(self.chromosome):
            gene[i // 35][i % 35] = g

        for i in range(1, len(gene) - 1):
            for j in range(1, len(gene[i]) - 1):
                if gene[i][j] != "N" and all(
                    gene[i + xi][j + xj] == "N"
                    for xi, xj in [
                        (1, 0),
                        (-1, 0),
                        (0, 1),
                        (0, -1),
                        (1, 1),
                        (-1, 1),
                        (1, -1),
                        (-1, -1),
                    ]
                ):
                    fitness += 1

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

    population = sorted(
        Genom().get_random_population(),
        key=lambda individual: individual.fitness,
        reverse=True,
    )
    while (
        population[0].fitness
        < 0.75
        * (
            population[0].chromosome.count("L")
            + population[0].chromosome.count("C")
            + population[0].chromosome.count("H")
        )
        and generation < 3000
    ):
        if generation % 50 == 0:
            print(f"Generation: {generation}\tBest fitness: {population[0].fitness}")
        new_population = population[:5]
        for _ in range(population[0].population_size - 5):
            parent1 = random.choice(population[:15])
            parent2 = random.choice(population[:15])
            new_population.append(parent1.mate(parent2))
        population = sorted(
            new_population, key=lambda individual: individual.fitness, reverse=True
        )
        generation += 1

    print(f"Generation: {generation}\tBest fitness: {population[0].fitness}")
    return population[0].chromosome
