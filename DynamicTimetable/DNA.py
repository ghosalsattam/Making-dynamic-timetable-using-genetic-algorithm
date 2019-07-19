from CustomObjects import *
import random
import copy

class DNA:
    def __init__(self, numOfPeriods, numOfWorkingDays, courseStructOfBatch):
        self.courseStructOfBatch = courseStructOfBatch
        self.numOfBatches = len(courseStructOfBatch)
        self.numOfPeriods = numOfPeriods
        self.numOfWorkingDays = numOfWorkingDays

        self.batchList = []  # a list of Batches
        self.fitness = 0
        self.softPenalty = 0

    def calcFitness(self):
        noClashfitness = 0
        for d in range(self.numOfWorkingDays):
            for p in range(self.numOfPeriods):

                # check for inter-batch clashing schedule of trainer
                trainersSoFar = []
                noClash = True
                for b in range(self.numOfBatches):
                    if self.batchList[b].timetable[d][p] != None:
                        if self.batchList[b].timetable[d][p].trainerIndex in trainersSoFar:
                            noClash = False
                            break
                        else:
                            trainersSoFar.append(self.batchList[b].timetable[d][p].trainerIndex)
                if noClash:
                    noClashfitness += 1

        # normalize to 1
        noClashfitness = float(noClashfitness)/(self.numOfWorkingDays * self.numOfPeriods)
        self.fitness = noClashfitness

        midFreeCount = 0
        totFreeCount = 0
        for b in range(self.numOfBatches):
            for d in range(self.numOfWorkingDays):
                freeCount = 0
                firstClassFound = False
                for p in range(0, self.numOfPeriods):
                    if self.batchList[b].timetable[d][p] == None:
                        freeCount += 1
                        totFreeCount += 1
                    else:
                        if firstClassFound:
                            midFreeCount += freeCount
                        freeCount = 0
                        firstClassFound = True

        self.softPenalty = midFreeCount

        # reduce soft constraint penalty 100 times so that it doesnt overpower hard constraint fitness
        if totFreeCount==0:
            penalty = 0
        else:
            penalty = (float(midFreeCount)/totFreeCount)/100

        self.fitness -= penalty




    def generateRandom(self):
        for i in range(self.numOfBatches):
            self.batchList.append(Batch(self.numOfPeriods,self.numOfWorkingDays,self.courseStructOfBatch[i]))
            self.batchList[i].generateRandomTimeTable()

    def setData(self, batchList):
        self.batchList = batchList

    def crossover(self, otherDNA):
        childBatchList = []
        for i in range(self.numOfBatches):
            if random.randint(0, 1):
                childBatchList.append(self.batchList[i])
            else:
                childBatchList.append(otherDNA.batchList[i])

        childDNA = DNA(self.numOfPeriods, self.numOfWorkingDays, self.courseStructOfBatch)
        childDNA.setData(childBatchList)
        return childDNA

    def mutate(self, mutationRate):
        for i in range(self.numOfWorkingDays):
            for j in range(self.numOfPeriods):
                if random.random() < mutationRate:
                    day = random.randrange(0, self.numOfWorkingDays)
                    period = random.randrange(0, self.numOfPeriods)
                    # swap
                    for batch in self.batchList:
                        batch.timetable[i][j], batch.timetable[day][period] = batch.timetable[day][period], batch.timetable[i][j]

    def deepClone(self):
        return copy.deepcopy(self)