import psycopg2
import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))


def check_connection(function):
    def inner(self, *args, **kwargs):
        if self.messenger:
            result = function(self, *args, **kwargs)
            return result
        else:
            print("Something is wrong with the connection")

    return inner


class DBHandler:
    def __init__(self):
        self.config: dict = {
            "db_name": env.str("DB_NAME"),
            "database_user": env.str("DB_USERNAME"),
            "postgres_host": env.str("DB_HOST"),
            "password": env.str("DB_PASSWORD"),
            "port": env.str("DB_PORT"),
        }

    def connect_to_db(self) -> None:
        # connect to postgres here
        try:
            self.db_connection = psycopg2.connect(
                database=self.config.get("db_name"),
                user=self.config.get("database_user"),
                host=self.config.get("postgres_host"),
                password=self.config.get("password"),
                port=self.config.get("port"),
            )
            self.messenger = self.db_connection.cursor()
        except psycopg2.OperationalError as err:
            print(str(err))
            self.db_connection = None
            self.messenger = None

    def refine_my_result(self, result: list) -> list:
        """
        Refine the result of the query
        then pack it up as a list of dictionaries and return it
        """
        data = []
        columns = self.messenger.description
        column_names = [x.name for x in columns]
        for row in result:
            data.append(dict(zip(column_names, row)))
        return data

    @check_connection
    def fetch_question(self, topic_name: str, question_id: int = 1) -> list:
        # fetch items
        try:
            query_string: str = "SELECT * FROM %s WHERE id = %%s;" % topic_name
            if not self.db_connection:
                self.connect_to_db()
            self.messenger.execute(query_string, str(question_id))
        except psycopg2.errors.UndefinedTable as error:
            print(str(error))
        else:
            items: list = self.messenger.fetchall()
            self.close_connection()
            refined_result = self.refine_my_result(items)
            return refined_result

    @check_connection
    def add_question(self, query: list) -> None:
        """
        [0] => main topic MUST BE FILLED
        [1] => sub topic
        [2] => difficulty MUST BE FILLED
        [3] => question MUST BE FILLED
        [4] => correct answer MUST BE FILLED
        [5] => wrong answer1 MUST BE FILLED
        [6] => wrong answer2 MUST BE FILLED
        [7] => wrong answer3 MUST BE FILLED
        """
        if self.find_table(query[0]):
            print("The topic table already exists")
        else:
            self.create_new_topic_table(query[0])
        try:
            self.connect_to_db()
            topic_name = query[0]
            query.pop(0)
            # query_string = f"{query[1]}, {query[2]}, {query[3]}, {query[4]}, {query[5]}, {query[6]}, {query[7]}"
            query_text = (
                """INSERT INTO %s (sub_module, difficulty, question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
                VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s);"""
                % topic_name
            )
            self.messenger.execute(query_text, (query))
        except psycopg2.OperationalError as e:
            print(f"Error {e}: Couldn't add the question in question...")
        else:
            self.db_connection.commit()
            self.close_connection()
        print("Adding your question was succesful")
        return

    def get_question_ids(self, topic_name: str) -> list:
        try:
            self.messenger.execute(f"SELECT id FROM {topic_name};")
        except psycopg2.OperationalError as e:
            print(f"Error {e}: Couldnt get the IDs from all the questions")
        else:
            result = self.messenger.fetchall()
            result = self.refine_my_result(result)
            new_result = [x["id"] for x in result]
            return new_result

    def close_connection(self) -> None:
        if self.db_connection:
            self.messenger.close()
            self.db_connection.close()

    def find_table(self, topic_name: str) -> bool:
        self.connect_to_db()
        self.messenger.execute(
            f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{topic_name}');"
        )
        result = self.messenger.fetchone()[0]
        self.close_connection()
        return result

    def create_new_topic_table(self, topic_name: str) -> None:
        # CREATE TABLE module_name (
        # id SERIAL PRIMARY KEY,
        # sub_module VARCHAR(100),
        # difficulty INT NOT NULL,
        # question TEXT NOT NULL,
        # correct_answer TEXT NOT NULL,
        # wrong_answer1 TEXT NOT NULL,
        # wrong_answer2 TEXT NOT NULL,
        # wrong_answer3 TEXT NOT NULL
        # );
        print("creating a new table")
        print("topic name:", topic_name)
        self.connect_to_db()
        self.messenger.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {topic_name} (
            id SERIAL PRIMARY KEY,
            sub_module VARCHAR(100),
            difficulty INT NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            wrong_answer1 TEXT NOT NULL,
            wrong_answer2 TEXT NOT NULL,
            wrong_answer3 TEXT NOT NULL
            );
            """
        )
        self.db_connection.commit()
        self.close_connection()
        print(f"A new table under the name of {topic_name} was created")
        return
