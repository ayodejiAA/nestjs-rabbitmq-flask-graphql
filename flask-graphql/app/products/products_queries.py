from app.config import client

class ProductQuery:
    def resolve_product(root, info, id):
        product = client.send('get-product', id)
        return product

    def resolve_products(root, info):
        products = client.send({ "cmd": 'retrieve-products' })
        return products
