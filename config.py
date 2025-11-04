# Configuration File for Association Rule Mining Project

# ============================================================================
# DATASET PARAMETERS
# ============================================================================

# Number of rows (transactions) in the dataset
NUM_ROWS = 1000

# Number of columns (items) in the dataset
NUM_COLUMNS = 20

# Split point for probability rules
# Columns 1 to K: P(1) = 0.2
# Columns K+1 to M: P(1) = 0.8
PROBABILITY_SPLIT = 14

# Probability of value 1 in first K columns
LOW_PROBABILITY = 0.2

# Probability of value 1 in remaining columns
HIGH_PROBABILITY = 0.8

# ============================================================================
# MINING PARAMETERS
# ============================================================================

# Minimum support threshold (as proportion)
# 0.05 means 50 out of 1000 transactions
MIN_SUPPORT = 0.05

# Minimum confidence threshold (0.0 to 1.0)
# 0.0 means all rules are kept
MIN_CONFIDENCE = 0.0

# Spark driver memory allocation
SPARK_DRIVER_MEMORY = "4g"

# ============================================================================
# VALIDATION PARAMETERS
# ============================================================================

# Number of iterations for validation
NUM_ITERATIONS = 10

# Minimum number of datasets a rule must appear in to be considered valid
# Must be > this value (so 6 means appear in 7, 8, 9, or 10 datasets)
MIN_OCCURRENCE_THRESHOLD = 6

# ============================================================================
# OUTPUT FILES
# ============================================================================

# Dataset file for first iteration
OUTPUT_DATASET = "input.csv"

# Rules file for first iteration
OUTPUT_RULES = "rule.txt"

# Valid rules from all iterations
OUTPUT_VALID_RULES = "valid_rules.csv"

# Prefix for iteration-specific files
ITERATION_DATASET_PREFIX = "input_iteration_"
ITERATION_RULES_PREFIX = "rules_iteration_"

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

# Clean up intermediate files after completion
CLEANUP_INTERMEDIATE_FILES = False

# Display detailed progress information
VERBOSE_OUTPUT = True

# Random seed for reproducibility (None for random each time)
RANDOM_SEED = None

# Number of sample rows to display
NUM_SAMPLE_ROWS = 5

# Number of top rules to display by confidence
NUM_TOP_RULES = 10

# ============================================================================
# NOTES
# ============================================================================
#
# To use this configuration:
# 1. Modify the values above as needed
# 2. Import in your scripts:
#    from config import NUM_ROWS, MIN_SUPPORT, etc.
#
# Recommended values:
# - MIN_SUPPORT: 0.03 to 0.10 (lower = more rules, but potentially less meaningful)
# - NUM_ITERATIONS: 10 to 20 (more iterations = better validation, but slower)
# - MIN_OCCURRENCE_THRESHOLD: 50-70% of iterations (e.g., 5 for 10 iterations)
#
# ============================================================================
