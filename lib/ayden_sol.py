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
                
    
    def group_presets(self, group):
        gpa_total = 0
        female_total = 0
        
        males = []
        females = []
        
        for person in group:
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

        print("Mouse", len(presets))
        for i in presets:
            print("Brae")
            for j in i:
                print(j)


            

 
        return 
        
        
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
        

        
    
test = Sorter()
result = test.group_presets(test.data["G-1"])

