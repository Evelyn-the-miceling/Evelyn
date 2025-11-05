import csv
import os
import copy

class Sorter:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "lib", "records.csv")
        self.data = {}
        
        #Storage
        self.group_dict = {}
        self.extract_to_dict()
        
        
        
    def extract_to_dict(self):
        temp = []
        with open(self.path, "r") as csvfile:
            reader = csv.reader(csvfile)
            
            next(reader)
            for i in reader:
                temp.append(i)
            
        for field in temp:
            if self.data.get(field[0]):
                self.data[field[0]].append(field)
            else:
                self.data[field[0]] = [field]
                
    
    def build_groups(self, tut_group):
        gpa_total = 0
        female_total = 0
        
        males = []
        females = []
        
        for person in tut_group:
            gpa_total += float(person[5])
            if person[4] == "Female":
                female_total += 1
                females.append(person)
            else:
                males.append(person)
        
        
        gpa_mean = gpa_total / 50
        female_ratio = female_total / 50
        
        males = self.qs(males)
        females = self.qs(females)
        
        update_list = []

        current_ratio = 0
        current_females = 0

        for i in range(50):
            if current_ratio < female_ratio:
                if females:
                    update_list.append(females[-1])
                    females.pop()
                    current_females += 1
                else:
                    update_list = update_list + males
            
            else:
                if males:
                    update_list.append(males[-1])
                    males.pop()
                else:
                    update_list = update_list + females

            current_ratio = current_females/(i+1)

        #Snake method cool idea, sort pass 1
        presets = []
        for i in range(5):
            if i % 2 == 0:
                presets.append(update_list[:10])
                update_list = update_list[10:]
            else:
                presets.append(update_list[:10][::-1])
                update_list = update_list[10:]

        new_groups = []
        temp = []
        for i in range(10):
            for j in presets:
                temp.append(j[i])
            new_groups.append(temp)
            temp = []

        group_dict = {}
        
        #Code to build a dictionary storing the people
        
        for i in range(len(new_groups)):
            group_dict[i] = [new_groups[i], self.calculate_means(new_groups[i])]
            
        #Copy dict for reference when debugging. Use deepcopy method from copy library.
        before_swap = copy.deepcopy(group_dict)
                
             
        #Code for swapping schools assuming they repeat
        for main_number in range(len(group_dict.values())):
            group = group_dict[main_number]
            replacements = []
            if group[1][2] > 2:
                #Identify 3 repeated schools:
                r_school = max(group[1][3], key = group[1][3].get)
                
                #Identify student to replace, populate with index, gender and GPA
                r_students = []
                for member_position in range(5):
                    r_student = group[0][member_position]
                    if r_student[2] == r_school:
                        #Append position, gender and gpa

                        r_students.append([member_position, r_student[4], float(r_student[5])])
                for i in range(10):
                    if group_dict[i][1][2] <3 and max(group_dict[i][1][3], key = group_dict[i][1][3].get) != r_school:
                        replacements.append(i)
                
                #Tuple of person to swap with other person. First is OG, second is swapped.
                #Default 5 as it is the widest range, hence impossible triggering the first new closest_gpa.
                suitable_pair = []
                closest_gpa = 5
                for group_number in replacements: 
                    for position in range(5):
                        substitute = group_dict[group_number][0][position]
                        #Screen replacemnets, ensure they are not from same school, continue if same school
                        if substitute[2] == r_school:
                            print("Mouse")
                            continue
                        gender = substitute[4]
                        gpa = float(substitute[5])
                        for original in r_students:
                            #Screen gender, ensuring same gender
                            if original[1] != gender:
                                pass
                            temp_closest_gpa = abs(gpa-original[2])
                            #Screen closest GPA, so that the result is not affected too much.
                            if temp_closest_gpa < closest_gpa:
                                closest_gpa = temp_closest_gpa
                                suitable_pair = [(main_number, original[0]), (group_number, position)]
                #Swap members into their new groups
                if suitable_pair:
                    print("swapped")
                    print(suitable_pair)
                    og_grp = suitable_pair[0][0]
                    og_pos = suitable_pair[0][1]
                    swp_grp = suitable_pair[1][0]
                    swp_pos = suitable_pair[1][1]
                    print(group_dict[og_grp][0][og_pos], group_dict[swp_grp][0][swp_pos])
                    group_dict[og_grp][0][og_pos], group_dict[swp_grp][0][swp_pos] = group_dict[swp_grp][0][swp_pos],group_dict[og_grp][0][og_pos]
                    print(group_dict[og_grp][0][og_pos], group_dict[swp_grp][0][swp_pos])

        #Update new means
        for i in range(10):
            group_dict[i][1] = self.calculate_means(group_dict[i][0])
            
        self.group_dict = group_dict
        self.display_sorted_tut(before_swap, self.group_dict)
        return 
        
    #Toolset
    def qs(self, ls):
        if len(ls) <2:
            return ls
        pivot = ls[0]
        left = []
        right = []
        
        for i in ls[1:]:
            if float(i[5]) < float(pivot[5]):
                left.append(i)
            else:
                right.append(i)
        
        return self.qs(left) + [pivot] + self.qs(right)
    
    def calculate_means(self, group):
        total_gpa = 0
        total_female = 0
        max_repeat = 0

        schools = {}

        for student in group:
            total_gpa += float(student[5])
            if student[4] == "Female":
                total_female += 1
            if not schools.get(student[2]):
                schools[student[2]] = 1
            else:
                schools[student[2]] = schools[student[2]] + 1
        
        gpa_mean = total_gpa / len(group)
        female_ratio = total_female / len(group)
        max_repeat = max(schools.values())

        #Round the GPA to make it more readable.

        return [round(gpa_mean, 3), female_ratio, max_repeat, schools]
    

    def display_sorted_tut(self, unsorted, sorted):
        text = f"Without school swapping:\n"
        print(text)
        for i in range(10):
            group = unsorted[i][0]
            data = unsorted[i][1]
            print(f"Group: {i+1}, Group Data: {data[:4]}\n")
            for person in group:
                print(person)
            print("\n")
            
            
        text_2 = f"With school swapping: \n__________________________" 
        print(text_2)
        for i in range(10):
            group = sorted[i][0]
            data = sorted[i][1]
            print(f"Group: {i+1}, Group Data: {data[:4]}\n")
            for person in group:
                print(person)
            
            print("\n")
        
    
test = Sorter()
result = test.build_groups(test.data["G-10"])

