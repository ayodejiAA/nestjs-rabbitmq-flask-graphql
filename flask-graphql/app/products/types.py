from graphene import ObjectType, String, NonNull, Int, ID, InputObjectType


class Product(ObjectType):
    id = ID(required=True)
    title = NonNull(String)
    desc = NonNull(String)
    price = NonNull(String)


class ProductInput(InputObjectType):
    title = NonNull(String)
    desc = NonNull(String)
    price = NonNull(Int)


class UpdateProductInput(InputObjectType):
    title = String()
    desc = String()
    price = Int()
