# Use a multi-stage build to combine frontend and backend

# Stage 1: Build frontend
FROM node:14 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build backend
FROM python:3.8-slim AS backend-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

# Stage 3: Combine frontend and backend
FROM python:3.8-slim
WORKDIR /app
COPY --from=backend-builder /app /app
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Ensure that the necessary environment variables are available
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
