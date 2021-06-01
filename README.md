# MethodsJ2
Building on MethodsJ, MethodsJ2 helps users write a materials and methods text for microscopy experiments by sourcing experiment information from metadata, as well as information from a microscope hardware specification file generated in Micro-Meta App. A draft experiment methods section text is generated which can then be revised and used in written manuscripts and reports, etc.

As requirements, to use MethodsJ2, users first need a raw image from a microscopy experiment as well as a previously generated Micro-Meta App microscope hardware specifications file (.json). 

DISCLAIMER: ***

## How it works
The MethodsJ2 script guides to users to input information about a microscopy experiment. The script displays dialog boxes wherein users can directly input information as text, or select the appropriate options from a drop-down menu assembled from the microscopy hardware specifications file generated in Micro-Meta App. User input and selections are then used to "fill in the blanks" in blocks of text designed to generate a draft of a experimental methods section.

## How to use MethodsJ2
Please install Fiji from fiji.sc following the recommended installation procedure.

Download the python script MethodsJ2.py file from this repo, as well as the example Micro-Meta App hardware specifications file (abif-axiovert1.json), and the example images (pumpkin_widefield.czi).

Drag and drop the python script MethodsJ2.py onto the main Fiji window, this should open a script editor window. Click Run, and follow the dialog boxes, filling in the information as accurately as possible.


