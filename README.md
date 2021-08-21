# Final-Project-JEM207
Final project for JEM207 Data Processing with Python

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

These are afterwards processed and added to our dataframe, which is later stored for the future use and evaluation in the form of statistics. 

User can select categories and years in which he is interested through easy GUI. For each of his selection, new dataset stored in csv file is created, permitting easy creation of multiple datasets with different searches chosen by user. 

Some statistics can be find in the Statistical Analysis jupyter notebook with brief explanation. 


