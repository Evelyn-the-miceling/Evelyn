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

#combine all functions together
def trys():
    students = OneBigList("records.csv")

    #print to check
    print("\nTotal records", len(students))
    print("Sample dicts(3 lines)")
    for i in range(3):
        print(students[i])

#trys()
