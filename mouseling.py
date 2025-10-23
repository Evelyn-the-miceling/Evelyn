print("I am a cute mouse!")

for i in range(5):
    print("Squeak!")    


def nibble():
    print("Nibbling on some cheese!")

while True:
    decision = input("Do you want to nibble? (yes/no): ").strip().lower()
    if decision == 'yes':
        nibble()
    elif decision == 'no':
        print("Okay, maybe later!")
        break
