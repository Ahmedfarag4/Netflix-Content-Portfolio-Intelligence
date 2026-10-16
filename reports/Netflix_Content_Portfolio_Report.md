# Netflix Content Portfolio Intelligence
## Executive Analytical Report

## 1. Executive Summary

This project analyzes a historical Netflix catalog dataset to understand content composition, market distribution, audience segments, genres, historical trends, and content characteristics.

The raw dataset contained 8,790 records. After data quality checks and business-level duplicate removal, the final cleaned dataset contained 8,787 unique content records.

The analysis shows that Movies dominate the catalog, accounting for approximately 69.7% of titles, while TV Shows represent approximately 30.3%.

The United States is the largest represented market in the dataset, while content strategy differs significantly across countries. Some markets are strongly Movie-oriented, while others are dominated by TV Shows.

Audience analysis indicates that Mature and Teen-oriented content represent the largest portions of the catalog.

Genre patterns also vary significantly between Movies and TV Shows. Movies are strongly represented by International Movies, Dramas, and Comedies, while TV Shows show broader representation across TV Dramas, TV Comedies, Crime TV Shows, Kids' TV, and International TV Shows.

The project also identified that approximately 63% of titles were added to Netflix within two years of release, indicating a strong concentration of relatively recent content while maintaining a meaningful long-tail of older titles.

---

## 2. Project Objective

The objective of this project is to transform raw Netflix catalog metadata into a structured analytical product that supports portfolio-level content analysis.

The analysis focuses on:

- Content composition
- Geographic market distribution
- Historical content trends
- Audience segmentation
- Genre structure
- Movie duration
- TV Show season distribution
- Content age
- Cross-market audience differences

---

## 3. Dataset Overview

The raw dataset contains:

- 8,790 records
- 10 original columns

Main fields include:

- show_id
- type
- title
- director
- country
- date_added
- release_year
- rating
- duration
- listed_in

The dataset covers:

- Release years from 1925 to 2021
- Netflix addition years from 2008 to 2021

This is a historical dataset and should not be interpreted as representing the current Netflix catalog.

---

## 4. Data Quality Assessment

Initial null-value checks showed no technical missing values.

However, deeper semantic inspection identified missing information stored as text:

- 2,588 director values represented as "Not Given"
- 287 country values represented as "Not Given"

Duplicate analysis identified:

- 0 exact duplicate rows
- 6 rows representing 3 duplicated content records with different show_id values

After removing business duplicates:

- Final cleaned records: 8,787

The cleaning process also included:

- Datetime conversion
- Duration parsing
- Semantic missing-value handling
- Genre extraction
- Feature engineering
- Final validation

---

## 5. Feature Engineering

The following analytical features were created:

- year_added
- month_added
- duration_value
- duration_unit
- content_age_at_addition
- content_age_valid
- director_clean
- country_clean
- audience_group
- content_age_group

A separate exploded genre dataset was created to support accurate genre-level analysis.

---

## 6. Content Portfolio Overview

The cleaned catalog contains:

- 6,124 Movies
- 2,663 TV Shows

This means:

- Movies: approximately 69.7%
- TV Shows: approximately 30.3%

The catalog is therefore strongly Movie-oriented overall.

---

## 7. Geographic Market Analysis

The largest represented markets are:

1. United States
2. India
3. United Kingdom
4. Pakistan
5. Canada
6. Japan
7. South Korea
8. France
9. Spain
10. Mexico

The United States is the dominant market by title count.

However, the content mix differs significantly across markets.

Examples:

- India is strongly Movie-oriented
- Pakistan is strongly TV Show-oriented
- South Korea is strongly TV Show-oriented
- Japan also has a majority TV Show mix
- The United States remains predominantly Movie-oriented

This indicates that catalog composition is not uniform across markets.

---

## 8. Historical Trend Analysis

The number of titles in the dataset increases significantly in more recent release years.

Movie growth is especially strong from the 2010s onward.

TV Shows also increase substantially in more recent years, though Movies remain the larger category overall.

A decline is visible in the final years of the dataset.

This decline should be interpreted cautiously because the dataset ends in 2021 and may not represent a complete observation period for the most recent years.

---

## 9. Audience Analysis

Content ratings were grouped into analytical audience segments:

- Kids
- Family
- Teens & Family
- Teens
- Mature
- Unrated

The largest audience segments are:

1. Mature
2. Teens
3. Teens & Family
4. Kids
5. Family
6. Unrated

Mature content is the largest segment overall.

The audience group classification was created for analytical purposes and is not an official Netflix audience segmentation system.

---

## 10. Genre Analysis

The most represented genres include:

- International Movies
- Dramas
- Comedies
- International TV Shows
- Documentaries
- Action & Adventure

Movie genres are dominated by:

- International Movies
- Dramas
- Comedies

TV Show genres show broader representation across:

- International TV Shows
- TV Dramas
- TV Comedies
- Crime TV Shows
- Kids' TV

This suggests that genre structure differs significantly between Movies and TV Shows.

---

## 11. Movie Duration Analysis

Average Movie duration:

- Approximately 99.6 minutes

Median Movie duration:

- 98 minutes

Most Movies cluster around typical feature-film lengths.

A small number of very short and very long titles create outliers.

---

## 12. TV Show Season Analysis

Average TV Show length:

- Approximately 1.75 seasons

Median:

- 1 season

Most TV Shows contain one or two seasons.

This indicates that the catalog contains a large number of relatively short TV series.

---

## 13. Content Age Analysis

Content age measures the number of years between release and Netflix addition.

The distribution is:

- Same Year: 36.90%
- 1–2 Years: 26.17%
- 3–5 Years: 12.73%
- 6–10 Years: 10.46%
- 10+ Years: 13.74%

Approximately 63% of titles were added to Netflix within two years of release.

This suggests that the catalog is strongly concentrated around relatively recent content while still maintaining a meaningful long-tail of older titles.

---

## 14. Market Audience Mix

Audience composition differs significantly across major markets.

Examples include:

- Spain has a strong Mature-content concentration
- Mexico is also heavily Mature-oriented
- India has a strong Teen-content concentration
- Pakistan has a relatively higher Kids share compared with many other major markets
- Japan and South Korea show a more balanced split between Mature and Teen content

These differences indicate that market-level catalog composition varies substantially.

---

## 15. Interactive Dashboard

The Streamlit dashboard provides:

- Executive KPI cards
- Content-type analysis
- Market distribution
- Movies vs TV Shows by market
- Historical trends
- Audience analysis
- Genre analysis
- Movie duration analysis
- TV Show season analysis
- Content age analysis
- Market audience heatmap
- Dynamic business insights
- Interactive filtering
- Filtered data exploration
- CSV download

Dashboard filters include:

- Content Type
- Country
- Audience Group
- Release Year

All major KPIs and analytical views update dynamically based on selected filters.

---

## 16. Business Interpretation

The analysis suggests that Netflix's catalog structure, as represented in this historical dataset, is highly segmented by market, audience type, genre, and content format.

Key strategic observations include:

- Movies dominate the catalog overall
- Market content strategies vary significantly
- Mature and Teen-oriented content represent the largest audience segments
- TV Shows show stronger concentration in recent-release content
- Different markets exhibit distinct audience and content-format profiles
- Genre composition differs substantially between Movies and TV Shows

These findings can support content portfolio analysis and market-level content planning.

---

## 17. Limitations

This analysis is based only on catalog metadata.

The dataset does not contain:

- Viewing behavior
- Watch time
- Revenue
- Subscriber counts
- Completion rates
- Content cost
- Licensing cost
- User demographics
- Recommendation data

Therefore, the project can analyze catalog structure and content strategy patterns, but it cannot directly measure:

- Content performance
- Viewer preference
- Profitability
- User engagement
- Commercial success

---

## 18. Conclusion

This project transforms raw Netflix catalog metadata into a structured analytical product combining data cleaning, exploratory analysis, business interpretation, and interactive dashboarding.

The final result provides a portfolio-level view of Netflix content across markets, audience groups, genres, time periods, and content formats.

The project demonstrates an end-to-end data analysis workflow from raw data preparation to interactive business intelligence.