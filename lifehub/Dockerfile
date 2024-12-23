FROM python:3

WORKDIR /app

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 3000

# Command to run the application
CMD [ "python", "app.py" ]
RUN pip install --no-cache-dir -r requirements.txt
