import { Document } from 'mongoose';

export class Product extends Document {
  id: string
  title: string
  desc: string
  price: number
}
