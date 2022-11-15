import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

"""
Function for pagination of questions endpoint
"""


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Sets cors origins from *
    """
    CORS(app, resources={'/api': {'origins': '*'}})

    """
    Sets access control headers with after_request decorator
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response

    """ 
    Endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if (len(categories) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    """
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    It return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/api/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if (len(current_questions) == 0):
            abort(404)

        categories = Category.query.order_by(Category.type).all()

        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'currentCategory': None
        })

    """
    Endpoint to DELETE question using a question ID.
    """
    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'question_id': question_id
            })
        
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    """
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route('/api/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        if ((new_question is None) or (new_answer is None)
                or (new_difficulty is None) or (new_category is None)):
            abort(422)
        try:
            new_question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
            new_question.insert()

            return jsonify({
                'success': True
            })

        except:
            abort(422)

    """
    Endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """
    @app.route('/api/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        results = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term))).all()

        if (len(results) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in results],
            'totalQuestions': len(results),
            'current_category': None
        })

    """
    GET endpoint to get questions based on category.
    """
    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        results = Question.query.filter(
            Question.category == '{}'.format(category_id)).all()

        if (len(results) == 0):
            abort(404)

        category = Category.query.filter_by(id=category_id).one_or_none()
        return jsonify({
            'success': True,
            'questions': [question.format() for question in results],
            'totalQuestions': len(results),
            'currentCategory': category.type
        })

    """
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """
    @app.route('/api/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        if ((previous_questions is None) or (quiz_category is None)):
            abort(400)

        category_id = quiz_category['id']

        questions = Question.query.all(
        ) if category_id == 0 else Question.query.filter_by(category=category_id).all()

        num_questions = len(questions)

        """
        Fetch Random questions function
        """
        def get_random_question():
            return questions[random.randrange(0, num_questions, 1)]

        """
        Check question has been used
        """
        def check_if_used(question):
            used = False
            for ques in previous_questions:
                if ques == question.id:
                    used = True
            return used

        question = get_random_question()

        while (check_if_used(question)):
            question = get_random_question()

            if (len(previous_questions) == num_questions):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': question.format()
        })

    # error handlers for all expected errors

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }),
            422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False,
                "error": 400,
                "message": "bad request"
            }),
            400)

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({
                "success": False, 
                "error": 405,
                "message": "method not allowed"
            }),
            405)

    return app
