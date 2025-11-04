# Association Rule Mining with Apache Spark

This project implements association rule mining using Apache Spark's FP-Growth algorithm with iterative validation across multiple datasets.

## 📋 Project Overview

The project consists of three main components:

1. **Dataset Generation**: Creates random binary datasets with controlled probability distributions
2. **Association Rule Mining**: Uses Apache Spark's FP-Growth to discover association rules
3. **Iterative Validation**: Runs 10 iterations to identify stable and improving rules

## 🎯 Requirements

### Dataset Specifications
- **G** = 1000 rows (transactions)
- **M** = 20 columns (items)
- **k** = 14 (split point for probability rules)

### Probability Rules
- Columns 1-14: P(value=1) = 0.2, P(value=0) = 0.8
- Columns 15-20: P(value=1) = 0.8, P(value=0) = 0.2

### Mining Parameters
- **Minimum Support**: 50 transactions (0.05 or 5%)
- **Algorithm**: FP-Growth (Frequent Pattern Growth)

### Valid Rule Criteria
A rule is considered valid if:
1. It appears in **more than 6 of the 10 datasets**
2. Its **confidence in the final dataset > confidence in the initial dataset**

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Java 8 or higher (required for PySpark)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pyspark==3.5.0 pandas==2.1.4 numpy==1.26.2
```

## 📁 Project Structure

```
bigDataSparkAss/
│
├── generate_dataset.py       # Dataset generation script
├── association_mining.py     # Spark FP-Growth implementation
├── iterative_validation.py   # Main validation script (10 iterations)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
└── Output files (generated after running):
    ├── input.csv             # First iteration dataset
    ├── rule.txt              # First iteration rules
    ├── valid_rules.csv       # Final valid rules
    ├── input_iteration_*.csv # Datasets from each iteration
    └── rules_iteration_*.txt # Rules from each iteration
```

## 💻 Usage

### Option 1: Run Complete Pipeline (Recommended)

Run all 10 iterations with a single command:

```bash
python iterative_validation.py
```

This will:
- Generate 10 different datasets
- Run association rule mining on each
- Identify and save valid rules to `valid_rules.csv`
- Display detailed statistics and results

### Option 2: Run Individual Steps

#### Step 1: Generate Dataset
```bash
python generate_dataset.py
```
Generates `input.csv` with 1000×20 binary data.

#### Step 2: Run Association Mining
```bash
python association_mining.py
```
Analyzes `input.csv` and saves rules to `rule.txt`.

## 📊 Output Files

### 1. `input.csv`
Binary dataset (1000 rows × 20 columns) from the first iteration.

Example:
```csv
col_1,col_2,col_3,...,col_20
0,1,0,...,1
1,0,0,...,1
...
```

### 2. `rule.txt`
Association rules from the first iteration with support, confidence, and lift values.

Example:
```
=== Association Rules ===

Rule 1:
  Antecedent: {col_15,col_16}
  Consequent: {col_17}
  Support: 0.0520
  Confidence: 0.8125
  Lift: 1.0156

...
```

### 3. `valid_rules.csv`
Valid rules meeting both criteria (appeared >6 times AND confidence improved).

Columns:
- `Antecedent`: Items in the rule antecedent
- `Consequent`: Items in the rule consequent
- `Count`: Number of times rule appeared (out of 10)
- `Initial_Confidence`: Confidence in first appearance
- `Final_Confidence`: Confidence in last appearance
- `Confidence_Improvement`: Final - Initial confidence
- `Average_Support`: Mean support across appearances
- `Average_Confidence`: Mean confidence across appearances

## 🔍 Understanding the Results

### Support
The proportion of transactions that contain the itemset.
```
Support(X) = Count(X) / Total Transactions
```

### Confidence
The likelihood that consequent appears given antecedent appears.
```
Confidence(X → Y) = Support(X ∪ Y) / Support(X)
```

### Lift
Measures how much more likely Y is given X compared to Y alone.
```
Lift(X → Y) = Confidence(X → Y) / Support(Y)
```
- Lift > 1: Positive correlation
- Lift = 1: Independence
- Lift < 1: Negative correlation

## 🧪 Algorithm Details

### FP-Growth Algorithm
FP-Growth (Frequent Pattern Growth) is an efficient algorithm for mining frequent patterns without candidate generation.

**Advantages:**
- Only two database scans
- No candidate generation
- Compressed data structure (FP-tree)
- Faster than Apriori for large datasets

**Steps:**
1. Scan database to find frequent 1-itemsets
2. Build FP-tree
3. Mine frequent patterns from FP-tree
4. Generate association rules from frequent patterns

## 📈 Expected Results

Given the probability distribution:
- **High support/confidence rules**: Likely involve columns 15-20 (high probability of 1)
- **Lower support rules**: May involve columns 1-14 (low probability of 1)
- **Valid rules**: Should show consistent patterns across iterations with improving confidence

## 🔧 Customization

You can modify parameters in `iterative_validation.py`:

```python
valid_rules_df = run_iterative_validation(
    num_iterations=10,    # Number of iterations
    G=1000,              # Number of rows
    M=20,                # Number of columns
    k=14,                # Probability split point
    min_support=0.05,    # Minimum support (5%)
    output_file='valid_rules.csv'
)
```

## 🧹 Cleanup

To remove intermediate files (optional), uncomment the cleanup line in `iterative_validation.py`:

```python
cleanup_intermediate_files()
```

This keeps only:
- `input.csv`
- `rule.txt`
- `valid_rules.csv`

## ⚠️ Troubleshooting

### Java Not Found
If you get "JAVA_HOME is not set" error:
```bash
# macOS/Linux
export JAVA_HOME=$(/usr/libexec/java_home)

# Or install Java
brew install openjdk@11
```

### Memory Issues
If Spark runs out of memory, increase driver memory in `association_mining.py`:
```python
.config("spark.driver.memory", "8g")  # Increase from 4g to 8g
```

### No Rules Found
If no rules are generated:
- Try lowering `min_support` (e.g., 0.03 or 0.01)
- Check dataset generation - ensure proper probability distribution
- Verify data format (binary values 0 and 1)

## 📚 References

- [Apache Spark MLlib - FPGrowth](https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html)
- [FP-Growth Algorithm Paper](https://doi.org/10.1145/335191.335372)
- [Association Rule Learning](https://en.wikipedia.org/wiki/Association_rule_learning)

## 📝 License

This project is for educational purposes.

## 👥 Author

Created for Big Data Analytics Assignment

---

**Note**: This implementation uses Apache Spark in local mode. For production use with large datasets, consider deploying on a Spark cluster.
