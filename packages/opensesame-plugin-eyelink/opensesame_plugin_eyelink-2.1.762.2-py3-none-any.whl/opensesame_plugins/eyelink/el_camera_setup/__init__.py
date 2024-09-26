category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 8
controls = [
{'type': 'combobox',
   'var': 'el_calib_type',
   'label': 'Calibration Type',
   'tooltip': 'Select the calibration type, i.e, HV9 9-point calibration',
   'name': 'combobox_el_calib_type',
   'options': ['H3', 'HV3', 'HV5', 'HV9', 'HV13']},
  {'type': 'checkbox',
   'var': 'el_calib_randomize',
   'label': 'Randomize Order',
   'tooltip': 'Randomize the order of the calibration/validation targets',
   'name': 'checkbox_el_calib_randomize'},
  {'type': 'checkbox',
   'var': 'el_calib_repeat_first',
   'label': 'Repeat First Point',
   'tooltip': 'Repeat the first point',
   'name' : 'checkbox_el_calib_repeat_first'},
  {'type': 'checkbox',
   'var': 'el_calib_force_manual',
   'label': 'Force Manual Accept',
   'tooltip': 'Manually accept fixation duration calibration/validation',
   'name': 'checkbox_el_calib_force_manual'},
  {'type': 'combobox',
   'var': 'el_cal_target_type',
   'label': 'Calibration Target',
   'tooltip': 'Select what calibration target to use',
   'name': 'combobox_el_cal_target_type',
   'options': ['Default', 'Image', 'Animation_Video']},
  {'type': 'filepool',
   'var': 'el_cal_target_file',
   'label': 'Custom Target Image/Video',
   'name': 'filepool_el_cal_target_file',
   'tooltip': 'Use an image or video file as the calibration target'}
   ]