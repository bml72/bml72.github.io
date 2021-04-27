# Benjamin Lee
# Professor Nima Zahadat
# DATS 6401-10: Visualization of Complex Data
# Due: 28 April 2021

# ======================================================================================================================
# Importing all necessary libraries.

from os import path
import numpy as np
import pandas as pd

# ======================================================================================================================
# Reading in the appropriate files.

base_path = path.dirname(__file__)

file_path = path.abspath(path.join(base_path, '../..', 'data'))

infection_data = pd.read_csv(file_path + '/raw/owid-covid-data.csv', header=0)

vaccination_data = pd.read_csv(file_path + '/raw/country_vaccinations.csv', header=0)

# ======================================================================================================================
# Deleting all data for countries that appear in "infection_data" but not "vaccination_data", and vice-versa.

infection_data = infection_data[infection_data['location'].isin(vaccination_data['country'])]

vaccination_data = vaccination_data[vaccination_data['country'].isin(infection_data['location'])]

# ======================================================================================================================
# Deleting all irrelevant columns of data.

infection_data = infection_data.drop(columns=['iso_code', 'new_cases', 'new_cases_smoothed', 'new_deaths',
                                              'new_deaths_smoothed', 'total_cases_per_million', 'new_cases_per_million',
                                              'new_cases_smoothed_per_million', 'total_deaths_per_million',
                                              'new_deaths_per_million', 'new_deaths_smoothed_per_million',
                                              'reproduction_rate', 'icu_patients', 'icu_patients_per_million',
                                              'hosp_patients', 'hosp_patients_per_million', 'weekly_icu_admissions',
                                              'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
                                              'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
                                              'total_tests_per_thousand', 'new_tests_per_thousand',
                                              'new_tests_smoothed', 'new_tests_smoothed_per_thousand', 'positive_rate',
                                              'tests_per_case', 'tests_units', 'total_vaccinations',
                                              'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
                                              'new_vaccinations_smoothed', 'total_vaccinations_per_hundred',
                                              'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
                                              'new_vaccinations_smoothed_per_million'])

vaccination_data = vaccination_data.drop(columns=['people_vaccinated', 'daily_vaccinations_raw',
                                                  'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
                                                  'people_fully_vaccinated_per_hundred',
                                                  'daily_vaccinations_per_million', 'source_name', 'source_website'])

# ======================================================================================================================
# Other pre-processing measures.

# Converting the "date" column to a DateTime variable. This helps when sequestering data for certain time periods.
infection_data['date'] = pd.to_datetime(infection_data['date'])

vaccination_data['date'] = pd.to_datetime(vaccination_data['date'])

# Pulling all unique country names into a list. This is useful for pulling data and creating new DataFrames.
infection_countries = infection_data['location'].unique().tolist()

vaccination_countries = vaccination_data['country'].unique().tolist()

# ======================================================================================================================
# Creating dataframes for specific visualizations.

# Total cases and deaths by country (as of 23 April 2021).
raw_total_cases_and_deaths = []

for country in infection_countries:
    data = [infection_data[infection_data['location'] == country]['location'].iloc[-1],
            infection_data[infection_data['location'] == country]['total_cases'].iloc[-1],
            infection_data[infection_data['location'] == country]['total_deaths'].iloc[-1]]

    raw_total_cases_and_deaths.append(data)

raw_total_cases_and_deaths_df = pd.DataFrame(raw_total_cases_and_deaths, columns=['country', 'total_cases', 'total_deaths'])

raw_total_cases_and_deaths_df = raw_total_cases_and_deaths_df.sort_values(by='total_deaths', ascending=False)

raw_total_cases_and_deaths_df = raw_total_cases_and_deaths_df.fillna(0)

raw_total_cases_and_deaths_top_ten_df = raw_total_cases_and_deaths_df.head(10)
# ======================================================================================================================
# Retrieving average of demographic and health-related factors for the top ten countries in terms of raw total deaths.

raw_top_ten_countries_deaths = ['United States', 'Brazil', 'Mexico', 'India', 'United Kingdom', 'Italy', 'Russia',
                                'France', 'Germany', 'Spain']

raw_top_ten_averages = infection_data[infection_data['location'].isin(raw_top_ten_countries_deaths)].reset_index(drop=True)

raw_top_ten_averages = raw_top_ten_averages.groupby(['location']).mean()

raw_top_ten_averages = raw_top_ten_averages.sort_values(by='total_deaths', ascending=False)

raw_top_ten_averages = raw_top_ten_averages.drop(columns=['total_cases', 'total_deaths'])

# ======================================================================================================================
# Computing the total cases and deaths in proportion to population.

prop_total_cases_and_deaths = []

for country in infection_countries:
    data = [infection_data[infection_data['location'] == country]['location'].iloc[-1],
            infection_data[infection_data['location'] == country]['total_cases'].iloc[-1],
            infection_data[infection_data['location'] == country]['total_deaths'].iloc[-1],
            infection_data[infection_data['location'] == country]['population'].iloc[-1]]

    prop_total_cases_and_deaths.append(data)

prop_total_cases_and_deaths_df = pd.DataFrame(prop_total_cases_and_deaths,
                                              columns=['country', 'total_cases', 'total_deaths', 'population'])

prop_total_cases_and_deaths_df['proportionate_total_cases'] = prop_total_cases_and_deaths_df['total_cases'] / \
                                                              prop_total_cases_and_deaths_df['population']

prop_total_cases_and_deaths_df['proportionate_total_deaths'] = prop_total_cases_and_deaths_df['total_deaths'] / \
                                                               prop_total_cases_and_deaths_df['population']

prop_total_cases_df = prop_total_cases_and_deaths_df.sort_values(by='proportionate_total_cases', ascending=False)

prop_total_cases_df = prop_total_cases_df.head(10)

prop_total_cases_df = prop_total_cases_df.drop(columns='proportionate_total_deaths')

prop_total_deaths_df = prop_total_cases_and_deaths_df.sort_values(by='proportionate_total_deaths', ascending=False)

prop_total_deaths_df = prop_total_deaths_df.head(10)

prop_total_deaths_df = prop_total_deaths_df.drop(columns='proportionate_total_cases')

# ======================================================================================================================
# Retrieving average of demographic and health-related factors for the top ten countries in terms of proportionate total
# cases and deaths.

prop_cases_top_ten_countries = ['Andorra', 'Montenegro', 'Czechia', 'San Marino', 'Slovenia', 'Luxembourg', 'Serbia',
                                'Bahrain', 'Israel', 'United States']

prop_cases_top_ten_averages = infection_data[infection_data['location'].isin(prop_cases_top_ten_countries)].reset_index(drop=True)

prop_cases_top_ten_averages = prop_cases_top_ten_averages.groupby(['location']).mean()

prop_cases_top_ten_averages['proportionate_total_cases'] = prop_cases_top_ten_averages['total_cases'] / \
                                                           prop_cases_top_ten_averages['population']

prop_cases_top_ten_averages = prop_cases_top_ten_averages.sort_values(by='proportionate_total_cases', ascending=False)

prop_cases_top_ten_averages = prop_cases_top_ten_averages.drop(columns=['total_cases', 'total_deaths'])

prop_deaths_top_ten_countries = ['Hungary', 'Czechia', 'San Marino', 'Bosnia and Herzegovina', 'Montenegro', 'Bulgaria',
                                 'North Macedonia', 'Slovakia', 'Belgium', 'Slovenia']

prop_deaths_top_ten_averages = infection_data[infection_data['location'].isin(prop_deaths_top_ten_countries)].reset_index(drop=True)

prop_deaths_top_ten_averages = prop_deaths_top_ten_averages.groupby(['location']).mean()

prop_deaths_top_ten_averages['proportionate_total_deaths'] = prop_deaths_top_ten_averages['total_deaths'] / \
                                                             prop_deaths_top_ten_averages['population']

prop_deaths_top_ten_averages = prop_deaths_top_ten_averages.sort_values(by='proportionate_total_deaths', ascending=False)

prop_deaths_top_ten_averages = prop_deaths_top_ten_averages.drop(columns=['total_cases', 'total_deaths'])

# ======================================================================================================================
# Finding the total raw vaccinations for each country.

people_fully_vaccinated = vaccination_data.dropna(axis=0, subset=['people_fully_vaccinated'])

people_fully_vaccinated_countries = people_fully_vaccinated['country'].unique().tolist()

raw_total_vaccinations = []

for country in people_fully_vaccinated_countries:
    data = [people_fully_vaccinated[people_fully_vaccinated['country'] == country]['country'].iloc[-1],
            people_fully_vaccinated[people_fully_vaccinated['country'] == country]['total_vaccinations'].iloc[-1],
            people_fully_vaccinated[people_fully_vaccinated['country'] == country]['people_fully_vaccinated'].iloc[-1],
            people_fully_vaccinated[people_fully_vaccinated['country'] == country]['vaccines'].iloc[-1]]

    raw_total_vaccinations.append(data)

raw_total_vaccinations_df = pd.DataFrame(raw_total_vaccinations, columns=['country', 'total_vaccinations',
                                                                          'people_fully_vaccinated', 'vaccines'])

raw_total_vaccinations_df = raw_total_vaccinations_df.sort_values(by='people_fully_vaccinated', ascending=False)

raw_total_vaccinations_df = raw_total_vaccinations_df.fillna(0)

# ======================================================================================================================
# Finding the total vaccinations for every day from March 1 to April 1 for each country.

total_vaccinations = vaccination_data.groupby('iso_code').fillna(method='ffill')

total_vaccinations = total_vaccinations[(total_vaccinations['date'] > '2021-02-28') & (total_vaccinations['date'] < '2021-04-01')]

# Now, finding the top ten countries with the most people vaccinated and filtering out 'total_vaccinations' accordingly.
people_fully_vaccinated = vaccination_data.dropna(axis=0, subset=['people_fully_vaccinated'])

people_fully_vaccinated_countries = people_fully_vaccinated['country'].unique().tolist()

population = infection_data.groupby('location').tail(1).reset_index(drop=True)

population = population[['location', 'population']]

prop_factors = infection_data.groupby('location', as_index=False).mean()

people_fully_vaccinated = pd.merge(left=people_fully_vaccinated, right=population, how='left', left_on='country', right_on=population['location'])

people_fully_vaccinated_factors = pd.merge(left=people_fully_vaccinated, right=prop_factors, how='left', left_on='country', right_on=prop_factors['location'])

people_fully_vaccinated_factors = people_fully_vaccinated_factors.groupby('country').tail(1).reset_index(drop=True)

people_fully_vaccinated_factors['prop_people_fully_vaccinated'] = people_fully_vaccinated_factors['people_fully_vaccinated'] / people_fully_vaccinated_factors['population_x']

people_fully_vaccinated_factors = people_fully_vaccinated_factors.sort_values(by='prop_people_fully_vaccinated', ascending=False).reset_index(drop=True)

people_fully_vaccinated = people_fully_vaccinated.groupby('country').tail(1).reset_index(drop=True)

people_fully_vaccinated['prop_people_fully_vaccinated'] = people_fully_vaccinated['people_fully_vaccinated'] / people_fully_vaccinated['population']

prop_people_fully_vaccinated = people_fully_vaccinated.sort_values(by='prop_people_fully_vaccinated', ascending=False).reset_index(drop=True)

people_fully_vaccinated = people_fully_vaccinated.sort_values(by='people_fully_vaccinated', ascending=False).reset_index(drop=True)

prop_people_fully_vaccinated_top_ten = prop_people_fully_vaccinated.head(10)

prop_people_fully_vaccinated_top_ten_countries = prop_people_fully_vaccinated_top_ten['country'].unique().tolist()

people_fully_vaccinated_top_ten = people_fully_vaccinated.head(10)

people_fully_vaccinated_top_ten_countries = people_fully_vaccinated_top_ten['country'].unique().tolist()

total_vaccinations = total_vaccinations[total_vaccinations['country'].isin(people_fully_vaccinated_top_ten_countries)].reset_index(drop=True)


# Fills the one NA values for Russia
total_vaccinations = total_vaccinations.fillna(method='bfill')

total_vaccinations = total_vaccinations.drop(columns=['daily_vaccinations', 'vaccines'])

total_vaccinations = total_vaccinations.sort_values(by=['date', 'country']).reset_index(drop=True)

total_vaccinations_countries = total_vaccinations['country'].unique().tolist()

prop_daily_vacc_progress = vaccination_data.groupby('iso_code').fillna(method='ffill')

prop_daily_vacc_progress = prop_daily_vacc_progress.drop(columns=['total_vaccinations', 'people_fully_vaccinated', 'vaccines'])

prop_daily_vacc_progress['country2'] = prop_daily_vacc_progress['country']

prop_daily_vacc_progress = prop_daily_vacc_progress.groupby(by='country2').fillna(method='bfill')

prop_daily_vacc_progress = pd.merge(left=prop_daily_vacc_progress, right=population, how='left', left_on='country', right_on=population['location'])

prop_daily_vacc_progress = prop_daily_vacc_progress.drop(columns='location')

prop_daily_vacc_progress = pd.merge(left=prop_daily_vacc_progress, right=prop_people_fully_vaccinated[['country', 'total_vaccinations', 'people_fully_vaccinated']], how='left', left_on='country', right_on='country')

prop_daily_vacc_progress = pd.merge(left=prop_daily_vacc_progress, right=infection_data[['location', 'continent']], how='left', left_on='country', right_on='location')

prop_daily_vacc_progress = prop_daily_vacc_progress.drop(columns='location')

prop_daily_vacc_progress = prop_daily_vacc_progress.fillna(0)

prop_daily_vacc_progress['prop_daily_vaccinations'] = prop_daily_vacc_progress['daily_vaccinations'] / prop_daily_vacc_progress['population']

prop_daily_vacc_progress = prop_daily_vacc_progress.drop_duplicates().reset_index(drop=True)

average_daily_progress = prop_daily_vacc_progress.groupby('country', as_index=False).mean().sort_values(by='prop_daily_vaccinations', ascending=False)

average_daily_progress = average_daily_progress[average_daily_progress['prop_daily_vaccinations'] != np.inf]

average_daily_progress = average_daily_progress.drop(columns=['daily_vaccinations']).reset_index(drop=True)

average_daily_progress = average_daily_progress.head(30)

# ======================================================================================================================
# Mapping the demographic factors to the top ten countries with the most people vaccinated.

factor_data_top_ten = infection_data[infection_data['location'].isin(people_fully_vaccinated_top_ten_countries)].reset_index(drop=True)

factor_data_top_ten_averages = factor_data_top_ten.groupby('location').mean()

factor_data_top_ten_averages = factor_data_top_ten_averages[['stringency_index', 'aged_65_older', 'gdp_per_capita',
                                                             'life_expectancy', 'human_development_index']]

top_ten_vaccination_averages = pd.merge(left=people_fully_vaccinated_top_ten, right=factor_data_top_ten_averages, how='left', left_on='country', right_on=factor_data_top_ten_averages.index)

# ======================================================================================================================
# Reading the cleaned files to Excel spreadsheets.

# CSV Files
infection_data.to_csv(file_path + '/cleaned/csv/base_data/owid-covid-data_cleaned.csv', index=False)

vaccination_data.to_csv(file_path + '/cleaned/csv/base_data/country_vaccinations_cleaned.csv', index=False)

raw_total_cases_and_deaths_df.to_csv(file_path + '/cleaned/csv/visualization_data/raw_total_cases_and_deaths.csv', index=False)

raw_top_ten_averages.to_csv(file_path + '/cleaned/csv/visualization_data/raw_top_ten_averages.csv', index=True)

prop_cases_top_ten_averages.to_csv(file_path + '/cleaned/csv/visualization_data/proportionate_total_cases_averages.csv', index=True)

prop_deaths_top_ten_averages.to_csv(file_path + '/cleaned/csv/visualization_data/proportionate_total_deaths_averages.csv', index=True)

prop_total_cases_df.to_csv(file_path + '/cleaned/csv/visualization_data/proportionate_total_cases.csv', index=False)

prop_total_deaths_df.to_csv(file_path + '/cleaned/csv/visualization_data/proportionate_total_deaths.csv', index=False)

raw_total_vaccinations_df.to_csv(file_path + '/cleaned/csv/visualization_data/total_raw_vaccinations.csv', index=False)

top_ten_vaccination_averages.to_csv(file_path + '/cleaned/csv/visualization_data/vaccination_factors.csv', index=False)

prop_people_fully_vaccinated.to_csv(file_path + '/cleaned/csv/visualization_data/prop_total_vaccinations.csv', index=False)

people_fully_vaccinated_factors.to_csv(file_path + '/cleaned/csv/visualization_data/prop_total_vaccinations_factors.csv', index=False)

# JSON Files

# Do not remove the "_og"; the file needs additional formatting in VSCode using regular expressions and find/replace.
raw_total_cases_and_deaths_top_ten_df.to_json(file_path + '/cleaned/json/raw_total_cases_and_deaths_og.json', orient='index')

# Do not remove the "_og"; the file needs additional formatting in VSCode using regular expressions and find/replace.
prop_total_cases_df.to_json(file_path + '/cleaned/json/proportionate_total_cases_og.json', orient='index')

# Do not remove the "_og"; the file needs additional formatting in VSCode using regular expressions and find/replace.
prop_total_deaths_df.to_json(file_path + '/cleaned/json/proportionate_total_deaths_og.json', orient='index')

# Do not remove the "_og"; the file needs additional formatting in VSCode using regular expressions and find/replace.
total_vaccinations.to_json(file_path + '/cleaned/json/total_vaccinations_march_og.json', orient='index', date_format='iso')

# Do not remove the "_og"; the file needs additional formatting in VSCode using regular expressions and find/replace.
average_daily_progress.to_json(file_path + '/cleaned/json/average_daily_vaccination_progress_og.json', orient='index')
