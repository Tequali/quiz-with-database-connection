# Quiz_mini_project

## Command Line Quiz

In this project, you will create a quiz application that will allow users to test their knowledge on various topics. Also to enrich the topics and questions that are provided. The application will use command line input and output to communicate with the user.

## Prerequisites:

- Python 3.10 or later
- PostgreSQL database

## Installation & Usage

To run the program follow these steps:

- Install Python if it is not already installed
- Create a PostgreSQL database called quiz_db
- Download it as a zip
- Unpack it in a directory/folder of your choice
- Open the .env file and adjust DB_USERNAME, DB_PASSWORD and DB_PORT to the fitting credentials to your local PostgreSQL server
- Open a terminal inside the folder
- Once inside the terminal, you have the following options of commands:
  Be sure to run "make install" first to ensure all necessary modules are installed

  ```bash
  make install <-- to install all necessary modules
  make run <-- runs the quiz application
  make test <-- runs all existing tests
  ```
- Type in one of the options from the chapter below
- If you select to take a quiz, write out the answer the same way it is shown to you
- If you select to add a topic/question you have to fill out necessary information

  - Submodule is not needed, in that case it will hold the value "Unknown"

## Options after running "make run"

- Take a quiz containing 5 questions from a random existing table as long as it has at least 5 questions
- Add (potentially new) topics and questions
  - Shows existing topics that don't qualify for the quiz
- List all topics stored in the database
- Store and retrieve questions using PostgreSQL

## Features that may be added

- Take a quiz from a selected table
- user management to keep track of different users and their scores between sessions
  - indirectly introducing a leaderboard for different topics etc.
