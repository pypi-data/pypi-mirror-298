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

class ElDisconnect(Item):
    # Provide an informative description for your plug-in.
    description = u'Terminate the link to the EyeLink tracker.'

    def reset(self):
        """ desc:Resets plug-in to initial values """

        # Here we provide default values for the variables that are specified
        # in __init__.py
        pass

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        Item.prepare(self)
        self.data_transfer_canvas = Canvas(self.experiment)
        self.data_transfer_canvas.clear()
        self.data_transfer_canvas.text('Retrieving EDF data file from the EyeLink Host PC...')

    def run(self):

        """The run phase of the plug-in goes here."""

        if self.experiment.dummy_mode is not True:

            # File transfer and cleanup!
            self.experiment.eyelink.setOfflineMode()
            pylink.pumpDelay(100)

            # Close the file and transfer it to Display PC
            self.experiment.eyelink.closeDataFile()
            pylink.pumpDelay(100)
            # shwo the "retrieving EDF data file ..." message during data transfer
            self.data_transfer_canvas.show()
            self.experiment.eyelink.receiveDataFile(self.experiment.edf_data_file,
                                                    self.experiment.edf_data_folder + self.experiment.edf_data_file)
            pylink.pumpDelay(1500)  # make sure the transfer file message shows for at least 1.5 sec
            self.experiment.eyelink.close()
        else:
            pass
            # print('No tracker is connected!')


class QtElDisconnect(ElDisconnect, QtAutoPlugin):

    """ this class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.	"""

    def __init__(self, name, experiment, script=None):

        # We don't need to do anything here, except call the parent
        # constructors.
        ElDisconnect.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
