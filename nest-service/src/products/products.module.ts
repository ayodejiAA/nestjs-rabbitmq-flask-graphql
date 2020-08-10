import { Module } from "@nestjs/common";
import { MongooseModule } from "@nestjs/mongoose";

import { ProductsController } from "./products.controller";
import { ProductSchema } from "./products.schema";

@Module({
  imports: [MongooseModule.forFeature([{ name: 'Product', schema: ProductSchema }])],
  controllers: [ProductsController]
})
export class ProductsModule { }
