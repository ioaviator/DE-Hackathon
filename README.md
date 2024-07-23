#  DATA ENGINEERING HACKATHON


##  Project Overview

This project aims to integrate comprehensive country information from a public REST API to enhance travel destination recommendations for our customers at the travel agency. The focus is on leveraging detailed data on countries' attributes such as language, continent, region, and currency to provide personalized and relevant travel suggestions.


###  Objective:

This project aims to integrate country information from a public REST API into the travel agency's data infrastructure. This data will be utilized to enhance customer travel destination recommendations based on various factors such as language, continent, region, currency, and more.

##  Project Architecture Overview
![pipeline_flow](https://github.com/protechanalysis/DE-Hackathon/blob/main/pipeline_flow.png)

###  Architecture Components:

###  Data Source: [Here](https://restcountries.com/v3.1/all)

- REST API: A public API providing comprehensive country information (e.g., country name, language, continent, region, currency, population).

###  Data Extraction and Transformation:

- Python Scripts:
    - Extract data from the REST API.
    - Clean and normalize the data.
    - Transform the data into a structured format suitable for loading into DuckDB.
      
- Docker: Containerize the Python ETL scripts to ensure consistency, portability, and scalability across different environments.

####  Data Storage:

- DuckDB:
    - Store the transformed data.
    - Utilize DuckDB for its efficient, high-performance analytical capabilities.

### Data Integration and Enhancement:

-  MotherDuck:
    -  Extend DuckDB with cloud storage, collaborative data processing, and enhanced scalability.
    -  Serve as the intermediary layer to integrate DuckDB with analytics tools.


###  Data Visualization and Analytics:

-  Power BI:
    -  Connect to MotherDuck to access up-to-date data.
    -  Create interactive visualizations and reports.
    -  Enable stakeholders to gain insights and make informed decisions based on the latest data.


## Analysis and Insights
### For Analysis Using SQL Code, [Click Here](./sql/README.md)

### Power BI Data Visualization Link [Click Here](https://app.powerbi.com/view?r=eyJrIjoiZDU1NTcxZGMtOTAxMC00MTgwLWFkYTctYTU0YmQyZmE4OGRhIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9)
