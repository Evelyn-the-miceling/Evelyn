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

""""
if __name__ == "__main__":
    groups = readfile()
    print("\nNumber of tutorial groups:", len(groups)) 
    print("Example group: G-1")
    for i in groups["G-1"][:5]:
        print(i["student_id"], i["name"], i["school"], i["cgpa"])


you need to type this if you build your code in differnce file

from step1_group_by_tut import *
groups = readfile()  

then you will get 1 big dictionary same as in file that I show you
"""

#split student into 4 groups
STEM = {"SCSE", "EEE", "MAE", "CEE", "MSE", "SPMS", "SBS", "ASE", "BIE"}

def splitandsort(groups):
    #create dictionary that will return in the end
    result = {}

    #run each tut group
    for tut, members in groups.items():
        buckets = {
            "male_stem": [],
            "male_nonstem": [],
            "female_stem": [],
            "female_nonstem": [],
        }
        #check students in tut group and append it to buckets
        for s in members:
            stem = (s["school"] in STEM)
            if s["gender"] == "Male":
                if stem:
                    buckets["male_stem"].append(s)
                else:
                    buckets["male_nonstem"].append(s)
            else:
                if stem:
                    buckets["female_stem"].append(s)
                else:
                    buckets["female_nonstem"].append(s)

        #sorting numbers of students
        items = list(buckets.items())
        items.sort(key = lambda kv: (len(kv[1]), kv[0]))

        #sorting cgpa
        #A is the smallest group
        (nameA, A), (nameB, B), (nameC, C), (nameD, D) = items
        A.sort(key = lambda s: s["cgpa"]) #asc
        B.sort(key = lambda s: s["cgpa"]) #asc
        C.sort(key = lambda s: s["cgpa"], reverse = True) #dsc
        D.sort(key = lambda s: s["cgpa"], reverse = True) #dsc

        #save result for this tut group
        result[tut] = {
            "A": A, "B": B, "C": C, "D": D,
            "names": {"A": nameA, "B": nameB, "C": nameC, "D": nameD}
        }
    return result

#design solution for perfect mode
def perfectmode(groups):
    A, B, C, D = groups["A"], groups["B"], groups["C"], groups["D"]

    #create 10 teams
    teams = [[] for _ in range(10)]
    for i in range(10):
        teams[i].append(A[i])
        teams[i].append(B[i])
        teams[i].append(C[i])
        teams[i].append(D[i])

    #collect 10 leftover students
    leftover = A[10:] + B[10:] + C[10:] + D[10:]
    return teams, leftover

#design solution for adjusted mode
from collections import deque
def adjustedmode(groups):
    A, B, C, D = deque(groups["A"]), deque(groups["B"]), deque(groups["C"]), deque(groups["D"])

    #create 10 teams
    teams = [[] for _ in range(10)]

    #split 1 student into each team
    t = 0
    while t < 10 and A:
        teams[t].append(A.popleft())
        t += 1
    while t < 10 and B:
        teams[t].append(B.popleft())
        t += 1
    while t < 10 and C:
        teams[t].append(C.popleft())
        t += 1
    while t < 10 and D:
        teams[t].append(D.popleft())
        t += 1

    #fill 4 students to each team
    #check each team consist of 4 stu
    def needmore():
        for i in teams:
            if len(i) < 4:
                return True
        return False
    
    #function to help to move student from A B C D to each team
    def pick(ABCD):
        if ABCD:
            return ABCD.popleft()
        return None
    
    #process
    i = 0
    while needmore() and (A or B or C or D):
        team = teams[i % 10]

        #add student until cannot add
        if len(team) < 4:
            for ABCD in (A, B, C, D):
                if len(team) < 4 and ABCD:
                    team.append(pick(ABCD))
        i += 1

        #adjusted case
        if len(team) < 4 and sum(bool(x) for x in (A, B, C, D)) <= 2:
            remain = [ABCD for ABCD in (A, B, C, D) if ABCD]

            #only 1 group left
            if len(remain) == 1:
                r = remain[0]

                #append 2 students
                if r:
                    team.append(r.popleft())
                if len(team) < 4 and r:
                    team.append(r.pop())
                #if len(team) < 4 and r:
                #    team.append(r.pop())

            #2 groups left
            elif len(remain) == 2:
                r1, r2 = remain

                #append 1 student
                larger = r1 if len(r1) > len(r2) else r2
                if len(team) < 4 and larger: team.append(larger.pop())

    leftover = list(A) + list(B) + list(C) + list(D)
    return teams, leftover

#add leftover group by cgpa
def addleftover(teams, leftover):
    if not leftover:
        return teams
    
    #sort within leftover
    leftover.sort(key = lambda s: s["cgpa"], reverse = True)
    
    #function to check mean cgpa in team
    def avg(team):
        total = 0
        for x in team:
            total += x["cgpa"]
        return total/len(team)
    
    #sort team by mean cgpa
    order_teams = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    order_teams.sort(key = lambda idx: avg(teams[idx]))

    #combine teams and leftover
    count = 0
    for i in order_teams:
        if count >= 10:
            break
        if count < len(leftover):
            teams[i].append(leftover[count])
            count += 1
        else:
            break
    return teams

#combine all function
def buildteam(group):
    sizes = [len(group[k]) for k in ("A", "B", "C", "D")]
    if min(sizes) >= 10:
        teams, leftover = perfectmode(group)
        mode = "perfect"
    else:
        teams, leftover = adjustedmode(group)
        mode = "adjusted"

    teams = addleftover(teams, leftover)
    return {"teams": teams, "leftover": [], "names": group["names"], "mode": mode}

#last function
def lastbuild():
    groups = readfile()
    splitsort = splitandsort(groups)

    #dictionary
    output = {}
    for tut, group in splitsort.items():
        output[tut] = buildteam(group)
    return output


#check
"""
if __name__ == "__main__":
    result = lastbuild()
    sample_tut = sorted(result.keys())[15]
    data = result[sample_tut]

    print(f"\nTutorial group: {sample_tut} | Mode: {data['mode']}")
    for i, team in enumerate(data["teams"], 1):
        gpas = [s["cgpa"] for s in team]
        avg = sum(gpas) / len(gpas) if gpas else 0

        # check male and female stem and nonstem
        male = sum(1 for s in team if s["gender"].lower().startswith("m"))
        female = sum(1 for s in team if s["gender"].lower().startswith("f"))
        stem = sum(1 for s in team if s["school"] in STEM)
        nonstem = len(team) - stem

        print(f"\nTeam {i}:")
        print(f"  GPA list  : {gpas}")
        print(f"  Avg GPA   : {avg:.2f}")
        print(f"  Male/Female: {male}/{female}")
        print(f"  STEM/Non-STEM: {stem}/{nonstem}")
"""

if __name__ == "__main__":
    result = lastbuild()

    print("\n===== SUMMARY OF ALL TUTORIAL GROUPS =====")
    for tut, data in sorted(result.items()):
        print(f"{tut}: mode = {data['mode']}")

    print("\n===== DETAIL OF SAMPLE GROUP =====")
    sample_tut = sorted(result.keys())[0]
    data = result[sample_tut]

    print(f"\nTutorial group: {sample_tut} | Mode: {data['mode']}")
    for i, team in enumerate(data["teams"], 1):
        gpas = [s["cgpa"] for s in team]
        avg = sum(gpas) / len(gpas) if gpas else 0

        # นับเพศและ STEM
        male = sum(1 for s in team if s["gender"].lower().startswith("m"))
        female = sum(1 for s in team if s["gender"].lower().startswith("f"))
        stem = sum(1 for s in team if s["school"] in STEM)
        nonstem = len(team) - stem

        print(f"\nTeam {i}:")
        print(f"  GPA list      : {gpas}")
        print(f"  Avg GPA       : {avg:.2f}")
        print(f"  Male/Female   : {male}/{female}")
        print(f"  STEM/Non-STEM : {stem}/{nonstem}")
