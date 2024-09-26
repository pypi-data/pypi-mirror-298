category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhigou Wang'
url = 'http://www.sr-research.com'
priority = 7
controls = [
{'type': 'line_edit',
   'var': 'el_drift_tar_x',
   'label': 'Target X',
   'tooltip': 'The X position of the drift-correction target.',
   'name': 'line_el_drift_tar_x'},
{'type': 'line_edit',
   'var': 'el_drift_tar_y',
   'label': 'Target Y',
   'tooltip': 'The Y position of the drift-correction target.',
   'name': 'line_el_drift_tar_y'},
{'type': 'combobox',
   'var': 'el_dc_target_type',
   'label': 'Drift-correction Target',
   'tooltip': 'Select what drift-correction target to use',
   'name': 'combobox_el_dc_target_type',
   'options': ['SameAsCalibration', 'Image']},
{'type': 'filepool',
   'var': 'el_dc_target_file',
   'label': 'Custom Target Image',
   'tooltip': 'Use an image as the drift-correction target',
   'name': 'filepool_el_dc_target_file'}
]