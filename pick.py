import time
import sys
import random
import goodreads


def show_shelves(user_id):
    """
    prints a formatted list of shelves from the user's Goodreads account
    :param user_id: Goodreads ID of user
    :return: list of a user's Goodreads shelves
    """
    print("Here's a list of your shelves:")
    load()
    print("")
    shelf_list = goodreads.get_user_shelves(user_id)
    for shelf in shelf_list:
        print(f"                [+] {shelf}")
    print("")
    load()
    return shelf_list


def out_of_genre_books(genre, genre_dict, genre_list):
    """
    function that handles the case if the user keeps rejecting the book suggestions and it runs out of books
    in a particular genre

    :param genre: genre selected by user
    :param genre_dict: dictionary of pairs in the format:
                        "{book} by {author}" : "genre"
    :param genre_list: array of genres in genre dict, with no duplicates
    :return: n/a
    """
    print(f"Sorry, there are no more {genre} books on your shelf. I have failed you!")
    try_again = input("Would you like to pick a new genre? (yes or no)\n").lower()

    if try_again == 'yes':
        print(f"Here is a list of the genres again, without {genre}:")
        load()
        print("")

        new_list = []
        for item in genre_list:
            if item != genre:
                new_list.append(item)

        for genres in new_list:
            print(f"                [+] {genres}")
        print("")
        load()

        while True:
            selected_genre = input("Out of those genres, what are you feeling?\n").lower()

            if selected_genre not in genre_list:
                print("Invalid genre. Please pick from the list above.")
            else:
                break

        print(f"Considering {selected_genre} books on your shelf...")
        load()

        suggest_book_by_genre(selected_genre, genre_dict, genre_list)
    elif try_again == 'no':
        print("No worries. Feel free to ask again anytime!")
        sys.stdout.write("Exiting...")
        sys.stdout.flush()
        time.sleep(2)
        quit()


def random_book_by_genre(genre, genre_dict):
    """
    given genre and a dictionary containing book-genre pairs, randomly selects a book from genre_dict that is mapped to
    the value of genre
    :param genre: genre selected by user
    :param genre_dict: dictionary of pairs in the format:
                        "{book} by {author}" : "genre"
    :return: randomly selected book within a particular genre
    """
    genre_list = []
    for books in genre_dict:
        if genre_dict[books] == genre:
            genre_list.append(books)

    # exception handling -- this comes in handy if the user keeps rejecting the book suggestions within a particular
    # genre choice, as (len(genre_list) - 1) will become negative and an invalid input for random.randint(a, b)
    try:
        return genre_list[random.randint(0, len(genre_list) - 1)]
    except ValueError:
        return None


def suggest_book_by_genre(genre, genre_dict, genre_list):
    """
    prints a formatted suggestion of a book within a particular genre and asks if the user wants a new suggestion
    :param genre: selected by user
    :param genre_dict: dictionary of pairs in the format:
                        "{book} by {author}" : "genre"
    :param genre_list:  array of genres in genre dict, with no duplicates
    :return: n/a
    """
    suggestion = random_book_by_genre(genre, genre_dict)

    if suggestion is None:
        out_of_genre_books(genre, genre_dict, genre_list)

    print(f"In my opinion, you should read {suggestion}.")

    while True:
        answer = input("Do you like this suggestion? If not, I'll think of a new book. (yes or no)\n")
        if answer.lower() == 'yes':
            print("Thank you for taking my suggestion! Feel free to ask again anytime.")
            sys.stdout.write("Exiting...")
            sys.stdout.flush()
            time.sleep(2)
            quit()
        elif answer.lower() == 'no':
            print("I'm sorry for picking a dud. Let me pick again...")
            load()
            del genre_dict[suggestion]
            suggest_book_by_genre(genre, genre_dict, genre_list)
            break
        else:
            print("Invalid response. Try again, 'yes' or 'no'?")


def remove_duplicates(original_list):
    """
    removes duplicate items from original_list, keeping first instance of duplicate
    :param original_list: list that contains duplicate items
    :return: list without duplicate items, keeping the first instance of the duplicated item
    """
    final_list = []
    for item in original_list:
        if item not in final_list:
            final_list.append(item)
    return final_list


def dict_genres(json_data):
    """
    compiles a dictionary of book-genre pairs from json_data
    :param json_data: json data provided by the Goodreads API for a given user shelf
    :return: dictionary of pairs in the format:
                        "{book} by {author}" : "genre"
    """
    total = json_data["GoodreadsResponse"]['reviews']["@total"]
    genre_dict = {}
    for i in range(0, int(total)):
        title = json_data["GoodreadsResponse"]["reviews"]["review"][i]["book"]["title"]
        author = json_data["GoodreadsResponse"]["reviews"]["review"][i]["book"]["authors"]["author"]["name"]
        book_id = json_data["GoodreadsResponse"]["reviews"]["review"][i]["book"]["id"]["#text"]
        genre = goodreads.get_genre(book_id)

        genre_dict[f"{title} by {author}"] = genre

    return genre_dict


def random_book(json_data):
    """
    selects a random book out of all books on a given user shelf via json_data
    :param json_data: json data provided by the Goodreads API for a given user shelf
    :return: string of a books title and author
    """
    total = json_data["GoodreadsResponse"]['reviews']["@total"]
    book_index = random.randint(1, int(total))

    title = json_data["GoodreadsResponse"]["reviews"]["review"][book_index]["book"]["title"]
    author = json_data["GoodreadsResponse"]["reviews"]["review"][book_index]["book"]["authors"]["author"]["name"]

    return f"{title} by {author}"


def load():
    """
    prints a loading bar graphic for aesthetic purposes
    :return: n/a
    """
    for i in range(74):
        sys.stdout.write('~')
        sys.stdout.flush()
        time.sleep(.02)
    print("")


def suggest_book(json_data):
    """
    prints a formatted suggestion of a book on a specific shelf and asks if the user wants a new suggestion
    :param json_data: json data provided by the Goodreads API for a given user shelf
    :return: n/a
    """
    print(f"In my opinion, you should read {random_book(json_data)}.")

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
            suggest_book(json_data)
            break
        else:
            print("Invalid response. Try again, 'yes' or 'no'?")


def main():
    """
    suggests a book for the user to read via the Goodreads API, guided by user input for shelf and genre selection
    :return: n/a
    """
    print("Hello!\nDon't know what to read next? Let me help with that! "
          "I'll pick a book from one of your Goodreads shelves.\n")

    user_id = input("Enter your Goodreads id: ")

    shelf_list = show_shelves(user_id)

    while True:
        shelf = input("Enter the name of the shelf for me to pick from: ")
        if shelf not in shelf_list:
            print("Sorry, invalid shelf. Please pick from the list above.")
        else:
            break

    print(f"Examining the books on {shelf}...")
    json_shelf_data = goodreads.get_shelf(user_id, shelf)

    while True:
        specific_genre = input("Would you like me to pick a book of a specific genre? (yes or no)\n").lower()

        if specific_genre == 'yes':
            print(f"Here is a list of the genres you have on '{shelf}':")

            load()
            print("")
            genre_dict = dict_genres(json_shelf_data)
            genre_list = []

            for books in genre_dict:
                genre_list.append(genre_dict[books])

            genre_list = remove_duplicates(genre_list)

            for genre in genre_list:
                print(f"                [+] {genre}")

            print("")
            load()

            while True:
                selected_genre = input("Out of those genres, what are you feeling?\n").lower()
                if selected_genre not in genre_list:
                    print("Invalid genre. Please pick from the list above.")
                else:
                    break

            print(f"Considering {selected_genre} books on your shelf...")
            load()
            suggest_book_by_genre(selected_genre, genre_dict, genre_list)
            break
        elif specific_genre == 'no':
            load()
            suggest_book(json_shelf_data)
            break
        else:
            print("Invalid response. Try again, 'yes' or 'no'?")


if __name__ == "__main__":
    main()
