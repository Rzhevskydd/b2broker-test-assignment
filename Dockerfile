# Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy project
COPY . /app/

# Run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
