# Based on python 3.11 image
FROM python:3.11.10-alpine3.20

# Set the working directory
WORKDIR /home/app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]