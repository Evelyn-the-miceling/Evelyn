def Mean_of_CGPA(list): #Evaluate AVG CGPA of tutorial group
    sum = 0
    for element in list:
        sum += element
    mean = sum/len(list)
    return mean

def Check_range(list):
    mean = Mean_of_CGPA(list)
    dev = mean / 10
    while True:
        for i in range(50):
            if abs(list["G-1"][i]["cgpa"] - mean) <= dev: #Fix to fit with output of list
                return True
            else: 
                return False


