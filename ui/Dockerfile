FROM node:13 as build
LABEL maintainer="kylie@unity3d.com"

ARG ENV

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN npm install && npm run build --fix

FROM nginx:1.15

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
