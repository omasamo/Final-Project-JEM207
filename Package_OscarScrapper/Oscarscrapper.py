### OOP   ### ROTTENTOMATOES

import time
import requests
from scrapy import Selector
from tqdm import tqdm
import pandas as pd
import re  # text processing
import numpy as np
import json
import jellyfish
from urllib.parse import quote
import os 
import sys # to use exit()
from tkinter import * # Window 

os.chdir(os.path.dirname(os.path.abspath(__file__))) # This changes the working directory to be the same as where the python script is.

class Oscar_Scraper:
    
    # *  Defining lists containing the future raw data
    list_names = []
    list_year = []
    list_category = []
    list_films = []
    list_results = [] 
    list_id_movie = []
    list_birthday = []
    list_gender = []
    list_id_indiv = []
    list_names_right = []
    list_films_right = []
    list_names_wrong = []
    list_films_wrong = []
    
    def __init__(self):
        """
        Initialization method.
        Initializes most lists used to select and store data.
        It endes by calling the Imput method to start the program.
        """

        # * List of the content of every oscars.org pages used
        self.links = {
            'oscars':[]
        }
        

        # * Lists of different names for same categories
        self.categories_dictionary = {
                    "Actor in a Leading Role": ['Actor', 'Actor in a Leading Role'],
                    "Actress in a Leading Role": ['Actress', 'Actress in a Leading Role'],
                    "Directing": ["Directing"],
                    "Best Picture": ['Outstanding Picture', 'Outstanding Production','Best Motion Picture', 'Best Picture'],
                    "Visual Effects" : ['Special Effects', 'Special Visual Effects','Special Achievement Award (Visual Effects)','Visual Effects'],
                    "Best Foreign Language Film": ["Foreign Language Film"]
                    }
        
        # * List of categories related to individuals.

        self.categories_individuals = ['Directing', 'Actor', 'Actor in a Leading Role', 'Actress', 'Actress in a Leading Role']


        # * Stores the user's selected categories to fetch
        self.selected_categories = []
        
                 
        # * Initialize the lists containing the future cleaned data
        self.data = {
                'category':[],
                'film':[],
                'year':[],
                'name':[],
                'gender':[],
                'result':[],
                'birthdate':[],
                'id_movie':[]
                
            }

        # * End of the initialization, fetching for user's imput.
        self.Imput()

    def Imput(self):
        """
        Main method.
        It creates a user interface to interact with the program.
        It asks for categories of interest, time period and how to proceed (autorun or manual run).
        Returns nothing.
        
        """
        window = Tk()
        window.geometry("400x500")
        window.title('Which categories do you want to compile ?')
        
        label1 = Label(window,
                    text = "The Oscar Scapper, by Yann Aubineau and Samuel Bozon",
                    font = ("Times New Roman", 10), 
                    padx = 10, pady = 10)
        label1.pack()

        Label(window, text="From:").pack(pady = 2)
        textExample = Entry(window)
        textExample.pack(pady=2)
        textExample.insert(END, '1930')

        Label(window, text="To:").pack(pady = 2)
        textExample2 = Entry(window)
        textExample2.pack(pady=2)
        textExample2.insert(END, '2021')
        
        # for scrolling vertically
        yscrollbar = Scrollbar(window)
        yscrollbar.pack(side = RIGHT, fill = Y)
        
        label2 = Label(window,
                    text = "Which categories do you want to compile ?\n Select the categories below :  ",
                    font = ("Times New Roman", 10), 
                    padx = 10, pady = 10)
        label2.pack()

        list_selection = Listbox(window, selectmode = "multiple", 
                    yscrollcommand = yscrollbar.set)
        

        list_selection.pack(padx = 2, pady = 2,
                expand = NO, fill = X)
        
        list_categories_possible = [item for item in list(self.categories_dictionary.keys())]


        for each_item in range(len(list_categories_possible)):
            list_selection.insert(END, list_categories_possible[each_item])
            list_selection.itemconfig(each_item, bg = "white")

        self.user_imput = IntVar() #Basically Links Any Radiobutton With The Variable=i.
        r1 = Radiobutton(window, text="Autorun (recommanded)", value=1, variable=self.user_imput)
        r1.pack(pady = 10, padx= 5)
        r2 = Radiobutton(window, text="Manual run", value=2, variable=self.user_imput)
        r2.pack(pady = 2, padx= 2)
        
        exit_button = Button(window, text="Done", command= lambda:[fCategories(),fDates(),window.destroy(),self.Run()])
        exit_button.pack(pady=20)
        

        def fCategories():

            # * Stores the index of the selected categories after the exit_button press.

            self.input_selected = []
            for i in list_selection.curselection():
        
                self.input_selected.append(list_selection.get(i)) 
            
            # * From the index of the selected categories to the selected categories.
            for input_categories in self.input_selected:
                if input_categories in self.categories_dictionary.get(input_categories):
                    for number_name in range(len(self.categories_dictionary.get(input_categories))):
                        self.selected_categories.append(self.categories_dictionary.get(input_categories)[number_name])

        def fDates():

            # ! It handles errors regarding time periods.

            try:
                self.from_time = int(textExample.get())
                if self.from_time < 1930:
                    print("The Academy Awards ceremony starts in 1929 but the categories are standardized in the 1930's ceremony. Please pick between 1930 and 2021.")
                    raise Exception

                self.to_time = int(textExample2.get())
                if self.to_time > 2021:
                    print("This program supports Academy Awards ceremonies until 2021. Please pick between 1930 and 2021.")
                    raise Exception

                if self.from_time > self.to_time:
                    raise Exception

                self.time_period = range(self.from_time, self.to_time + 1)
                
            except Exception as e:
                print("You must enter a valid range of dates.\nThe object was not created.")

        window.mainloop()

        
        
        
 
        

    def getHTML(self):

        """"
        Main method.
        Used to extract the content of the oscar.org webpage for each ceremonies included in the time period chose by the utilisator.
        It stocks them in self.links['oscars']
        Returns nothing
        """

        print("Getting the content of oscars.org webpages ...")
        for number_year in tqdm(self.time_period):
            try:
                #time.sleep(10) # Crawlerdelay
                url = "https://www.oscars.org/oscars/ceremonies/{}".format(number_year)
                response_oscars = requests.get(url)
                sel = Selector(text = response_oscars.text)   # Scrapy chose over BeautifulSoup for selector CSS
                self.links['oscars'].append(sel)
            except requests.exceptions.RequestException as e:  
                print("There was an error while requesting oscars.org website. Please retry or check your connection or the status of the website. See next the error message: ", e)
                raise SystemExit(e)

    def getNominees(self, years, i, category, number_nominees, number_winners):

        """
        Sub-method.
        It takes itself, the index of which year it is, the index of which category it is, the category, the number of nominees and the number of winners
        It extracts and stock the name of the nominees and the film nominated
        Returns nothing.
        """

        for number_people_nominated in range(number_nominees):   
            if number_winners == 1:
                # NAME
                path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-field-actor-name > h4::text".format(i+1, 4 + number_people_nominated)
                nominee_name = ''.join(self.links['oscars'][years].css(path_name).extract()) # ''.join() transforms the list produced by the selector into a string
            if number_winners == 2:
                 # NAME
                path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-field-actor-name > h4::text".format(i+1, 5 + number_people_nominated)
                nominee_name = ''.join(self.links['oscars'][years].css(path_name).extract()) # ''.join() transforms the list produced by the selector into a string
            
            if category == "Directing": # For Directing, titles and names are swapped on the website
                self.list_films.append(nominee_name)
            else:
                self.list_names.append(nominee_name)

            # FILM
            if number_winners == 1:
                path_film = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-title > span::text".format(i+1, 4 + number_people_nominated)
                nominee_film = ''.join(self.links['oscars'][years].css(path_film).extract()) # ''.join() transforms the list produced by the selector into a string
                nominee_film = nominee_film.replace("\n", "") # Cleaning up the string
            if number_winners == 2:
                path_film = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-title > span::text".format(i+1, 5 + number_people_nominated)
                nominee_film = ''.join(self.links['oscars'][years].css(path_film).extract()) # ''.join() transforms the list produced by the selector into a string
                nominee_film = nominee_film.replace("\n", "") # Cleaning up the string
            if category == "Directing": # For Directing, titles and names are swapped on the website
                self.list_names.append(nominee_film)
            else:
                self.list_films.append(nominee_film)
            
            self.list_year.append(self.from_time + years)         
            self.list_category.append(category)
            self.list_results.append("Nominee")

    def getWinners(self, years, i, category, number_winners):
        """
        Sub-method.
        It takes itself, the index of which year it is, the index of which category it is, the category and the number of winners
        It extracts and stock the name of the winners and the film winning.
        Returns nothing.       
        """

        if number_winners == 1: # 1 Winner
        # NAME
            path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div.views-row.views-row-1.views-row-odd.views-row-first.views-row-last > div.views-field.views-field-field-actor-name > h4::text".format(i+1)
            nominee_name = ''.join(self.links['oscars'][years].css(path_name).extract()) # ''.join() transforms the list produced by the selector into a string

            if category == "Directing": # For Directing, titles and names are swapped on the website
                self.list_films.append(nominee_name)
            else:
                self.list_names.append(nominee_name)
            
        
            # FIlM
            path_film = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div.views-row.views-row-1.views-row-odd.views-row-first.views-row-last > div.views-field.views-field-title > span::text'.format(i+1)
            nominee_film = ''.join(self.links['oscars'][years].css(path_film).extract()) # ''.join() transforms the list produced by the selector into a string
            nominee_film = nominee_film.replace("\n", "") # Cleaning up the string

            if category == "Directing":# For Directing, titles and names are swapped on the website
                self.list_names.append(nominee_film)
            else:
                self.list_films.append(nominee_film)
           
            self.list_year.append(self.from_time + years)
            self.list_category.append(category)
            self.list_results.append("Winner")


        if number_winners == 2: # 2 Winners
            # NAME 1st Winner 
            path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2) > div.views-field.views-field-field-actor-name > h4::text".format(i+1)
            nominee_name = ''.join(self.links['oscars'][years].css(path_name).extract()) # ''.join() transforms the list produced by the selector into a string4

            if category == "Directing": # For Directing, titles and names are swapped on the website
                self.list_films.append(nominee_name)
            else:
                self.list_names.append(nominee_name)

            self.list_year.append(self.from_time + years)
            self.list_category.append(category)
            self.list_results.append("Tie-winner")

            # NAME 2st Winner 
            path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(3) > div.views-field.views-field-field-actor-name > h4::text".format(i+1)
            nominee_name = ''.join(self.links['oscars'][years].css(path_name).extract()) # ''.join() transforms the list produced by the selector into a string4

            if category == "Directing": # For Directing, titles and names are swapped on the website
                self.list_films.append(nominee_name)
            else:
                self.list_names.append(nominee_name)

            self.list_year.append(self.from_time + years)
            self.list_category.append(category)
            self.list_results.append("Tie-winner")

            # FILM
            path_film1 = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2) > div.views-field.views-field-title > span::text'.format(i+1)
            path_film2 = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(3) > div.views-field.views-field-title > span::text'.format(i+1)

            nominee_film = ''.join(self.links['oscars'][years].css(path_film1).extract()) # ''.join() transforms the list produced by the selector into a string
            nominee_film = nominee_film.replace("\n", "") # Cleaning up the string

            if category == "Directing":# For Directing, titles and names are swapped on the website
                self.list_names.append(nominee_film)
            else:
                self.list_films.append(nominee_film)

            winner2_film = ''.join(self.links['oscars'][years].css(path_film2).extract()) # ''.join() transforms the list produced by the selector into a string
            winner2_film = winner2_film.replace("\n", "") # Cleaning up the string

            if category == "Directing":# For Directing, titles and names are swapped on the website
                self.list_names.append(winner2_film)
            else:
                self.list_films.append(winner2_film)        



    def getDATA(self): 

        """
        Main method:
        Using the content of each oscar.org webpage per year to identify the number of winners and nominated of each category in the list, then through two sub-methods it identifies the result, year, name of the winner/nominee,
        title of the movie and category, and save them in a dictionnary of list.
        Then it calls a sub-method to proceed some corrections on these lists, as some errors exist in the oscar.org website.
        Returns nothing
        """

        print("Extracting the data of the website ...")    
        for years in tqdm(range(len(self.links['oscars']))):

            categories = self.links['oscars'][years].css('#quicktabs-tabpage-honorees-0 > div > div.view-content > div.view-grouping > div.view-grouping-header > h2::text').extract()    
            for i in range(len(categories)):
                if categories[i] in self.selected_categories:

                    # Need the number of winners (might be ties) and nominated          
                    path_nominated = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:last-child".format(i+1)
                    number_of_film_nominated = int(''.join(self.links['oscars'][years].css(path_nominated).extract()).split("views-row-")[1])

                    path_winner = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2)".format(i+1)
                    trial = ''.join(self.links['oscars'][years].css(path_winner).extract()).split("views-row-first views-row-last") # If 1 winner then it splits the string into 1 list of 2 elements, if 2 winners, it does nothing
                    if len(trial) == 2:
                        number_winners = 1
                    elif len(trial) == 1:
                        number_winners = 2
                    else:
                        print("problem")


                    ## WINNERS                 
                    self.getWinners(years, i, categories[i], number_winners)     
                    
                    ## NOMINEES
                    self.getNominees(years, i, categories[i], number_of_film_nominated, number_winners)   

                    
        self.data = {
            'year': self.list_year,
            'category': self.list_category,
            'film': self.list_films,
            'name': self.list_names,
            'result':self.list_results
        }            
    
        self.Correction(0,True)
        print(self.data)


    def getINDIVIDUALS(self):
        df = pd.DataFrame(self.data)
        df = df.set_index(['year','category'])
        individuals = df.loc(axis = 0)[pd.IndexSlice[:, self.categories_individuals]]
        return(individuals)
    
    def saveINDIVIDUALS(self):
        df = pd.DataFrame(self.data)
        df = df.set_index(['year','category'])
        individuals = df.loc(axis = 0)[pd.IndexSlice[:, self.categories_individuals]]
        individuals.reset_index() # For some reasons the index is not saved with the rest so we make it back to two columns 
        individuals.to_csv("Individuals.csv")
        return(print("The dataframe was saved as Individuals.csv in your working directory."))

        
    def getFILMS(self):
        df = pd.DataFrame(self.data)
        df = df.set_index(['year','category'])
        films = df.loc(axis = 0)[pd.IndexSlice[:, self.categories_interest[5:]]]
        films.columns = ('film', 'Studio/Creator(s)', 'result')
        return(films)
    
     #creating big dataframe with all data
    def getAllCategories(self):
        df = pd.DataFrame(self.data)
        df = df.set_index(['year','category'])
        return(df)
        
        
    def getAPI_TMDB(self):

        """
        Main method.
        From the title, it searches in an complete movie database for the movie, then we extract the matching individual and collect their birthdate and gender.
        It uses the sub-method getTMDB
        Returns nothing
        
        """
        API_KEY_MDB = "a68690ebf69567801e68c26ee82d7787"
        URL_MDB_SEARCH = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page={}&include_adult=false"
        URL_MDB_PERSON = "https://api.themoviedb.org/3/person/{}?api_key={}"

        print("Requesting TheMovieDataBase API for the gender and birthdays ...")    

        try:
            for film_number in tqdm(range(len(self.data['film']))):
                title_standard = quote(self.data['film'][film_number])
                response_search = json.loads(requests.get(URL_MDB_SEARCH.format(API_KEY_MDB,title_standard,1)).text)
                if response_search["total_results"] != 0:        
                    if self.TMDB_get(response_search, film_number) == True:

                        response_person = json.loads(requests.get(URL_MDB_PERSON.format(self.list_id_indiv[film_number],API_KEY_MDB)).text)
                        if response_person.get("success") != False: # Check if the API find a person

                            if response_person["birthday"] in (None,0):
                                pass
                            
                            if response_person["gender"] in (None,0):
                                pass
                            self.list_birthday.append(response_person["birthday"])
                            self.list_gender.append(response_person["gender"])
                        else:
                            pass
                    else:
                        response_search = json.loads(requests.get(URL_MDB_SEARCH.format(API_KEY_MDB,title_standard,2)).text)
                        if response_search["total_results"] != 0:        
                            if self.TMDB_get(response_search, film_number) == True:
                                response_person = json.loads(requests.get(URL_MDB_PERSON.format(self.list_id_indiv[film_number],API_KEY_MDB)).text)
                                if response_person.get("success") != False: # Check if the API find a person
                                    if response_person["birthday"] in (None,0):
                                        pass
                                    
                                    if response_person["gender"] in (None,0):
                                        pass
                                    self.list_birthday.append(response_person["birthday"])
                                    self.list_gender.append(response_person["gender"])
                                else:
                                    pass
                            else:
                                # specific problems with some 1930's movies
                                URL_MDB_SEARCH1930 = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page={}&include_adult=false&year=1930"
                                response_search = json.loads(requests.get(URL_MDB_SEARCH1930.format(API_KEY_MDB,title_standard,1)).text)
                                if response_search["total_results"] != 0:        
                                    if self.TMDB_get(response_search, film_number) == True:
                                        response_person = json.loads(requests.get(URL_MDB_PERSON.format(self.list_id_indiv[film_number],API_KEY_MDB)).text)
                                        if response_person.get("success") != False: # Check if the API find a person
                                            
                                            if response_person["birthday"] in (None,0):
                                                pass
                                            if response_person["gender"] in (None,0):
                                                pass
                                            self.list_birthday.append(response_person["birthday"])
                                            self.list_gender.append(response_person["gender"])
                                        else:
                                            pass
                else:
                    pass
                    self.Correction(film_number, False)
        except requests.exceptions.RequestException as e:  
            print("There was an error while requesting the API of TheMovieDataBase website. Please retry or check your connection or the status of the website. See next the error message: ", e)
            raise SystemExit(e)
        
        for i in tqdm(range(len(self.data['film']))): 
            if self.list_gender[i] == 1:
                self.list_gender[i] = "Female"
            elif self.list_gender[i] == 2:
                self.list_gender[i] = "Male"
            elif self.list_gender[i] == 3:
                self.list_gender[i] = "Non-binary"

            self.list_birthday[i] = int(self.list_birthday[i][0:4]) # We keep only the year and transform from string to float
            
        self.data['gender'] = self.list_gender
        self.data['birthday'] = self.list_birthday
        
        
                                        
    def TMDB_get(self, response_search, film_number):
        """
        Sub-method.
        It takes itself, the content of the response of the API, the index number of the film in self.data["film"].
        Used by getAPI_tmdb to extract to confirm the right movie was picked (it contains the individual it is looking for)
        Returns True or False, True if the individual was present in the credits of the movie.
        """
        
        url_MDB_credit = "http://api.tmdb.org/3/movie/{}/credits?api_key={}"
        API_KEY_MDB = "a68690ebf69567801e68c26ee82d7787"
        found_individual = False
        try :
            for number_results in range(len(response_search["results"])):
                if found_individual == False:
                    if response_search["results"][number_results].get("release_date") not in (None,0,''): # There is a release date
                        if (int(response_search["results"][number_results]["release_date"][0:4]) in (self.data["year"][film_number],self.data["year"][film_number]-1, self.data["year"][film_number]-2, self.data["year"][film_number]-3)) and found_individual == False:
                            id_MDB = response_search["results"][number_results]["id"]
                            response_credit = json.loads(requests.get(url_MDB_credit.format(id_MDB,API_KEY_MDB)).text)
                            if response_credit.get("success") != False: # Check if the API find a person
                                if self.data["category"][film_number] == "Directing":
                                    for acteurs in range(len(response_credit["crew"])):
                                        if jellyfish.damerau_levenshtein_distance(response_credit["crew"][acteurs]["name"], self.data["name"][film_number]) < 2:
                                            self.list_id_indiv.append(response_credit["crew"][acteurs]["id"])
                                            found_individual = True
                                        
                                            break


                                    if not any(jellyfish.damerau_levenshtein_distance(response_credit["crew"][acteurs]["name"], self.data["name"][film_number]) < 2 for acteurs in range(len(response_credit["crew"]))):
                                        pass
                                        # self.Correction(film_number, False)
                                        
                                else:
                                    for acteurs in range(len(response_credit["cast"])):
                                        if jellyfish.damerau_levenshtein_distance(response_credit["cast"][acteurs]["name"], self.data["name"][film_number]) < 2:
                                            self.list_id_indiv.append(response_credit["cast"][acteurs]["id"])
                                            found_individual = True  # Empêche d'avoir plusieurs fois le même acteur si on l'a déjà trouvé
                                            break   
                                            
                                    if not any(jellyfish.damerau_levenshtein_distance(response_credit["cast"][acteurs]["name"], self.data["name"][film_number]) < 2 for acteurs in range(len(response_credit["cast"]))):
                                        pass
                                        # self.Correction(film_number, False)
                                        

                            else:
                                pass
                        else:
                            pass

                    else:
                        pass
        except requests.exceptions.RequestException as e:  
            print("There was an error while requesting oscars.org website. Please retry or check your connection or the status of the website. See next the error message: ", e)
            raise SystemExit(e)
            
        return(found_individual)
                                

    def Correction(self,film_number, corrected):
        """
        Sub-method.
        Used in two ways:
        1) It was used to manually identify and correct mistakes hidden in the oscar.org website, stocking them in a dataframe to use at each iteration of the script. It has been disabled once every mistake was corrected.
        2) It loads the dataframes precedently created, then correct them 
        Returns nothing.
        """
        if corrected == False:
            question = input("Film (f) or Name (n) or Both (b) or Pass (p)?")
            if question == "f":
                answer = input("Bon titre film ?")
                self.list_films_wrong.append(self.data["film"][film_number])
                self.list_films_right.append(answer)
                self.data["film"][film_number] = answer
                pd.DataFrame(self.list_films_right).to_csv('list_films_right.csv',index=False) 
                pd.DataFrame(self.list_films_wrong).to_csv('list_films_wrong.csv',index=False) 
            if question == "n":
                answer = input("Bon nom ?")
                self.list_names_wrong.append(self.data["name"][film_number])
                self.list_names_right.append(answer)           
                self.data["name"][film_number] = answer
                pd.DataFrame(self.list_names_right).to_csv('list_names_right.csv',index=False) 
                pd.DataFrame(self.list_names_wrong).to_csv('list_names_wrong.csv',index=False) 
            if question == "b":
                answer1 = input("Bon titre film ?")
                answer2 = input("Bon nom ?")
                self.list_films_wrong.append(self.data["film"][film_number])
                self.list_names_wrong.append(self.data["name"][film_number])
                self.list_films_right.append(answer1)
                self.list_names_right.append(answer2)
                self.data["film"][film_number] = answer1
                self.data["name"][film_number] = answer2
                pd.DataFrame(self.list_names_right).to_csv('list_names_right.csv',index=False) 
                pd.DataFrame(self.list_names_wrong).to_csv('list_names_wrong.csv',index=False)
                pd.DataFrame(self.list_films_right).to_csv('list_films_right.csv',index=False) 
                pd.DataFrame(self.list_films_wrong).to_csv('list_films_wrong.csv',index=False) 
            if question == "p":
                pass

        if corrected == True:
            list_films_right = pd.read_csv("list_films_right.csv")
            list_films_wrong = pd.read_csv("list_films_wrong.csv")
            list_names_right = pd.read_csv("list_names_right.csv")
            list_names_wrong = pd.read_csv("list_names_wrong.csv")
            l_films = len(list_films_right)
            l_names = len(list_names_right)
            l_data = len(self.data["film"])
            
            for i in range(max(l_films,l_names)):
                if i < l_names:
                    self.list_names_right.append(list_names_right.values.tolist()[i][0])
                    self.list_names_wrong.append(list_names_wrong.values.tolist()[i][0])
                if i < l_films:
                    self.list_films_right.append(list_films_right.values.tolist()[i][0])
                    self.list_films_wrong.append(list_films_wrong.values.tolist()[i][0])
                    
            for i in range(l_data):
                for y in range(max(l_films,l_names)):
                    if y < l_films:
                        if self.data['film'][i] == self.list_films_wrong[y]:
                            self.data['film'][i] = self.list_films_right[y]
                    if y < l_names:       
                        if self.data['name'][i] == self.list_names_wrong[y]:
                            self.data['name'][i] = self.list_names_right[y]

   
    def Run(self):
        if self.user_imput.get() == 1: # Autorun
            self.getHTML()
            self.getDATA()
            self.getAPI_TMDB()
            self.getINDIVIDUALS()
            self.saveINDIVIDUALS()

test = Oscar_Scraper()

