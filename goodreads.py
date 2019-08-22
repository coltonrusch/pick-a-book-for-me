import json
import requests
import xmltodict                # the Goodreads API returns data as XML
from secret import API_KEY      # Goodreads API key hidden


def get_genre(book_id):
    """
    Goodreads API call to retrieve the top genre of a book with ID book_id
    :param book_id: Goodreads ID for a given book
    :return: genre of given book
    """
    params = (
        ('key', {API_KEY}),
    )

    response = requests.get(f'https://www.goodreads.com/book/show/{book_id}', params=params)
    xml_pars = xmltodict.parse(response.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)

    i = 0
    while True:
        current_genre = json_data["GoodreadsResponse"]["book"]["popular_shelves"]["shelf"][i]["@name"]
        if current_genre not in ["to-read", "currently-reading", "favorites", "owned", "books-i-own", "audiobook",
                                 "want"]:
            return current_genre

        i = i + 1


def get_user_shelves(user_id):
    """
    Goodreads API call to retrieve the shelves of user with ID user_id
    :param user_id: Goodreads ID for a given user
    :return: list of shelves on the Goodreads user's account
    """
    params = (
        ('key', {API_KEY}),
    )

    response = requests.get(f'https://www.goodreads.com/user/show/{user_id}.xml', params=params)
    xml_pars = xmltodict.parse(response.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)

    user_shelves = []
    for shelf in range(len(json_data["GoodreadsResponse"]["user"]["user_shelves"]["user_shelf"])):
        current_user_shelf = json_data["GoodreadsResponse"]["user"]["user_shelves"]["user_shelf"][shelf]["name"]
        user_shelves.append(current_user_shelf)

    return user_shelves


def get_shelf(user_id, shelf):
    """
    Goodreads API call to retrieve data concerning shelf of user with ID user_id
    :param user_id: Goodreads ID for a given user
    :param shelf: name of user's shelf to fetch data about
    :return:
    """
    params = (
        ('key', {API_KEY}),
        ('v', '2'),
        ('shelf', {shelf}),
        ('per_page', '200'),
    )

    response = requests.get(f'https://www.goodreads.com/review/list/{user_id}.xml', params=params)
    xml_pars = xmltodict.parse(response.text)
    json_dump = json.dumps(xml_pars)
    json_data = json.loads(json_dump)
    return json_data
