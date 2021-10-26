from sqlalchemy.orm import sessionmaker
from database_model import *

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

user1 = Users(full_name='Augustin Porebryk', login='augus', password='qwe123QWE', email='ap@gmail.com')
user2 = Users(full_name='Lavandos', login='lav', password='pirate', email='gaskjglasf@gmail.com')
session.add(user1)
session.add(user2)
session.flush()

major1 = Major(name='Physics')
major2 = Major(name='Math')
major3 = Major(name='Medicine')
major4 = Major(name='Literature')
major5 = Major(name='Computer Science')
session.add(major1)
session.add(major2)
session.add(major3)
session.add(major4)
session.add(major5)
session.flush()

subject1 = Subject(name='Applied Programming')
subject2 = Subject(name='Quantum Physics')
subject3 = Subject(name='Numerical Analysis')
subject4 = Subject(name='Ancient History')
session.add(subject1)
session.add(subject2)
session.add(subject3)
session.add(subject4)
session.flush()

student1 = Student(name='Yurii Stebelskij', major_id=major5.id, rating=100)
student2 = Student(name='Alex', major_id=major5.id, rating=4)
session.add(student1)
session.add(student2)
session.flush()

mark1 = Mark(student_id=student1.id, subject_id=subject3.id, grade=87)
mark2 = Mark(student_id=student1.id, subject_id=subject2.id, grade=42)
mark3 = Mark(student_id=student2.id, subject_id=subject2.id, grade=64)
mark4 = Mark(student_id=student2.id, subject_id=subject1.id, grade=2)
session.add(mark1)
session.add(mark2)
session.add(mark3)
session.add(mark4)
session.flush()

session.commit()

# session.add(Mark())


# locations = session.query(Location).all()
# users = session.query(Users).all()
# ads = session.query(Ad).all()
# for location in locations:
#     print('\n', location)

# for user in users:
#     print('\n', user)

# for ad in ads:
#     print('\n', ad)