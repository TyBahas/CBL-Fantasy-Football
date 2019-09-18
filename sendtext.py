'''
AT&T: [number]@txt.att.net
Sprint: [number]@messaging.sprintpcs.com or [number]@pm.sprint.com
T-Mobile: [number]@tmomail.net
Verizon: [number]@vtext.com
Boost Mobile: [number]@myboostmobile.com
Cricket: [number]@sms.mycricket.com
Metro PCS: [number]@mymetropcs.com
Tracfone: [number]@mmst5.tracfone.com
U.S. Cellular: [number]@email.uscc.net
Virgin Mobile: [number]@vmobl.com
'''


import smtplib 
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendText:

        def __init__(self, **kwargs):
            self.email = kwargs.get('email', None)
            self.pas = kwargs.get('pas', None)
            self.smsgateway = kwargs.get('smsgateway', None)
            self.port = 587
            self.smtp = "smtp.gmail.com" 
            self.subject = kwargs.get('text_subject', None)
            self.body = kwargs.get('text_content', None)
            self.img_data = open('./img/golum.gif', 'rb').read()
        
        # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
        # and port is also provided by the email provider.
        
        def send(self):
            server = smtplib.SMTP(self.smtp,self.port)
        # Starting the server
            server.starttls()
        # Now we need to login
            server.login(self.email,self.pas)
            # Now we use the MIME module to structure our message.
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.smsgateway
            # Make sure you add a new line in the subject
            msg['Subject'] = self.subject + "\n"
            msg.attach(MIMEText(self.body, 'plain'))

            sms = msg.as_string()
            server.sendmail(self.email, self.smsgateway, sms)
            # lastly quit the server
            server.quit()


