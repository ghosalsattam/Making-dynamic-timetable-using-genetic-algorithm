from Population import Population
import mysql.connector
class FetchTimetable():
    def __init__(self,filename,numOfPeriods,numOfWorkingDays,absentList):
        self.filename=filename
        self.numOfPeriods=numOfPeriods
        self.numOfWorkingDays=numOfWorkingDays
        self.trainerList=[]
        self.courseList=[]
        self.classPerWeekList=[]
        self.timetable=[]
        self.absentList=list(absentList.split())
        
    def createSkillAndTrainerList(self):
        
        file = open(self.filename, "r")
        c = []
        
        for line in file:
            if line == "\n":
                continue;
                
            else:
                course, trainer, classPerWeek = list(line.split())
                if course not in self.courseList:
                    self.courseList.append(course)
                    
                

                if trainer not in self.trainerList:
                    self.trainerList.append(trainer)
                        
                
                    

    def fetchTimetableFromDatabase(self):
        

        #populationSize = 200
        #mutationRate = 0.1

        mydb=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='Timetable'
        )

        cur=mydb.cursor()
        cur.execute('select * from Routine')
        li=cur.fetchall()
       
        for i in li:
            j=list(i)
            self.timetable.append(j)
        #print(timetable)

        for i in range( len(self.timetable)): 
            for j in range(2,len(self.timetable[i])):
                st=self.timetable[i][j]
                if '|' in st:
                    l=list(st.split('|'))
                    l=[int(l[0]),int(l[1])]
                    self.timetable[i][j]=l
        #print(self.timetable)
        
        for i in range( len(self.timetable)): 
            for j in range(2,len(self.timetable[i])):
                st=self.timetable[i][j]
                if(st[2] in self.absentList):
                    timetable[i]
                
    '''for i in range(len(timetable)):
        for j in range(2,len(timetable[i])):
            if 'day' not in timetable[i][j] and'_' not in timetable[i][j]:
               print(courseList[timetable[i][j][0]]+" "+trainerList[timetable[i][j][1]],end='\t')
            else:
                print('        ',end='\t')
        print()
        if((i+1)%numOfWorkingDays==0):
            print('-'*93)'''
            
            
            
ft=FetchTimetable("input.txt",8,5)
ft.createSkillAndTrainerList()
ft.fetchTimetableFromDatabase()
         
