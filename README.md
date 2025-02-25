# Quiz_mini_project

## Command Line Quiz

In this project, you will create a quiz application that will allow users to test their knowledge on various topics. Also to enrich the topics and questions that are provided. The application will use command line input and output to communicate with the user.

## Prerequisites:

- Python 3.10 or later
- Python Modules: PyTest, Psycopg2
- PostgreSQL database

## Installation & Usage
To run the program follow these steps:
- Install Software & Modules mentioned in the chapter above
- download it as a zip
- unpack it in a directory/folder of your choice
- open a terminal
- type in:
  ```bash
  python main.py
  ```
- Type in one of the options from the chapter below
- If you select to take a quiz, write out the answer the same way it is shown to you
- If you select to add a topic/question you have to fill out all but one field as it will showcase "Unknown" in that case

## Options during use
- Take a quiz containing 5 questions from a random existing table
- Add new topics and questions
  - Shows existing topics that don't qualify for the quiz
- List all topics stored in the database
- Store and retrieve questions using PostgreSQL



## Features that may be added
- Take a quiz from a selected table
- user management to keep track of different users and their scores between sessions
  - indirectly introducing a leaderboard for different topics etc.
