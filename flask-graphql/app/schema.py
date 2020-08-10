from graphene import ObjectType, Field, Schema, List, ID
from app.products.products_mutations import AddProduct, UpdateProduct, RemoveProduct
from app.products.types import Product
from app.products.products_queries import ProductQuery


class Query(
        ObjectType,
        ProductQuery
):
    product = Field(Product, id=ID(required=True))
    products = List(Product)


class Mutation(ObjectType):
    add_product = AddProduct.Field()
    update_product = UpdateProduct.Field()
    remove_product = RemoveProduct.Field()


schema = Schema(query=Query, mutation=Mutation)
