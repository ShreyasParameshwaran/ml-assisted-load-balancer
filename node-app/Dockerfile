FROM node:14.17.0-alpine
WORKDIR /app
ADD package*.json ./
RUN npm install
ADD index.js ./
ADD index.html ./
EXPOSE 4000
CMD [ "node", "index.js"]