# Use Python as base image
FROM python:3.10

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Install Nginx
RUN apt update && apt install -y nginx

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Start both FastAPI and Nginx
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]

