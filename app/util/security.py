from itsdangerous import URLSafeTimedSerializer
from EmailHelper import EmailClass

from .. import config

# key = app.config["SECRET_KEY"]
key = 'asdsdfgo2u340912uj3@#)_$R@*+!$#I@P)#{R:LJSDCI){@*I#RON'
ts = URLSafeTimedSerializer(key)
# token = ts.dumps('gtalarico@gmail.com', salt='email-confirm-key')

# print token

def send_email(to_email,to_name,subject,html_body_msg):
    auto_send = True
    email = EmailClass(to_email = to_email, to_name = to_name, subject = subject, \
                        html_body_msg = html_body_msg , auto_send = auto_send)


# html_body_msg = '<html><body>Could not generate report. Reason:<br></body></html>'
# to_name= ['Gui Talarico']
# to_email= ['gtalarico@gmail.com']
# subject = 'Welcome'

# send_email(to_name, to_email, subject, html_body_msg)
