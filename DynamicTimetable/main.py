from CustomObjects import *
from Population import Population
from time import time
import mysql.connector



class CreateTimetable:
    def __init__(self):
        self.trainerList = []
        self.courseList = []
        self.courseStructureOfBatch = []


    def readFromFile(self,filename):
        file = open(filename, "r")
        c = []
        for line in file:
            if line == "\n":
                self.courseStructureOfBatch.append(c)
                c = []
            else:
                course, trainer, classPerWeek = list(line.split())
                courseIndex = 0
                trainerIndex = 0
                if course not in self.courseList:
                    self.courseList.append(course)
                    courseIndex = len(self.courseList) - 1
                else:
                    courseIndex = self.courseList.index(course)

                if trainer not in self.trainerList:
                    self.trainerList.append(trainer)
                    trainerIndex = len(self.trainerList) - 1
                else:
                    trainerIndex = self.trainerList.index(trainer)

                c.append(Course(courseIndex, trainerIndex, int(classPerWeek)))

        if len(c) != 0:
            self.courseStructureOfBatch.append(c)


    def printTimeTableFromDNA(self,dna):
        for batch in dna.batchList:
            print('-' * 93)
            for day in range(dna.numOfWorkingDays):
                for period in range(dna.numOfPeriods):
                    course = batch.timetable[day][period]
                    # if course == FreePeriod:
                    if course == None:
                        print("        ", end="|\t")
                    else:
                        print(self.courseList[course.skillIndex], self.trainerList[course.trainerIndex], end="|\t")
                print('')
            print("")
            


class CreateDatabase():
    def __init__(self,userName,password):
        self.mydb=mysql.connector.connect(
            host="localhost",
            user=userName,
            passwd=password,
            database='Timetable'
        )
     
    def createTable(self,noOfPeriods,noOfWorkingDays,noOfBatches,dna):
        cur=self.mydb.cursor()
        cur.execute('''create table Routine(
        batch varchar(50),
        day varchar(50));  '''      
       )
        for i in range(1,noOfPeriods+1):
            cur.execute("alter table Routine add column Period"+str(i)+" varchar(10);")
        D=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        B=['Year1','Year2','Year3','Year4']
        i=0
        timeTableForDay=[]
        command="insert into Routine values(%s, %s"
        for z in range(noOfPeriods):
            command=command+", %s"
        command=command+")"
        #print (command)
        i=0
        for batch in dna.batchList:
            for day in range(dna.numOfWorkingDays):
                for period in range(dna.numOfPeriods):
                    course = batch.timetable[day][period]
                    # if course == FreePeriod:
                    if course==None:
                        timeTableForDay.append(",_")
                    else:
                        timeTableForDay.append(str(course.skillIndex)+"|"+str(course.trainerIndex))
                        
                #timeTableForDay=timeTableForDay[:-1]
                 
                print(B[i],",",D[day],timeTableForDay) 
                t=(B[i],D[day]) +tuple(timeTableForDay)
                cur.execute(command,t)
                self.mydb.commit()
                timeTableForDay=[]
                    
            i=i+1
            
            
        
        



if __name__ == "__main__":
    ct=CreateTimetable()
    ct.readFromFile("input.txt")

    numOfPeriods = 8
    numOfWorkingDays = 5
    numOfBatches=4

    populationSize = 200
    mutationRate = 0.1

    # generate intial population
    p = Population(numOfPeriods, numOfWorkingDays, ct.courseStructureOfBatch, mutationRate, populationSize)

    # keep making generations until desired result is achieved
    gen = 0
    prev = 0
    genAfterPrev = 0

    totElapsed = 0.0

    p.calcFitness()
    while not p.isComplete:
        s = time()

        p.crossOver()
        p.calcFitness()
        p.calcStatistics()

        e = time()

        elapsed = e - s
        totElapsed += elapsed

        gen += 1

        if p.bestDNA.fitness > prev:
            prev = p.bestDNA.fitness
            print("New Best Found!")
            # printTimeTableFromPopulation(p)
            genAfterPrev = 0
        else:
            genAfterPrev += 1

        print("Generation:", str(gen).rjust(4), "  Fitness:", p.bestDNA.fitness, "  softPenalty:", p.bestDNA.softPenalty,
              "  Avg Fitness:", p.avgFitness, " time:", elapsed, " avgTime:", totElapsed/gen, genAfterPrev)

        if genAfterPrev > 1000:
            break

    print("Finished at Generation", gen, "  Fitness:", p.bestDNA.fitness, "  softPenalty:", p.bestDNA.softPenalty)

    # Show Result
    ct.printTimeTableFromDNA(p.bestDNA)

    p.bestDNA.calcFitness()
    print("Fitness:", p.bestDNA.fitness, "  softPenalty:", p.bestDNA.softPenalty)
    
    
    #print (ct.trainerList)
    
#--------------------------Modified by Sattam---------------------------------------------
    cd=CreateDatabase('root','root')
    cd.createTable(numOfPeriods,numOfWorkingDays,numOfBatches,p.bestDNA)

 



