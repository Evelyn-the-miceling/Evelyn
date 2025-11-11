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

        #Code to use our Groups_of_5 and Swapping_students functions:
        subgroups = Groups_of_5(Male_Students_sorted, Female_Students_sorted, ratio_boy_girl)
        subgroups = Swapping_students(subgroups)

        #To mark the subgroups with its index:
        for i, subgroup in enumerate(subgroups):
            for students in subgroup:
                students["subgroup"] = f"{students["tutorial_group"]}-T{i + 1}"

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

    #To handle anyone remaining in the unsorted students by putting them into a group. This should be empty
    if Unsorted_Students_sorted:
        remaining_groups = [remaining_students for remaining_students in Unsorted_Students_sorted]
        all_subgroups.append(remaining_groups)

    return all_subgroups

#____________________________________________________________________#

#Code to enhance school diversity:

# Before assigning each tutorial group with a key, we will re-arrange the students to enhance school diversity
# without altering too much the gender and CGPA dynamics that we made when we put everyone into groups
# To alter, we will modify this lists of lists we made after calling the Groups_of_5 function directly
# [[Tutgroup 1 - Group 1 members], [Tutgroup 1 - Group 2 members], ...]
# The way to go is:
# 1. Find out a group (call this group "undesired_group" that has 2+ people of the same school)
# 2. Find the type of schools inside that group
# 4. Find a student that has school similarity in the "undesired_group". We call this student "undesired_student"
# 5. Find a different group (call this group "swapper_group") does not have the same school types as the "undesired_student"
# 6. Find a student that has school similarity in the "undesired_group". We call this student "undesired_student"
# 7. Swap. Note that steps 2-5 we should have also found the indices of the students and the groups we wish to swap
# 8. And continue until either we have successfully swapped everything (maximise school diversity), or we cannot swap anymore.
# ! The "we cannot swap anymore" in 8. happens when the number of students with the same school is larger than the number of groups.
# ! If that happens, we must concede again and have to accept a few groups that are not school-diverse enough.

def Check_School_types_in_subgroup(a_list):
    #Function to count number of school types + number of students at what school
    Reps = {}
    for students in a_list:
        Reps[students["school"]] = 0
    for students in a_list:
        Reps[students["school"]] += 1
    return Reps

def Check_School_Diversity(a_list):
    #Function to ensure the group has school diversity.
    School_type = Check_School_types_in_subgroup(a_list)
    for schools in School_type.keys():
        if School_type[schools] > 1:
            return False
    else:
        return True

def Check_Repeating_School(a_list):
    #Function to return the first type of school that repeats itself
    School_type = Check_School_types_in_subgroup(a_list)
    for schools in School_type.keys():
        if School_type[schools] > 1:
            return schools

def Pick_out_the_student(a_list):
    #Function to pick one student that is from a repeated school by their index in the list and themself
    repeated_school = Check_Repeating_School(a_list)
    for student_index, student in enumerate(a_list):
        if student["school"] == repeated_school:
            return (student_index, student)
    else:
        return False
        
def Group_swapper(list_of_lists, group_a, student_a, group_b, student_b):
    #Function to swap students using their indices in the big list
    list_of_lists[group_b][student_b], list_of_lists[group_a][student_a] = list_of_lists[group_a][student_a], list_of_lists[group_b][student_b]
    return list_of_lists

def CGPA_variance_check(student_a, student_b):
    #Function to check for grade variance between the students
    if abs(student_a["cgpa"] - student_b["cgpa"]) <= student_a["cgpa"] * 0.05:
        return True
    else:
        return False

def Swapping_students(list_of_lists):
    #Function to keep swapping students until we have school diversity
    while True:

        undesired_group_index = -1
        undesired_group = []

        #Code to find the first undesired_group
        for group_index in range(len(list_of_lists)):
            if not Check_School_Diversity(list_of_lists[group_index]):
                undesired_group_index = group_index
                undesired_group = list_of_lists[group_index]
                break
        
        #Code to get our student in the undesired group. 
        if Pick_out_the_student(undesired_group) != False:
            undesired_student_index, undesired_student = Pick_out_the_student(undesired_group)
        else: # If there is no more undesired_groups, of course we cannot choose our student, so we break out of the while loop
            break

        #Code to get the school types in that undesired group
        School_types_in_undesired_group = Check_School_types_in_subgroup(undesired_group)

        # Code to find the indices of our swapper group and the student in the swapper group, as well as swap the students.
        # We just need to find the first group and first student that satifies the criteria to swap.
        # Basically, the criteria is the swapping student in the undesired group must have different schools to the students
        # in the swapper group, and vice versa.
        # This is to ensure that the loop does not run forever when meet cases like:
        # undesired_group = [A, A, B, C, D]; swapper_group = [A, X, Y, Z, T] (Letters are examples for schools)
        # When we swap A between 2 groups, the problem is still there since after swapping, there will still be 2 students 
        # coming from the same school in one of the 2 groups.
        # Moreover, the swapping student must have the same gender and CGPA difference of less
        # than 5% compared to the undesired student to make sure that our list_of_lists's dynamics
        # does not change much after swapping
        
        swapped_yet_or_not = False #Marker to check if we have made a swapping move or not
        
        for swapper_group_index in range(len(list_of_lists)):
            if swapper_group_index == undesired_group_index:
                continue

            #Get the index and school types for the swapper_group
            swapper_group = list_of_lists[swapper_group_index]
            School_types_in_swapper_group = Check_School_types_in_subgroup(swapper_group)

            for swapper_student_index in range(len(swapper_group)):
                swapper_student = swapper_group[swapper_student_index]
                
                if undesired_student["school"] not in School_types_in_swapper_group.keys():
                    #If the undesired student has different school to the swapper group
                    
                    if swapper_student["school"] not in School_types_in_undesired_group.keys(): 
                        #If the swapper student has different school to the undesired group
                        
                        if swapper_student["gender"] == undesired_student["gender"] and CGPA_variance_check(undesired_student, swapper_student) == True:
                            #If the swapper student has the same gender and CGPA around as the undesired student(5%)
                                
                            list_of_lists = Group_swapper(list_of_lists, undesired_group_index, undesired_student_index, swapper_group_index, swapper_student_index)
                            #After satisfying all the conditions above, we swap students
                            
                            swapped_yet_or_not = True #Mark as having swapped the 2 students
                            break #Get out of the small loop

            if swapped_yet_or_not == True: #After swapping, of course get out of the big loop
                break
        
        if swapped_yet_or_not == False: 
            #In case when the number of students with the same school is larger than the number of groups
            break
    
    return list_of_lists

#____________________________________________________________________#

#Code to write our output into a .csv file

def WriteOutput(Output_groups, filename = "OutputFile.csv"):
    try:
        with open(filename, mode='w') as file:
            header_row = ",".join(["Tutorial Group", "Student ID", "School", "Name", "Gender", "CGPA", "Subgroups"]) + "\n"
            file.write(header_row)
            for tutgroup in Output_groups.values(): #Take out each tutorial group in output file
                for allocated_groups in tutgroup: #Take out each allocated group in the tutorial group
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
                        data_row = ",".join(row_values) + "\n"

                        file.write(data_row)
    except:
        print("Error!")


#Debugging function

groups = readfile()

Output_groups = Group_Sorting(groups)

#WriteOutput(Output_groups)

Output_group1 = Output_groups['G-1']

""" for name, groups in Output_groups.items():
    print(groups)
    print("________________________") """

""" for group in Output_group1:
    print(group)

    print("________________________") """
