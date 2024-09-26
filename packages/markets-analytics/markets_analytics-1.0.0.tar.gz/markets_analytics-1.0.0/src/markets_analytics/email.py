import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    def __init__(self, sender_email, app_password, stylesheet=None):
        """
        Initialize the Email object.

        Parameters:
        ----------
        sender_email : str
            The email address from which the emails will be sent.
        app_password : str
            The app password from Google Accounts used for auth purposes.
        stylesheet : str, optional
            An optional string that holds CSS stylesheet.
            Defaults to None, meaning default stylesheet would be applied.

        Example:
        --------
        >>> email_sender = Email("your_email@example.com", "your_app_password")
        """
        
        self.sender = sender_email
        self.password = app_password
        
        # default CSS3 stylesheet
        self.stylesheet = '''
            <style>
                body {
                  font-family: helvetica;
                }

                table {
                  text-align: center;
                  border-collapse: collapse;
                }

                table td, table th {
                  padding: 5px;
                  border: 1px solid black;
                }

                table thead {
                  color: white;
                  font-weight: bold;
                  background-color: #333;
                }
            </style>
        '''
        
        # if sender provided his stylesheet then use it
        if stylesheet != None:
            self.stylesheet = stylesheet
            
        # initializing queue for internal purposes
        self.__queue__ = []
    
    def __append__(self, html):
        """
        Appends the html to the internal message queue.

        Parameters:
        ----------
        html : str
            html string to append to the internal message queue.
        """
        self.__queue__.append(html)
        
    def create_paragraph(self, msg):
        """
        Creates a HTML paragraph (<p>) from provided message.

        Parameters:
        ----------
        msg : str
            The message to convert to HTML.
        """
        
        html = '<p>{}</p>'.format(msg)
        self.__append__(html)
        
    def create_header(self, msg, header_level=1):
        """
        Creates a HTML header (<hx>) from provided message.

        Parameters:
        ----------
        msg : str
            The message to convert to HTML.
            
        header_level : int, optional
            The header level.
            Defaults to 1 for <h1>, supported values range from 1 to 6.
        """
        
        html = '<h{hl}>{msg}</h{hl}>'.format(msg=msg, hl=header_level)
        self.__append__(html)
        
    def create_table(self, df):
        """
        Creates a HTML table (<table>) from provided dataframe.

        Parameters:
        ----------
        df: pandas.DataFrame
            The dataframe to convert to HTML table.
        """
        
        html = df.to_html(index=False)
        html = html.replace('border="1" ', '')
        html = html.replace(' style="text-align: right;"', '')
        self.__append__(html)
        
    def get_message(self):
        """
        Returns the message from the internal message queue.

        Returns:
        ----------
        A message string with appropriate HTML tags.
        """
        
        body = '<body>\n'
        for msg in self.__queue__:
            body += msg + '\n'
        
        body += '</body>'
        return body
        
    def send_email(self, to, subject, body, cc=None):
        """
        Sends an email to the specified recipient(s).

        Parameters:
        ----------
        to : str or list
            The primary recipient's email address(es).
        subject : str
            The subject line of the email.
        body : str
            The body content of the email in HTML format.
        cc : str or list, optional
            An individual email addresses or a list addresses to send a carbon copy (CC) of the email.
            Defaults to None, meaning no CC recipients will be added.

        Returns:
        -------
        email.mime.multipart.MIMEMultipart

        Raises:
        ------
        smtplib.SMTPException
            If an error occurs while sending the email.

        Example:
        --------
        >>> send_email("recipient@example.com", "Hello", "This is a test email.", cc=["cc@example.com"])
        """

        # Checking whether it's a list of or an individual receiver
        if type(to) == type([]):
            to = ', '.join(to)
            
        # Checking whether it's a list of cc receivers
        if type(cc) == type([]):
            cc = ', '.join(cc)
        
        # Setting up the message
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = to
        msg['Subject'] = subject
        
        if cc != None:
            msg['Cc'] = cc
        
        # Adding CSS3 stylesheet to the message
        body = body.replace('<html>', '').replace('</html>', '')
        body = '<html>\n<head>' + self.stylesheet + '</head>\n' + body + '\n</html>'
        msg.attach(MIMEText(body, 'html'))
        
        # Trying to send the email using gmail server
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender, self.password)
            text = msg.as_string()
            server.sendmail(self.sender, to, text)
            print('Email sent successfully!')
        except Exception as e:
            print('Error: {}'.format(e))
        finally:
            server.quit()
            
        # Returning the message in case inspection is needed
        return msg