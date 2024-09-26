# Item: el_gaze_trigger

A gaze contingent trigger that can fire within / outside of a specifed screen region after a minimum duration.

* <b>Trigger Location (x,y)</b>

	The pixel location of gaze trigger (centre coordinate)
	
* <b>Trigger Size (pixels)</b>

	The pixel size of the gaze trigger centred around the Trigger Location

* <b>Fire Within</b>

	The trigger will fire when within the specified region when checked, or outside if unchecked.

* <b>Minimum Duration (ms)</b>

	The minimum duration of gaze in milliseconds required to fire the trigger

* <b>Allow Skip (x key)</b>

	Allow the gaze trigger to be skipped by pressing the x key. Note this will only skip when connected to the tracker.
	In dummy mode the trigger will automatically fire after the minimum duration.

* <b>Create Interest Area in EyeLink Data Viewer</b>

	Automatically create an interest area of the gaze trigger for Data Viewer
	