import os
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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #create new question
        self.new_question = {
            'question': 'Why is the sky blue?',
            'answer': 'Because of the way the light refracts',
            'category': 1,
            'difficulty': 4
        }

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test for successful get request in questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #test for get request error behaviour in questions
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    #test for successful get request in categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    #test for get request error behaviour in categories
    def test_404_sent_requesting_beyond_valid_id(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #test for delete request in questions
    def test_delete_question(self):
        res = self.client().delete('/questions/47')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==47).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 47)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    #test for deletion of non-existant items in questions
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable entity')

    #test for creation of new question
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    #test for question creation which is not allowed
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('questions/1000', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #test for getting questions based on a search term
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'cassius clay'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        #self.assertEqual(len(data['questions']), 1)

    #test for getting question with a search term that has no matches 
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'hippy hitman'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)


    #test for question request based on categories
    def test_get_questions_based_on_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEquals(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)

    #test for getting question 
    def test_get_questions_for_invalid_category(self):
        res = self.client().get('/categories/8/questions', json={'category': 8})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEquals(data['success'], False)

    #test for selecting a category and generating random question in quizzes endpoint
    def test_select_category_to_generate_(self):
        #create mock data
        mock_data = {
            'previous_questions': [12, 13],
            'quiz_category': {
                'type': 'Geography',
                'id': 3
            }
        }
        res = self.client().post('/quizzes', json=mock_data)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        #check that question returned is not on the previous questions list
        self.assertNotEqual(data['question']['id'], 12)
        self.assertNotEqual(data['question']['id'], 13)

        #check that category is the currebt category (3)
        self.assertEqual(data['question']['category'], 3)

    #test for quizzes endpoint where no data is sent
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()