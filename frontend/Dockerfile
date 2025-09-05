FROM node:lts-alpine

# Set working directory
WORKDIR /app/frontend/

# Install pnpm globally
RUN npm install -g pnpm

# Copy package.json first for better caching
COPY package.json ./

# Install dependencies
RUN pnpm install

# Copy the rest of the source code
COPY . .

# Start development server
CMD ["pnpm", "run", "dev"]
