"""
Iterative Validation Script
Runs association rule mining 10 times on different datasets
and identifies valid rules based on specified criteria.
"""
import os
import pandas as pd
from collections import defaultdict
from generate_dataset import generate_binary_dataset
from association_mining import perform_association_mining

def run_iterative_validation(num_iterations=10, G=1000, M=20, k=14, 
                            min_support=0.05, output_file='valid_rules.csv'):
    """
    Run association rule mining multiple times and identify valid rules.
    
    Valid rules criteria:
    - Confidence in the last dataset > confidence in the first dataset
    - Appears in more than 6 of the 10 datasets
    
    Parameters:
    - num_iterations: number of iterations to run (default: 10)
    - G: number of rows in dataset (default: 1000)
    - M: number of columns in dataset (default: 20)
    - k: split point for probability rules (default: 14)
    - min_support: minimum support threshold (default: 0.05)
    - output_file: output file for valid rules (default: 'valid_rules.csv')
    """
    
    # Dictionary to track rules across iterations
    # Key: (antecedent, consequent), Value: list of (iteration, support, confidence)
    rules_tracker = defaultdict(list)
    
    print("="*80)
    print(f"Starting Iterative Validation: {num_iterations} iterations")
    print("="*80)
    
    for iteration in range(1, num_iterations + 1):
        print(f"\n{'='*80}")
        print(f"ITERATION {iteration}/{num_iterations}")
        print(f"{'='*80}")
        
        # Step 1: Generate new dataset
        print(f"\nStep 1: Generating dataset for iteration {iteration}...")
        dataset_file = f'input_iteration_{iteration}.csv'
        generate_binary_dataset(G=G, M=M, k=k, output_file=dataset_file)
        
        # Step 2: Perform association rule mining
        print(f"\nStep 2: Performing association rule mining...")
        rules_file = f'rules_iteration_{iteration}.txt'
        rules_df = perform_association_mining(
            input_file=dataset_file,
            output_file=rules_file,
            min_support=min_support,
            min_confidence=0.0
        )
        
        # Step 3: Track rules
        if len(rules_df) > 0:
            for _, row in rules_df.iterrows():
                rule_key = (row['Antecedent'], row['Consequent'])
                rules_tracker[rule_key].append({
                    'iteration': iteration,
                    'support': row['Support'],
                    'confidence': row['Confidence'],
                    'lift': row['Lift']
                })
            
            print(f"\nIteration {iteration}: Found {len(rules_df)} rules")
        else:
            print(f"\nIteration {iteration}: No rules found")
        
        # Keep the first dataset as input.csv for reference
        if iteration == 1:
            import shutil
            shutil.copy(dataset_file, 'input.csv')
            shutil.copy(rules_file, 'rule.txt')
    
    print(f"\n{'='*80}")
    print("IDENTIFYING VALID RULES")
    print(f"{'='*80}")
    
    # Identify valid rules
    valid_rules = []
    
    for rule_key, occurrences in rules_tracker.items():
        antecedent, consequent = rule_key
        count = len(occurrences)
        
        # Check if rule appears in more than 6 datasets
        if count > 6:
            # Get first and last occurrence
            first_occurrence = min(occurrences, key=lambda x: x['iteration'])
            last_occurrence = max(occurrences, key=lambda x: x['iteration'])
            
            initial_confidence = first_occurrence['confidence']
            final_confidence = last_occurrence['confidence']
            
            # Check if confidence improved
            if final_confidence > initial_confidence:
                valid_rules.append({
                    'Antecedent': antecedent,
                    'Consequent': consequent,
                    'Count': count,
                    'Initial_Confidence': initial_confidence,
                    'Final_Confidence': final_confidence,
                    'Confidence_Improvement': final_confidence - initial_confidence,
                    'Average_Support': sum(occ['support'] for occ in occurrences) / count,
                    'Average_Confidence': sum(occ['confidence'] for occ in occurrences) / count
                })
    
    # Create DataFrame and save
    if valid_rules:
        valid_rules_df = pd.DataFrame(valid_rules)
        valid_rules_df = valid_rules_df.sort_values('Confidence_Improvement', ascending=False)
        valid_rules_df.to_csv(output_file, index=False)
        
        print(f"\n{'='*80}")
        print(f"VALID RULES SUMMARY")
        print(f"{'='*80}")
        print(f"Total valid rules found: {len(valid_rules_df)}")
        print(f"Saved to: {output_file}")
        print(f"\n{valid_rules_df.to_string()}")
        
        # Display detailed statistics
        print(f"\n{'='*80}")
        print("VALIDATION STATISTICS")
        print(f"{'='*80}")
        print(f"Total unique rules across all iterations: {len(rules_tracker)}")
        print(f"Rules appearing in >6 datasets: {sum(1 for r in rules_tracker.values() if len(r) > 6)}")
        print(f"Valid rules (appeared >6 times AND confidence improved): {len(valid_rules_df)}")
        
        # Show distribution of rule occurrences
        occurrence_dist = defaultdict(int)
        for occurrences in rules_tracker.values():
            occurrence_dist[len(occurrences)] += 1
        
        print(f"\nRule occurrence distribution:")
        for count in sorted(occurrence_dist.keys()):
            print(f"  Appeared in {count} dataset(s): {occurrence_dist[count]} rule(s)")
        
    else:
        print(f"\nNo valid rules found that meet the criteria:")
        print("  - Appeared in more than 6 datasets")
        print("  - Confidence improved from first to last appearance")
        
        # Still save an empty file with headers
        valid_rules_df = pd.DataFrame(columns=[
            'Antecedent', 'Consequent', 'Count', 'Initial_Confidence', 
            'Final_Confidence', 'Confidence_Improvement', 'Average_Support', 'Average_Confidence'
        ])
        valid_rules_df.to_csv(output_file, index=False)
    
    print(f"\n{'='*80}")
    print("ITERATIVE VALIDATION COMPLETED")
    print(f"{'='*80}")
    
    return valid_rules_df

def cleanup_intermediate_files():
    """
    Optional: Clean up intermediate files from iterations.
    Keeps input.csv, rule.txt, and valid_rules.csv
    """
    import glob
    
    print("\nCleaning up intermediate files...")
    
    # Remove iteration-specific files
    for pattern in ['input_iteration_*.csv', 'rules_iteration_*.txt']:
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"  Removed: {file}")
            except Exception as e:
                print(f"  Error removing {file}: {e}")
    
    print("Cleanup completed.")

if __name__ == "__main__":
    # Run iterative validation with 10 iterations
    valid_rules_df = run_iterative_validation(
        num_iterations=10,
        G=1000,
        M=20,
        k=14,
        min_support=0.05,
        output_file='valid_rules.csv'
    )
    
    # Optional: Uncomment the line below to clean up intermediate files
    # cleanup_intermediate_files()
    
    print("\n" + "="*80)
    print("All tasks completed successfully!")
    print("="*80)
    print("\nGenerated files:")
    print("  - input.csv: First iteration dataset")
    print("  - rule.txt: First iteration rules")
    print("  - valid_rules.csv: Valid rules from all 10 iterations")
    print("  - input_iteration_*.csv: Datasets from each iteration")
    print("  - rules_iteration_*.txt: Rules from each iteration")
    print("="*80)
