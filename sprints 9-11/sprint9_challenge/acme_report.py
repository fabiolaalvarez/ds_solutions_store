from acme import Product
import random

ADJECTIVES = ['Awesome', 'Shiny', 'Impressive', 'Portable', 'Improved']
NOUNS = ['Anvil', 'Catapult', 'Disguise', 'Mousetrap', 'Sword']

def generate_products(num_products: int = 30):
    product_list = []

    for num in range(0, num_products):
        product = Product(
            name=random.sample(ADJECTIVES, 1)[0] + " " + random.sample(NOUNS, 1)[0],
            price=random.randint(
                5,
                100),
            weight=random.randint(
                5,
                100),
            flammability=random.uniform(0.0, 2.5))
        product_list.append(product)
    return product_list


def inventory_report(product_list):
    uniq = len(set([product.name for product in product_list]))

    avg_price = sum([product.price for product in product_list]
                    ) / len(product_list)
    avg_weight = sum(
        [product.weight for product in product_list]) / len(product_list)
    avg_flammability = sum(
        [product.flammability for product in product_list]) / len(product_list)
    return tuple((uniq, avg_price, avg_weight, avg_flammability))


if __name__ == "__main__":
    product_list = generate_products()
    print(f'The product has been generated with {len(product_list)} items')
    print(inventory_report(product_list))
