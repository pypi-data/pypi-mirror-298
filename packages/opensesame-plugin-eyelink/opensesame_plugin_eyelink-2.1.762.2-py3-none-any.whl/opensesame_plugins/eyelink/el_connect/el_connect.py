# -*- coding:utf-8 -*-
#
# Copyright (c) 1996-2024, SR Research Ltd., All Rights Reserved
#
# For use by SR Research licencees only. Redistribution and use in source
# and binary forms, with or without modification, are NOT permitted.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# 2024
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Import Python 3 compatibility functions
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin

import os
import pylink


class ElConnect(Item):
    # Provide an informative description for your plug-in.
    description = u'Establish a link to the EyeLink tracker'

    def reset(self):

        """ desc: Resets plug-in to initial values. """

        # Here we provide default values for the variables that are specified
        # in __init__.py
        self.var.el_dummy_mode = u'no'
        self.var.el_custom_ip = u'no'
        self.var.el_ip = u'100.1.1.1'
        self.var.el_disable_audio = u'yes'

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        Item.prepare(self)


    def run(self):
        
        """The run phase of the plug-in goes here."""
        if self.var.el_dummy_mode == u'yes':  # check if we have dummy mode enabled
            print('dummy mode enabled')
            self.experiment.eyelink = pylink.EyeLink(None)
            self.experiment.dummy_mode = True
        else:
            print('attempting to connect to tracker')
            self.experiment.dummy_mode = False
            self.experiment.eyelink = pylink.EyeLink(self.var.el_ip)
            
        if self.var.el_disable_audio == u'yes':
            self.experiment.disable_el_audio = True
        else:
            self.experiment.disable_el_audio = False

        # Create a Results folder if it does not exist, the create the session folder to place the EDF and any other files
        # for example, .IAS and .DLF files.
        if os.name == u'nt': 
                self.experiment.results_path = self.experiment.experiment_path + '\\' + 'results' + '\\'
        else:
                self.experiment.results_path = self.experiment.experiment_path + '/' + 'results' + '/'
        if not os.path.exists(self.experiment.results_path):
            os.makedirs(self.experiment.results_path)
        
        # Create a session folder within the results folder to store the EDF and other files.
        self.el_edf_folder_name = '{:.8}'.format(str(self.var.subject_nr))

        if os.name == u'nt': 
            self.experiment.edf_data_folder = self.experiment.results_path + '\\' + '\\' + self.el_edf_folder_name + '\\'
        else:  
            self.experiment.edf_data_folder = self.experiment.results_path + '/' + '/' + self.el_edf_folder_name + '/'
        if not os.path.exists(self.experiment.edf_data_folder):
            os.makedirs(self.experiment.edf_data_folder)

        # add 'eyelink' to the Python workspace, so users can reference to "eyelink" directly
        #self.python_workspace[u'eyelink'] = self.experiment.eyelink

        if self.experiment.dummy_mode is False:
            # check tracker version, and set data stored in data file and passed over the link (online)
            eyelinkVer = self.experiment.eyelink.getTrackerVersion()
            self.experiment.eyelink.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
            self.experiment.eyelink.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT")
            if eyelinkVer >= 3:  # eyelink 1000/1000 plus
                self.experiment.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT")
                self.experiment.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT")
            else:  # EyeLink II/I
                self.experiment.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT")
                self.experiment.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT")

            # Link and file filter level
            self.experiment.eyelink.sendCommand('heuristic_filter 1 2')

            # tracking setting
            # Eye event type
            self.experiment.eyelink.sendCommand("recording_parse_type GAZE")

            # saccade sensitivity
            self.experiment.eyelink.sendCommand('select_parser_configuration 0')

            # Track area pupil data
            self.experiment.eyelink.sendCommand('pupil_size_diameter AREA')

            # use subject number to name the EDF data file; the EDF file name cannot exceed 8 characters
            self.experiment.edf_data_file = '{:.8}'.format(str(self.var.subject_nr)) + '.EDF'
            self.experiment.eyelink.openDataFile(self.experiment.edf_data_file)

            # write file preable text
            self.experiment.eyelink.sendCommand("add_file_preamble_text '%s'" % self.var.title)
		

class QtElConnect(ElConnect, QtAutoPlugin):

    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):
        # We don't need to do anything here, except call the parent
        # constructors.
        ElConnect.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def apply_edit_changes(self):
        # Applies the controls.
        if not QtAutoPlugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()

    def edit_widget(self):
        # Refreshes the controls.
        if self.lock:
            return
        self.lock = True
        w = QtAutoPlugin.edit_widget(self)
        self.custom_interactions()
        self.lock = False
        return w

    def custom_interactions(self):
        ''' all necessary option changes for the tracker.'''

        if self.checkbox_el_dummy.isChecked():
            self.line_el_ip.setEnabled(False)
            self.checkbox_el_custom_ip.setEnabled(False)
            self.checkbox_el_disable_audio.setEnabled(False)
        else:
            self.checkbox_el_custom_ip.setEnabled(True)
            self.checkbox_el_disable_audio.setEnabled(True)

        if self.checkbox_el_custom_ip.isChecked():
            self.line_el_ip.setEnabled(True)
        else:
            self.line_el_ip.setEnabled(False)