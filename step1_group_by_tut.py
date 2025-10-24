"""
convert each line into dictionary like:
{
     "tutorial_group": "G-1",
     "student_id": "U1234567X",
     "school": "SCSE",
     "name": "Zone",
     "gender": "M",
     "cgpa": 4.23
   }
"""

#function convert each line to dictionary
def ConvertToDict(line):
    #split line into list with ,
    lists = line.strip().split(",")

    #return dictionary
    return{
        "tutorial_group" : lists[0],
        "student_id" : lists[1],
        "school" : lists[2],
        "name" : lists[3],
        "gender" : lists[4],
        "cgpa" : float(lists[5])
    }

#function append each dictionary to 1 big list
def OneBigList(data = "records.csv"):
    #create 1 big list
    students = []

    #read each line from file
    with open(data, "r", encoding="utf-8") as file:
        #skip header
        header = file.readline().strip()

        #read each line and append to students
        for line in file:
            line = line.strip()
            students.append(ConvertToDict(line))
    return students

#function to gather same tut group in 1 dictionary with key = tut no.
def GroupByTut(students):
    #create dictionary
    groups = {}

    #d is dictionary
    for d in students:
        #assign tut no.
        tutno = d["tutorial_group"]

        #check tutno in groups
        if tutno not in groups:
            #create key in groups
            groups[tutno] = []
        
        #append data into groups(list)
        groups[tutno].append(d)

    #return big dictionary
    return groups

#comebine functions
def readfile():
    students = OneBigList("records.csv")
    groups = GroupByTut(students)
    return groups

if __name__ == "__main__":
    groups = readfile()
    print("\nNumber of tutorial groups:", len(groups)) 
    print("Example group: G-1")
    for i in groups["G-1"][:5]:
        print(i["student_id"], i["name"], i["school"], i["cgpa"])

"""
you need to type this if you build your code in differnce file

from step1_group_by_tut import *
groups = readfile()  

then you will get 1 big dictionary same as in file that I show you
"""