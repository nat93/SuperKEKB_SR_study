# SR simulation for the SuperKEKB collider using SynradG4

1. Generate the survey file with the ring lattice:

	```
	/Users/andriinatochii/SAD/oldsad/bin/gs survey.sad
	```

(Un)comment the relevant lines to switch between the rings. It will generate a .survey file with twiss and ring parameters.

2. Draw the output parameters:

	```
	python plot.py
	```
