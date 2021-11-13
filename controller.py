from flask import Flask, request
from flask_bcrypt import Bcrypt
import schemas
import commands
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

# ======== USER ========

@app.route('/user', methods=['POST'])
def userRoot():
    try:
        schema = schemas.UserSchema()
        data = request.json
        userInfo = schema.load(data)
    except ValidationError as err:
      return f'Validation error.\n{err}', 400
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
        commands.AddUser(userInfo)
    except IntegrityError as err:
      return f'User with the same email or login already exists', 403
    except Exception as err:
      return f'Internal server error. {err}', 500

    return f'User added successfully'

@app.route('/user/login', methods=['GET'])
def userLogin():
  try:
    schema = schemas.LoginSchema()
    data = request.json
    loginInfo = schema.load(data)
  except ValidationError as err:
    return f'Validation error.\n{err}', 400
  except Exception as err:
    return f'Internal server error. {err}', 500
  
  try:
    commands.Login(loginInfo)
  except ValueError as err:
    return f'Incorrect username / password', 400
  except Exception as err:
    return f'Internal server error. {err}', 500
  
  return 'Successful login!'

# CAN'T IMPLEMENT WITHOUT AUTH !!!
@app.route('/user/logout', methods=['GET'])
def userLogout():
  # IMPLEMENT 500
  return 'Logout success?'

@app.route('/user/<login>', methods=['GET', 'PUT', 'DELETE'])
def userHandling(login):
  if request.method == 'GET':
    try:
      schema = schemas.ValidateUserFieldsSchema().load({"login": login})
    except ValidationError as err:
      return f'{err}', 400
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
      userInfo = commands.GetUserInfo(login)
      displayValue = f'''
      full_name = {userInfo.full_name}; 
      login = {userInfo.login}; 
      email = {userInfo.email}; 
      '''
    except ValueError as err:
      return f'{err}', 404
    except Exception as err:
      return f'Internal server error. {err}', 500
    return f'{displayValue}'

  elif request.method == 'PUT':
    userInfo = None
    try:
      schema = schemas.ValidateUserFieldsSchema()
      data = request.json
      userInfo = schema.load(data)
    except ValidationError as err:
      return f'Validation error.\n{err}', 400
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
      commands.UpdateUserInfo(login, userInfo)
    except ValueError as err:
      return f'{err}', 404
    except IntegrityError as err:
      return f'Already exists', 403
    except Exception as err:
      return f'Internal server error. {err}', 500
    return f'Info changed successfully'

  elif request.method == 'DELETE':

    try:
      schema = schemas.ValidateUserFieldsSchema().load({"login": login})
    except ValidationError as err:
      return f'{err}', 400
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
      commands.DeleteUser(login)
    except ValueError as err:
      return f'{err}', 404
    except Exception as err:
      return f'Internal server error. {err}', 500
    return f'Deleted {login}'

# ======== Student ========

@app.route('/student', methods=['POST'])
def studentRoot():
    try:
        schema = schemas.StudentSchema()
        data = request.json
        studentInfo = schema.load(data)
    except ValidationError as err:
      return f'Validation error.\n{err}', 400
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
        commands.AddStudent(studentInfo.copy())
    except Exception as err:
      return f'Internal server error. {err}', 500
    return f'{studentInfo}'     

@app.route('/student/<id>', methods=['GET', 'PUT', 'DELETE'])
def studentHandling(id):
    if request.method == 'GET':
        try:
          schema = schemas.ValidateStudentFieldsSchema().load({"id": id})
        except ValidationError as err:
          return f'Not a valid integer', 400
        except ValueError as err:
          return f'{err}', 404
        except Exception as err:
          return f'Internal server error. {err}', 500

        try:
          studentInfo = commands.GetStudent(id)
          displayStudent = f'''
              name = {studentInfo['name']};
              major = {studentInfo['major']['name']};
              rating = {studentInfo['rating']};
              marks = {studentInfo['marks']};

          '''
        except ValueError as err:
          return f'{err}', 404
        except Exception as err:
          return f'Internal server error. {err}', 500
        return f'{displayStudent}'
    elif request.method == 'PUT':
        studentInfo = None
        try:
          schema = schemas.ValidateStudentFieldsSchema()
          data = request.json
          studentInfo = schema.load(data)
        except ValidationError as err:
          return f'Validation error.\n{err}', 400
        except Exception as err:
          return f'Internal server error. {err}', 500

        try:
          commands.UpdateStudentInfo(id, studentInfo)
        except ValueError as err:
          return f'{err}', 404
        except IntegrityError as err:
          return f'Already exists', 403
        except Exception as err:
          return f'Internal server error. {err}', 500

        return f'Info changed successfully'
    elif request.method == 'DELETE':
        try:
          schema = schemas.ValidateStudentFieldsSchema().load({"id": id})
        except ValidationError as err:
          return f'{err}', 400
        except Exception as err:
          return f'Internal server error. {err}', 500

        try:
          commands.DeleteStudent(id)
        except ValueError as err:
          return f'{err}', 404
        except Exception as err:
          return f'Internal server error. {err}', 500

        return f'Deleted {id}'

@app.route('/university/<top>', methods=['GET'])
def universityTop(top):
    try:
        if int(top) < 1:
            return f'Enter number more than 0', 400
        result = commands.GetStudentsTopRank(int(top))
    except ValueError as err:
        return f'Enter number. Not a string or decimal', 404
    except Exception as err:
      return f'Internal server error. {err}', 500

    try:
        displayValue = f''''''
        for key, value in result.items():
            displayStudent = f'''
              name = {value['name']};
              major = {value['major']['name']};
              rating = {value['rating']};
              marks = {value['marks']};

            '''
            displayValue = displayValue + displayStudent
        if int(top) > len(result):
            return f'{displayValue} \n{top} students was asked to show, but there are only {len(result)} of them'
        else:
            return f'{displayValue}'
    except Exception as err:
      return f'Internal server error. {err}', 500

if __name__ == '__main__':
  app.run(host='localhost', port='5000', debug=True)
