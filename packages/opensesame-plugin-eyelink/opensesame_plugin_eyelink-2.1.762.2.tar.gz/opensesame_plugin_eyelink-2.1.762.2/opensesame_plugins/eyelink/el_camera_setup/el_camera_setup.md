# Item: el_camera_setup

This item wraps all the functions a user may need to calibrate the tracker. Using animation calibration target (video) has not yet been implemented. One should put this item at the beginning of each block of trials. The configuration options are explained in the table below.

* <b>Calibration Type</b>

	Select the calibration type, i.e, HV9 for a 9-point calibration. When tracking in remote mode, it is recommended to use HV13, whereas in head-stabilized mode, HV9 gives the best calibration results.

* <b>Randomize Order</b>

	Randomize the order of the calibration/validation targets

* <b>Repeat First Point</b>

	Repeat the first point. This option is enabled by default, helps to improve calibration results.

* <b>Force Manual Accept</b>

	Manually accept fixation duration calibration/validation by pressing SPACEBAR or ENTER. One can switch to automatic mode at any time during calibration/validation by pressing “A” key on the Host or experimental PC keyboard.


* <b>Calibration Target</b>

	Select which type of calibration target to use. The default is a bull’s eye shaped dot, but one can also use an image or a video as the calibration target.

* <b>Custom Target Image/Video</b>
	Select an image or a video file from the File Pool to use as the calibration target.
