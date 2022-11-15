import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    tests for categories
    """
    def test_get_categories(self):
        """
        test for getting categories
        """
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    """
    Questions tests
    """

    def test_get_paginated_questions(self):
        """
        test for getting paginated questions
        """
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_request_beyond_valid_page(self):
        """
        test for getting beyond valid page
        """
        res = self.client().get('/api/questions?page=400')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question(self):
        """
        test for delete question
        """
        new_question = Question(question='What type of food is an apple?', answer='Fruit',
                            difficulty=1, category=1)
        new_question.insert()
        question_id = new_question.id

        res = self.client().delete('/api/questions/{}'.format(question_id))
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question_id'], question_id)

    def test_404_delete_non_existing_question(self):
        """
        test non-existent question
        """
        res = self.client().delete('/api/questions/142341243214222')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question(self):
        """
        test create question
        """
        new_question = {
            'question': 'what comes after 1?',
            'answer': 'two',
            'difficulty': 1,
            'category': 1
        }

        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_422_create_question(self):
        """
        test no body in create question
        """

        res = self.client().post('/api/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        """
        test successfully found search questions
        """
        search_term = {
            'searchTerm': 'bio'
        }
        res = self.client().post('/api/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['totalQuestions'])
    
    def test_404_search_questions(self):
        """
        test not found search questions
        """

        search_term = {
            'searchTerm': 'cdascdascsad'
        }

        res = self.client().post('/api/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')


    def test_get_questions_by_category(self):
        """
        test getting questions by category
        """

        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['totalQuestions'],0)
        self.assertEqual(data['currentCategory'], 'Science')

    def test_404_get_questions_by_category(self):
        """
        test not found questions
        """

        res = self.client().get('/api/categories/4231342/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
    """
    Quiz tests
    """

    def test_play_quiz(self):
        """
        test for playing quiz game with extra question
        """

        test_body = {
            'previous_questions': [2,4],
            'quiz_category': {'type': 'Entertainment', 'id': 5}
        }


        res = self.client().post('/api/quizzes',json=test_body)
        data = json.loads(res.data)


        # check response status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that a question is returned
        self.assertTrue(data['question'])

        # check that the question returned is in correct category
        self.assertEqual(data['question']['category'], 5)

        # check that question returned is not on previous q list
        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 4)
    
    def test_play_quiz_used(self):
        """
        test if all questions have been used
        """

        test_body = {
            'previous_questions': [2,4,6],
            'quiz_category': {'type': 'Entertainment', 'id': 5}
        }

        res = self.client().post('/api/quizzes',json=test_body)
        data = json.loads(res.data)
        
        expected = {'success': True}
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertDictEqual(data,expected)
    
    def test_400_play_quiz(self):
        """
        test if POST body is invalid
        """
        res = self.client().post('/api/quizzes', json={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
