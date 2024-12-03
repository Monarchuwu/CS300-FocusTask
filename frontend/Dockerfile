# frontend/Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the project files
COPY . .

# Expose the port
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]