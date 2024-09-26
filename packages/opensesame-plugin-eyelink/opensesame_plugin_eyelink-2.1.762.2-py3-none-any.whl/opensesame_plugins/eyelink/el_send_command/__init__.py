category = 'EyeLink'
version = 1.0
author: 'Jono Batten' 'Zhiguo Wang'
url = 'http://www.sr-research.com'
priority = 4
controls = [
    {'type': 'editor',
     'var': 'el_commands_to_send',
     'label': 'Command List',
     'name': 'editor_el_commands_to_send'},
    {'type': 'text',
     'label': '<b>Send command(s) to the tracker </b><br />If you need to send multiple commands, put each command in a line, i.e.:<br /> &nbsp;&nbsp;&nbsp;&nbsp;sampling_rate 500<br/>&nbsp;&nbsp;&nbsp;&nbsp;draw_cross 512 384<br /> The various "draw" commands can be very useful and one can use them to draw simple landmarks on the Host display during recording. <br />These commands (e.g., clear_screen, draw_line, draw_box, draw_text) can be found in the COMMANDS.INI file on the Host PC, under /elcl/exe.',
     'name': 'text_el_command'}
     ]