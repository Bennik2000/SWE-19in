from vereinswebseite import db
from vereinswebseite.models import User, Article


def insert_dummy_users():
    db.session.add(User("Max Mustermann", "max.mustermann@email.com", "123456"))
    db.session.add(User("Kristin Krause ", "kristin.krause@email.com", "123456"))
    db.session.add(User("Dieter Goldschmidt", "dieter.goldschmidt@email.com", "123456"))

    db.session.add(Article("First article", "Content of first article, lorem ipsum dolor sit amet", "1"))
    db.session.add(Article("Second article", "Content of second article, lorem ipsum dolor sit amet", "1"))
    db.session.add(Article("Third article", "Content of third article, lorem ipsum dolor sit amet", "2"))

    db.session.commit()


# CAUTION: This will delete all data and create a new database!
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    insert_dummy_users()
