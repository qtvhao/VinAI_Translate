FROM translate-base

# Set working directory
WORKDIR /app

# Copy requirements file to working directory
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to working directory
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Set entrypoint to run the application
ENTRYPOINT ["python", "app.py"]
