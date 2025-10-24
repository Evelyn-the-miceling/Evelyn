import pandas as pd

# Read the grouped data
df = pd.read_csv('zone_groups.csv')

# Group by tutorial group and gender
gender_groups = df.groupby(['tutorial_group', 'gender']).agg({
    'student_id': 'count',
    'zone': lambda x: list(x)
}).reset_index()

# Rename the count column
gender_groups = gender_groups.rename(columns={'student_id': 'count'})

# Save to a new CSV file
gender_groups.to_csv('gender_groups.csv', index=False)

# Display the results
print("Groups by gender created and saved to 'gender_groups.csv'")
print(gender_groups)