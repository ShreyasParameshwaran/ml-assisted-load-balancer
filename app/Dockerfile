FROM node:22.5.1-alpine
WORKDIR /app
COPY package.json ./
RUN npm i
COPY index.js /app/
EXPOSE 8080
CMD ["node" , "index.js"]

