#!/usr/bin/env python3
"""
Quick Start Runner
Executes the complete association rule mining pipeline.
"""

import sys
import os

def main():
    """
    Main runner function that executes the iterative validation.
    """
    print("="*80)
    print("ASSOCIATION RULE MINING WITH APACHE SPARK")
    print("Iterative Validation Pipeline")
    print("="*80)
    print()
    print("This script will:")
    print("  1. Generate 10 random binary datasets (1000×20)")
    print("  2. Run FP-Growth association mining on each")
    print("  3. Identify valid rules based on:")
    print("     - Appeared in >6 datasets")
    print("     - Confidence improved from first to last appearance")
    print()
    print("Expected runtime: 2-5 minutes")
    print("="*80)
    print()
    
    # Import and run
    try:
        from iterative_validation import run_iterative_validation
        
        # Run the complete validation
        valid_rules_df = run_iterative_validation(
            num_iterations=10,
            G=1000,
            M=20,
            k=14,
            min_support=0.05,
            output_file='valid_rules.csv'
        )
        
        print("\n" + "="*80)
        print("✅ SUCCESS!")
        print("="*80)
        print("\nGenerated files:")
        print("  📄 input.csv - First iteration dataset")
        print("  📄 rule.txt - First iteration association rules")
        print("  📄 valid_rules.csv - Valid rules across all 10 iterations")
        print("  📄 input_iteration_*.csv - Individual iteration datasets")
        print("  📄 rules_iteration_*.txt - Individual iteration rules")
        print("\n" + "="*80)
        
        return 0
        
    except ImportError as e:
        print(f"❌ ERROR: Missing dependencies")
        print(f"   {e}")
        print("\nPlease install required packages:")
        print("   pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
