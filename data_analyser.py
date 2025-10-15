# File: data_analyzer.py
import pandas as pd
import matplotlib.pyplot as plt

def analyze_data(csv_path="sample_data.csv", output_image="analysis_plot.png"):
    """Reads a CSV file, calculates basic stats, and creates a plot."""
    try:
        # Read the data from the CSV file using pandas
        df = pd.read_csv(csv_path)
        
        print("--- Data Analysis ---")
        print("First 5 rows of the data:")
        print(df.head())
        
        print("\nBasic Statistics:")
        # describe() gives stats like mean, min, max, etc.
        print(df.describe())

        # Create a simple plot
        # This example assumes the CSV has 'Year' and 'Rainfall_mm' columns
        df.plot(kind='bar', x='Year', y='Rainfall_mm', title='Annual Rainfall Analysis')
        
        # Save the plot to an image file
        plt.savefig(output_image)
        
        print(f"\nAnalysis complete. Plot saved to '{output_image}'")

    except FileNotFoundError:
        print(f"Error: The file '{csv_path}' was not found.")
    except KeyError as e:
        print(f"Error: The CSV file is missing a required column: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_data()