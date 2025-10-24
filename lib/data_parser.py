import random
import csv  
import os


class Group_Sorter:
    def __init__(self):
        self.file_path = os.path.join(os.getcwd(), "lib/records.csv")
        self.tutorial_groups = {}


        #Cleaning up data
        self.parse_data()
        self.clean_data()

    def parse_data(self):
        

        with open(self.file_path, "r") as file:
            csv_reader = csv.reader(file)
            
            fields = next(csv_reader)

            rows = []

            for row in csv_reader:
                rows.append(row)
        parsed_data = {}


        for record in rows:
            if parsed_data.get(record[0]):
                parsed_data[record[0]].append(record)
            else:
                parsed_data[record[0]] = [record]

        self.tutorial_groups = parsed_data

    def clean_data(self):
        non_stem = ["CoB (NBS)", "NIE", "ADM", "SoH", "SSS", "ASE"]
        for group_key in self.tutorial_groups.keys():
            group = self.tutorial_groups.get(group_key)

            for student in group:
                if student[2] in non_stem:
                    
                    student[2], student[5] = "NS",float(student[5])
            
                else:
                    student[2], student[5] = "S",float(student[5])

    def determine_group_means(self, tutorial_group):

        group = self.tutorial_groups.get(tutorial_group)
        
        GPA_total = 0
        F_total = 0
        M_total = 0
        S_school = 0
        NS_school = 0

        for person in group:
            GPA_total += person[5]

            if person[4] == "Female":
                F_total += 1
            else:
                M_total += 1
            
            if person[2] == "S":
                S_school += 1
            else:
                NS_school += 1

        GPA_mean = GPA_total / len(group)
        F_M_ratio = F_total / len(group) 
        S_NS_ratio = S_school / len(group) 

        return GPA_mean, F_M_ratio, S_NS_ratio
    
    def reshuffle_group(self, group_list):
        return random.shuffle(group_list)
    
    def sort_small_group(self, tutorial_group):
        GPA_mean, F_M_ratio, S_NS_ratio = self.determine_group_means(tutorial_group)

        tutorial_group_list = self.retrieve_tut_group(tutorial_group)

        group = list(range(1, 50))
        while True:
            groups = self.reshuffle_group(group)
            
            curr_group = groups[:5]

            for number in curr_group:






        




    #Accessor
    def retrieve_tut_group(self, key):
        return(self.tutorial_groups.get(key))
    





        
DataParser = Group_Sorter()

print(DataParser.determine_group_means("G-10"))

