# Use a base image with Python installed
FROM python:3.9-slim

# Install DuckDB CLI
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl -L -o duckdb_cli.zip "https://github.com/duckdb/duckdb/releases/download/v0.5.0/duckdb_cli-linux-amd64.zip" && \
    unzip duckdb_cli.zip && \
    rm duckdb_cli.zip && \
    mv duckdb /usr/local/bin/duckdb

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY api_ingestion.py .

# Install any Python dependencies if needed
# RUN pip install some_package

# Command to run the DuckDB CLI
CMD ["duckdb", "/data/countries_tour_data.duckdb"]
