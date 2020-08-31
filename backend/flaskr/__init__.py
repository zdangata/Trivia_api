import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]
    #current_questions = selection
    return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  
  #@TODO: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, DELETE, OPTIONS')
    return response
  
  '''
  @TODO: DONE
  #Create an endpoint to handle GET requests 
  #for all available categories.
  '''
  @app.route('/categories')
  def categories():
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    if (len(categories) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(categories)
    })


  '''
  @TODO: DONE
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions')
  def all_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    total_questions = len(selection)

    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    #if questions == 0:
    if (len(current_questions) == 0):
      abort(404)
    
    return jsonify({
      #'questions': questions,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': None,
      'success': True
      })
  
  '''
  @TODO: Works but gives an error message(422 unprocessable entity) whenever used
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      total_questions = len(selection)
      return jsonify({
        'success': True,
        'deleted': question_id,
        'total_questions': total_questions
        })
    
    except:
      abort(422)
  
  '''
  @TODO: DONE
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    body=request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    
    try:
      question = Question(question=new_question, answer=new_answer, difficulty=difficulty, category=category)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      total_questions = len(selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': total_questions
      })

    except:
      abort(422)
  
  '''
  @TODO: DONE
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def question_search():
    body=request.get_json()

    search_term = body.get('searchTerm', None)

    #sets selection equal to an array of all the questions which contain the string input, search_term
    try:
      if search_term:
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in selection]
        total_questions = len(selection)

        return jsonify({
          'questions': formatted_questions,
          'total_questions': total_questions,
          'current_category': None,
          'success': True
        })
      abort(404)

    except:
      abort(422)

  '''
  @TODO: DONE
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  # ask for explanation of app route selection. @app.route('/questions/<int:category_id>') 
  @app.route('/categories/<int:category_id>/questions')
  def question_sieve(category_id):
    try:
      selection = Question.query.filter(Question.category == category_id).all()   
    
      current_questions = paginate_questions(request, selection)
      total_questions = len(selection)

      if (len(current_questions) == 0):
        abort(404)

      return jsonify({
        'questions': current_questions,
        'total_questions': total_questions,
        'current_category': category_id,
        'success': True
      })
      
    except:
      abort(404)
      
  


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  
  @app.route('/quizzes', methods=['POST'])
  def question_generator():
    body = request.get_json()

    category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)

    if (category==None):
      abort(400)

    if (previous_questions==None):
      abort(400)

    #Creates a filtered list of questions based on the category selected
    if (category['id']==0):
      selection = Question.query.order_by(Question.id).all()

    else:
      selection = Question.query.filter(Question.category == category['id']).all()

    formatted_questions = [question.format() for question in selection]
    total_questions = len(selection)

    #chooses a random question from the selected category
    def choose_random_question():
      y =  random.randrange(0, total_questions, 1)
      question = formatted_questions[y]
      return question

    #checks if the randomly selected question has been used
    def check_in_previous(question):
      been_used = False
      for q in previous_questions:
        if (q==question['id']):
          been_used = True

      return been_used
    
    #choose random question
    question = choose_random_question()

    #create while loop. While length of array less than no. questions in category chosen, choose a random question from that category.
    while (check_in_previous(question)):
      question = choose_random_question()
      if (len(previous_questions) == total_questions):
        return jsonify({
          'success': True
          })

    # return the question
    return jsonify({
        'success': True,
        'question': question
    })

  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not allowed"
    }), 405

  @app.errorhandler(422)
  def not_processed(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    }), 422
    
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }), 500
  return app