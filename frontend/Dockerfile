# Use the official lightweight Node.js 14 image
# https://hub.docker.com/_/node
FROM node:14 AS build

# Create and change to the app directory
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY frontend/package*.json ./

# Install production dependencies.
RUN npm install

# Copy local code to the container image
COPY frontend/ ./

# Build the app
RUN npm run build

# Use official Nginx image as the base image
# https://hub.docker.com/_/nginx
FROM nginx:alpine

# Copy built app to Nginx html directory
COPY --from=build /usr/src/app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
