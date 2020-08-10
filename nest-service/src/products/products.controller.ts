import { Controller } from "@nestjs/common";
import { InjectModel } from "@nestjs/mongoose";
import { MessagePattern, RpcException } from '@nestjs/microservices';
import { Model } from 'mongoose'

import { Product } from './products.interface';


@Controller()
export class ProductsController {
  constructor(
    @InjectModel('Product') private readonly ProductModel: Model<Product>
  ) { }

  @MessagePattern('add')
  async insertProduct(product: Product) {
    const newProduct = new this.ProductModel({ 
      title:product.title, 
      desc:product.desc, 
      price: product.price })
    const  { id, title, desc, price } = await newProduct.save()
    return { id, title, desc, price } as Product;
  }

  @MessagePattern({ cmd: 'retrieve-products' })
  async retrieveProducts() {
    const products = await this.ProductModel.find().exec()
    return products
      .map(({ id, title, desc, price }) =>
        ({ id, title, desc, price })) as Array<Product>;
  }

  @MessagePattern('get-product')
  async retrieveProduct(productId: string) {
    const product = await this.findProduct(productId)
    const { id, title, desc, price } = product
    return { id, title, desc, price } as Product;
  }

  @MessagePattern('update-product')
  async updateProduct({ id, title, desc, price }: Product) {
    const updatedProduct = await this.findProduct(id);
    if (title) updatedProduct.title = title;
    if (desc) updatedProduct.desc = desc;
    if (price) updatedProduct.price = price;
    await updatedProduct.save()
    return true
  }

  @MessagePattern('remove-product')
  async removeProduct(productId: string): Promise<boolean> {
    try {
      const result = await this.ProductModel.deleteOne({ _id: productId }).exec()
      if (result.n === 0) throw new RpcException('Product not found')
      return true
    } catch (error) {
      throw new RpcException('Product not found')
    }
  }

  @MessagePattern('ping')
  async ping() {
    console.log("Ping!");
    return 'ping'
  }

  private async findProduct(productId: string): Promise<Product> {
    try {
      const product = await this.ProductModel.findById(productId)
      if (!product) throw new RpcException('Product not found')
      return product;
    } catch (error) {
      throw new RpcException('Product not found')
    }
  }
}


