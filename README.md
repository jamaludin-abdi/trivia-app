# Full Stack Trivia Project

This project is a simple trivia app to test general knowledge. This project consists of the following features:
1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.

2. Delete questions.

3. Add questions and require that they include question and answer text.

4. Search for questions based on a text query string.

5. Play the quiz game, randomizing either all questions or within a specific category.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 
 

## Getting Started

### Pre-requisites and Local Development 
You should already have Python3.7, pip and node installed on their local machines. It is recommended to use a python virtual environment to keep package version consistency. The projects consists of two major parts in two folders:- backend and frontend.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands in the backend folder: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed

### Endpoints 
#### GET /api/categories
- General:
    - Returns a list of categories.
- Sample: `curl http://127.0.0.1:5000/api/categories`

``` {
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"success": true
}
```

#### GET /api/questions
- General:
    - Gets a list of questions with categories and total number of questions
    - Results are paginated in groups of 10.Include a request argument to choose page number, starting from 1
- Sample: `curl http://127.0.0.1:5000/api/questions?page=1`
- Response:
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
	"currentCategory": null,
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
	"totalQuestions": 19
}
```
#### DELETE /api/questions/\<int:id\>
- General:
  * Deletes a question by id using url parameters.
  * Returns id of deleted question upon success.
- Sample: `curl http://127.0.0.1:5000/api/questions/1 -X DELETE`
- Response: 
```
        {
            "question_id": 1, 
            "success": true
        }
```
#### POST /api/questions

This endpoint creates a new question
- General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question, as well as paginated questions.
 - Sample: `curl http://127.0.0.1:5000/api/questions -X POST -H "Content-Type: application/json" -d '{
	        "question": "what comes after 1?",
			"answer": "two",
			"difficulty": 1,
			"category": 1
        }'`<br>
 
 - Response: `{"success": true}`
        
#### POST /api/questions/search
- General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with paginated matching questions.
 - Sample: `curl http://127.0.0.1:5000/api/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "auto"}'`
 - Response:
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```

#### GET /api/categories/\<int:id\>/questions

- General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated questions that belong to that category.
- Sample: `curl http://127.0.0.1:5000/api/categories/1/questions`
- Response:
```
{
  "currentCategory": "Science",
  "questions": [
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
      "answer": "two",
      "category": 1,
      "difficulty": 1,
      "id": 25,
      "question": "what comes after 1?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```

#### POST /api/quizzes

* General:
  * Allows users to play the quiz game.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question not among previous questions.
* Sample: `curl http://127.0.0.1:5000/api/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21],"quiz_category": {"type": "Science", "id": "1"}}'`
- Response:
```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

## Deployment N/A

## Authors
Jamaludin Abdi edited some files inside backend and frontend
## Acknowledgements
The awesome team at Udacity that supplied main source folder
