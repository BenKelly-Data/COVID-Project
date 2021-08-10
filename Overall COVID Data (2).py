#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandasql')
import pandas as pd
import pandasql as psql
import numpy as np


# In[3]:


deaths = pd.read_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/28Jul2021Deaths.csv',header=0)
vax = pd.read_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/28Jul2021Vax.csv',header=0)


# In[4]:


#DeathPercent show's likelihood of dying if you contract COVID in each country 
#Overall at a certain snap shot, does not highlight changes overtime
query="""
SELECT location, date,total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercent 
FROM deaths 
WHERE continent IS NOT NULL 
ORDER BY 1,2"""
deathPercent =  psql.sqldf(query)
deathPercent


# In[8]:


#Countries with proportionally highest infection rates
query="""
SELECT location,population,max(total_cases) AS highestCount, max((total_cases/population))*100 AS proportionalPercent 
FROM deaths 
WHERE continent IS NOT NULL 
GROUP BY location, population 
ORDER BY proportionalPercent DESC
"""
infPercent =  psql.sqldf(query)
infPercent.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/3 Infection Percent.xlsx')


# In[7]:


#Countries with proportionally highest infection rates by Date
query="""
SELECT location,population,date,max(total_cases) AS highestCount, 
       max((total_cases/population))*100 AS proportionalPercent 
FROM deaths 
WHERE continent IS NOT NULL 
GROUP BY location, population, date 
ORDER BY proportionalPercent DESC
"""
infPercentDate =  psql.sqldf(query)
infPercentDate.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/4 Infection Percent Dates.xlsx')


# In[6]:


#Proportional death rates
query="""
SELECT location, max(total_deaths) AS deathCount, max((total_deaths/population))*100 AS propDeathPercent 
FROM deaths 
WHERE continent IS NOT NULL 
GROUP BY location, population 
ORDER BY propDeathPercent DESC
"""
propDeath =  psql.sqldf(query)
propDeath


# In[32]:


#Proportional deaths by continent
query="""
SELECT location, max(total_deaths) AS deathCount, max((total_deaths/population))*100 AS propDeathPercent 
FROM deaths 
WHERE continent IS NULL 
GROUP BY location 
ORDER BY propDeathPercent DESC
"""
propDeathContinent =  psql.sqldf(query)
propDeathContinent


# In[27]:


#Global Numbers
query="""
SELECT SUM(new_cases) AS total_cases ,SUM(new_deaths) AS total_deaths, 
       (SUM(new_deaths)/SUM(new_cases))*100 as DeathPercentage 
FROM deaths 
WHERE continent IS NOT NULL 
ORDER BY 1,2
"""
globalDeaths =  psql.sqldf(query)
globalDeaths.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/1 Global Deaths.xlsx')


# In[9]:


# Vaccinations by population

#Use CTE
query="""
WITH PopvsVax (Continent, Location, Date, Population,New_Vaccinations, RollingVaxCount) 
    AS (SELECT deaths.continent,deaths.location,deaths.date,deaths.population, 
    vax.new_vaccinations, SUM(vax.new_vaccinations) 
        OVER (PARTITION BY deaths.location 
              ORDER BY deaths.location, deaths.date) AS rollingVaxCount 
    FROM deaths 
    JOIN vax ON deaths.location=vax.location and deaths.date=vax.date 
    WHERE deaths.continent IS NOT NULL) 
SELECT *,(RollingVaxCount/Population)*100 AS RollingVaxPercent 
FROM PopvsVax
"""
popVax=psql.sqldf(query)
popVax


# In[13]:


#Creating View for later visualizations
#Saving it to a variable would be the pandasql version of these views. 
query="""
CREATE VIEW PercentPopVaxxed AS 
SELECT deaths.continent,deaths.location,deaths.date,deaths.population, vax.new_vaccinations, 
        SUM(vax.new_vaccinations) 
            OVER (PARTITION BY deaths.location 
                  ORDER BY deaths.location, deaths.date) AS rollingVaxCount 
FROM deaths 
JOIN vax ON deaths.location=vax.location and deaths.date=vax.date 
WHERE deaths.continent IS NOT NULL
"""
view=psql.sqldf(query)
view


# In[14]:


#Total Deaths
query="""
SELECT location, SUM(new_deaths) as TotalDeathCount FROM deaths 
WHERE continent IS NULL 
GROUP BY location 
ORDER BY TotalDeathCount DESC
"""
tdeaths=psql.sqldf(query)
tdeaths.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/2 Death Totals.xlsx')


# In[15]:


# Example of a temp table if pandasql if CREATE TABLE functioned normally
# I beleive the issues arise with setting the data types
query="""
CREATE TABLE PercentVax (Continent nvarchar(255), Location nvarchar(255), Date datetime, 
                        Population numeric, New_Vaccinations numeric, RollingVaxCount numeric) 
INSERT INTO PercentVax 
    SELECT deaths.continent,deaths.location,deaths.date,deaths.population, vax.new_vaccinations, 
        SUM(vax.new_vaccinations) 
            OVER (PARTITION BY deaths.location 
                  ORDER BY deaths.location, deaths.date) AS rollingVaxCount 
        FROM deaths 
        JOIN vax ON deaths.location=vax.location and deaths.date=vax.date 
        WHERE deaths.continent IS NOT NULL 

SELECT *,(RollingVaxCount/Population)*100 AS RollingVaxPercent FROM #PercentVax
"""
#popVax=psql.sqldf(query)

