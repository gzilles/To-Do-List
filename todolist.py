# Import libraries
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Create database
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
# Describe table
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    def __str__(self):
        return self.task


# Create table
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()


# Create new row
def create_new_row():
    print('\nEnter task')
    task = input('> ')
    print('Enter deadline')
    deadline = datetime.strptime(input('> '), '%Y-%m-%d')
    new_row = Table(task=task, deadline=deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!')


# Select all rows
def select_all_rows():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('\nAll tasks:')
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            print('{}. {}. {} {}'.format(i + 1, rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b')))


# Select today rows
def select_today_rows():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print('\nToday {} {}:'.format(today.day, today.strftime('%b')))
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            print('{}. {}'.format(i + 1, rows[i].task))


# Select week rows
def select_week_rows():
    today = datetime.today()
    weekdays = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for i in range(7):
        print('\n{} {} {}:'.format(weekdays[today.weekday()], today.day, today.strftime('%b')))
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        today += timedelta(days=1)
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for j in range(len(rows)):
                print('{}. {}'.format(j + 1, rows[j].task))


# Select missed rows
def select_missed_rows():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).all()
    print('\nMissed tasks:')
    if len(rows) == 0:
        print('Nothing is missed!')
    else:
        for i in range(len(rows)):
            print('{}. {}. {} {}'.format(i + 1, rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b')))


# Delete specific row
def delete_specific_row():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('\nChoose the number of the task you want to delete:')
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            print('{}. {}. {} {}'.format(i + 1, rows[i].task, rows[i].deadline.day, rows[i].deadline.strftime('%b')))
        delete_task = int(input('> '))
        session.delete(rows[delete_task - 1])
        session.commit()
        print('The task has been deleted!')


# Create menu
def create_menu():
    menu = True
    while menu:
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
        index = input('> ')
        if index == '1':
            select_today_rows()
        elif index == '2':
            select_week_rows()
        elif index == '3':
            select_all_rows()
        elif index == '4':
            select_missed_rows()
        elif index == '5':
            create_new_row()
        elif index == '6':
            delete_specific_row()
        elif index == '0':
            print('\nBye!')
            menu = False
        else:
            print('\nWrong input. Try again!')


create_menu()
