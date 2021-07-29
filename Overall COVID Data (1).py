#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandasql')
import pandas as pd
import pandasql as psql
import numpy as np


# In[2]:


deaths = pd.read_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/28Jul2021Deaths.csv',header=0)
vax = pd.read_csv('/Users/benkelly/Downloads/Projects/COVID Overview/Data/28Jul2021Vax.csv',header=0)


# In[3]:


#DeathPercent show's likelihood of dying if you contract COVID in each country 
#Overall at a certain snap shot, does not highlight changes overtime

deathPercent =  psql.sqldf("SELECT location, date,total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercent FROM deaths WHERE continent IS NOT NULL ORDER BY 1,2")
deathPercent


# In[23]:


#Countries with proportionally highest infection rates
infPercent =  psql.sqldf("SELECT location,population,max(total_cases) AS highestCount, max((total_cases/population))*100 AS proportionalPercent FROM deaths WHERE continent IS NOT NULL GROUP BY location, population ORDER BY proportionalPercent DESC")
infPercent.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/3 Infection Percent.xlsx')


# In[24]:


#Countries with proportionally highest infection rates by Date
infPercentDate =  psql.sqldf("SELECT location,population,date,max(total_cases) AS highestCount, max((total_cases/population))*100 AS proportionalPercent FROM deaths WHERE continent IS NOT NULL GROUP BY location, population, date ORDER BY proportionalPercent DESC")
infPercentDate.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/4 Infection Percent Dates.xlsx')


# In[27]:


#Proportional death rates
propDeath =  psql.sqldf("SELECT location, max(total_deaths) AS deathCount, max((total_deaths/population))*100 AS propDeathPercent FROM deaths WHERE continent IS NOT NULL GROUP BY location, population  ORDER BY propDeathPercent DESC")
propDeath


# In[32]:


#Proportional deaths by continent
propDeathContinent =  psql.sqldf("SELECT location, max(total_deaths) AS deathCount, max((total_deaths/population))*100 AS propDeathPercent FROM deaths WHERE continent IS NULL GROUP BY location ORDER BY propDeathPercent DESC")
propDeathContinent


# In[27]:


#Global Numbers
globalDeaths =  psql.sqldf("SELECT SUM(new_cases) AS total_cases ,SUM(new_deaths) AS total_deaths, (SUM(new_deaths)/SUM(new_cases))*100 as DeathPercentage FROM deaths WHERE continent IS NOT NULL ORDER BY 1,2")
globalDeaths.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/1 Global Deaths.xlsx')


# In[55]:


# Vaccinations by population

#Use CTE
popVax=psql.sqldf("WITH PopvsVax (Continent, Location, Date, Population,New_Vaccinations, RollingVaxCount) AS (SELECT deaths.continent,deaths.location,deaths.date,deaths.population, vax.new_vaccinations, SUM(vax.new_vaccinations) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS rollingVaxCount FROM deaths JOIN vax ON deaths.location=vax.location and deaths.date=vax.date WHERE deaths.continent IS NOT NULL) SELECT *,(RollingVaxCount/Population)*100 AS RollingVaxPercent FROM PopvsVax")
popVax


# In[60]:


popVax.dtypes


# In[64]:


# Example of a temp table if pandasql if CREATE TABLE functioned normally
# I beleive the issues arise with setting the data types
popVax=psql.sqldf("DROP TABLE IF EXISTS #PercentVax CREATE TABLE #PercentVax (Continent nvarchar(255), Location nvarchar(255), Date datetime, Population numeric, New_Vaccinations numeric, RollingVaxCount numeric) INSERT INTO #PercentVax SELECT deaths.continent,deaths.location,deaths.date,deaths.population, vax.new_vaccinations, SUM(vax.new_vaccinations) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS rollingVaxCount FROM deaths JOIN vax ON deaths.location=vax.location and deaths.date=vax.date WHERE deaths.continent IS NOT NULL SELECT *,(RollingVaxCount/Population)*100 AS RollingVaxPercent FROM #PercentVax")


# In[67]:


#Creating View for later visualizations
#Saving it to a variable would be the pandasql version of these views. 
view=psql.sqldf('CREATE VIEW PercentPopVaxxed AS SELECT deaths.continent,deaths.location,deaths.date,deaths.population, vax.new_vaccinations, SUM(vax.new_vaccinations) OVER (PARTITION BY deaths.location ORDER BY deaths.location, deaths.date) AS rollingVaxCount FROM deaths JOIN vax ON deaths.location=vax.location and deaths.date=vax.date WHERE deaths.continent IS NOT NULL')
view


# In[12]:


#Total Deaths
tdeaths=psql.sqldf('SELECT location, SUM(new_deaths) as TotalDeathCount FROM deaths WHERE continent IS NULL GROUP BY location ORDER BY TotalDeathCount desc')
tdeaths.to_excel('/Users/benkelly/Downloads/Projects/COVID Overview/Data/2 Death Totals.xlsx')

