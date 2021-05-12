from flask_mail import Mail, Message

from vereinswebseite.models.user import User

mail = Mail()


def send_reset_password_email(user: User, reset_url: str):
    send_email("Passwort zurücksetzen",
               "Hallo " + user.name +
               ",\n"
               "benutze diesen Link um dein Passwort zurückzusetzen:\n"
               + reset_url +
               "\n"
               "\n"
               "Falls Du kein neues Passwort angefordert hast, kannst Du diese Email ignorieren.",
               [user.email])


def send_email(subject, message, recipients):
    msg = Message(subject,
                  sender='vereinSWEbseite@gmail.com',
                  recipients=recipients)

    msg.body = message

    if mail is not None:
        mail.send(msg)
