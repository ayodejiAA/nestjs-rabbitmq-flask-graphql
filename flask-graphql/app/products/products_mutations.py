from graphene import Mutation, String, Boolean
from app.products.types import ProductInput, Product, UpdateProductInput
from app.config import client


class AddProduct(Mutation):
    class Arguments:
        data = ProductInput(required=True)

    Output = Product

    def mutate(root, info, data=None):
        newProduct = client.send('add', data)
        return Product(
            title=newProduct['title'],
            desc=newProduct['desc'],
            price=newProduct["price"],
            id=newProduct["id"])


class UpdateProduct(Mutation):
    class Arguments:
        id = String(required=True)
        data = UpdateProductInput(required=True)

    Output = Boolean

    def mutate(root, info, id, data=None):
        data['id'] = id
        result = client.send("update-product", data)
        return result


class RemoveProduct(Mutation):
    class Arguments:
        id = String(required=True)

    Output = Boolean

    def mutate(root, info, id):
        result = client.send("remove-product", id)
        return result
