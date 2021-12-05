from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
import os

# CHANGE THIS SETTINGS IF YOU HAVE ANY DIFFERENT
DB_SCHEME = 'postgresql'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'test'
DB_SERVER = 'localhost'
DB_PORT = '5432'

# Not necessary to change
DB_NAME = 'denys_project'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = '{}://{}:{}@{}:{}/{}'.format(
    DB_SCHEME,
    DB_USERNAME,
    DB_PASSWORD,
    DB_SERVER,
    DB_PORT,
    DB_NAME
)
engine = create_engine(connection_string, echo=True)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    full_name = Column(String(64), nullable=False)
    login = Column(String(24), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    email = Column(String(80), nullable=False, unique=True)


class Major(Base):
    __tablename__ = 'major'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)


class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    name = Column(String(64), nullable=False)
    major_id = Column(Integer(), ForeignKey('major.id'), nullable=False)
    major = relationship('Major', backref='students')
    rating = Column(Integer(), nullable=False)


class Mark(Base):
    __tablename__ = 'mark'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    student_id = Column(Integer(), ForeignKey('student.id'))
    subject_id = Column(Integer(), ForeignKey('subject.id'))
    student = relationship('Student', backref='marks')
    subject = relationship('Subject', backref='marks')
    grade = Column(Integer(), nullable=False)
