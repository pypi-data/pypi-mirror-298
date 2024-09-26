category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 5
controls = [
    {'type': 'checkbox',
    'var': 'el_log_all_vars',
    'label': 'Log all experiment variables in the EDF data file',
    'name': 'checkbox_el_log_all_vars',
    'tooltip': 'Log all variables in the EDF data file.'},
    {'type': 'text',
     'label': 'If unchecked you can specify variables to log in the editor below. Use one line for each variable',
     'name': 'text_for_editor'},
    {'type': 'editor',
     'var': 'el_log_editor',
     'label': 'Specify variables to log in the EDF fata file',
     'name': 'editor_el_log_files',
     'tooltip': 'Add a line for each variable you wish to log'}
 ]