# Final-Project-JEM207
Final project for JEM207 Data Processing with Python
We scrape from oscars.org site historical datasets of every nominees for the following 4 awards:
>

> Best Picture (1927-2021)
> Best Director (1927-2021)
> Best Actor (1927-2021)
> Best Actress (1927-2021)

Each dataset would be indexed by year and category.

The sources used for the following datas are: 
oscars.org and tmdb.com's API

Firstly we scrape the data for nominees and winners for each selected year for all the selected categories. 
Then, we will use these datas to aks tmdb's API for more informations about the movie. However, given that there may be multiple films and persons with the same name, we are selecting from the API's response only relevant informations. 

These are afterwards processed and added to our dataframe, which is later stored for the future use. 

User can through easy GUI select categories and years in which he is interested. For each of his selection, new dataset stored in csv file is created, permitting easy creation of multiple datasets with different searches. 



