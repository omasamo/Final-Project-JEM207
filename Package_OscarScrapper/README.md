# The OscarScrapper (1930-2021)

This is the final project for JEM207 Data Processing with Python made by Yann Aubineau and Samuel Božoň of Charles University.

The aim for our project is to scrape and process the historical data of the **Academy Awards** popularly known as **the Oscars**, and create a user friendly package with easy way to select categories and years which should be scraped
We scrape from oscars.org website historical datas of every nominee and winner for the following 4 categories:
>

> Best Picture (1927-2021)
> Best Director (1927-2021)
> Best Actor (1927-2021)
> Best Actress (1927-2021)

Each dataset would be indexed by year and category.

The sources used for the following datas are: 
- oscars.org
- tmdb.com's API

Firstly we scrape the data for nominees and winners for each selected year for all the selected categories. 

Then, we will use these datas to aks tmdb's API for more informations about the movie. However, given that there may be multiple films and persons with the same name, we are selecting from the API's response only relevant informations. 

These are afterwards processed and added to our dataframe, which is later stored for the future use. 

User can select categories and years in which he is interested through easy GUI. For each of his selection, new dataset stored in csv file is created, permitting easy creation of multiple datasets with different searches chosen by user. 

To use the OscarScrapper, you can either download the repository and execute Package_OscarScrapper/src/Oscarscrapper_package/Oscarscrapper.py or use pip to download it as a package.

```sh
# Pypi
pip install OscarScrapper
```

```sh
from Oscarscrapper_package import Oscarscrapper

Scraper = Oscarscrapper.Oscar_Scraper()
```

Please see or use Example.py to understand how to use the package



