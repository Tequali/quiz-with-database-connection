from stringcolor import cs
from src import Quiz
from time import sleep


def main():
    """
    Main function of the program.

    This function creates an instance of the Quiz class
    and then enters a loop where it prints a menu
    with options to the user. Depending on the user's
    input, it will either start a quiz, add a question
    or exit the program.
    """
    quiz = Quiz()
    while True:
        print(cs("---------------------------------", "green"))
        print(cs("Welcome to our database filled with questions!", "yellow"))
        print(cs("Here are the options available to you:", "yellow"))
        print(cs("1. Take a quiz", "yellow"))
        print(cs("2. Add a question to a topic", "yellow"))
        print(cs("2. Show all topics", "yellow"))
        print(cs("4. Exit", "yellow"))
        print(cs("The Database is saving questions for you!", "orange"))
        print(cs("---------------------------------", "green"))
        option = input(cs("Please select an option: ", "yellow"))
        if option == "1":
            print(cs("You have selected to take a quiz.", "blue"))
            sleep(1.5)
            # take_quiz()
            quiz.take_quiz()
        elif option == "2":
            print(cs("You have selected to add a question.", "blue"))
            sleep(1.5)
            # add_question()
            quiz.add_question()
        elif option == "3":
            print(cs("You have selected to show all topics.", "blue"))
            sleep(1.5)
            # show_topics()
            print(quiz.get_tables())
        elif option == "4":
            print(cs("Goodbye!", "green"))
            sleep(0.1)
            break
        else:
            print(cs("Invalid option. Please try again.", "red"))
            sleep(1.5)


if __name__ == "__main__":
    main()
