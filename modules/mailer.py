import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .constants import config

def send_email(message: str, subject: str = "Trend Vision One - Error Report"):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        username = config["email"]["email"]
        password = config["email"]["password"]
        report = config["email"]["report"]
        alternative_report = config["email"]["alternative_report"]

        mime = MIMEMultipart("alternative")
        mime["Subject"] = subject
        mime["From"] = f"Trend Vision One <{username}>"
        mime["To"] = f"{report}, {alternative_report}"

        text = MIMEText(message, "plain")
        mime.attach(text)

        try:
            server.login(username, password)
            server.sendmail(username, [report, alternative_report], mime.as_string())
        except smtplib.SMTPAuthenticationError:
            print("No se ha podido iniciar sesión en el servidor de correo.")
            print("Por favor, compruebe que el nombre de usuario y la contraseña son correctos.")
            print("Para más información, visite el siguiente enlace: https://support.google.com/mail/?p=BadCredentials")
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            server.quit()