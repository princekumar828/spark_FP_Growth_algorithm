"""
Association Rule Mining using Apache Spark
Performs FP-Growth algorithm on binary dataset to find association rules.
"""
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth
from pyspark.sql.functions import col, size, split
import pandas as pd

def load_and_convert_to_transactions(input_file='input.csv'):
    """
    Load CSV file and convert binary data to transaction format.
    Each row becomes a list of column names where value = 1.
    
    Parameters:
    - input_file: path to input CSV file
    
    Returns:
    - DataFrame with 'items' column containing transaction lists
    """
    # Read CSV using pandas first
    df_pandas = pd.read_csv(input_file)
    
    # Convert each row to transaction format
    transactions = []
    for idx, row in df_pandas.iterrows():
        # Get column names where value is 1
        items = [col_name for col_name, val in row.items() if val == 1]
        transactions.append((idx, items))
    
    return transactions

def perform_association_mining(input_file='input.csv', output_file='rule.txt', 
                               min_support=0.05, min_confidence=0.0):
    """
    Perform association rule mining using FP-Growth algorithm.
    
    Parameters:
    - input_file: path to input CSV file
    - output_file: path to output rules file
    - min_support: minimum support threshold (default: 0.05)
    - min_confidence: minimum confidence threshold (default: 0.0)
    
    Returns:
    - DataFrame containing association rules with support and confidence
    """
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("AssociationRuleMining") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    
    # Suppress Spark logs
    spark.sparkContext.setLogLevel("ERROR")
    
    try:
        # Load and convert to transactions
        print(f"Loading dataset from {input_file}...")
        transactions = load_and_convert_to_transactions(input_file)
        
        # Create Spark DataFrame
        df_spark = spark.createDataFrame(transactions, ["id", "items"])
        
        print(f"Total transactions: {df_spark.count()}")
        print(f"Sample transactions:")
        df_spark.show(5, truncate=False)
        
        # Apply FP-Growth algorithm
        print(f"\nApplying FP-Growth with min_support={min_support}...")
        fpGrowth = FPGrowth(itemsCol="items", minSupport=min_support, minConfidence=min_confidence)
        model = fpGrowth.fit(df_spark)
        
        # Get frequent itemsets
        freq_itemsets = model.freqItemsets
        print(f"\nFrequent itemsets found: {freq_itemsets.count()}")
        
        # Get association rules
        rules = model.associationRules
        print(f"Association rules found: {rules.count()}")
        
        # Convert to Pandas for easier manipulation
        rules_pandas = rules.toPandas()
        
        if len(rules_pandas) > 0:
            # Convert lists to strings for better readability
            rules_pandas['antecedent'] = rules_pandas['antecedent'].apply(lambda x: ','.join(sorted(x)))
            rules_pandas['consequent'] = rules_pandas['consequent'].apply(lambda x: ','.join(sorted(x)))
            
            # Rename columns for clarity
            rules_pandas = rules_pandas.rename(columns={
                'antecedent': 'Antecedent',
                'consequent': 'Consequent',
                'confidence': 'Confidence',
                'lift': 'Lift',
                'support': 'Support'
            })
            
            # Save to file
            with open(output_file, 'w') as f:
                f.write("=== Association Rules ===\n\n")
                for idx, row in rules_pandas.iterrows():
                    f.write(f"Rule {idx + 1}:\n")
                    f.write(f"  Antecedent: {{{row['Antecedent']}}}\n")
                    f.write(f"  Consequent: {{{row['Consequent']}}}\n")
                    f.write(f"  Support: {row['Support']:.4f}\n")
                    f.write(f"  Confidence: {row['Confidence']:.4f}\n")
                    f.write(f"  Lift: {row['Lift']:.4f}\n")
                    f.write("\n")
            
            print(f"\nRules saved to {output_file}")
            
            # Display summary statistics
            print("\n=== Rules Summary ===")
            print(f"Total rules: {len(rules_pandas)}")
            print(f"Average confidence: {rules_pandas['Confidence'].mean():.4f}")
            print(f"Average support: {rules_pandas['Support'].mean():.4f}")
            print(f"\nTop 10 rules by confidence:")
            print(rules_pandas.nlargest(10, 'Confidence')[['Antecedent', 'Consequent', 'Support', 'Confidence']])
        else:
            print("No association rules found with the given parameters.")
            rules_pandas = pd.DataFrame(columns=['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift'])
        
        return rules_pandas
        
    finally:
        # Stop Spark session
        spark.stop()

if __name__ == "__main__":
    # Perform association mining with default parameters
    # Minimum support = 50 transactions out of 1000 = 0.05
    rules = perform_association_mining(
        input_file='input.csv',
        output_file='rule.txt',
        min_support=0.05,
        min_confidence=0.0
    )
    
    print(f"\n{'='*60}")
    print("Association rule mining completed successfully!")
    print(f"{'='*60}")
