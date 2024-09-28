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

from openexp.canvas import Canvas
import pylink


class ElStopRecording(Item):
    # Provide an informative description for your plug-in.
    description = u'Stop data recording and log trial variables'

    def reset(self):

        """ desc: Resets plug-in to initial values. """
        # Here we provide default values for the variables that are specified
        # in __init__.py
        self.var.el_log_all_vars = u'yes'

    def prepare(self):

        """The preparation phase of the plug-in goes here."""
        # Call the parent constructor.
        Item.prepare(self)

    def run(self):

        """The run phase of the plug-in goes here."""
        
        if self.experiment.dummy_mode is False:
            # send all task-relevant variables to the tracker

            # stop recording
            pylink.pumpDelay(100)  # wait for 100 msec to catch end events
            self.experiment.eyelink.stopRecording()

            # Clear the Host PC screen
            self.experiment.eyelink.sendCommand('clear_screen 0')

            # custom variables are not automatically sent
            if self.var.el_log_all_vars == u'yes':
                for logvar, info in self.experiment.var.inspect().items():
                        # Construct the message with the variable name and value      
                        msg = '!V TRIAL_VAR %s %s' % (logvar, str(info[u'value']))
                        # Send the message to the EyeLink device
                        self.experiment.eyelink.sendMessage(msg)
                        # Sleep for 2 milliseconds between messages
                        self.clock.sleep(2)
            else:
                # Split the user-defined variables by newline and iterate over them
                for log_ind in self.var.el_log_editor.split(u'\n'):
                    # Check if the variable exists in the experiment's variable list
                    if log_ind in self.experiment.var.inspect():
                        # If the variable exists, retrieve its value
                        log_value = self.experiment.var.inspect()[log_ind][u'value']
                    else:
                        # If the variable does not exist, use placeholder value "NA"
                        log_value = "NA"
                    # Construct the message with the variable name and value
                    msg = '!V TRIAL_VAR %s %s' % (log_ind, log_value)
                    # Send the message to the EyeLink
                    self.experiment.eyelink.sendMessage(msg)
                    # Sleep for 2 milliseconds between messages
                    self.clock.sleep(2)

            # send a keyword message to mark the ene of a trial
            self.experiment.eyelink.sendMessage('TRIAL_RESULT 0')
        else:
            pass

class QtElStopRecording(ElStopRecording, QtAutoPlugin):

    """ This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        ElStopRecording.__init__(self, name, experiment, script)
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
        if self.checkbox_el_log_all_vars.isChecked():
            self.editor_el_log_files.setEnabled(False)
        else:
            self.editor_el_log_files.setEnabled(True)
