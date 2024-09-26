# Installation of the EyeLink Plugin

This plugin should also work on Linux and Mac, but we have only tested it on the Windows platform. The installation instructions presented below are for the Windows platform.

* Download the latest version of the Plugin from the SR Support website, under the Getting Started with Experimental Programming section.
* Unzip the downloaded .zip file and copy the eyelink folder contained in the .zip file to C:\Program Files (x86)\OpenSesame\Lib\site-packages\opensesame_plugins\
* Copy the EyeinkCoreGraphicsOpenSesame folder to C:\Program Files (x86)\OpenSesame\Lib\site-packages
* OpenSesame needs the Pylink library to communicate with the tracker. To install this enter 'pip install sr-research-pylink' in the Open Sesame Console
* Download and install the latest version of the EyeLink Developer’s Kit from the SR Support website, from the Downloads->Eyelink Display Software section. https://www.sr-support.com/forum/downloads/eyelink-display-software/39-eyelink-developers-kit-for-windows-windows-display-software
* After the above steps, please be sure to set the IP address of the experimental PC to “100.1.1.2” (without quotes) and Subnet mask to “255.255.255.0” (without quotes) so the experimental PC is on the same network as the EyeLink Host PC. Open the example experiment that comes with the EyeLink plugin to test the link between the two machines.  

OpenSesame supports Pygame (legacy), Psychopy, and Expyriment as its backend. We have found the Expyriment backend is crash-prone and would encourage users to stick to the Psychopy backend, which is robust and supports frequently used visual stimuli for visual psychophysics (e.g., gratings).

# Usage Guidelines

After the Plugin has been installed, one should see eight items come up in the item toolbar of the OpenSesame interface. To use the plugin, simply drag one of these items to the required location in the experiment sequence. For general cognitive tasks, we recommend that users follow these integration steps.

## Experiment level
1. Connect to the tracker when the script initializes. Please use the el_connect item for this task. The configuration options available for this item will be elaborated in the next section.
2. Calibrate the tracker at the beginning of each block. This will help the user to maintain optimal tracking accuracy. For fMRI or tasks in which interruption of the task should be avoided, users can calibrate the tracker once at the beginning of each run/session. The item for this function is el_camera_setup. This item will help users to transfer the camera image to the experimental PC, to adjust the pupil/CR threshold by using hot keys on the experimental PC keyboard, to calibrate the tracker and validate the calibration results. 
3. Run the experimental trials one-by-one and record eye movement data.
4. Disconnect from the EyeLink Host PC and transfer the data file to the experimental PC.

## Trial level
1. Drift-check. This procedure will check the tracking accuracy and give the user a chance to re-calibrate the tracker, if needed.
2. Send commands/messages to the tracker to draw reference landmarks on the Host PC screen (optional, use the el_Command or el_Message items).
3. Start recording. We start and stop recording at the beginning and end of each trial, so the inter-trial intervals won’t be recorded; this will reduce the size of the EDF data file. For EEG and tasks where  continuous recording is preferred, please start recording at the beginning of each run/session. The user also has the option to send a “recording status” message to the tracker; this message will be shown in the bottom-right corner of the Host PC screen.
4. Draw experimental graphics and send messages to the tracker to mark the onset of these stimuli, and maybe also the interest areas that will be used in data analysis. This is IMPORTANT, otherwise, there is no way to tell when and what stimuli was presented from the eye movement data file.
5. Collect subject responses and send messages to the tracker.
6. Stop recording and send all experimental variables to the tracker. These variables will be accessible from the Data Viewer software, a nifty data analysis and visualization tool developed by SR Research.

We have provided an example script with all the recommended usage of the tracker. The functions of each of the items in the plugin are briefly explained below. Depending on the hardware, some options may not be configrable through the EyeLink Plugin (and will be grayed out).

# Item: el_connect

Establish a link to the EyeLink Host PC, configure the tracker, and automatically open a data file on the Host to record the eye movement data. The options can be set with this item are explained in the table below.

* <b>Dummy Mode</b>

	Run the tracker in “simulation” mode, i.e., no physical connection to the tracker is established. In Dummy Mode, the user should press F1 to skip Camera setup/calibration, and the drift-correction/check target will briefly flashes and then disappear (as not tracker is physically connected to the experimental PC).

* <b>Use Custom IP Address</b>

	The EyeLink Host PC has a default IP address of 100.1.1.1; in some use cases this IP address is modified and this checkbox can be selected and the Custom IP can be configured

* <b>Disable Calibration Sound</b>

	This option turns off / on the tone sounds played with the presentation of the calibration targets and as calibration / validation feedback.

* <b>Tracker Address</b>	

	The IP address of the EyeLink Host PC can be modified to a custom IP address when the default IP is changed on the Host PC
