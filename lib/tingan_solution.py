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

            # for student in group:
            #     if student[2] in non_stem:
                    
            #         student[2], student[5] = "NS",float(student[5])
            
            #     else:
            #         student[2], student[5] = "S",float(student[5])
            
            for student in group:
                student[5] = float(student[5])
                
class Node:
    def __init__(self, name):
        self.child = []
        self.name = None
        self.content = []
        self.bucket = {}
        

class TaTree:
    def __init__(self):
        self.root = None
        
    def calculate_percentiles(self, ls):
        ls = self.qs(ls)
        
        first = ls[:10]
        second = ls[10:20]
        third = ls[20:30]
        fourth = ls[30:40]
        fifth = ls[40:50]
        
        return first, second, third, fourth, fifth
        
    def insert_person(self, person):
        gender = person[4]
        gpa = float(person[5])
        
        
        
        curr_node = self.root
        curr_node = curr_node.bucket[gender]
        curr_node = curr_node.bucket[]
            
            
    def build_tree(self):
        self.add_gender("Male")
        self.add_gender("Female")
                    
        
    def add_genders(self, name):
        if not self.root:
            self.root = Node("Start")
        else:
            self.root.bucket[name] = Node(name)
            
        for gender in self.root.bucket:
            self.add_gpa(gender)
            
    def add_gpa(self, node):
        for i in range(1,5):
            node.bucket[str(i)] = Node(i)
        
    def qs(self, ls):
        pivot = ls[0]
        left = []
        right = []
        for i in ls[1:]:
            if i < pivot:
                left.append(i)
            else:
                right.append(i)
        
        return left + [pivot] + right
        
        