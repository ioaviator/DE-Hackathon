<br />

## Back to main Repo. [Click Here](../README.md)

<br/>

## How many countries speaks French
## How many countries speaks english

```
SELECT language, 
  COUNT(country_name) AS speakers 
FROM countries_language_expand
GROUP BY language
  HAVING language IN ('English', 'French')

```
| language | speakers |
| -------- | -------- |
| English  | 91       |
| French   | 46       |

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
| countries_with_> one_official_language |
| -------------------------------------- |
| 96                                     |

<br />

## How many country official currency is Euro
```sql
SELECT currency_name, 
  COUNT(currency_name) AS 'number of users' 
FROM countries_tour_data
GROUP BY currency_name
  HAVING currency_name = 'Euro'

```
| currency_name | number of users |
| ------------- | --------------- |
| Euro          | 36              |

<br />

## Back to main Repo. [Click Here](../README.md)

<br />


## How many country is from West europe
```sql
SELECT  sub_region, 
  COUNT('country_name') AS 'number of countries' 
FROM countries_tour_data
GROUP BY sub_region
  HAVING sub_region = 'Western Europe'
```
| sub_region     | number of countries |
| -------------- | ------------------- |
| Western Europe | 8                   |
<br />

## How many country has not yet gain independence
```sql
SELECT independence, 
  COUNT(country_name) AS 'Total Number' 
FROM countries_tour_data
GROUP BY independence
ORDER BY "Total Number" DESC
```
| independence | Total Number |
| ------------ | ------------ |
| True         | 194          |
| False        | 55           |
| Unknown      | 1            |

<br />

## How many distinct continent and how many country from each
```sql
SELECT continents, 
  COUNT(country_name) AS Countries 
FROM countries_tour_data
GROUP BY continents
ORDER BY countries DESC
```
| continents    | countries |
| ------------- | --------- |
| Africa        | 58        |
| Europe        | 55        |
| Asia          | 50        |
| North America | 41        |
| Oceania       | 27        |
| South America | 14        |
| Antarctica    | 5         |

<br />

## How many country whose start of the week is not Monday
```sql
SELECT COUNT(country_name) AS Countries 
FROM countries_tour_data
WHERE startOfWeek <> 'monday'
```
| countries |
| --------- |
| 21        |

<br />

## How many countries are not a United Nation member
```sql
SELECT CASE WHEN united_nation_members THEN 'True' ELSE 'False' END AS united_nation_members, 
  COUNT(country_name) AS "number of countries" 
FROM countries_tour_data
GROUP BY united_nation_members

```
| united_nation_members | number of countries |
| --------------------- | ------------------- |
| False                 | 58                  |
| True                  | 192                 |


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
| continents    | country_name                                 | population |
| ------------- | -------------------------------------------- | ---------- |
| Africa        | Saint Helena, Ascension and Tristan da Cunha | 53192      |
| Africa        | Seychelles                                   | 98462      |
| Antarctica    | Heard Island and McDonald Islands            | 0          |
| Antarctica    | Bouvet Island                                | 0          |
| Asia          | Cocos (Keeling) Islands                      | 544        |
| Asia          | Christmas Island                             | 2072       |
| Europe        | Vatican City                                 | 451        |
| Europe        | Svalbard and Jan Mayen                       | 2562       |
| North America | Saint Barthélemy                             | 4255       |
| North America | Montserrat                                   | 4922       |
| Oceania       | Pitcairn Islands                             | 56         |
| Oceania       | United States Minor Outlying Islands         | 300        |
| South America | Falkland Islands                             | 2563       |
| South America | French Guiana                                | 254541     |

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
| continents    | country_name                        | area     |
| ------------- | ----------------------------------- | -------- |
| Africa        | Algeria                             | 2381741  |
| Africa        | DR Congo                            | 2344858  |
| Antarctica    | Antarctica                          | 14000000 |
| Antarctica    | French Southern and Antarctic Lands | 7747     |
| Asia          | China                               | 9706961  |
| Asia          | India                               | 3287590  |
| Europe        | Russia                              | 17098242 |
| Europe        | Turkey                              | 783562   |
| North America | Canada                              | 9984670  |
| North America | United States                       | 9372610  |
| Oceania       | Australia                           | 7692024  |
| Oceania       | Papua New Guinea                    | 462840   |
| South America | Brazil                              | 8515767  |
| South America | Argentina                           | 2780400  |
<br />

## Top 5 countries with the largest Area

```sql
SELECT continents, 
  country_name, area 
FROM countries_tour_data
ORDER BY Area DESC
LIMIT 5
```
| continents    | country_name  | area     |
| ------------- | ------------- | -------- |
| Europe        | Russia        | 17098242 |
| Antarctica    | Antarctica    | 14000000 |
| North America | Canada        | 9984670  |
| Asia          | China         | 9706961  |
| North America | United States | 9372610  |

<br />

## Top 5 countries with the lowest Area

```sql
SELECT continents, 
  country_name, area 
FROM countries_tour_data
ORDER BY area
LIMIT 5
```
| continents | country_name            | area |
| ---------- | ----------------------- | ---- |
| Europe     | Vatican City            | 0.44 |
| Europe     | Monaco                  | 2.02 |
| Europe     | Gibraltar               | 6    |
| Oceania    | Tokelau                 | 12   |
| Asia       | Cocos (Keeling) Islands | 14   |

<br />

## Back to main Repo. [Click Here](../README.md)