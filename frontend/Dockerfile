# Use official Node.js image
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Install dependencies first (caching step)
COPY package.json package-lock.json ./
RUN npm install

# Copy all frontend source code
COPY . .

# Build React app for production
RUN npm run build

# Use a lightweight web server to serve the built app
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Default command to run nginx
CMD ["nginx", "-g", "daemon off;"]
