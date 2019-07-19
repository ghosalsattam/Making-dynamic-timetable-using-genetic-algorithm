import random


class Course:
    def __init__(self, skillIndex, trainerIndex, lecturesPerWeek):
        self.skillIndex = skillIndex
        self.trainerIndex = trainerIndex
        self.lecturesPerWeek = lecturesPerWeek


class Batch:
    def __init__(self, numOfPeriods, numOfWorkingDays, courses):
        self.numOfPeriods = numOfPeriods
        self.numOfWorkingDays = numOfWorkingDays
        self.courses = courses
        self.timetable = []

    def generateRandomTimeTable(self):
        # Initialize time table with all free periods
        for i in range(self.numOfWorkingDays):
            dayRoutine = []
            for j in range(self.numOfPeriods):
                dayRoutine.append(None)
            self.timetable.append(dayRoutine)

        for course in self.courses:
            # add a course to timetable randomly, lecturesPerWeek number of times
            for i in range(course.lecturesPerWeek):
                # Select a random day, period until we find a free period
                # and assign the course to it
                while True:
                    day = random.randrange(0, self.numOfWorkingDays)
                    period = random.randrange(0, self.numOfPeriods)
                    if self.timetable[day][period] == None:
                        self.timetable[day][period] = course
                        break
