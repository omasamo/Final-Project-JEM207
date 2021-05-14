import requests
import time
from scrapy import Selector

list_response = []  ## LIST OF EVERY SELECTOR (scrapy) for every year of OSCARS

for i in range(1930, 1950):  # from 1930 (first Oscars to 2021 Oscars)
    #time.sleep(0.2)  # Crawlerdelay
    print(i)
    url = "https://www.oscars.org/oscars/ceremonies/{}".format(i)
    response_oscars = requests.get(url)
    sel = Selector(text=response_oscars.text)  # Scrapy chose over BeautifulSoup for selector CSS
    list_response.append(sel)


list_names = []
list_year = []
list_category = []
list_films = []
list_results = []

for years in range(len(list_response)):

    categories = list_response[years].css(
        '#quicktabs-tabpage-honorees-0 > div > div.view-content > div.view-grouping > div.view-grouping-header > h2::text').extract()
    for i in range(len(categories)):
        if categories[i] in ('Directing', 'Actor', 'Actor in a Leading Role', 'Actress', 'Actress in a Leading Role','Outstanding Picture', 'Outstanding Production', 'Best Motion Picture', 'Foreign Language Film', 'Special Effects','Special Visual Effects', 'Special Achievement Award (Visual Effects)' ):

            # Need the number of winners (might be ties) and nominated
            path_nominated = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:last-child".format(
                i + 1)
            number_of_film_nominated = ''.join(list_response[years].css(path_nominated).extract()).split("views-row-")

            path_winner = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2)".format(
                i + 1)
            number_of_film_winner = ''.join(list_response[years].css(path_winner).extract()).split(
                "views-row-first views-row-last")  # If 1 winner then it splits the string into 1 list of 2 elements, if 2 winners, it does nothing

            ### WINNER(S) ####
            if len(number_of_film_winner) == 2:  # 1 Winner
                # NAME
                path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div.views-row.views-row-1.views-row-odd.views-row-first.views-row-last > div.views-field.views-field-field-actor-name > h4::text".format(
                    i + 1)
                nominee_name = ''.join(list_response[years].css(
                    path_name).extract())  # ''.join() transforms the list produced by the selector into a string
                list_year.append(1930 + years)
                list_category.append(categories[i])
                list_results.append("Winner")
                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_films.append(nominee_name)
                else:
                    list_names.append(nominee_name)

                # FIlM
                path_film = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div.views-row.views-row-1.views-row-odd.views-row-first.views-row-last > div.views-field.views-field-title > span::text'.format(
                    i + 1)
                nominee_film = ''.join(list_response[years].css(
                    path_film).extract())  # ''.join() transforms the list produced by the selector into a string
                nominee_film = nominee_film.replace("\n", "")  # Cleaning up the string
                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_names.append(nominee_film)
                else:
                    list_films.append(nominee_film)

                for number in range(int(number_of_film_nominated[1])):
                    ### NOMINEES ####
                    # NAME
                    path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-field-actor-name > h4::text".format(
                        i + 1, 4 + number)
                    nominee_name = ''.join(list_response[years].css(
                        path_name).extract())  # ''.join() transforms the list produced by the selector into a string4
                    list_year.append(1930 + years)
                    list_category.append(categories[i])
                    list_results.append("Nominee")

                    if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                        list_films.append(nominee_name)
                    else:
                        list_names.append(nominee_name)

                    # FILM
                    path_film = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-title > span::text".format(
                        i + 1, 4 + number)
                    nominee_film = ''.join(list_response[years].css(
                        path_film).extract())  # ''.join() transforms the list produced by the selector into a string
                    nominee_film = nominee_film.replace("\n", "")  # Cleaning up the string
                    if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                        list_names.append(nominee_film)
                    else:
                        list_films.append(nominee_film)

            if len(number_of_film_winner) == 1:  # 2 Winners
                ### WINNERS ###
                # NAME 1st Winner
                path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2) > div.views-field.views-field-field-actor-name > h4::text".format(
                    i + 1)
                nominee_name = ''.join(list_response[years].css(
                    path_name).extract())  # ''.join() transforms the list produced by the selector into a string4
                list_year.append(1930 + years)
                list_category.append(categories[i])
                list_results.append("Tie-winner")

                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_films.append(nominee_name)
                else:
                    list_names.append(nominee_name)

                # NAME 2st Winner
                path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(3) > div.views-field.views-field-field-actor-name > h4::text".format(
                    i + 1)
                nominee_name = ''.join(list_response[years].css(
                    path_name).extract())  # ''.join() transforms the list produced by the selector into a string4
                list_year.append(1930 + years)
                list_category.append(categories[i])
                list_results.append("Tie-winner")
                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_films.append(nominee_name)
                else:
                    list_names.append(nominee_name)

                # FILM
                path_film1 = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(2) > div.views-field.views-field-title > span::text'.format(
                    i + 1)
                path_film2 = '#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child(3) > div.views-field.views-field-title > span::text'.format(
                    i + 1)

                nominee_film = ''.join(list_response[years].css(
                    path_film1).extract())  # ''.join() transforms the list produced by the selector into a string
                nominee_film = nominee_film.replace("\n", "")  # Cleaning up the string

                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_names.append(nominee_film)
                else:
                    list_films.append(nominee_film)

                winner2_film = ''.join(list_response[years].css(
                    path_film2).extract())  # ''.join() transforms the list produced by the selector into a string
                winner2_film = winner2_film.replace("\n", "")  # Cleaning up the string

                if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                    list_names.append(nominee_film)
                else:
                    list_films.append(nominee_film)

                for number in range(int(number_of_film_nominated[1])):
                    #### NOMINEES ####
                    # NAME
                    path_name = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-field-actor-name > h4::text".format(
                        i + 1, 5 + number)
                    nominee_name = ''.join(list_response[years].css(
                        path_name).extract())  # ''.join() transforms the list produced by the selector into a string4
                    list_year.append(1930 + years)
                    list_category.append(categories[i])
                    list_results.append("Nominee")
                    if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                        list_films.append(nominee_name)
                    else:
                        list_names.append(nominee_name)

                    # FILM
                    path_film = "#quicktabs-tabpage-honorees-0 > div > div.view-content > div:nth-child({}) > div.view-grouping-content > div:nth-child({}) > div.views-field.views-field-title > span::text".format(
                        i + 1, 5 + number)
                    nominee_film = ''.join(list_response[years].css(
                        path_film).extract())  # ''.join() transforms the list produced by the selector into a string
                    nominee_film = nominee_film.replace("\n", "")  # Cleaning up the string

                    if categories[i] == "Directing":  # For Directing, titles and names are swapped on the website
                        list_names.append(nominee_film)
                    else:
                        list_films.append(nominee_film)

import pandas as pd

# dictionary of lists
dict = {'name': list_names, 'category': list_category, 'film': list_films, 'result': list_results, 'year': list_year}

df = pd.DataFrame(dict)
"""for i,row in df.iterrows():
    if row['category'] == ('Outstanding Picture' or  'Outstanding Production' or 'Best Motion Picture' or 'Foreign Language Film' or 'Special Effects' or 'Special Visual Effects'or 'Special Achievement Award (Visual Effects)'):
        df.to_csv(r'films.txt', sep=' ', mode='a')"""


films = df.loc[df['category'] == ('Outstanding Picture' and  'Outstanding Production'  'Best Motion Picture' and 'Foreign Language Film' and 'Special Effects' and 'Special Visual Effects' and 'Special Achievement Award (Visual Effects)')]
print(films)
films.to_csv(r'films.txt', sep=' ', mode='a')
