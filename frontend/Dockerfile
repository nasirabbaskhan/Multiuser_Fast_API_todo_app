# Use a specific Node.js version for consistency
FROM node:latest

# Set the working directory
WORKDIR /code

# Copy all fileas except .dockerignore file into ./code
COPY . /code/


RUN npm install

# RUN npm run build

EXPOSE 3000

ENTRYPOINT ["npm", "run", "dev"]