from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from src import schemas
from src import commands
from src.main import session
from src.database_model import *
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_httpauth import HTTPBasicAuth


api_blueprint = Blueprint('api_blueprint', __name__)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login, password):
    found_user = session.query(Users).filter_by(login=login).first()
    if not found_user:
        return False
    try:
        if Bcrypt().check_password_hash(found_user.password, password):
            return found_user
    except ValueError:
        return False


# ======== USER ========

@api_blueprint.route('/user', methods=['POST'])
def userRoot():
    try:
        schema = schemas.UserSchema()
        data = request.json
        userInfo = schema.load(data)
    except ValidationError as err:
        return f'Validation error.\n{err}', 400

    try:
        commands.AddUser(userInfo)
    except IntegrityError as err:
        return f'User with the same email or login already exists', 403

    return f'User added successfully'


@api_blueprint.route('/user/login', methods=['GET'])
@auth.login_required
def userLogin():
    return 'Successful login!'


# ? No reason to implement this
@api_blueprint.route('/user/logout', methods=['GET'])
def userLogout():
    # data = request.json
    # login = data.pop('login', None)
    # if login is None:
    #     return f'No login provided', 400
    # try:
    #     schema = schemas.ValidateUserFieldsSchema().load({"login": login})
    # except ValidationError as err:
    #     return f'{err}', 400
    # except Exception as err:
    #     return f'Internal server error. {err}', 500

    # try:
    #     userInfo = commands.GetUserInfo(login)
    #     displayValue = f'''
    # full_name = {userInfo.full_name};
    # login = {userInfo.login};
    # email = {userInfo.email};
    # '''
    # except ValueError as err:
    #     return f'{err}', 404
    # except Exception as err:
    #     return f'Internal server error. {err}', 500
    # return f'{displayValue}'
    return 'Successful logout!'


@api_blueprint.route('/user/<login>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def userHandling(login):
    global auth
    logged_user_info = auth.current_user()

    if request.method == 'GET':
        try:
            schema = schemas.ValidateUserFieldsSchema().load({"login": login})
        except ValidationError as err:
            return f'{err}', 400

        try:
            userInfo = commands.GetUserInfo(login)
            displayValue = f'''
      full_name = {userInfo.full_name}; 
      login = {userInfo.login}; 
      email = {userInfo.email}; 
      '''
        except ValueError as err:
            return f'{err}', 404
        return f'{displayValue}'

    elif request.method == 'PUT':

        userInfo = None
        try:
            schema = schemas.ValidateUserFieldsSchema()
            data = request.json
            userInfo = schema.load(data)
        except ValidationError as err:
            return f'Validation error.\n{err}', 400

        if login != logged_user_info.login:
            return f'Access denied', 400

        try:
            commands.UpdateUserInfo(login, userInfo)
        except ValueError as err:
            return f'{err}', 404
        except IntegrityError as err:
            return f'Already exists', 403
        return f'Info changed successfully'

    elif request.method == 'DELETE':

        try:
            schema = schemas.ValidateUserFieldsSchema().load({"login": login})
        except ValidationError as err:
            return f'{err}', 400

        if login != logged_user_info.login:
            return f'Access denied', 400

        try:
            commands.DeleteUser(login)
        except ValueError as err:
            return f'{err}', 404
        return f'Deleted {login}'

# ======== Student ========


@api_blueprint.route('/student', methods=['POST'])
@auth.login_required
def studentRoot():
    try:
        schema = schemas.StudentSchema()
        data = request.json
        auth = data.pop('authorization', None)
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


@api_blueprint.route('/student/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def studentHandling(id):
    if request.method == 'GET':
        try:
            schema = schemas.ValidateStudentFieldsSchema().load({"id": id})
        except ValidationError as err:
            return f'Not a valid integer', 400
        except ValueError as err:
            return f'{err}', 404

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

        try:
            commands.DeleteStudent(id)
        except ValueError as err:
            return f'{err}', 404

        return f'Deleted {id}'


@api_blueprint.route('/university/<top>', methods=['GET'])
def universityTop(top):
    try:
        if int(top) < 1:
            return f'Enter number more than 0', 400
        result = commands.GetStudentsTopRank(int(top))
    except ValueError as err:
        return f'Enter number. Not a string or decimal', 404

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
