import sys
import smtplib
from smtplib import SMTPException, SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils as utils

from .. import app

SMTP_SSL_SERVER = 'server41.web-hosting.com'
SMTP_SSL_PORT   = '465'
SENDER_USER     = 'suporte@brcharge.com'
SENDER_PWD      = 'suporte@brcharge.com'

FROM_EMAIL      = 'suporte@brcharge.com'
FROM_NAME       = 'Test'


#simplify class. take only TO, EMAIL, SUBJ, CODE,
class EmailClass(object):

    def __init__(self, to_email=None, to_name=None, subject=None, html_body_msg=None,auto_send=False):

        debuglevel = 0

        if to_name is None or to_email is None or html_body_msg is None:
            app.logger.error('to_email: %s / to_name: %s / type(html_body_msg): %s' % (
                        to_name,to_email,html_body_msg))
            raise TypeError('Something went wrong. Email cannot be sent.')

        if subject is None:
            app.logger.info('Subject not passed. Subject will be Report Operacional.')
            subject = 'Report Operacional'

        self.to_name = to_name
        self.to_email = to_email
        self.subject = subject
        self.html_body_msg = html_body_msg

        self.smtp = smtplib.SMTP_SSL()
        self.smtp.set_debuglevel(debuglevel)
        self.smtp.connect(SMTP_SSL_SERVER, SMTP_SSL_PORT)

        self.login()
        self.encode_msg()

        if auto_send == True:
            app.logger.info('auto_send is TRUE. Sending email...')
            self.send()
        else:
            app.logger.info('auto_send is FALSE. Will NOT send email')


    def login(self):
        try:
            self.smtp.login(SENDER_USER, SENDER_PWD)
            app.logger.info("Authentication Successfully. Encoding msg...")
        except SMTPAuthenticationError:
            app.logger.error("Authentication Error.")
            raise RuntimeError('Could not loging to email server.')

    def encode_msg(self):
        self.mime_msg = MIMEMultipart('alternative')
        html = MIMEText(self.html_body_msg, 'html')
        self.mime_msg.attach(html)

        print utils.formataddr((FROM_NAME,FROM_EMAIL))

        self.mime_msg['From'] = utils.formataddr((FROM_NAME,FROM_EMAIL))
        #FROM_NAME and email are constanst set by config fil

        if len(self.to_name) != len(self.to_email):
            app.logger.warn('to_name and to_email not the same length')

        if len(self.to_name) == 1:
            app.logger.debug('Only one recipeient')
            self.mime_msg['To'] = utils.formataddr((self.to_name[0],self.to_email[0]))

        elif len(self.to_name) > 1:
            app.logger.debug('MORE than one recipeient')
            # recipients = [("John Doe", "john@domain.com"), ("Jane Doe", "jane@domain.com")]
            recipients = zip(self.to_name,self.to_email)
            self.mime_msg['To'] = ', '.join([utils.formataddr(recipient) for recipient in recipients])

        app.logger.debug('TO FORMATED: %s', self.mime_msg['To'])
        #Gui Talarico <gui@brcharge.com>, Guilherme <talaricotalarico@hotmail.com>

        self.mime_msg['Subject'] = self.subject


        app.logger.info('Message encoded. Just call send()')
        app.logger.debug('Encoded email message: \n %s', self.mime_msg)

    def send(self):
        try:
            self.smtp.sendmail(FROM_EMAIL, self.to_email, self.mime_msg.as_string())
            app.logger.info("Email Sent.")

        except SMTPException:
            app.logger.error('Error: Unable to send email.')
            app.logger.error('Unexpected error: %s', sys.exc_info())

        self.smtp.quit()

if __name__ == '__main__':

    def TEST_email_send():
        CODE = 'TEST'
        to_name = ['Gui']
        to_email = ['gtalarico@gmail.com']
        email = EmailClass(to_email=to_email, to_name=to_name, subject='Report', html_body_msg = CODE)
        email.send()
    TEST_email_send()
    pass
