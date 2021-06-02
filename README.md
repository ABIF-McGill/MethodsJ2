
# MethodsJ2
Building on [MethodsJ](https://github.com/tp81/MethodsJ) , **MethodsJ2** helps users write a materials and methods text for microscopy experiments by sourcing experiment information from metadata, as well as information from a microscope hardware specification file generated in Micro-Meta App. A draft experiment methods section text is generated which can then be revised and used in written manuscripts and reports, etc.

As requirements, to use **MethodsJ2**, users first need a raw image from a microscopy experiment as well as a previously generated in [Micro-Meta App](https://github.com/WU-BIMAC/MicroMetaApp-Electron/releases/tag/1.2.2-b1-1) microscope hardware specifications file (.json) (see bioRxiv preprint [here](https://www.biorxiv.org/content/10.1101/2021.05.31.446382v2)). The script runs in Fiji, and an active internet connection is required.

<br />

DISCLAIMER: ***

## How it works
The MethodsJ2 script guides to users to input information about a microscopy experiment. The script displays dialog boxes wherein users can directly input information as text, or select the appropriate options from a drop-down menu assembled from the microscopy hardware specifications file generated in Micro-Meta App. User input and selections are then used to "fill in the blanks" in blocks of text designed to generate a draft of a experimental methods section.

<br />


![Montage_BPAE__8bit_Montage](https://user-images.githubusercontent.com/64212264/120518327-77ad6200-c39f-11eb-9a6c-5a49c5aca810.png)

<br />

The output of MethodsJ2 should look something like this:

```

----- MethodsJ2 text generation based on user input and on a Micro-Meta App hardware file:

Images were acquired on a Axiovert 200M Compound Commercial-custom modified inverted microscope 
(Zeiss) configured for Widefield Epifluorescence microscopy, controlled with Zen software 
(2.6 Blue edition, Zeiss), equipped with a 63x NA 1.4 Apochromat DIC Mineral Oil objective 
(Zeiss). 

Images had a width of 1012 and a height of 1020 pixels, 1 planes (z), 3 channels, 1 timepoints, 
with dimensional order XYCZT. Voxels had a lateral size of 0.14 um.

DAPI was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and wavelength 
selection was carried out with a G 365 excitation filter (Zeiss), a FT 395 dichroic mirror 
(Zeiss) and a BP 445/50 emission filter (Zeiss). Images were acquired on a Axiocam506 
CCD camera (Zeiss) with an exposure time of 200.00 ms with gain set to and 2x2 binning. 
Phalloidin-Alexa488 was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and 
wavelength selection was carried out with a BP 450-490 excitation filter (Zeiss), a FT 510 
dichroic mirror (Zeiss) and a BP 515-565 emission filter (Zeiss). Images were acquired on a 
Axiocam506 CCD camera (Zeiss) with an exposure time of 200.00 ms with gain set to and 2x2 binning.
Mitotracker Orange was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and 
wavelength selection was carried out with a BP 546/12 excitation filter (Zeiss), a FT 580 dichroic 
mirror (Zeiss) and a LP 590 emission filter (Zeiss). Images were acquired on a Axiocam506 CCD 
camera (Zeiss) with an exposure time of 200.00 ms with gain set to and 2x2 binning.

Acknowledgements: 
Images were collected and/or image processing and analysis for this manuscript was performed 
in (the) Advanced BioImaging Facility (ABIF) at McGill, with the assistance of Joel Ryan. 
(RRID: SCR_017697).

```

Acknowledgements: 
 Images were collected and/or image processing and analysis for this manuscript was performed in (the) Advanced BioImaging Facility (ABIF) at McGill, with the assistance of Joel Ryan. (RRID: SCR_017697).

## How to use MethodsJ2
Please install Fiji from [fiji.sc](fiji.sc) following the recommended installation procedure. Make sure you have an active internet connection

Download the python script MethodsJ2.py file from this repo, as well as the example Micro-Meta App hardware specifications file (abif-axiovert1.json), and the example images (BPAE_3color_30p-200ms_63xOil_003_diffExp_Int__.czi).

Drag and drop the python script MethodsJ2.py onto the main Fiji window, this should open a script editor window. Alternatively, click on File > New > Script... to open a script editor window, and then in that script editor, click on File > Open, navigate to the appropriate folder and select MethodsJ2.py

Once the script is loaded, make sure the appropriate language is selected - click on Language, select Python.

Click the "Run" button, and follow the dialog boxes, filling in the information as accurately as possible. More information on each dialog box is given below

<br />

### -- Welcome to MethodsJ2
This first window will prompt you for a microscopy image file, in order to extract metadata. You can drag and drop a file into the text input field, or click Browse, navigate to the appropriate folder, and select the appropriate image. We recommend you check the metadata and Bio-Formats metadata boxes, which will open metadata files which can help fill in crucial information.

Please note that MethodsJ2 will open the image in Fiji (using Bio-Formats), and so memory limits might apply. 

### -- Sample preparation Information

This dialog box asks users to fill out sample preparation information. **Given the variety specimens and preparations, this input will not contribute to text generation**, but is rather there as a reminder for what information is important when writing a methods section. As per community guidelines, it is important for Materials and Methods to clearly indicate a sample description, sample preparation, mounting medium, coverglass and sample holder. 

Since this can easily be redundant, it is up to the user to generate the sample preparation text make sure these elements are covered.

For example:

* Sample description: e.g. HEK-293T cells expressing GFP-tubulin

* Sample preparation: grown on No. 1.5 glass coverslips, fixed with 4% PFA and stained with 1 ug/ul DAPI 

* Mounting medium: mounted in Vectashield

* Coverglass: _(1.5 glass coverslips)_

* Sample holder: on glass slides


Another example

* Sample description: e.g. Live CHO-K1 cells expressing GFP-Paxillin

* Sample preparation: grown overnight on Geltrex-coated glass bottom Ibidi u-well slides

* Mounting medium: in DMEM with phenol red supplemented with 10% Fetal Calf Serum, and 1x Pen/Strep

* Coverglass: _(1.5 glass bottom ibidi u-well slides)_

* Sample holder: _(glass bottom ibidi u-well slides)_


### -- Image Dimensions

Here, the script gets image dimensions metadata from the previously selected image. If this data appears to be wrong, it is possible that the metadata is not readable by Fiji / BioFormats - in which case, crucial metadata is likely missing, and we recommend paying close attention to the information 

### -- Microscope hardware: select the Micro-Meta App Microscope.json file

In this dialog box, the script will attempt to describe the system as best as it can based on the metadata. From there, the user is prompted to select a Micro-Meta App hardware specifications file corresponding to the microscope used to acquire the image. This hardware specification file will be used by the script to provide drop-down menus for the user to select which components were used to acquire the image, for example which objective from the list of objectives available on the selected microscope.

### -- Microscope system overview

Here, the user is asked to select the best general descriptor for the microscopy system selected, as well as the the acquisition software detected in the hardware specifications file

### -- Select objective

The user is asked to select from a drop-down menu which objective was used. The drop-down menu is populated by the objectives available in the hardware specifications selected for this microscope. By selecting an objective based on its "name", the script will collect important objective information from the hardware specifications file (e.g. Magnification, Numerical Aperture, Correction, Collar, Manufacturer, etc). 

### -- Channel 1: Excitation, wavelength and detector selection

The user will now be prompted to provide information on the acquisition channel(s), for each channel separately, based on the order in which they appear in the image file. 

This channel dialog box will ask for a channel description, in which the user should generally input the fluorophore detected in the channel (fluorophore fusion or antibody conjugate is fine). Then, the user can choose the light source, the intensity of the light source, the excitation filter, dichroic mirror, emission filter and the detector used for this channel. These drop-down menus are again populated by information sourced from the hardware specifications file.

### -- Channel 1: Detector settings

This next dialog box allows users to input the settings on the detector. The dialog box itself and the requested information depends on whether a camera or point detector (PMT, APD, hybrid detector) was selected. For camera settings, the exposure time, gain and binning is requested, whereas for point detectors, dwell-time, and line/frame averaging information in requested.

Importantly, these two dialog boxes will appear for each channel in the image.

### -- Select optional devices:

If "optional" devices which are present on the microscopy system, the user will be prompted to select whether these have been used. For example, many systems are equipped with devices to control the environment (temperature, CO2, humidity, etc), however not all users will use these devices during their acquisition. Here, the users can select whether they used these systems for this experiment, and further information will be requested if needed.

### -- Acknowledgements

For core facilities, citations and acknowledgements are extremely to show progress, impact on research, and help enormously in securing funding. It is crucial for core facilities and imaging scientists to be acknowledged on manuscripts where their systems have been used. To this end, this final dialog box asks the user to input the name of the core facility, any staff member who contributed to training and support for the microscopy experiments, and a Research Resource ID (if applicable). These inputs will be used for text generation of a draft acknowledgement sentence, which can be revised and added to a manuscript.



<br />


## Known issues
### OMERO plugins in Fiji
Currently, the script does not work if OMERO plugins are installed (selected for updates) in Fiji. The current workaround is to either uncheck OMERO as an update site in your current Fiji installation (Help > Update > Manage Update Sites) -- or -- simply use a fresh installation of Fiji making sure OMERO is not selected as an update site.

### Transmitted light image channels not yet supported
We are modifying the script to allow transmitted light images to be described (e.g. DIC, Brightfield, Phase Contrast, Dark field). 

<br />

## Customization
It will be possible for imaging scientists and core facilities to customize the dialog boxes and output text ot better suit the needs of their users. Rather than make changes  in the python script, the information required to generate dialog boxes is found in a MethodsJ2 structure file, which is a JSON file stored in this github repository. 

For example, imaging scientists could add dialog boxes to select devices that are specific to their work, but which might not appear in Micro-Meta App, such as fluidics devices, stimulus projectors, electrophysiology pipettes and electrodes, etc. 

More information will be available soon, but the MJ2 json file can be downloaded, modified following the general structure of the file, and link that modified file either locally, or via a URL, provided it is publicly accessible.




