#MergeSort algorithm with different criterias:

def Sorting_criteria(student_a, student_b): 
    #Criterias considered: CGPA, Gender, School
    if student_a["cgpa"] != student_b["cgpa"]:
        return student_a["cgpa"] > student_b["cgpa"] #CGPA is sorted from high to low
    elif student_a["gender"] != student_b["gender"]:
        return student_a["gender"] < student_b["gender"] #Gender is Female then Male
    elif student_a["school"] != student_b["school"]:
        return student_a["school"] < student_b["school"] #Alphabetical order   

def MergeSort(a_list):
    if len(a_list) < 2:
        return a_list
    else:
        a_left_list = a_list[:len(a_list) // 2]
        a_right_list = a_list[len(a_list) // 2:]

        a_left_list = MergeSort(a_left_list)
        a_right_list = MergeSort(a_right_list)

        a_sorted_list = []
        i = j = 0
        while i < len(a_left_list) and j < len(a_right_list):
            if Sorting_criteria(a_left_list[i], a_right_list[j]):
                a_sorted_list.append(a_left_list[i])
                i += 1
            else:
                a_sorted_list.append(a_right_list[j])
                j += 1
        else:
            a_sorted_list.extend(a_left_list[i:])
            a_sorted_list.extend(a_right_list[j:])

        return a_sorted_list
    
#Time Complexity: O(nlogn)
#Space Complexity: O(n + logn) = O(n)