# Heredity

This project involves creating an AI to assess the likelihood that a person will have a particular genetic trait based on their family's genetic information. The project uses a Bayesian Network to model the inheritance of a gene and the corresponding trait expression.

## Project Description

### Overview
The AI assesses the likelihood of genetic traits in individuals by using a Bayesian Network to analyze family data. The network accounts for genetic inheritance and mutations, allowing the AI to infer probabilities of gene presence and trait expression. The primary goal is to accurately model genetic inheritance patterns and predict the probability of traits appearing in family members.

### How It Works
1. **Data Input**: The program reads family genetic data from a CSV file.
2. **Probability Calculation**: It calculates the joint probability of various gene/trait combinations using the Bayesian Network, considering both genetic inheritance and mutation probabilities.
3. **Probability Update**: It updates the probability distributions for each person based on the joint probabilities.
4. **Normalization**: It normalizes these probabilities to ensure they sum to 1.
5. **Output**: The program outputs the probabilities of each person having 0, 1, or 2 copies of the gene and whether or not they exhibit the trait.

### Gene Values Explained
- **2**: The individual has two copies of the gene.
- **1**: The individual has one copy of the gene.
- **0**: The individual has no copies of the gene.

### Files
- **data/family0.csv**: Sample data file containing family genetic information.
- **data/family1.csv**: Sample data file containing family genetic information.
- **data/family2.csv**: Sample data file containing family genetic information.
- **heredity.py**: Main Python script to implement the AI.

### Key Functions Implemented
- **joint_probability**: Calculates the joint probability of a gene/trait distribution.
- **update**: Updates the probability distributions with a new joint probability.
- **normalize**: Normalizes the probabilities to sum to 1.

### Usage
```bash
python heredity.py data/family0.csv
```
```bash
python heredity.py data/family1.csv
```
```bash
python heredity.py data/family2.csv
```

### Example Output
```bash
python heredity.py data/family1.csv
Arthur:
  Gene:
    2: 0.0329
    1: 0.1035
    0: 0.8636
  Trait:
    True: 0.0000
    False: 1.0000
Charlie:
  Gene:
    2: 0.0018
    1: 0.1331
    0: 0.8651
  Trait:
    True: 0.0000
    False: 1.0000
Fred:
  Gene:
    2: 0.0065
    1: 0.6486
    0: 0.3449
  Trait:
    True: 1.0000
    False: 0.0000
Ginny:
  Gene:
    2: 0.0027
    1: 0.1805
    0: 0.8168
  Trait:
    True: 0.1110
    False: 0.8890
Molly:
  Gene:
    2: 0.0329
    1: 0.1035
    0: 0.8636
  Trait:
    True: 0.0000
    False: 1.0000
Ron:
  Gene:
    2: 0.0027
    1: 0.1805
    0: 0.8168
  Trait:
    True: 0.1110
    False: 0.8890
```
