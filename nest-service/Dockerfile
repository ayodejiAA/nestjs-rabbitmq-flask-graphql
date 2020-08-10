FROM node:lts-buster-slim as development

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install --only=development; npm install --save-dev inherits

COPY . .

RUN npm run build


FROM node:lts-buster-slim as production

ENV NODE_ENV=production

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install --only=production

COPY . .

COPY --from=development /usr/src/app/dist ./dist
