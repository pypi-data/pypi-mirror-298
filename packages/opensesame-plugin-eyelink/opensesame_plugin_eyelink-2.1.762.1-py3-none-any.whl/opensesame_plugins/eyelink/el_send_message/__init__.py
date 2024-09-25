category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 3
controls = [
    {'type': 'editor',
     'var': 'el_message_to_send',
     'label': 'Message List',
     'syntax': 'false'},
    {'type': 'text',
     'label': '<b>Messages are IMPORTANT</b> and we need messages in the data file to tell what event happened during a trial and at what time. <br/>Messages should be sent to the tracker everytime a stimulus screen is on or a response has been issued. <br/>You will also need to send formatted messages if you plan to use Data Viewer for data analysis and visualization. <br/> You can find information on how to format these integration messages in the Data Viewer manual: Chapter 8.',
     'name': 'text_el_message'}
]