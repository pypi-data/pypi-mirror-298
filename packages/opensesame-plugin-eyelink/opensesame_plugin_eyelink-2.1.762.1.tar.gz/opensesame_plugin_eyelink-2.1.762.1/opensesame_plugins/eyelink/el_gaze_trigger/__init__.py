category = 'EyeLink'
priority = 2
author = 'Jono Batten'
controls = [
    {'type': 'line_edit',
    'var': 'el_gaze_trigger_location',
    'label': 'Trigger Location (x,y)',
    'name': 'line_el_trigger_location',
    'tooltip': 'Enter the location to centre the gaze trigger'},
    {'type': 'line_edit',
     'var': 'el_gaze_trigger_size',
     'label': 'Trigger Size (pixels)',
     'name': 'line_el_trigger_size'},
    {'type': 'checkbox',
     'var': 'el_trigger_within',
     'label': 'Fire Within',
     'name': 'checkbox_el_trigger_within',
     'tooltip': 'Option to fire when within (when selected) or outside of (when unselected) the specified region'},
    {'type': 'line_edit',
      'var': 'el_trigger_duration',
      'label': 'Minimum Duration (ms)',
      'name': 'line_trigger_duration',
      'tooltip': 'The minimum duration of gaze samples required within/outside the region'},
    {'type': 'checkbox',
      'var': 'el_abort_key',
      'label': 'Allow Skip (x key)',
      'name': 'checkbox_abort_key',
      'tooltip': 'Allow an x keypress to skip past the gaze trigger'},
    {'type': 'checkbox',
      'var': 'el_create_ia',
      'label': 'Create Interest Area in EyeLink Data Viewer',
      'name': 'checkbox_create_ia',
      'tooltip': 'Automatically create an interest area for EyeLink Data Viewer'}
 ]