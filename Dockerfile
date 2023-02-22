FROM translate-base

# Set working directory
WORKDIR /app

# Copy application code to working directory
COPY . .

# Expose port 8000 for the application
EXPOSE 80
RUN pytest test_app.py -v

CMD ["python", "app.py"]