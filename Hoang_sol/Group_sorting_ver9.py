#Function to read the files
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

#____________________________________________________________________#

#Code to sort by Gender of a group:
def criteria_gender(student):
    return student["gender"]

def SortbyGender(student_list, reverse_or_not):
    return sorted(student_list, reverse=reverse_or_not, key=criteria_gender)

#____________________________________________________________________#

#Code to sort by CGPA of a group:
def criteria_cgpa(student):
    return student["cgpa"]

def SortbyCGPA(student_list, reverse_or_not):
    return sorted(student_list, reverse=reverse_or_not, key=criteria_cgpa)

#____________________________________________________________________#

#Code to only iterate through ALL tutorial groups to return the groupings
def Group_Sorting(groups):
    #Code to sort by CGPA of a group:
    Output_groups = {}

    #The output should be a dict with keys are the original groups and values are the lists of lists of allocated groups

    for tut_group_name, student_list in groups.items():
        #Code to classify Male and Female students and sort them by ascending/descending GPA
        Male_Students = []
        Female_Students = []

        for students in student_list:
            if students["gender"] == "Male":
                Male_Students.append(students)
            elif students["gender"] == "Female":
                Female_Students.append(students)

        number_of_male = len(Male_Students) # Number of boys in the group
        number_of_female = len(Female_Students) # Number of girls in the group

        Male_Students_sorted = SortbyCGPA(Male_Students, True) # Sort by CGPA from high -> low
        Female_Students_sorted = SortbyCGPA(Female_Students,True) # Sort by CGPA from high -> low


        # ratio_boy_girl is used to handle one-gendered groups
        if number_of_male == 0:
            ratio_boy_girl = 0.0
        elif number_of_female == 0:
            ratio_boy_girl = float('inf')
        else:
            ratio_boy_girl = number_of_male/number_of_female
        #print(f"Male/Female ratio: {number_of_male}/{number_of_female}")

        #____________________________________________________________________#

        #Code to use our Groups_of_5 function:
        subgroups = Groups_of_5(Male_Students_sorted, Female_Students_sorted, ratio_boy_girl)

        Output_groups[tut_group_name] = subgroups
    
    return Output_groups

#____________________________________________________________________#

#Code to assign students into groups of 5:

def Groups_of_5(Male_Students_sorted, Female_Students_sorted, ratio_boy_girl):
    all_subgroups = []
    group_counter = 0
    max_groups = 10
    number_of_male = len(Male_Students_sorted)
    number_of_female = len(Female_Students_sorted)

    if 2/3 <= ratio_boy_girl <= 3/2:
    #Assign students into groups of 1 Male/High CGPA + 1 Male/Low CGPA + 1 Female/High CGPA + 1 Female/Low CGPA first. The
    #boy/girl ratio is to ensure that we can make 10 groups of the above type.
        while len(Male_Students_sorted) >= 2 and len(Female_Students_sorted) >= 2 and group_counter < max_groups:
            team = [
                    Male_Students_sorted.pop(0), #Male/High CGPA
                    Male_Students_sorted.pop(), #Male/Low CGPA
                    Female_Students_sorted.pop(0), #Female/High CGPA
                    Female_Students_sorted.pop() #Female/Low CGPA
                    ]

            all_subgroups.append(team)
            group_counter += 1


    elif ratio_boy_girl < 2/3:
    #If this happens, we cannot form 10 groups that has 2 boys - 2 girls. E.g: Group "G-2" has 18 boys and 32 girls
    #We must make a copromise: There can be groups of 1 boy - 4 girls. In the above example, an optimal way should be to take
    #n groups of 1 boy - 4 girls and m groups of 2 boy - 3 girls for the example above
    #n m satisfies the above matrix:
    # [2 1] * [m] = [x] # x = number of males; y = number of females; x < y
    # [3 4]   [n]   [y]
    # n(x, y) = (-3x + 2y) / 5 (Cramer's Law)
    # m(x, y) = (+4x - 1y) / 5  
    # Note that x + y = 50 and m + n = 10
    # Thus, m = x - 10 
    
        while len(Male_Students_sorted) >= 2 and len(Female_Students_sorted) >= 4 and group_counter < max_groups:
            if group_counter < number_of_male - 10:
                team = [
                        Male_Students_sorted.pop(0), #Male/High CGPA
                        Male_Students_sorted.pop(), #Male/Low CGPA
                        Female_Students_sorted.pop(0), #Female/High CGPA
                        Female_Students_sorted.pop(), #Female/Low CGPA
                        Female_Students_sorted.pop() #Female/Low CGPA
                        ]

            elif group_counter >= number_of_male - 10:
                team = [
                        Male_Students_sorted.pop(0), #Male/High CGPA
                        Female_Students_sorted.pop(), #Female/Low CGPA
                        Female_Students_sorted.pop(0), #Female/High CGPA
                        Female_Students_sorted.pop(), #Female/Low CGPA
                        Female_Students_sorted.pop(0) #Female/High CGPA
                        ]

            all_subgroups.append(team)
            group_counter += 1
    
    elif ratio_boy_girl > 3/2:
    #Same as above, just swap "boys" with "girls" 
    #Note: Both "elif" clauses only apply for the situation where there are 18 - 32 of boys - girls
        while len(Male_Students_sorted) >= 4 and len(Female_Students_sorted) >= 2 and group_counter < max_groups:
            if group_counter < number_of_female - 10:
                team = [
                        Female_Students_sorted.pop(0), #Female/High CGPA
                        Female_Students_sorted.pop(), #Female/Low CGPA
                        Male_Students_sorted.pop(0), #Male/High CGPA
                        Male_Students_sorted.pop(), #Male/Low CGPA
                        Male_Students_sorted.pop() #Male/Low CGPA
                        ]

            elif group_counter >= number_of_female - 10:
                team = [
                        Female_Students_sorted.pop(0), #Female/High CGPA
                        Male_Students_sorted.pop(), #Male/Low CGPA
                        Male_Students_sorted.pop(0), #Male/High CGPA
                        Male_Students_sorted.pop(), #Male/Low CGPA
                        Male_Students_sorted.pop(0) #Male/High CGPA
                        ]

            all_subgroups.append(team)
            group_counter += 1

    #Group all remaining students into a list
    Unsorted_Students = Male_Students_sorted + Female_Students_sorted
    Unsorted_Students_sorted = SortbyCGPA(Unsorted_Students, True) #Sort the remaining student's CGPA from high to low
    
    num_of_4_people_groups = len(all_subgroups)
    num_of_remaining_students = len(Unsorted_Students)

    for i in range(min(num_of_4_people_groups, num_of_remaining_students)): 
        if len(all_subgroups[i]) == 4: #To ensure that subgroups are addable
            all_subgroups[i].append(Unsorted_Students_sorted.pop(0))

    #To handle anyone remaining in the unsorted students by putting them into a group
    if Unsorted_Students_sorted:
        remaining_groups = [remaining_students for remaining_students in Unsorted_Students_sorted]
        all_subgroups.append(remaining_groups)

    #To mark the subgroups with its index:
    for i, subgroup in enumerate(all_subgroups):
        for students in subgroup:
            students["subgroup"] = f"{students["tutorial_group"]}-T{i + 1}"

    return all_subgroups

#____________________________________________________________________#

#Code to write our output into a .csv file

def WriteOutput(Output_groups, filename = "OutputFile.csv"):
    header = ["Tutorial Group", "Student ID", "School", "Name", "Gender", "CGPA", "Subgroups"]

    try:
        with open(filename, mode='w', encoding="utf-8") as file:

            header_row = ",".join(header) + "\n"
            file.write(header_row)
            for tutgroup in Output_groups.values(): #Take out each tutorial group in output file
                for allocated_groups in tutgroup: #Take out each allocated group
                    for students in allocated_groups: #Take out each student in that particular allocated group
                        row_values =[
                                    students["tutorial_group"],
                                    students["student_id"],
                                    students["school"],
                                    students["name"],
                                    students["gender"],
                                    str(students["cgpa"]),
                                    students["subgroup"]
                                    ]
                        data_row = ",".join(row_values) +"\n"

                        file.write(data_row)
    except:
        print("Error!")


#Debugging function

groups = readfile()

Output_groups = Group_Sorting(groups)

WriteOutput(Output_groups)

""" Output_group1 = Output_groups['G-1']

for name, groups in Output_groups.items():
    print(groups)
    print("________________________") """

def test():
    print(Output_groups)

test()