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
# 6. Find a student that has school similarity in the "undesired_group". We call this student "swapper_student"
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
    if abs(student_a["cgpa"] - student_b["cgpa"]) <= student_a["cgpa"] * 0.075:
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

import csv
import matplotlib.pyplot as plt
import math # Only used for sqrt function in standard deviation

# --- CONFIGURATION ---
INPUT_FILE = 'OutputFile.csv'
REQUIRED_TEAM_SIZE = 5

# --- DATA STRUCTURES ---

# Stores the full nested student data grouped by Tutorial Group and then Team
# Structure: { 'G-1': { 'G-1-T1': [{data}, ...], ... }, ... }
tut_groups_map = {}

# Stores results for plotting and summarizing
group_stats = {}

# Stores the final counts for bar charts
gender_ratio_counts = {'5:0': 0, '4:1': 0, '3:2': 0, '2:3': 0, '1:4': 0, '0:5': 0, 'Other': 0}
school_diversity_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0} # Key is number of unique schools

# Stores the standard deviation distribution
sd_distribution_counts = {}

# Define the boundaries for the 0.01 interval bins (up to 0.15)
SD_BINS = [round(i * 0.01, 2) for i in range(17)] # 0.00, 0.01, ..., 0.16

# --- MANUAL STATISTICAL HELPER FUNCTIONS (NO NUMPY) ---

def calculate_mean(data):
    """Calculates the mean (average) of a list of numbers."""
    if not data:
        return 0.0
    return sum(data) / len(data)

def calculate_std_dev(data, mean_value):
    """Calculates the population standard deviation of a list of numbers."""
    N = len(data)
    if N < 2:
        return 0.0
    
    # Calculate sum of squared differences from the mean
    sum_sq_diff = sum([(x - mean_value) ** 2 for x in data])
    
    # Population standard deviation formula: sqrt(sum_sq_diff / N)
    variance = sum_sq_diff / N
    
    return math.sqrt(variance)

def get_sd_bin(sd_value): #******change this part******
    """Assigns the SD value to a 0.01 interval bin (e.g., 0.015 -> '0.01-0.02')."""
    # Check if value is outside the defined range
    if sd_value > 0.15:
        return '>0.15'

    # Iterate through the 0.01 bins
    for i in range(len(SD_BINS) - 1):
        lower_bound = SD_BINS[i]
        upper_bound = SD_BINS[i+1]
        
        # We handle the lower bound (0.00-0.01) explicitly for 0.00 inclusion
        if i == 0 and 0.0 <= sd_value <= 0.01:
            return '0.00-0.01'
        
        # For all other bins, check if lower_bound < sd_value <= upper_bound
        if lower_bound < sd_value <= upper_bound:
            return f'{lower_bound:.2f}-{upper_bound:.2f}'
    
    return 'Other' # Fallback for unexpected values (should not happen)

def initialize_sd_bins():
    """Initializes the standard deviation counts dictionary based on SD_BINS."""
    global sd_distribution_counts
    for i in range(len(SD_BINS) - 1):
        lower_bound = SD_BINS[i]
        upper_bound = SD_BINS[i+1]
        sd_distribution_counts[f'{lower_bound:.2f}-{upper_bound:.2f}'] = 0
    # Add the final bin for values above the range
    sd_distribution_counts['>0.15'] = 0
#until here *****
# --- CORE LOGIC: DATA LOADING AND GROUPING ---

def load_and_group_data(file_path):
    """Loads student data and groups it by Tutorial Group and then Team."""
    print(f"--- Loading data from {file_path} ---")

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) # Skip header

            # Map column names to indices
            col_index = {
                'Tutorial Group': header.index('Tutorial Group'),
                'Gender': header.index('Gender'),
                'CGPA': header.index('CGPA'),
                'School': header.index('School'),
                'Subgroups': header.index('Subgroups'),
            }

            for row in reader:
                # Basic row validation
                if len(row) <= max(col_index.values()): continue

                tut_grp_name = row[col_index['Tutorial Group']]
                team_name = row[col_index['Subgroups']]
                cgpa_str = row[col_index['CGPA']]

                try:
                    cgpa = float(cgpa_str)
                except ValueError:
                    continue # Skip if CGPA is not a valid number

                student_data = {
                    'gender': row[col_index['Gender']],
                    'school': row[col_index['School']],
                    'cgpa': cgpa
                }

                # Populate the nested grouping map
                if tut_grp_name not in tut_groups_map:
                    tut_groups_map[tut_grp_name] = {}
                if team_name not in tut_groups_map[tut_grp_name]:
                    tut_groups_map[tut_grp_name][team_name] = []

                tut_groups_map[tut_grp_name][team_name].append(student_data)

            print(f"Data loaded and grouped into {len(tut_groups_map)} Tutorial Groups.")
            return True

    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        return False

# --- CORE LOGIC: DIVERSITY AND STATISTICAL ANALYSIS ---

def analyze_diversity_and_stats():
    """Performs all team-level and group-level statistical analysis."""

    print("\n--- Analyzing Diversity and CGPA Standard Deviation ---")

    all_group_sd_values = []

    for tut_grp_name, teams_in_group in tut_groups_map.items():
        
        team_cgpa_means = []
        
        if tut_grp_name not in group_stats:
             group_stats[tut_grp_name] = {
                'team_cgpa_means': [],
                'group_mean_cgpa': 0.0,
                'sd_of_team_means': 0.0
            }

        # List to collect all CGPAs in the group for overall mean calculation
        all_group_cgpas = []
        
        for team_name, students in teams_in_group.items():
            team_size = len(students)
            
            # --- 1. Team CGPA Mean and Collection ---
            team_cgpas = [s['cgpa'] for s in students]
            team_mean_cgpa = calculate_mean(team_cgpas)
            team_cgpa_means.append(team_mean_cgpa)
            all_group_cgpas.extend(team_cgpas)

            # --- 2. Gender Diversity Ratio Evaluation (Teams of 5) ---
            if team_size == REQUIRED_TEAM_SIZE:
                male_count = sum(1 for s in students if s['gender'] == 'Male')
                female_count = team_size - male_count
                ratio_key = f'{male_count}:{female_count}'
                
                if ratio_key in gender_ratio_counts:
                    gender_ratio_counts[ratio_key] += 1
                else:
                    gender_ratio_counts['Other'] += 1
            elif team_size != 0:
                 gender_ratio_counts['Other'] += 1

            # --- 3. School Diversity Evaluation ---
            unique_schools = set(s['school'] for s in students)
            num_unique_schools = len(unique_schools)
            
            if num_unique_schools in school_diversity_counts:
                school_diversity_counts[num_unique_schools] += 1

        # --- Group-Level CGPA Statistics (Step 3) ---
        
        # Calculate Group Mean CGPA (Mean of all students in the tutorial group)
        group_mean_cgpa = calculate_mean(all_group_cgpas)
        group_stats[tut_grp_name]['group_mean_cgpa'] = group_mean_cgpa

        # Calculate Standard Deviation (SD) of Team Means within the group
        # This checks the consistency of team quality within the tutorial group.
        if len(team_cgpa_means) >= 2:
            mean_of_team_means = calculate_mean(team_cgpa_means)
            sd_of_means = calculate_std_dev(team_cgpa_means, mean_of_team_means)
            group_stats[tut_grp_name]['sd_of_team_means'] = sd_of_means
            all_group_sd_values.append(sd_of_means)
        else:
            group_stats[tut_grp_name]['sd_of_team_means'] = 0.0

    # --- 4. Plot SD Distribution (Step 3 plotting) ---
    initialize_sd_bins() # Ensure bins are ready
    
    for sd_val in all_group_sd_values:
        bin_key = get_sd_bin(sd_val)
        if bin_key in sd_distribution_counts:
            sd_distribution_counts[bin_key] += 1
    
    print("\n--- CGPA Statistics Summary ---")
    for group, data in group_stats.items():
        print(f"Group {group}: Group Mean CGPA = {data['group_mean_cgpa']:.3f} | SD of Team Means = {data['sd_of_team_means']:.3f}")


# --- VISUALIZATION FUNCTIONS ---

def plot_gender_diversity(counts):
    """Generates a bar chart showing the distribution of gender ratios."""
    
    # Filter out 'Other' for cleaner plotting if its count is 0
    labels = [k for k in counts.keys() if counts[k] > 0 or k != 'Other']
    data = [counts[k] for k in labels]
    
    if not labels or sum(data) == 0:
        print("No gender ratio data to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color=['#3498db', '#5dade2', '#85c1e9', '#e74c3c', '#ec7063', '#f1948a', '#95a5a6'])
    
    plt.xlabel(f'Male:Female Ratio (Teams of {REQUIRED_TEAM_SIZE})', fontsize=12)
    plt.ylabel('Number of Teams', fontsize=12)
    plt.title(f'1. Gender Diversity (Male:Female Ratio) Across All Teams', fontsize=14, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show() # ADDED: Force plot display [Image of a bar chart illustrating gender distribution by ratio]


def plot_school_diversity(counts):
    """Generates a bar chart showing the distribution of unique school counts."""
    
    # Sort keys for consistent plotting order (5 down to 1)
    # Filter for keys that have data and map to string labels
    present_keys = sorted([k for k in counts.keys() if counts[k] > 0], reverse=True)
    labels_str = [str(k) for k in present_keys]
    data = [counts[k] for k in present_keys]

    if sum(data) == 0:
        print("No school diversity data to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(labels_str, data, color=['#2ecc71', '#27ae60', '#1abc9c', '#16a085', '#34495e'])
    
    plt.xlabel('Number of Unique Schools per Team', fontsize=12)
    plt.ylabel('Number of Teams', fontsize=12)
    plt.title('2. School Diversity Across All Teams', fontsize=14, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show() # ADDED: Force plot display 


def plot_sd_distribution(counts):
    """Generates a bar chart showing the frequency of Standard Deviation values in 0.01 bins."""
    
    # Ensure all bins are included, in sorted order
    labels = sorted(counts.keys())
    # Move '>0.15' to the end for logical display
    if '>0.15' in labels:
        labels.remove('>0.15')
        labels.append('>0.15')
        
    data = [counts[k] for k in labels]

    if sum(data) == 0:
        print("No SD distribution data to plot (Need at least two teams per group).")
        return
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, data, color='#f39c12')
    
    plt.xlabel('Standard Deviation (SD) Range of Team Mean CGPAs (0.01 Intervals)', fontsize=12)
    plt.ylabel('Number of Tutorial Groups', fontsize=12)
    plt.title('3. Distribution of CGPA Consistency (SD of Team Means per Group)', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show() # ADDED: Force plot display [Image of a bar chart illustrating the distribution of standard deviation values]

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    if load_and_group_data(INPUT_FILE):
        
        # Run the combined analysis
        analyze_diversity_and_stats()
        
        # Generate the required charts
        plot_gender_diversity(gender_ratio_counts)
        plot_school_diversity(school_diversity_counts)
        plot_sd_distribution(sd_distribution_counts)