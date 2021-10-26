from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
import os

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    full_name = Column(String(64), nullable=False)
    login = Column(String(24), nullable=False, unique=True)
    password = Column(String(48), nullable=False)
    email = Column(String(80), nullable=False, unique=True)

class Major(Base):
    __tablename__ = 'major'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    name = Column(String(80), nullable=False, unique=True)

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    name = Column(String(80), nullable=False, unique=True)

class Mark(Base):
    __tablename__ = 'mark'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    subject_id = Column(Integer(), ForeignKey('subject.id'))
    grade = Column(Integer, nullable=False)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), autoincrement=True, primary_key=True, unique=True)
    name = Column(String(64), nullable=False)
    major_id = Column(Integer(), ForeignKey('major.id'))
    rating = Column(Integer(), nullable=False)

class StudentMark(Base):
    __tablename__ = 'student_mark'
    student_id = Column(Integer(), ForeignKey('student.id'), primary_key=True)
    mark_id = Column(Integer(), ForeignKey('mark.id'), primary_key=True)