from DNA import DNA
import random


class Population:
    def __init__(self, numOfPeriods, numOfWorkingDays, courseStructOfBatch, mutationRate, populationSize):
        self.courseStructOfBatch = courseStructOfBatch
        self.numOfBatches = len(courseStructOfBatch)
        self.numOfPeriods = numOfPeriods
        self.numOfWorkingDays = numOfWorkingDays

        self.popSize = populationSize
        self.mutationRate = mutationRate

        self.isComplete = False
        self.bestDNA = None
        self.bestFitness = 0.0
        self.avgFitness = 0.0

        self.targetFitness = 1

        self.population = []
        self.generateRandom()

    def generateRandom(self):
        for i in range(self.popSize):
            self.population.append(DNA(self.numOfPeriods, self.numOfWorkingDays,self.courseStructOfBatch))
            self.population[i].generateRandom()

    def rouletteSelect(self):
        i = 0
        while True:
            i = random.randrange(0, self.popSize)
            if random.random() < self.population[i].fitness:
                break

        return self.population[i]

    def tournamentSelection(self):
        k = self.popSize//10
        parentList = []

        for i in range(0, self.popSize, k):
            parentList.append(self.population[random.randrange(i, i+k)])

        index = -1
        max = 0.0
        for i in range(len(parentList)):
            if parentList[i].fitness > max:
                max = parentList[i].fitness
                index = i

        return parentList[index]

    def crossOver(self):
        newPopulation = []

        for i in range(self.popSize):
            # parentA = self.rouletteSelect()
            # parentB = self.rouletteSelect()
            #
            parentA = self.tournamentSelection()
            parentB = self.tournamentSelection()

            if parentA.fitness < 0.99 and parentB.fitness < 0.99:
                childDNA = parentA.crossover(parentB)

            # crossover only if hard constraint is not met
            elif parentA.fitness > parentB.fitness:
                childDNA = parentA.deepClone()
            else:
                childDNA = parentB.deepClone()

            childDNA.mutate(self.mutationRate)
            newPopulation.append(childDNA)

        self.population = newPopulation

    def calcStatistics(self):
        totFitness = 0.0
        bestFitness = self.bestFitness
        bestIndex = -1
        for i in range(self.popSize):
            totFitness += self.population[i].fitness
            if self.population[i].fitness > bestFitness:
                bestFitness = self.population[i].fitness
                bestIndex = i
            if self.population[i].fitness == self.targetFitness:
                self.isComplete = True

        self.bestFitness = bestFitness
        if bestIndex >=0:
            self.bestDNA = self.population[bestIndex].deepClone()

        self.avgFitness = totFitness/self.popSize

    def calcFitness(self):
        for dna in self.population:
            dna.calcFitness()