# Use Node.js official image as base
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all backend source files
COPY . .

# Expose the port your app listens on
EXPOSE 5000

# Start your backend app
CMD ["node", "server.js"]
