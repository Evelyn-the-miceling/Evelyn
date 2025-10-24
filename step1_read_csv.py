# test
# read file
def main():
    with open("records.csv", "r", encoding = "utf-8") as file:
        #read header
        header = file.readline()#.strip()
        print("Header:", header)

        #read sample rows
        for i in range(5):
            sample = file.readline().strip()
            print(f"{i+1}. ", sample)

#main()
