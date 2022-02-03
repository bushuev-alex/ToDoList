from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Task:

    today: datetime

    def __init__(self, sql_table):
        self.today = datetime.today()
        self.day_today = self.today.day
        self.weekday = self.today.weekday()
        self.fullname_weekday = self.today.strftime('%A')
        self.time_today = self.today.time
        self.month_today = self.today.strftime('%b')
        self.sql_table = sql_table

    def menu(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

    def new_choice(self):
        return int(input())

    def view_today_tasks(self):
        print('Today ' + str(self.day_today) + ' ' + self.month_today + ':')
        rows = session.query(self.sql_table).filter(self.sql_table.deadline == self.day_today).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for row in rows:
                print(row)
        print()

    def view_week_tasks(self):
        for day in range(0, 7):
            new_day = self.today + timedelta(days=day)
            fullname_weekday = new_day.strftime('%A')
            day_today = new_day.day
            rows = session.query(self.sql_table).filter(self.sql_table.deadline == new_day.date()).all()
            print(fullname_weekday + ' ' + str(day_today) + ' ' + self.month_today + ':')
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                for row in rows:
                    print(row)
            print()

    def all_tasks(self):
        print('All tasks:')
        rows = session.query(self.sql_table).order_by(self.sql_table.deadline).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
        print()

    def missed_tasks(self):
        rows = session.query(self.sql_table).filter(self.sql_table.deadline < self.today.date()).order_by(self.sql_table.deadline).all()
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
        print()

    def enter_task(self):
        new_task = input('Enter task:\n')
        new_deadline = datetime.strptime(input('Enter deadline:\n'), '%Y-%m-%d')
        new_row = self.sql_table(task=new_task, deadline=new_deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')
        print()

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        rows = session.query(self.sql_table).order_by(self.sql_table.deadline).all()
        if len(rows) == 0:
            print('Nothing to delete!\n')
        else:
            for row in rows:
                print(str(row.id) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + str(row.deadline.strftime('%b')))
            session.query(self.sql_table).filter(self.sql_table.id == int(input())).delete()
            session.commit()
            print('The task has been deleted!\n')

My_journal = Task(Table)

while True:
    My_journal.menu()
    my_choice = My_journal.new_choice()
    print()
    if my_choice == 1:
        My_journal.view_today_tasks()
    elif my_choice == 2:
        My_journal.view_week_tasks()
    elif my_choice == 3:
        My_journal.all_tasks()
    elif my_choice == 4:
        My_journal.missed_tasks()
    elif my_choice == 5:
        My_journal.enter_task()
    elif my_choice == 6:
        My_journal.delete_task()
    else:
        print('Bye!')
        break
