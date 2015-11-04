import argparse
import json
import random
import math
import re

### Global Settings ###
random.seed(1)
THRESHOLD = 2.0


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
    :param float fraction: 0 <= fraction <= 1
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
                        u'manufacturer_tags': list(set(re.split(expr, entry[u'manufacturer'])))}
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
def matching_product_words(product_tags, listings_tags, threshold):
    """
    :param dict product_tags:
    :param dict listings_tags:
    :param float threshold: 0 < threshold <= 2
    :rtype: dict
    """
    matches = {}
    for index, product in enumerate(product_tags):
        name_tags = len(product[u'name_tags'])
        manufacturer_tags = len(product[u'manufacturer_tags'])
        for listing_index, listing in enumerate(listings_tags):
            score = 0.0
            for tag in listing[u'name_tags']:
                score += float(tag in product[u'name_tags']) / name_tags
            for tag in listing[u'manufacturer_tags']:
                score += float(tag in product[u'manufacturer_tags']) / manufacturer_tags
            if score >= threshold and index not in matches:
                matches[index] = [listing_index]
            elif score >= threshold:
                matches[index].append(listing_index)
    return matches


def associate_records(matches, products_data, listings_data):
    """
    :param dict matches:
    :param list products_data:
    :param list listings_data:
    :rtype: str
    """
    return '\n'.join([json.dumps({u'product_name': products_data[match][u'product_name'],
                                  u'listings': [listings_data[listings_match] for listings_match in matches[match]]})
                     for match in matches])


### Main ###
if __name__ == '__main__':
    # Argument Parsing #
    parser = argparse.ArgumentParser(description='Build linkages between products and listings')
    parser.add_argument('products', type=str, help='The text file containing products')
    parser.add_argument('listings', type=str, help='The text file containing listings')
    args = parser.parse_args()

    listings = import_json_file(args.listings)
    products = import_json_file(args.products)

    products_dict = parse_products(products)
    listings_dict = parse_listings(listings)

    product_listing_associations = matching_product_words(products_dict, listings_dict, THRESHOLD)
    with open('output.txt', 'w') as out_file:
        out_file.write(associate_records(product_listing_associations, products, listings))


