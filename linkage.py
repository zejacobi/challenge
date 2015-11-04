import argparse
import json
import random
import math
import re

random.seed(1)


### Functions ###
# Import Functions #
def import_json_file(file_path):
    """
    :param str file_path:
    :rtype: list
    """
    with open(file_path) as file_obj:
        lines = file_obj.read().splitlines()
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


def parse_products(products_data):
    """
    :param list products_data:
    :rtype: list
    """
    product_tags = []
    expr = re.compile(r'[-_(),\s]+')
    for entry in products_data:
        name_tags = list(set(re.split(expr, entry[u'product_name'])))
        product_dict = {u'name_tags': None,
                        u'manufacturer_tags': list(set(re.split(r'[-_().,\s]+', entry[u'manufacturer'])))}
        if u'family' in entry.keys():
            name_tags.extend(list(set(re.split(expr, entry[u'family']))))
        if u'model' in entry.keys():
            name_tags.extend(list(set(re.split(expr, entry[u'model']))))
        name_tags = list(set(name_tags))
        product_dict[u'name_tags'] = name_tags
        product_tags.append(product_dict)
    return product_tags


def parse_listings(listings_data):
    """
    :param list products_data:
    :rtype: list
    """
    expr = re.compile(r'[-_(),\s]+')
    return [{u'name_tags': list(set(re.split(expr, entry[u'title']))),
             u'manufacturer_tags': list(set(re.split(expr, entry[u'manufacturer'])))}
            for entry in listings_data]


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

    print parse_listings(import_json_file(listings))[:100]