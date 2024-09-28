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
from openexp.keyboard import Keyboard
from libqtopensesame.items.feedpad import Feedpad
import time
from math import fabs
import pylink

class ElGazeTrigger(Item):
    description = u'Gaze trigger plugin'

    def __init__(self, name, experiment, string=None):
        super().__init__(name, experiment, string)
        self.status = 'NOT_STARTED'
        # keeps track of the time when the eye most recently entered triggering region
        self.gazeInHitRegionStartTime = -1
        # keeps track of whether gaze is currently in the triggering region
        self.inHitRegion = False
        # keeps track of whether the gaze criteria have been met
        self.gazeWindowGazeCompletedStatus = False
        # will log time when gaze criteria were met
        self.gazeWindowGazeCompletedTime = -1
        # keeps track of time whether gaze criteria checking period has started
        self.elFixCheckOnsetDetected = False
        # keeps track of time whether gaze criteria checking period has ended
        self.elFixCheckOffsetDetected = False
        # stores the time of the last (i.e., previous) sample
        self.lastSampleTime = -1

    def reset(self):

        """ desc: Resets plug-in to initial values. """

        # Here we provide default values for the variables that are specified
        # in init.py
        self.el_gaze_trigger_location = u'0,0'
        self.el_gaze_trigger_size = u'100'
        self.el_trigger_within = u'yes'
        self.el_trigger_duration = u'500'
        self.el_abort_key = u'no'
        self.el_create_ia = u'yes'


    def run(self):
        """The run phase of the plug-in goes here."""
        
        #Set initial variables for the gaze trigger to check
        keep_checking = True
        self.status = 'NOT_STARTED'
        new_sample = None
        self.lastSampleTime = -1
        self.trigger_fired = False
        self.inHitRegion = False
        self.gazeInHitRegionStartTime = -1
        self.elFixCheckOnsetDetected = False
        
        # determine which eye(s) is/are available
            # 0- left, 1-right, 2-binocular
        eye_used = self.experiment.eyelink.eyeAvailable()
        if eye_used == 1:
            self.experiment.eyelink.sendMessage("EYE_USED 1 RIGHT")
        elif eye_used == 0 or eye_used == 2:
            self.experiment.eyelink.sendMessage("EYE_USED 0 LEFT")
            eye_used = 0
        else:
            print("Error in getting the eye information!")


        # Draw the defined region as an interest area for EyeLink Data Viewer
        pos_list = self.var.el_gaze_trigger_location.split(sep = ',')
        pos_list = [int(x) for x in pos_list]

        region_x_eyelink_units = pos_list[0] + self.var.width/2
        region_y_eyelink_units = pos_list[1] + self.var.height/2

        # If create IA is selected write some interest area info to the EDF
        if self.var.el_create_ia == u'yes':
            ia_left = int(pos_list[0] -self.var.el_gaze_trigger_size/2 + self.var.width/2)
            ia_right = int(pos_list[0] + self.var.el_gaze_trigger_size/2 + self.var.width/2)
            ia_top = int(pos_list[1] -self.var.el_gaze_trigger_size/2 + self.var.height/2)
            ia_bottom = int(pos_list[1] + self.var.el_gaze_trigger_size/2 + self.var.height/2)
            ia_msg_param = (0, 999, ia_left, ia_top, ia_right, ia_bottom, 'gaze_trigger')
            ia_msg = '%d !V IAREA RECTANGLE %d %d %d %d %d %s' % ia_msg_param
            self.experiment.eyelink.sendMessage(ia_msg) 

        # This section of EyeLink component code checks to see whether the gaze checking
        # period has started (and marks it with a message when it
        # does), grabs the gaze data online, and uses it to check whether the
        # gaze window criteria have been satisfied
        # Checks whether it is the first frame of the gaze trigger checking period

        while self.status != 'FINISHED' and keep_checking == True:

            # If the abort key is checked define keyboard and check for key presses
            if self.var.el_abort_key == u'yes':
                kb = Keyboard(self)
                # Check for abort key (x)
                key, time = kb.get_key(timeout =0)
                if key == 'x':
                    self.status = 'FINISHED'
                    keep_checking = False
                    print('abort key pressed')
                    if not self.experiment.dummy_mode:
                        self.experiment.eyelink.sendMessage('GazeTrigger_Aborted')
                        self.experiment.eyelink.sendMessage('!V TRIAL_VAR Gaze_Trigger_Aborted True')
                        
                    break
            
            if self.experiment.dummy_mode:
                print('Gaze trigger will fire automatically at the minimum duration in dummy mode')
                self.clock.sleep(self.var.el_trigger_duration)
                keep_checking == False
                self.status = 'FINSIHED'
                break

            if self.status == 'NOT_STARTED' and self.elFixCheckOnsetDetected == False:
                self.status = 'STARTED'
                self.time_start = self.experiment.clock.time()

                # draw a green box on the host for the defined region
                left = int(pos_list[0] -self.var.el_gaze_trigger_size/2 + self.var.width/2)
                right = int(pos_list[0] + self.var.el_gaze_trigger_size/2 + self.var.width/2)
                top = int(pos_list[1] -self.var.el_gaze_trigger_size/2 + self.var.height/2)
                bottom = int(pos_list[1] + self.var.el_gaze_trigger_size/2 + self.var.height/2)
                coord_params = (left, top, right, bottom, 10)
                box_msg = 'draw_box %d %d %d %d %d' % coord_params
                self.experiment.eyelink.sendCommand(box_msg)

                self.experiment.eyelink.sendMessage('GazeTrigger_Onset')
                self.elFixCheckOnsetDetected = True


            if self.status == 'STARTED':
                #Get the latest sample
                new_sample = self.experiment.eyelink.getNewestSample()
                
                if new_sample is not None:
                    if self.experiment.clock.time() != self.lastSampleTime:
                        self.lastSampleTime = self.experiment.clock.time()               
                        # check if the new sample has data for the eye
                        # currently being tracked; if so, we retrieve the current
                        # gaze position and PPD (how many pixels correspond to 1
                        # deg of visual angle, at the current gaze position)
                        if eye_used == 1 and new_sample.isRightSample():
                            eyelinkGazeX, eyelinkGazeY = new_sample.getRightEye().getGaze()
                        if eye_used == 0 and new_sample.isLeftSample():
                            eyelinkGazeX, eyelinkGazeY = new_sample.getLeftEye().getGaze()

                        if self.var.el_trigger_within == u'yes':
                            # check if gaze is insde (within) the triggering region
                            if fabs(eyelinkGazeX - region_x_eyelink_units) < self.var.el_gaze_trigger_size/2 and fabs(eyelinkGazeY - region_y_eyelink_units) < self.var.el_gaze_trigger_size/2:

                                if not self.inHitRegion:
                                    if self.gazeInHitRegionStartTime == -1:
                                        self.gazeInHitRegionStartTime = self.experiment.clock.time()
                                        self.inHitRegion = True

                                # check the gaze duration and fire
                                if self.inHitRegion:
                                    self.gazeDur = self.experiment.clock.time() - self.gazeInHitRegionStartTime
                                    if self.gazeDur > self.var.el_trigger_duration:
                                        self.gazeWindowGazeCompletedTime = self.experiment.clock.time()
                                        self.gazeWindowGazeCompletedStatus = True
                                        self.experiment.eyelink.sendMessage('GazeTrigger_Fired')
                                        self.experiment.eyelink.sendMessage('!V TRIAL_VAR Gaze_Trigger_Aborted False')
                                        keep_checking == False
                                        self.status = 'FINSIHED'
                                        break
                            else:  # gaze outside the hit region, reset variables
                                self.inHitRegion = False
                                self.gazeInHitRegionStartTime = -1

                        if self.var.el_trigger_within == u'no':
                            
                            # check if gaze is insde (within) the triggering region
                            if not (fabs(eyelinkGazeX - region_x_eyelink_units) < self.var.el_gaze_trigger_size/2 and fabs(eyelinkGazeY - region_y_eyelink_units) < self.var.el_gaze_trigger_size/2):
                                if not self.inHitRegion:
                                    if self.gazeInHitRegionStartTime == -1:
                                        self.gazeInHitRegionStartTime = self.experiment.clock.time()
                                        self.inHitRegion = True

                                # check the gaze duration and fire
                                if self.inHitRegion:
                                    self.gazeDur = self.experiment.clock.time() - self.gazeInHitRegionStartTime
                                    if self.gazeDur > self.var.el_trigger_duration:
                                        self.gazeWindowGazeCompletedTime = self.experiment.clock.time()
                                        self.gazeWindowGazeCompletedStatus = True
                                        self.experiment.eyelink.sendMessage('GazeTrigger_Fired')
                                        self.experiment.eyelink.sendMessage('!V TRIAL_VAR Gaze_Trigger_Aborted False')
                                        keep_checking == False
                                        self.status = 'FINSIHED'
                                        break
                            else:  # gaze outside the hit region, reset variables
                                self.inHitRegion = False
                                self.gazeInHitRegionStartTime = -1

    def pause(self):
        RuntimeError('Esc key pressed at gaze trigger')
        pass


class QtElStartRecording(ElGazeTrigger, QtAutoPlugin):

    """ This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in __init__.py. """

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        ElGazeTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
