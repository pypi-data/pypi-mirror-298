category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 6
controls = [
    {'type': 'checkbox',
      'var': 'el_link_data_events',
      'label': 'Eye Events Available Over Link',
      'tooltip': 'Allows accessing events data over the link during recording',
      'name': 'checkbox_el_link_data_events'},
    {'type': 'checkbox',
      'var': 'el_link_data_samples',
      'label': 'Samples Available Over Link',
      'tooltip': 'Allows accessing sample data over the link during recording',
      'name': 'checkbox_el_link_data_samples'},
    {'type': 'line_edit',
      'label': 'Recording Status Message',
      'var': 'el_recording_status_msg',
      'name': 'el_recording_status_msg',
      'tooltip': 'Send a message to the Host PC screen to show the current trial number, condition, etc.'}
 ]