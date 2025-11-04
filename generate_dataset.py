"""
Dataset Generation Script
Generates a random binary dataset with specified probability rules.
"""
import numpy as np
import pandas as pd

def generate_binary_dataset(G=1000, M=20, k=14, output_file='input.csv'):
    """
    Generate a binary dataset with specified probability rules.
    
    Parameters:
    - G: number of rows (default: 1000)
    - M: number of columns (default: 20)
    - k: split point for probability rules (default: 14)
    - output_file: output CSV file name
    
    Probability rules:
    - Columns 1 to k (1-14): P(1) = 0.2, P(0) = 0.8
    - Columns k+1 to M (15-20): P(1) = 0.8, P(0) = 0.2
    """
    np.random.seed()  # Use random seed for different results each time
    
    # Initialize empty dataset
    dataset = np.zeros((G, M), dtype=int)
    
    # Fill columns 1 to k with probability 0.2 for value 1
    for col in range(k):
        dataset[:, col] = np.random.choice([0, 1], size=G, p=[0.8, 0.2])
    
    # Fill columns k+1 to M with probability 0.8 for value 1
    for col in range(k, M):
        dataset[:, col] = np.random.choice([0, 1], size=G, p=[0.2, 0.8])
    
    # Convert to DataFrame with column names
    column_names = [f'col_{i+1}' for i in range(M)]
    df = pd.DataFrame(dataset, columns=column_names)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Dataset generated successfully: {G} rows x {M} columns")
    print(f"Saved to: {output_file}")
    
    return df

if __name__ == "__main__":
    # Generate dataset with default parameters
    df = generate_binary_dataset()
    
    # Display sample statistics
    print("\n=== Dataset Statistics ===")
    print(f"Shape: {df.shape}")
    print(f"\nProportion of 1s in first {14} columns:")
    print(df.iloc[:, :14].sum().sum() / (df.shape[0] * 14))
    print(f"\nProportion of 1s in last {6} columns:")
    print(df.iloc[:, 14:].sum().sum() / (df.shape[0] * 6))
    print(f"\nFirst 5 rows:")
    print(df.head())
