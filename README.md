# Full Stack API Final Project

## Trivia API

This API powers a web application which allows people to play Trivia. In this game, users can interact with the app by:

1. Previewing all existing questions and searching for specific ones
2. Adding new questions and deleting existing ones
3. Playing the game. Here the application randomly selects questions and takes an answer from the user, calculating their score based on how many questions they answered correctly


## Getting Started

### Installing Dependencies
#### Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs.

#### Virtual Environment
We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

`pip install -r requirements.txt`

This will install all of the required packages we selected within the requirements.txt file.

Key Dependencies:

1. Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

2. SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

3. Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

`psql trivia < trivia.psql`

### Running the Server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

`export FLASK_APP=flaskr`

`export FLASK_ENV=development`

`flask run`

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

### Frontend Dependencies
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

`npm install`
#### Running your Frontend in Dev Mode
The frontend app was built using create-react-app. In order to run the app in development mode use npm start. You can change the script in the package.json file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

`npm start`
## Testing
To run the tests, run:

`dropdb trivia_test`

`createdb trivia_test`

`psql trivia_test < trivia.psql`

`python test_flaskr.py`


# API Reference
## Getting Started
Base URL: http://127.0.0.1:3000/

Authentication: Authentication or API keys are not used in the project yet.

## Error Handling
Errors will be returned in JSON and will use the format below:
  
      {
        "success": "False",
        "error": 404,
        "message": "resource not found",
      }
The error codes which may be returned are:

400-Bad request

404-Resource not found

405-Method not allowed

422-Unprocessable entity

500-Internal server error
## Endpoints
### GET /categories
* General:

    * Returns a list of each of the category objects and their unique id's
* Sample: `curl http://127.0.0.1:3000/categories`

    ```{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_categories": 6
    }
### GET /questions
* General:

    * First returns a list of the categories
    * Then returns a list of question objects, each with their corresponding answer, category number, difficulty and their unique id's
    * Paginated requests can be made (a limit of 10 questions to each page)
* Sample: `curl http://127.0.0.1:3000/questions`

    ```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "current_category": null,
        "questions": [
            {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
            },
            {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
            },
            {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
            },
            {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
            },
            {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
            },
            {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
            },
            {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
            },
            {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
            },
            {
            "answer": "Scarab",
            "category": 4,
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            }
        ],
        "success": true,
        "total_questions": 19
    }
### POST /questions
* General:

    * Creates a new question
    * Returns the number of the created question, a list of all the questions, the success status of the request and the new total of questions.
* Sample: `curl http://127.0.0.1:3000/questions -X POST -H "Content-Type: application/json" -d '{
    "question": "Why are there 50 stripes on the American Flag?",
    "answer": "There are 50 states in America",
    "category": "3",
    "difficulty": "2"
}'`
    ```
    {
    "created": 43,
    "questions": [
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
        },
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 21
    }

### DELETE /questions/<int:question_id>
* General:

    * Deletes a specific questions, using their unique id as in input
    * Returns the deleted question number, the success status of the request and the new total of questions.
* Sample: `curl http://127.0.0.1:3000/questions/44 -X DELETE -H "Content-Type: application/json"`

    ```
    {
        "deleted": 44,
        "success": true,
        "total_questions": 19
    }

### POST /questions/search
* General:

    * Allow user to search for questions
    * Finds all case insensitive matches for the input string the user enters in
    * Returns the number of the created question, a list of all the questions, the success status of the request and the new total of questions.
* Sample: `curl http://127.0.0.1:3000/questions -X POST -H "Content-Type: application/json" -d '{
    "question": "Why are there 50 stripes on the American Flag?",
    "answer": "There are 50 states in America",
    "category": "3",
    "difficulty": "2"
}'`

    ```
    {
        "current_category": null,
        "questions": [
            {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
            }
        ],
        "success": true,
        "total_questions": 1
    }

### POST /categories/<int:category_id>/questions
* General:

    * Returns questions by category
    * Takes category number as input from the user
* Sample: `curl http://127.0.0.1:3000/questions`
    ```
    {
        "current_category": 3,
        "questions": [
            {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
            },
            {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
            }
        ],
        "success": true,
        "total_questions": 3
    }
### POST /quizzes
* General:

    * Takes the current category and the previous questions
    * Returns random question which is not in previous questions
* Sample: `curl http://127.0.0.1:3000/quizzes -X POST -H "Content-Type: application/json" -d '{
    "previous_questions": [12, 13],
    "quiz_category": {
        "type": "Geography", 
        "id": "3"
        }
}`

    ```
    {
        "question": {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        "success": true
    }
## Authors
Udacity provided the starter files for the project as well as the frontend code.

Zanang Dangata worked on the API and the test suite to integrate with the frontend.

## Acknowledgements
Shout out to my mentor, Jonathan Carrol for guiding me through this process.

I would also like to thank Nicolas Georgiou, Andrew Muir, James Wilson, and Duncan Bailey for their support in this assignment.