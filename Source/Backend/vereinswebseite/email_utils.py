from flask_mail import Mail, Message

from vereinswebseite.models.user import User
from vereinswebseite.request_utils import get_server_root

mail = Mail()


def send_reset_password_email(user: User, reset_url: str):
    """
    Sends the reset password email to the specified user.
    :param reset_url: The one time url which the user can use to reset the password
    :return:
    """
    send_email("Passwort zurücksetzen",
               "Hallo " + user.name +
               ",\n"
               "benutze diesen Link um dein Passwort zurückzusetzen:\n"
               + get_server_root() + reset_url +
               "\n"
               "\n"
               "Falls Du kein neues Passwort angefordert hast, kannst Du diese Email ignorieren.",
               [user.email])


def send_email(subject, message, recipients):
    """
    Send an email to the specified recipient(s)
    :param subject:
    :param message: The message in plain text
    :param recipients: A list of recipients where the mail gets send to.
                       All recipients are visible for all other recipients
    :return:
    """
    msg = Message(subject,
                  sender='vereinSWEbseite@gmail.com',
                  recipients=recipients)

    msg.body = message

    if mail is not None:
        mail.send(msg)
