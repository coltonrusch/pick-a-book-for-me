from secret import API_KEY      # Goodreads API key hidden
import requests
import xmltodict
import time
import sys
import json
import random


def random_book(user_id, shelf):
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

    total = json_data["GoodreadsResponse"]['reviews']["@total"]
    book_index = random.randint(1, int(total))

    title = json_data["GoodreadsResponse"]["reviews"]["review"][book_index]["book"]["title"]
    author = json_data["GoodreadsResponse"]["reviews"]["review"][book_index]["book"]["authors"]["author"]["name"]

    return f"{title} by {author}"


def load():
    print("")
    for i in range(74):
        sys.stdout.write('~')
        sys.stdout.flush()
        time.sleep(.02)
    print("")


def suggest_book(user_id, shelf):
    print(f"\nIn my opinion, you should read {random_book(user_id, shelf)}.")

    while True:
        answer = input("Do you like this suggestion? If not, I'll think of a new book. (yes or no)\n")
        if answer.lower() == 'yes':
            print("Thank you for taking my suggestion! Feel free to ask again anytime.")
            sys.stdout.write("Exiting...")
            sys.stdout.flush()
            time.sleep(2)
            break
        elif answer.lower() == 'no':
            print("I'm sorry for picking a dud. Let me pick again...")
            load()
            suggest_book(user_id, shelf)
            break
        else:
            print("Invalid response. Try again, 'yes' or 'no'?")


def main():
    print("Hello!\nDon't know what to read next? Let me help with that! "
          "I'll pick a book from one of your Goodreads shelves.\n")

    user_id = input("Enter your Goodreads id: ")

    shelf = input("Enter the name of the shelf for me to pick from: ")

    load()
    suggest_book(user_id, shelf)


if __name__ == "__main__":
    main()
