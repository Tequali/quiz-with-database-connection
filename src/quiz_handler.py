from .db_handler import DBHandler
import random
import time
from stringcolor import cs
from dataclasses import dataclass


@dataclass
class Question:
    topic: str = ""
    submodule: str = "Unknown"
    difficulty: int = 1
    question: str = ""
    correct_answer: str = ""
    wrong_answer1: str = ""
    wrong_answer2: str = ""
    wrong_answer3: str = ""


class Quiz:
    def __init__(self):
        """
        Initialises the quiz and its components

        Initialises the database connector
        Gets the IDs of all existing questions in the database
        Initialises the score of the quiz to 0
        """
        self.db_connection = DBHandler()
        # contains names of all possible tables/topics inside a list
        self.tables: list = (
            self.get_tables()
        )  # <= needs update to only include tables with at least 5 questions
        self.quiz_tables = self.get_suitable_quiz_tables()
        self.question_ids: list = []
        self.score = 0
        # add conditions to the preload_questions function to only work if the database is empty or doesnt exist
        self.preload_questions()

    def take_quiz(self):
        """
        Runs the quiz for the user

        Selects a random topic from the list of available topics
        Resets the score
        Selects a number of random questions from the database
        Shuffles them
        Asks the user each question
        Checks if the answer is correct
        Adds 1 to the score if the answer is correct
        Prints the possible score at the end
        """
        # region prepwork
        topic_name: str = random.choice(self.quiz_tables)
        self.score = 0
        self.question_ids = self.get_amount_of_questions(topic_name)
        selected_questions: list = (
            self.select_questions()
        )  # <= selects 5 random questions
        random.shuffle(selected_questions)
        # endregion
        print(cs(f"Topic: {topic_name}", "yellow"))
        print(cs(f"Selected questions: {selected_questions}", "yellow"))
        for question_id in selected_questions:
            self.db_connection.connect_to_db()
            fetched_query = self.db_connection.fetch_question(topic_name, question_id)
            self.db_connection.close_connection()
            question: dict = fetched_query[0]
            print(cs(f"Question: {question['question']}", "yellow"))
            anwers: list = [
                question["correct_answer"],
                question["wrong_answer1"],
                question["wrong_answer2"],
                question["wrong_answer3"],
            ]
            random.shuffle(anwers)
            for answer in anwers:
                print(cs(f"{anwers.index(answer)+1}. {answer}", "yellow"))
            user_answer = input(
                "Enter your answer, please enter the text after the number:\n"
            )
            if user_answer == question["correct_answer"]:
                print(cs("Correct!", "yellow"))
                self.score += 1
            else:
                print(cs("Incorrect!", "yellow"))
                print(
                    cs(
                        f"The correct answer is: {question['correct_answer']}",
                        "#d48824",
                    )
                )
            time.sleep(1.5)
        print("The possible score is:", len(selected_questions))
        print("Your score is:", self.score)
        return

    def select_questions(self) -> list:
        """
        Selects 5 random questions from the existing questions in the database
        Returns it to the take_quiz function
        """
        selected_questions = []
        if not self.question_ids:
            print("There are no questions in the database")
            return []
        else:
            selected_questions = random.sample(range(1, len(self.question_ids) + 1), 5)
            return selected_questions

    def add_question(self):
        """
        Asks the user for input to add a new question
        Input will be stored in a list which will be passed to the database handler
        """
        print("Here are the available topics that already exist: ", self.tables)
        lacking_tables = []
        question_to_be_added = Question()
        for table in self.tables:
            if table not in self.quiz_tables:
                lacking_tables.append(table)
        if lacking_tables:
            print(
                "And here is a list of tables that don't have enough questions: ",
                lacking_tables,
            )
        while True:
            table_name = input("Enter the name of the table: ")
            if table_name:
                question_to_be_added.topic = table_name
                break
        sub_module = input("Enter the sub module (optional): ")
        if not sub_module:
            sub_module = "Unknown"
        question_to_be_added.submodule = sub_module
        while True:
            difficulty = input("Enter the difficulty: ")
            if difficulty.isnumeric():
                question_to_be_added.difficulty = int(difficulty)
                break
        while True:
            question = input("Enter the question: ")
            if question:
                question_to_be_added.question = question
                break
        while True:
            correct_answer = input("Enter the correct answer: ")
            if correct_answer:
                question_to_be_added.correct_answer = correct_answer
                break
        while True:
            wrong_answer1 = input("Enter the wrong answer 1: ")
            if wrong_answer1:
                question_to_be_added.wrong_answer1 = wrong_answer1
                break
        while True:
            wrong_answer2 = input("Enter the wrong answer 2: ")
            if wrong_answer2:
                question_to_be_added.wrong_answer2 = wrong_answer2
                break
        while True:
            wrong_answer3 = input("Enter the wrong answer 3: ")
            if wrong_answer3:
                question_to_be_added.wrong_answer3 = wrong_answer3
                break
        # mock with patch inputs for while loops with pytest
        # maybe even mock the whole function

        self.db_connection.add_question(question_to_be_added)
        self.tables = self.get_tables()
        self.quiz_tables = self.get_suitable_quiz_tables()
        return question_to_be_added

    def get_amount_of_questions(self, topic_name: str) -> list:
        """Get the IDs from all the questions that exist"""
        self.db_connection.connect_to_db()
        result: list = self.db_connection.get_question_ids(topic_name)
        self.db_connection.close_connection()
        return result

    def get_tables(self) -> list:
        """
        Get a list of all existing tables in the database
        """
        result: list = []
        self.db_connection.connect_to_db()
        self.db_connection.messenger.execute(
            "SELECT * FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        )
        query_result: list = self.db_connection.messenger.fetchall()
        if not query_result:
            print("There are no tables in the database")
        else:
            for table in query_result:
                result.append(table[2])
        self.db_connection.close_connection()
        return result

    def get_suitable_quiz_tables(self) -> list:
        result: list = []
        self.db_connection.connect_to_db()
        self.db_connection.messenger.execute(
            """
            SELECT 
                relname AS table_name
            FROM 
                pg_stat_user_tables
            WHERE 
                n_live_tup >= 5;
            """
        )
        query_result: list = self.db_connection.messenger.fetchall()
        if not query_result:
            print("There are no tables in the database")
        else:
            for table in query_result:
                result.append(table[0])
        self.db_connection.close_connection()
        return result

    def preload_questions(self):
        """
        If the table "yugioh" does not exist, create it and fill it with questions
        from the file "initial_questions.sql"
        """

        if not self.db_connection.find_table("yugioh"):
            self.db_connection.create_new_topic_table("yugioh")

            # needs to reestablish a connection, because "create_new_topic_table" already connects and then disconnects real fast
            self.db_connection.connect_to_db()
            with open("src/initial_questions.sql", "r") as file:
                sql_script = file.read()
                self.db_connection.messenger.execute(sql_script)
                self.db_connection.db_connection.commit()
            self.db_connection.close_connection()
        return


if __name__ == "__main__":
    test = Quiz()
