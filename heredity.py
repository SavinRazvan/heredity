import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having a gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of the gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of the gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if the current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with a new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    The file is assumed to be a CSV containing fields name, mother, father, trait.
    Mother and father must both be blank, or both be valid names in the CSV.
    Trait should be 0 or 1 if the trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False
                    if row["trait"] == "0"
                    else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def check_genes(person, one_gene, two_genes):
    """
    Determine the number of gene copies for a person based on whether they are in the one_gene or two_genes sets.
    """
    if person in two_genes:
        return 2
    if person in one_gene:
        return 1
    else:
        return 0


def check_mutation(parent, one_gene, two_genes):
    """
    Calculate the probability of gene mutation for a given parent.

    For anyone with parents in the dataset, each parent will pass one of their two genes on to their child randomly,
    and there is a PROBS["mutation"] chance that it mutates (goes from being the gene to not being the gene, or vice versa).
    """
    # If the parent has two copies of the gene, the probability of passing the gene without mutation is (1 - PROBS["mutation"])
    if parent in two_genes:
        return 1 - PROBS["mutation"]
    # If the parent has one copy of the gene, the probability of passing the gene without mutation is 0.5
    elif parent in one_gene:
        return 0.5
    # If the parent has no copies of the gene, the probability of acquiring the gene through mutation is PROBS["mutation"]
    else:
        return PROBS["mutation"]


def check_trait(person, have_trait):
    """
    Check if a person has a trait based on whether they are in the have_trait set.
    If the person is in have_trait return True, otherwise False.
    """
    if person in have_trait:
        return True
    else:
        return False


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """
    joint_probability = 1

    # Iterate over each person in the dataset
    for person in people:
        person_probability = 1
        # Determine the number of gene copies and trait for the current person
        person_genes = check_genes(person, one_gene, two_genes)
        person_trait = check_trait(person, have_trait)
        mother = people[person]["mother"]
        father = people[person]["father"]

        # If the person has no parents in the dataset, calculate the probability based on unconditional gene probability
        if mother is None and father is None:
            person_probability *= PROBS["gene"][person_genes]

        # If the person has parents, calculate the probability based on gene inheritance rules
        else:
            mother_probability = check_mutation(mother, one_gene, two_genes)
            father_probability = check_mutation(father, one_gene, two_genes)

            # Calculate the probability based on the number of gene copies of the person and their parents' probabilities
            if person in two_genes:
                person_probability *= mother_probability * father_probability
            elif person in one_gene:
                person_probability *= (1 - mother_probability) * father_probability + mother_probability * (1 - father_probability)
            else:
                person_probability *= (1 - mother_probability) * (1 - father_probability)

        # Multiply the person's probability by the trait probability
        person_probability *= PROBS["trait"][person_genes][person_trait]

        # Multiply the joint probability by the person's probability
        joint_probability *= person_probability

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Iterate over each person in the probabilities dictionary
    for person in probabilities:
        person_genes = check_genes(person, one_gene, two_genes)
        person_trait = check_trait(person, have_trait)
        # Update the gene distribution with the joint probability
        probabilities[person]["gene"][person_genes] += p
        # Update the trait distribution with the joint probability
        probabilities[person]["trait"][person_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Iterate over each person in the probabilities dictionary
    for person in probabilities:
        # Calculate the sum of probabilities for the gene distribution
        gene_sum = sum(probabilities[person]["gene"].values())

        # Normalize the gene distribution by dividing each value by the sum
        for gene_val in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_val] /= gene_sum

        # Calculate the sum of probabilities for the trait distribution
        trait_sum = sum(probabilities[person]["trait"].values())

        # Normalize the trait distribution by dividing each value by the sum
        for trait_val in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait_val] /= trait_sum


if __name__ == "__main__":
    main()
