category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 10
controls = [
{'type': 'checkbox',
   'var': 'el_dummy_mode',
   'label': 'Dummy Mode',
   'tooltip': 'If checked the experiment will run without attempting to connect to the EyeLink tracker.',
   'name': 'checkbox_el_dummy'},
{'type': 'checkbox',
   'var': 'el_custom_ip',
   'label': 'Use Custom IP Address',
   'name': 'checkbox_el_custom_ip',
   'tooltip': 'If checked you can edit the IP address used to connect to your EyeLink Host'},
{'type': 'checkbox',
    'var': 'el_disable_audio',
    'name': 'checkbox_el_disable_audio',
    'label': 'Disable calibration sound'},
{'type': 'line_edit',
   'label': 'Tracker Address',
   'var': 'el_ip',
   'name': 'line_el_ip',
   'tooltip': 'The EyeLink IP address, default=100.1.1.1'},
  {'type': 'text',
   'label': 'The EyeLink data file will be saved on the Host PC and retrieved to a Results folder at the end of the<br/> session. By default, the subject number the user specified at the beginning of a session will be used to name the <br/>EDF data file. Please bear in mind that the length of the EDF data file name and hence the subject number you <br/>specified CANNOT exceed 8 characters.<br /> <br /> This plugin relies on <b>PyLink</b> to communicate with the EyeLink tracker. Please see the EyeLink Plugin for <br/>OpenSesame User Manual for detailed instructions.',
   'name': 'text_pylink_install'}
   ]