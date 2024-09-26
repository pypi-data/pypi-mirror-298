import json
import requests

class GoogleChat:
    def __init__(self, webhook_url):
        """
        Initialize the GoogleChat object.

        Parameters:
        ----------
        webhook_url : str
            The webhook link to google chat space where you want to send the message.

        Example:
        --------
        >>> gchat = GoogleChat("https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYY&token=ZZZZ")
        """
        
        self.url = webhook_url
        
        self.__header__ = {}
        self.__cards__ = []
        self.__widgets__ = []
        self.__sections__ = []
        
    def __reset__(self):
        """
        Resets all private variable to JSON Arrays (List) or Objects (Dict).
        """
        
        self.__header__ = {}
        self.__cards__ = []
        self.__widgets__ = []
        self.__sections__ = []
    
    def __close_widget__(self):
        """
        Combines all widgets into one.
        """
        
        section = {}
        section.update({'widgets': self.__widgets__})
        self.__sections__.append(section)
        self.__widgets__ = []
        
    def __close_section__(self):
        """
        Combines the header and widget section into one.
        """
        
        sections = {}
        sections.update({'header': self.__header__, 'sections': self.__sections__})
        self.__cards__.append(sections)
        self.__sections__ = []
     
    def create_button_message(self, title, subtitle, button_text, button_url):
        """
        Create a button message.

        Parameters:
        ----------
        title: str
            Title of the message.
            
        subtitle: str
            Subtitle (remarks) of the message.
            
        button_text: str
            Name of the button.
            
        button_url: str
            Hyperlink where the button will take the user.
        """
        
        return {
            'cards': [
                {
                    'header': {
                        'title': '{}'.format(title),
                        'subtitle': '{}'.format(subtitle)
                    },
                    'sections': [
                        {
                            'widgets': [ 
                                {
                                    'buttons': [
                                        {
                                            'textButton': {
                                                'text': '{}'.format(button_text),
                                                'onClick': {
                                                    'openLink': {
                                                        'url': '{}'.format(button_url)
                                                      }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    
    def set_title(self, title, subtitle):
        """
        Sets the title and subtitle of the message.

        Parameters:
        ----------
        title: str
            Title of the message.
            
        subtitle: str
            Subtitle (remarks) of the message.
        """
        
        header = {}
        
        header.update({'title': title})
        header.update({'subtitle': subtitle})
        
        self.__header__ = header
    
    def create_paragraph_widget(self, paragraph):
        """
        Creates a paragraph in the widget section.

        Parameters:
        ----------
        button_text: str
            Name of the button.
            
        button_url: str
            Hyperlink where the button will take the user.
        """
        
        pgh, tmp = {}, {}
        
        tmp.update({'text': paragraph})
        pgh.update({'textParagraph': tmp})
        
        self.__widgets__.append(pgh)
        
    def create_key_value_widget(self, key, value):
        """
        Creates a Key-Value pair in the widget section.

        Parameters:
        ----------
        key: str
            Name of the KPI.
            
        value: str
            Value of the KPI.
        """
        
        key_value, tmp = {}, {}
        tmp.update({'topLabel': key, 'content': value})
        key_value.update({'keyValue': tmp})
        
        self.__widgets__.append(key_value)
        
    def create_url_button(self, button_text, button_url):
        """
        Creates a button with hyperlink attached to it in the widget section.

        Parameters:
        ----------
        button_text: str
            Name of the button.
            
        button_url: str
            Hyperlink where the button will take the user.
        """
        
        temp = {}
        buttons = []
        
        temp.update({'url': button_url})
        temp = {'openLink': temp}
        temp = {'text': button_text, 'onClick': temp}
        temp = {'textButton': temp}
        buttons.append(temp)
        temp = {'buttons': buttons}
        
        self.__widgets__.append(temp)
        
    def get_message(self):
        """
        Returns the message to be send to a Google Chat Space.

        Returns:
        -------
        Message in dict format.
        """
        
        self.__close_widget__()
        self.__close_section__()
        
        message = {}
        message.update({'cards': self.__cards__})
        
        return json.loads(json.dumps(message))
    
    def send_message(self, message):
        """
        Sends a message to a specific google chat space.

        Parameters:
        ----------
        message : str or dict
            A plain text in the form of string, or
            A card message in the form of dict data type

        Returns:
        -------
        None

        Example:
        --------
        >>> send_message('ETL Pipeline X completed successfully')
        """

        # Setting the headers
        headers = { 'Content-Type': 'application/json; charset=UTF-8' }
        
        # Checking if message is a string or a card message
        data = { 'text': message }
        if type(message) == type({}):
            data = message
        
        # Posting the message via HTTP POST call
        response = requests.post(self.url, headers=headers, data=json.dumps(data))
        
        # Validating if the message was successfully posted
        if response.status_code == 200:
            self.__reset__()
            print('Message sent successfully!')
        else:
            print('Failed to send message: {}, {}'.format(response.status_code, response.text))