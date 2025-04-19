import os
import smtplib
from email.mime.text import MIMEText
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig:
    """Базова конфігурація"""

    APP_NAME = os.getenv("APP_NAME", "Topchik")
    SECRET_KEY = os.getenv("SECRET_KEY", "Вап, секретного ключа тут немає, ХА-ХА!")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    DEBUG_TB_ENABLED = False
    WTF_CSRF_ENABLED = False

    @staticmethod
    def configure(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "development.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(BASE_DIR, "production.sqlite3"),
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def send_welcome_email(user_email):
    sender = "illya.d.donchenko@ukr.net"
    password = "T0XX2Udvx6MzPOOO"
    subject = "Вітаємо з реєстрацією!"
    body = "Вітаємо, ви зареєструвалися на нашому сайті з купою цікавих та захоплюючих новин. Сподіваємося ваш досвід користування нашим сайтом буде виключно позитивним"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, user_email, msg.as_string())
            print("Лист надіслано на", user_email)
    except Exception as e:
        print("Помилка при надсиланні листа:", e)
