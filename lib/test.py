import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def plot_last_column_distribution(filepath):
    """
    Reads a CSV file, identifies the last column, and plots its distribution.

    Args:
        filepath (str): The path to the CSV file.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        print("Please make sure the file path is correct and the file exists.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    if df.empty:
        print("The CSV file is empty. Cannot plot distribution.")
        return

    # Get the name of the last column
    last_column_name = df.columns[-1]
    
    # Extract the data from the last column
    last_column_data = df[last_column_name]

    # Check if the data is numeric. If not, try to convert it.
    if not pd.api.types.is_numeric_dtype(last_column_data):
        print(f"The last column ('{last_column_name}') is not numeric. Attempting to convert...")
        try:
            # Try to convert to numeric, coercing errors to NaN (Not a Number)
            last_column_data = pd.to_numeric(last_column_data, errors='coerce')
            
            # Count how many values could not be converted
            nan_count = last_column_data.isna().sum()
            if nan_count > 0:
                print(f"Warning: {nan_count} non-numeric values were ignored in the column.")
                
            # Drop the NaN values for plotting
            last_column_data = last_column_data.dropna()
            
            if last_column_data.empty:
                print("After removing non-numeric values, the column is empty. Cannot plot.")
                return
                
        except Exception as e:
            print(f"Could not convert column '{last_column_name}' to numeric data. Error: {e}")
            return

    # --- Plotting ---
    
    # Set a nice style for the plot
    sns.set_theme(style="whitegrid")
    
    plt.figure(figsize=(10, 6))
    
    # Create the histogram (distribution plot)
    # 'kde=True' adds a smooth line (Kernel Density Estimate) over the bars
    sns.histplot(last_column_data, kde=True, bins=30)
    
    # Set titles and labels
    plt.title(f"Distribution of '{last_column_name}'", fontsize=16)
    plt.xlabel(last_column_name, fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    
    # Show the plot
    print(f"Displaying plot for column: {last_column_name}")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # --- How to use ---
    
    # 1. Make sure you have the required libraries:
    #    pip install pandas matplotlib seaborn
    
    # 2. Change this variable to the path of your CSV file
    FILE_PATH = os.path.join(os.getcwd(), "lib", "records.csv")  # <--- IMPORTANT: UPDATE THIS PATH

    # You can also pass the file path as an argument when running the script
    # Example: python plot_csv_distribution.py my_data.csv
    if len(sys.argv) > 1:
        FILE_PATH = sys.argv[1]
    elif FILE_PATH == "your_file.csv":
        print("Please update the 'FILE_PATH' variable in the script to point to your CSV file.")
        # We exit here so the user doesn't get an error for the default path
        sys.exit(0)

    plot_last_column_distribution(os.path.join(os.getcwd(), "lib", "records.csv"))