#to divide each student into their tut group

#import from step2
from step2_convert_to_list import OneBigList

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
def main():
    students = OneBigList("records.csv")
    groups = GroupByTut(students)

    #print to check
    print("\nNumber of tutorial groups:", len(groups)) 
    print("Example group: G-1")
    for i in groups["G-1"][:5]:
        print(i["student_id"], i["name"], i["school"], i["cgpa"])

main()
