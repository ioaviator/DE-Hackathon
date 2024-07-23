# Data Engineering Hackathon

## Project Overview

This project integrates comprehensive country information from a public REST API to enhance travel destination recommendations for our customers at the travel agency. By leveraging detailed data on attributes such as language, continent, region, and currency, the system provides personalized and relevant travel suggestions.

### Objective

To integrate country information from a public REST API into the travel agency's data infrastructure. The data will be utilized to enhance customer travel destination recommendations based on various factors such as language, continent, region, currency, and more.

##  Project Architecture Overview
![](https://github.com/protechanalysis/DE-Hackathon/blob/main/pipeline_flow.png)

### Architecture Components

1. **Data Source:**
   - **REST API:** A public API providing comprehensive country information, including country name, language, continent, region, currency, and population.

2. **Data Extraction and Transformation:**
   - **Python Scripts:**
     - Extract data from the REST API.
     - Clean and normalize the data.
     - Transform the data into a structured format suitable for loading into DuckDB.
   - **Docker:**
     - Containerize the Python ETL scripts to ensure consistency, portability, and scalability across different environments.

3. **Data Storage:**
   - **DuckDB:**
     - Store the transformed data.
     - Utilize DuckDB for its efficient, high-performance analytical capabilities.

4. **Data Integration and Enhancement:**
   - **MotherDuck:**
     - Extend DuckDB with cloud storage, collaborative data processing, and enhanced scalability.
     - Serve as the intermediary layer to integrate DuckDB with analytics tools.

5. **Data Visualization and Analytics:**
   - **Power BI:**
     - Connect to MotherDuck to access up-to-date data.
     - Create interactive visualizations and reports.
     - Enable stakeholders to gain insights and make informed decisions based on the latest data.

## Docker Setup

### Build and Push Docker Image

1. **Script Overview:**
   This script builds and pushes a Docker image for DuckDB. It checks if the latest version of DuckDB is already available; if not, it builds and pushes the image.

2. **Script:**

   ```bash
   #!/usr/bin/env bash

   platforms="linux/amd64,linux/arm64"

   echo "Getting latest tag version from duckdb"
   duckdb_version=$(git -C build/duckdb describe --tags --abbrev=0)
   image_name=ogunseye/duckdb:"${duckdb_version}"

   if [ -z "$(DOCKER_CLI_EXPERIMENTAL=enabled docker manifest inspect "$image_name" 2> /dev/null)" ]; then
     echo "Building for duckdb version: ${duckdb_version}"

     docker run --privileged --rm tonistiigi/binfmt --install all
     docker buildx create --use --name builder
     docker buildx inspect --bootstrap builder

     docker buildx build \
       --platform "$platforms" \
       --build-arg "DUCKDB_VERSION=${duckdb_version}" \
       -t "$image_name" --push .

     echo "Done!"
   else
     echo "Latest duckdb image version already exists, version: ${duckdb_version}"
   fi

### Verify Data:

- Check the DuckDB instance to ensure the data has been correctly loaded and is accessible.

### Notes

- **DuckDB CLI:** DuckDB works as an in-process SQL OLAP database, meaning it can be used within the Docker container to process and analyze data without requiring a separate database server. The Docker setup ensures that DuckDB and all necessary scripts are packaged together, providing a consistent and isolated environment.

- **Non-Docker Usage:** While Docker provides an easy way to ensure consistency and portability, you can also run the Python ETL scripts and DuckDB locally. However, using Docker simplifies dependencies and environment management.

For more information on DuckDB and its usage, refer to the [DuckDB documentation](https://duckdb.org/docs/). For any issues or questions, please contact the project maintainers.
