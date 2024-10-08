# Build the React frontend
FROM node:16-alpine AS frontend-build

# Set working directory
WORKDIR /app/frontend

# Install dependencies and build the frontend
COPY app/frontend/package.json app/frontend/yarn.lock ./
RUN yarn install
COPY app/frontend/ ./
RUN yarn build

# Build the FastAPI backend
FROM python:3.9-slim AS backend-build

# Set working directory
WORKDIR /app/backend

# Install backend dependencies
COPY app/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/backend/ .

# Copy built frontend to backend
COPY --from=frontend-build /app/frontend/dist /app/backend/static

# Expose ports for both FastAPI (8000) and the frontend (3000)
EXPOSE 8000

# Command to run both frontend and backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
