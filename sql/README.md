<br />

## To go back to main Repo. [Click Here](../README.md)

<br/>

## How many countries speaks French
## How many countries speaks english

```sql
SELECT language, 
  COUNT(country_name) AS speakers 
FROM countries_language_expand
GROUP BY language
  HAVING language IN ('English', 'French')

```
<br />

## How many country have more than 1 official language
```sql
WITH countries_with_more_language AS (
  SELECT 
    country_name, 
    COUNT(language) AS number_of_spoken_language 
  FROM countries_language_expand
  GROUP BY country_name
    HAVING number_of_spoken_language > 1
  ORDER BY number_of_spoken_language 
)	

SELECT COUNT(country_name) AS 'countries_with_> 1_official_language'
FROM countries_with_more_language

```

<br />

## How many country official currency is Euro
```sql
SELECT currency_name, 
  COUNT(currency_name) AS 'number of users' 
FROM countries_tour_data
GROUP BY currency_name
  HAVING currency_name = 'Euro'

```

<br />

## How many country is from West europe
```sql
SELECT  sub_region, 
  COUNT('country_name') AS 'number of countries' 
FROM countries_tour_data
GROUP BY sub_region
  HAVING sub_region = 'Western Europe'
```

<br />

## How many country has not yet gain independence
```sql
SELECT independence, 
  COUNT(country_name) AS 'Total Number' 
FROM countries_tour_data
GROUP BY independence
ORDER BY "Total Number" DESC
```

<br />

## How many distinct continent and how many country from each
```sql
SELECT continents, 
  COUNT(country_name) AS Countries 
FROM countries_tour_data
GROUP BY continents
ORDER BY countries DESC
```

<br />

## How many country whose start of the week is not Monday
```sql
SELECT COUNT(country_name) AS Countries 
FROM countries_tour_data
WHERE startOfWeek <> 'monday'
```

<br />

## How many countries are not a United Nation member
```sql
SELECT CASE WHEN united_nation_members THEN 'True' ELSE 'False' END AS united_nation_members, 
  COUNT(country_name) AS "number of countries" 
FROM countries_tour_data
GROUP BY united_nation_members

```
<br />

## Least 2 countries with the lowest population for each continents

```sql
WITH ranked_population AS (
  SELECT continents, 
    country_name, 
    population, 
    ROW_NUMBER() OVER(PARTITION BY continents ORDER BY population ) AS rnk 
  FROM countries_tour_data
)

SELECT continents, 
  country_name, 
  population 
FROM ranked_population
WHERE rnk <= 2
```

<br />

## Top 2 countries with the largest Area for each continent

```sql
WITH ranked_country_area AS (
  SELECT continents, 
    country_name, 
    area, 
    ROW_NUMBER() OVER(PARTITION BY continents ORDER BY area DESC) AS rnk 
  FROM countries_tour_data
)

SELECT Continents, 
  country_name, 
  area 
FROM ranked_country_area
WHERE rnk < 3
```
<br />

## Top 5 countries with the largest Area

```sql
SELECT continents, 
  country_name, area 
FROM countries_tour_data
ORDER BY Area DESC
LIMIT 5
```

## Top 5 countries with the lowest Area

```sql
SELECT continents, 
  country_name, area 
FROM countries_tour_data
ORDER BY area
LIMIT 5
```

<br />

## To go back to main Repo. [Click Here](../README.md)