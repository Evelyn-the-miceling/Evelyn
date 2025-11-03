import csv
import os

class Sorter:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "lib", "records.csv")
        self.data = {}
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

        #Snake method cool idea
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
        
        for i in range(len(new_groups)):
            group_dict[i] = (new_groups[i], self.calculate_means(new_groups[i]))
             
        print(group_dict)
                    
        






            

 
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


        return gpa_mean, female_ratio, max_repeat



        
    
test = Sorter()
result = test.build_groups(test.data["G-1"])

