## Use Python 3

plain_pizza = 10.

toppings = ['pineapple', 'pepperoni', 'anchovies', 'olives']

def pizza_price(plain_pizza, toppings):
    for topping in toppings:
        if topping == 'pepperoni':
            plain_pizza += 2.
        else:
            plain_pizza += 1.
    return plain_pizza

plain_pizza = pizza_price(plain_pizza, toppings)

print("The pizza costs ${:.2f}".format(plain_pizza))
