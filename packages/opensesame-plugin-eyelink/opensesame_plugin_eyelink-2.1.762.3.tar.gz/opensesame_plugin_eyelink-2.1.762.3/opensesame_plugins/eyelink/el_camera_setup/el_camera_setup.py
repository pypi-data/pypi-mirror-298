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
# 2021
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
from openexp.keyboard import Keyboard

import pylink
from EyeLinkCoreGraphicsOpensesame import EyeLinkCoreGraphicsOpensesame


class ElCameraSetup(Item):
    # Provide an informative description for your plug-in.
    description = u'Adjust the camera and calibrate the tracker'

    def reset(self):

        """ desc: Resets plug-in to initial values.
        """

        # Here we provide default values for the variables that are specified
        # in __init__.py
        self.var.el_calib_type = u'HV9'
        self.var.el_calib_randomize = u'yes'
        self.var.el_calib_repeat_first = u'yes'
        self.var.el_calib_force_manual = u'no'
        self.var.el_cal_target_type = u'Default'
        self.var.el_cal_target_file = u''
        self.var.el_disable_audio = u'no'

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        Item.prepare(self)

        # Initialize player object, if animation calibration target is enabled
        if self.var.el_cal_target_type == u'Default':
            self.experiment.cal_target_type = 'default'
        elif self.var.el_cal_target_type == u'Image':
            self.experiment.cal_target_type = 'image'
        else:
            self.experiment.cal_target_type = 'video'

        if self.var.el_cal_target_file == u'':
            self.experiment.cal_target_img = None
            self.experiment.cal_target_vid = None
        else:
            self.experiment.cal_target_img = self.experiment.pool[self.var.el_cal_target_file]
            self.experiment.cal_target_vid = self.experiment.pool[self.var.el_cal_target_file]

    def run(self):
        """The run phase of the plug-in goes here."""
	
	# Skip Camera Setup if in Dummy mode 
        if self.experiment.dummy_mode is True:
            pass
        else:
            # set a few calibration parameters
            self.experiment.eyelink.setOfflineMode()
            # calibration type
            self.experiment.eyelink.sendCommand('calibration_type %s' % self.var.el_calib_type)
            # randomize order?
            if self.var.el_calib_randomize == u'no':
                self.experiment.eyelink.sendCommand('randomize_calibration_order NO')
                self.experiment.eyelink.sendCommand('randomize_validation_order NO')
            else:
                self.experiment.eyelink.sendCommand('randomize_calibration_order YES')
                self.experiment.eyelink.sendCommand('randomize_validation_order YES')
            # force manual accept?
            if self.var.el_calib_force_manual == u'no':
                self.experiment.eyelink.sendCommand('enable_automatic_calibration YES')
            else:
                self.experiment.eyelink.sendCommand('enable_automatic_calibration NO')
            # repeat first point
            if self.var.el_calib_repeat_first == u'no':
                self.experiment.eyelink.sendCommand('cal_repeat_first_target NO')
                self.experiment.eyelink.sendCommand('val_repeat_first_target NO')
            else:
                self.experiment.eyelink.sendCommand('cal_repeat_first_target YES')
                self.experiment.eyelink.sendCommand('val_repeat_first_target YES')

            # open custom calibration graphics
            genv = EyeLinkCoreGraphicsOpensesame(self.experiment, self.experiment.eyelink)
            pylink.openGraphicsEx(genv)

            # show an initial calibration instruction, so users won't be confused
            # by the blank screen.
            self.calib_promp_canvas = Canvas(self.experiment)
            self.calib_promp_canvas.clear()
            
            self.calib_promp_canvas.text('TRACKER CALIBRATION', center=True, x=0, y=-50, font_size=20)
            self.calib_promp_canvas.text('Press Enter TWICE to show the calibration instructions!', center=True, font_size=20)
            self.calib_promp_canvas.show()
            __kbd__ = Keyboard(self.experiment, timeout=0)
            while True:
                response, timestamp = __kbd__.get_key(timeout=1000)
                if response is not None:
                    break
       
            # execute the following command to calibrate the tracker
            try:
                self.experiment.eyelink.doTrackerSetup()
            except RuntimeError as err:
                print('ERROR:', err)
                self.experiment.eyelink.exitCalibration()
                
class QtElCameraSetup(ElCameraSetup, QtAutoPlugin):
    """ This class handles the GUI aspect of the plug-in. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        ElCameraSetup.__init__(self, name, experiment, script)
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

        if self.combobox_el_cal_target_type.currentIndex() == 0:
            self.filepool_el_cal_target_file.setEnabled(False)
        else:
            self.filepool_el_cal_target_file.setEnabled(True)
