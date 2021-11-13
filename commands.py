from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from database_model import *
from controller import bcrypt
import schemas

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# ======== User ========

def AddUser(userInfo):
    try:
        userInfo['password'] = bcrypt.generate_password_hash(userInfo['password'])
        session.add(Users(**userInfo))
        session.commit()
    except Exception as err:
        session.rollback()
        raise err

def Login(loginInfo):
  try:
    result = session.query(Users).filter_by(login=loginInfo['login']).first()
    if result == None:
      raise ValueError('No user found')
    if bcrypt.check_password_hash(result.password, loginInfo['password']) != True:
      raise ValueError('Incorrect password')
  except Exception as err:
    session.rollback()
    raise err

def GetUserInfo(login):
  try:
    result = session.query(Users).filter_by(login=login).first()
    if result == None:
      raise ValueError('No user found')
    return result
  except Exception as err:
    session.rollback()
    raise err

def UpdateUserInfo(login, userInfo):
  try:
    isAny = session.query(Users).filter_by(login=login).first()
    if isAny == None:
      session.rollback()
      raise ValueError('No user found')
    if 'password' in userInfo:
        userInfo['password'] = bcrypt.generate_password_hash(userInfo['password'])
    session.query(Users).filter_by(login=login).update(userInfo)
    session.commit()
  except Exception as err:
    session.rollback()
    raise err

def DeleteUser(login):
  try:
    isAny = session.query(Users).filter_by(login=login).first()
    if isAny == None:
      session.rollback()
      raise ValueError('No user found')
    session.delete(isAny)
    session.commit()
  except Exception as err:
    session.rollback()
    raise err

# ======== Student ========

def AddStudent(studentInfo):
    try:
        # Major handling
        major_name = studentInfo['major']['name']
        isAny = session.query(Major).filter_by(name=major_name).first()
        if isAny == None:
          session.rollback()
          raise ValueError('No major found')
        studentInfo.pop('major')
        studentInfo['major_id'] = isAny.id

        # Student handling
        createStudentDict = studentInfo.copy()
        createStudentDict.pop('marks')
        session.add(Student(**createStudentDict))
        session.commit()

        # Mark handling
        if 'marks' in studentInfo:
            marks = studentInfo['marks']
            index = 0
            for mark in marks:
                markInfo = {}
                markInfo['student_id'] = (session.query(Student)
                                          .order_by(desc(Student.id))
                                          .limit(1)
                                          .first()).id
                subject = (session.query(Subject)
                                        .filter_by(name=studentInfo['marks'][index]['subject']['name'])
                                        .first())
                if subject == None:
                    raise ValueError('No subject found')
                markInfo['subject_id'] = subject.id
                markInfo['grade'] = studentInfo['marks'][index]['grade']
                session.add(Mark(**markInfo))
                index += 1
        session.commit()
    except Exception as err:
        session.rollback()
        raise err

def GetStudent(id):
    try:
      student = session.query(Student).filter_by(id=id).first()
      if student == None:
          raise ValueError('No student found')
      major = session.query(Major).filter_by(id=student.major_id).first()
      marks = session.query(Mark).filter_by(student_id=student.id).all()

      student.major = major
      student.marks = marks
      studentInfo = schemas.StudentSchema().dump(student)
      return studentInfo
    except Exception as err:
      session.rollback()
      raise err

def UpdateStudentInfo(id, studentInfo):
    try:
      marks = studentInfo.get('marks', None)
      studentInfo.pop('marks')

      student = session.query(Student).filter_by(id=id).first()
      if student == None:
        session.rollback()
        raise ValueError('No student found')
      if 'major' in studentInfo:
          major = session.query(Major).filter_by(name=studentInfo['major']['name']).first()
          if major != None:
              studentInfo.pop('major')
              studentInfo['major_id'] = major.id
          else:
              raise ValueError('No major found')
      session.query(Student).filter_by(id=id).update(studentInfo)
      session.commit()

      if marks != None:
        index = 0
        for mark in marks:
            markInfo = {}
            markInfo['student_id'] = id
            subject = (session.query(Subject)
                                    .filter_by(name=marks[index]['subject']['name'])
                                    .first())
            if subject == None:
                raise ValueError('No subject found')
            markInfo['subject_id'] = subject.id
            markInfo['grade'] = marks[index]['grade']
            session.add(Mark(**markInfo))
            index += 1
        session.commit()
    except Exception as err:
      session.rollback()
      raise err

def DeleteStudent(id):
    try:
        marks = session.query(Mark).filter_by(student_id=id).all()
        if marks != None:
            for mark in marks:
                session.delete(mark)
                session.commit()
            
        student = session.query(Student).filter_by(id=id).first()
        if student == None:
          session.rollback()
          raise ValueError('No user found')
        session.delete(student)
        session.commit()
    except Exception as err:
        session.rollback()
        raise err

# ======== University ========

def GetStudentsTopRank(top):
    try:
        students = session.query(Student).order_by(desc(Student.rating)).limit(top).all()
        if students == None:
            session.rollback()
            raise ValueError('No user found')
        
        result = {}
        index = 1
        for student in students:
            result[f'Student {index}'] = schemas.StudentSchema().dump(student)
            index += 1
        return result
    except Exception as err:
        session.rollback()
        raise err
