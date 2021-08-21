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

User can through easy GUI select categories and years in which he is interested and for each of his selection, new dataset stored in csv file is created, permitting easy creation of multiple datasets with different searches. 

```sh
# Pypi
pip install OscarScrapper
```



## Notes from WIP:

#####  1. Recommandation : use string familiarity library python
- Used jellyfish

##### 2. Raise error if problem during scrapping
- Done and we added a GUI to provi

##### 3. Full documentation 
- The code is documented and scripts show the typical use both as a package and a executable.

##### 4 . Executable project: one script executable 
- Done

#### 5. Jupyter is good for exploratory + presentation, but "professional" = script executable
- We switched from jupyter to python script and made a package out of it

#### 6. Make it installable : Python package
- Done

