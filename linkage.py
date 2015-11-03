import argparse
import json
import random
import math

random.seed(1)


### Functions ###
# Import Functions #
def import_json_file(file_path):
    """
    :param str file_path:
    :rtype: list
    """
    with open(file_path) as file_obj:
        lines = file_obj.read().split('\n')
        return [json.loads(line) for line in lines]


def cross_validation_sets(dataset, fraction):
    """
    :param list dataset:
    :param float fraction: 0<=float<=1
    :rtype: tuple
    """
    num_recs = int(math.floor(fraction * len(dataset)))
    dataset = dataset[:]
    random.shuffle(dataset)
    train = dataset[:num_recs]
    test = dataset[num_recs:]
    return train, test

# Analysis Functions #

### Main ###
if __name__ == '__main__':
    # Argument Parsing #
    parser = argparse.ArgumentParser(description='Build linkages between products and listings')
    parser.add_argument('products', type=str, help='The text file containing products')
    parser.add_argument('listings', type=str, help='The text file containing listings')
    args = parser.parse_args()

    listings = args.listings
    products = args.products