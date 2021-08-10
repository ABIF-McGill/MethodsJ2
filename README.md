
# MethodsJ2
Building on [MethodsJ](https://github.com/tp81/MethodsJ) , **MethodsJ2** helps users write a materials and methods text for microscopy experiments by sourcing experiment information from metadata, as well as information from a microscope hardware configuration file generated in Micro-Meta App. A draft experiment methods section text is generated which can then be revised and used in written manuscripts and reports, etc. 

See [MethodsJ2: A Software Tool to Improve Microscopy Methods Reporting](https://www.biorxiv.org/content/10.1101/2021.06.23.449674v1) on bioRxiv

<br />




## Current version:

Current version in progress: 1.2


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5172827.svg)](https://doi.org/10.5281/zenodo.5172827)


Please run 'MethodsJ2_v1_2_.py'

**Main updates** : Script checks for appropriate file formats (e.g. images, Micro-Meta App hardware configuration files) and alerts user if unreadable file is selected. Verifies microscope manufacturer from image metadata and microscope hardware configuration file, alerts user if these are different. Outputs and saves a csv file containing all detected information (from image metadata) and all user input information (either manually entered or selected from Micro-Meta App hardware configuration file), as well as image file path, Micro-Meta App hardware configuration file path, and generated methods text output, allowing to check for discrepancies and to store and share the information. --Many thanks to our reviewers for these helpful suggestions!



<br />

## Requirements

This Python/Jython script requires [Fiji/ImageJ](fiji.sc) - a recent or fresh installation of Fiji is recommended, since the script requires that the BioFormats library is installed, and that the OMERO plugins are disabled.

MethodsJ2 version 1.0 available in this repository, tested in Fiji (ImageJ version 1.53c) on macOS Mojave 10.14.6 and macOS Catalina 10.15.7, and in Fiji (ImageJ version 1.53c) on Windows 10 Home. Requires BioFormats. Please note that OMERO plugins must be disabled in Fiji.

As requirements, to use **MethodsJ2**, users first need a raw image from a microscopy experiment as well as a previously generated in [Micro-Meta App](https://github.com/WU-BIMAC/MicroMetaApp-Electron/releases/tag/1.2.2-b1-1) microscope hardware specifications file (.json) (see bioRxiv preprint [here](https://www.biorxiv.org/content/10.1101/2021.05.31.446382v2)). 

The script runs in Fiji, and an active internet connection is required. A demo microscope hardware specifications file (.json) and image are provided to test the script.

<br />


<br />


DISCLAIMER: As per MethodsJ, this is not meant to be applied blindly, but rather to be used as a starting point. Metadata is recorded by the microscope driving software, so at best it reflects the way the microscope's software was configured. In addition, this script uses the fantastic BioFormats library. It has been designed to extract as much information as possible from the image data, but formats change occasionally so don't be surprised if the text doesn't completely reflect what you expect. If you do find some discrepancy, check with your facility staff (if the microscope is part of an imaging facility) for help on the appropriate wording or to check the configuration, and then with the BioFormats community to see if the metadata was not read correctly. If you believe there is an error in the script (not unlikely), feel free to reach out.


**Importantly**, please verify the text generation output and the csv file carefully or with someone familiar with the microscope or your experiments, in order to make sure that the information is correct, and that the grammar and syntax are ok, before copy-pasting the text into your manuscript. 


<br />

## Installation
No installation required. Please download the contents of this repository, and run the MethodsJ2_v1_2_.py script file in Fiji (detailed instructions below). The zipped repository should be around 20 Mb, mostly due to demo images, and download times depend on internet connection speed (should be under 1 minute on a standard system with a reasonable internet connection).

<br />



## How it works
The MethodsJ2 script guides users to input information about a microscopy experiment based on information from the image metadata, information from the hardware specifications file, and information directly input by the user. 

The script displays dialog boxes wherein users can directly input information as text, or select the appropriate options from a drop-down menu assembled from the microscopy hardware specifications file generated in Micro-Meta App. User input and selections are then used to "fill in the blanks" in blocks of text designed to generate a draft of a experimental methods section.


<br />


![Montage_BPAE__8bit_Montage](https://user-images.githubusercontent.com/64212264/120518327-77ad6200-c39f-11eb-9a6c-5a49c5aca810.png)
> Demo image (BPAE_3color_30p-200ms_63xOil_003_diffExp_Int__.czi).


<br />


<br />


<img src="https://user-images.githubusercontent.com/64212264/121219507-c3558500-c851-11eb-9d81-9748d386ea76.PNG" width="615" height="322">

> Screenshot from Micro-Meta App, used to generate a demo hardware specifications file. 
<br />

<br />




For the demo image and [Micro-Meta App](https://github.com/WU-BIMAC/MicroMetaApp-Electron/releases/tag/1.2.2-b1-1) hardware specifications file displayed above, the output of MethodsJ2 should look like this:
```

----- MethodsJ2 text generation based on user input and on a Micro-Meta App hardware file:

Images were acquired on a Axiovert 200M Compound Commercial-custom modified inverted microscope 
(Zeiss) configured for Widefield Epifluorescence microscopy, controlled with Zen software 
(2.6 Blue edition, Zeiss), equipped with a 63x NA 1.4 Apochromat DIC oil objective 
(Zeiss). 

Images had a width of 1012 and a height of 1020 pixels, 1 planes (z), 3 channels, 1 timepoints, 
with dimensional order XYCZT. Voxels had a lateral size of 0.14 um.

DAPI was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and wavelength 
selection was carried out with a G 365 excitation filter (Zeiss), a FT 395 dichroic mirror 
(Zeiss) and a BP 445/50 emission filter (Zeiss). Images were acquired on a Axiocam506 
CCD camera (Zeiss) with an exposure time of 200.00 ms with 2x2 binning. 
Phalloidin-Alexa488 was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and 
wavelength selection was carried out with a BP 450-490 excitation filter (Zeiss), a FT 510 
dichroic mirror (Zeiss) and a BP 515-565 emission filter (Zeiss). Images were acquired on a 
Axiocam506 CCD camera (Zeiss) with an exposure time of 200.00 ms with 2x2 binning.
Mitotracker Orange was excited with a X-Cite 120 LED light source (Excelitas) set to 30 % and 
wavelength selection was carried out with a BP 546/12 excitation filter (Zeiss), a FT 580 dichroic 
mirror (Zeiss) and a LP 590 emission filter (Zeiss). Images were acquired on a Axiocam506 CCD 
camera (Zeiss) with an exposure time of 200.00 ms with 2x2 binning.

Acknowledgements: 
Images were collected and/or image processing and analysis for this manuscript was performed 
in (the) Advanced BioImaging Facility (ABIF) at McGill, with the assistance of Joel Ryan. 
(RRID: SCR_017697).

```

<br />


<br />


## Instructions with demo image and hardware specifications file

Please install Fiji from [fiji.sc](fiji.sc) following the recommended installation procedure. Make sure you have an active internet connection

Please download the contents of this repository, including the python script MethodsJ2.py file, as well as the example Micro-Meta App hardware specifications file (abif-axiovert1.json), and the example images (BPAE_3color_30p-200ms_63xOil_003_diffExp_Int__.czi).

Drag and drop the python script MethodsJ2_v1_2_.py onto the main Fiji window, this should open a script editor window. Alternatively, click on File > New > Script... to open a script editor window, and then in that script editor, click on File > Open, navigate to the appropriate folder and select MethodsJ2_v1_2_.py

Once the script is loaded, make sure the appropriate language is selected - click on Language, select Python.

Click the "Run" button, and follow the dialog boxes, filling in the information as accurately as possible. More information on each dialog box is given below

When first running the script in Fiji, it may take up to ~30 seconds for the script to launch (before seeing the first dialog box). Running the script is pretty quick, and simply depends on availability of the required information about the image. If all parameters are known by the user, it should take only a couple of minutes to go through the script and generate a draft methods section. 

<br />

### -- Welcome to MethodsJ2


<img width="832" alt="Screen Shot 2021-08-09 at 9 46 07 PM" src="https://user-images.githubusercontent.com/64212264/128796096-1db67878-6473-488b-8802-60da200a01c7.png">


This first window will prompt you for a microscopy image file, in order to extract metadata. You can drag and drop a file into the text input field, or click Browse, navigate to the appropriate folder, and select the appropriate image. We recommend loading the metadata and Bio-Formats metadata (check boxes), which will open metadata files which can help fill in crucial information. 
***As a demo, please select 'BPAE_3color_30p-200ms_63xOil_003_diffExp_Int__.czi' 

Then, please select where to save the csv output for this run of MethodsJ2. The csv file can be saved in the same folder as the image, or you can choose another folder.

Please note that MethodsJ2 will open the image in Fiji (using Bio-Formats), and so memory limits might apply. 

After selecting the file and target folder, the script will try to open the image using Bio-Formats (memory limits might apply). 

Error check: If the file is unreadable by Bio-Formats (not an image, etc), it will alert the user and return to the previous window, allowing the user to select a new file. 


<br />

### -- Sample preparation Information

<img width="681" alt="Screen Shot 2021-06-02 at 2 38 48 PM" src="https://user-images.githubusercontent.com/64212264/121744748-56502280-cad1-11eb-9c98-ec1e14412cb8.png">


This dialog box asks users to fill out sample preparation information. **Given the variety specimens and preparations, this input will not contribute to text generation**, but is rather there as a reminder for what information is important when writing a methods section. As per community guidelines, it is important for Materials and Methods to clearly indicate a sample description, sample preparation, mounting medium, coverglass and sample holder. 

Since this can easily be redundant, it is up to the user to generate the sample preparation text make sure these elements are covered.

For the demo:

* Sample description: e.g. Cultured BPAE cells

* Sample preparation: grown on No. 1.5 glass coverslips, fixed with 4% PFA and stained with DAPI, Phalloidin Alexa Fluor-488 and MitoTracker Orange

* Mounting medium: mounted in Cytoseal

* Coverglass: _(1.5 glass coverslips)_

* Sample holder: on glass slides


Another example

* Sample description: e.g. Live CHO-K1 cells expressing GFP-Paxillin

* Sample preparation: grown overnight on Geltrex-coated glass bottom Ibidi u-well slides

* Mounting medium: in DMEM with phenol red supplemented with 10% Fetal Calf Serum, and 1x Pen/Strep

* Coverglass: _(1.5 glass bottom ibidi u-well slides)_

* Sample holder: _(glass bottom ibidi u-well slides)_

<br />

### -- Image Dimensions

<img width="717" alt="Screen Shot 2021-06-02 at 2 39 18 PM" src="https://user-images.githubusercontent.com/64212264/121744766-5d773080-cad1-11eb-8bea-a601fe9c5be5.png">


Here, the script gets image dimensions metadata from the previously selected image. If this data appears to be wrong, it is possible that the metadata is not readable by Fiji / BioFormats - in which case, crucial metadata is likely missing, and we recommend paying close attention to the information 

<br />

### -- Microscope hardware: select the Micro-Meta App Microscope.json file

<img width="1332" alt="Screen Shot 2021-06-02 at 2 39 31 PM" src="https://user-images.githubusercontent.com/64212264/121744779-66680200-cad1-11eb-9405-d72a370f0801.png">

In this dialog box, the script will attempt to describe the system as best as it can based on the metadata. From there, the user is prompted to select a Micro-Meta App hardware specifications file corresponding to the microscope used to acquire the image. This hardware specification file will be used by the script to provide drop-down menus for the user to select which components were used to acquire the image, for example which objective from the list of objectives available on the selected microscope.

Error check: If the selected file is not a .json file generated with Micro-Meta App (by searching for the manufacturer of the microscope stand), the script will alert the user and return to the previous window, to select an appropriate .json file. Additionally, if the manufacturer detected in the image metadata does not match the manufacturer of the microscope stand (in the hardware configuration file), it will alert the user, who can then decide to choose a new file or continue with this file.

For the demo, please select 'abif_axiovert1_.json'


<br />

### -- Microscope system overview

<img width="732" alt="Screen Shot 2021-06-02 at 2 39 37 PM" src="https://user-images.githubusercontent.com/64212264/121744792-6d8f1000-cad1-11eb-94d4-8d16b9c382b2.png">


Here, the user is asked to select the best general descriptor for the microscopy system selected, as well as the the acquisition software detected in the hardware specifications file.

For the demo, please select 'Widefield Epifluorescence', and the software 'Zen' should have been detected by the script, sourced from the hardware specifications file.

### -- Select objective

<img width="589" alt="Screen Shot 2021-06-02 at 2 39 44 PM" src="https://user-images.githubusercontent.com/64212264/121744799-71229700-cad1-11eb-82a0-6bbbd79a5034.png">


The user is asked to select from a drop-down menu which objective was used. The drop-down menu is populated by the objectives available in the hardware specifications selected for this microscope. By selecting an objective based on its "name", the script will collect important objective information from the hardware specifications file (e.g. Magnification, Numerical Aperture, Correction, Collar, Manufacturer, etc). 

For the demo, please select '63X PLAN APOCHROMAT, NA=1.40, OIL, DIC' from the list of objectives available in the system

<br />

### -- Channel 1: Excitation, wavelength and detector selection

<img width="965" alt="Screen Shot 2021-06-02 at 2 40 23 PM" src="https://user-images.githubusercontent.com/64212264/121744820-77187800-cad1-11eb-8bfb-ff7b7826564d.png">


The user will now be prompted to provide information on the acquisition channel(s), for each channel separately, based on the order in which they appear in the image file. 

This channel dialog box will ask for a channel description, in which the user should generally input the fluorophore detected in the channel (fluorophore fusion or antibody conjugate is fine). Then, the user can choose the light source, the intensity of the light source, the excitation filter, dichroic mirror, emission filter and the detector used for this channel. These drop-down menus are again populated by information sourced from the hardware specifications file.

For the demo, the first channel can be described as 'DAPI', and the light source intensity used for acquisition of this channel was 50 %.

<br />

### -- Channel 1: Detector settings


<img width="460" alt="Screen Shot 2021-06-02 at 2 40 31 PM" src="https://user-images.githubusercontent.com/64212264/121744835-7aabff00-cad1-11eb-8cc1-69717494dcbe.png">


This next dialog box allows users to input the settings on the detector. The dialog box itself and the requested information depends on whether a camera or point detector (PMT, APD, hybrid detector) was selected. For camera settings, the exposure time, gain and binning is requested, whereas for point detectors, dwell-time, and line/frame averaging information in requested.

For the demo, the exposure time should be detected automatically. The gain setting is unavailable, and the Camera Binning should be set to 2x2

Importantly, these two dialog boxes will appear for each channel in the image. (Channel 1 is 'DAPI', Channel 2 is 'Phalloidin-488', and Channel 3 is 'MitoTracker Orange')

<br />

### -- Select optional devices:

<img width="671" alt="Screen Shot 2021-06-02 at 2 41 37 PM" src="https://user-images.githubusercontent.com/64212264/121744858-85ff2a80-cad1-11eb-855f-69bab0a315f8.png">

If "optional" devices which are present on the microscopy system, the user will be prompted to select whether these have been used. For example, many systems are equipped with devices to control the environment (temperature, CO2, humidity, etc), however not all users will use these devices during their acquisition. Here, the users can select whether they used these systems for this experiment, and further information will be requested if needed.

For the demo, neither there was no environmental conditioning or focus stabilization used for the acquisition.

<br />

### -- Acknowledgements

<img width="984" alt="Screen Shot 2021-06-02 at 2 42 07 PM" src="https://user-images.githubusercontent.com/64212264/121744874-8b5c7500-cad1-11eb-95c4-e23e26c7cce8.png">


For core facilities, citations and acknowledgements are extremely to show progress, impact on research, and help enormously in securing funding. It is crucial for core facilities and imaging scientists to be acknowledged on manuscripts where their systems have been used. To this end, this final dialog box asks the user to input the name of the core facility, any staff member who contributed to training and support for the microscopy experiments, and a Research Resource ID (if applicable). These inputs will be used for text generation of a draft acknowledgement sentence, which can be revised and added to a manuscript.

<br />

### -- Output

![Untitled_output_width_Cropped_v2](https://user-images.githubusercontent.com/64212264/121747449-6ec23c00-cad5-11eb-8434-0d7165d3d64f.png)


The output will appear in a popup window, already selected and copied to the clipboard. More information about the instance of the MethodsJ2 run is available in the ImageJ Log Window, as well as in the script editor console window (e.g. user selections, image file, microscope file, structure file, and output based only on metadata, as per MethodsJ)

<br />

### -- csv file 

A csv file is generated containing all the information detected from the image metadata and all the user input information (both manually entered and selected from the Micro-Meta App configuration file). The csv is saved either in the same folder as the image file, or in a folder selected by the user (in the first welcome dialog box). This csv file can be used to check for accuracy of the user-input information (compared to the metadata), and is the record for this particular run of MethodsJ2.

In many cases, information is input differently in the image metadata compared to how it is stored in Micro-Meta App (and OMERO). For example, information about the objective might be stored in the image metadata as "PlanApo 100x NA 1.4 (Zeiss)" or "Zeiss 100X Plan-Apo 1.4 N.A." or other permutations of the same information, depending on who set up the microscope. This makes text/string matching difficult. Thus, in the csv file, the user can directly compare and judge for themselves whether the information is accurate, by directly comparing the image metadata information with the user selection. 

As an example, rows 21 and 24 ('Microscope' and 'Select Objective') in the following screenshot are examples of information which coincide accurately, but do not have matching text.


![CSV_output_](https://user-images.githubusercontent.com/64212264/128735433-6a44693a-46cb-432c-a495-8f94a8741ffb.PNG)

> See [the example csv file here](https://github.com/ABIF-McGill/MethodsJ2/blob/main/MethodsJ2_methods_text_BPAE_3color_30p-200ms_63xOil_003_diffExp_Int___000.csv)


<br />


## Known issues
### OMERO plugins in Fiji
Currently, the script does not work if OMERO plugins are installed (selected for updates) in Fiji. The current workaround is to either uncheck OMERO as an update site in your current Fiji installation (Help > Update > Manage Update Sites) -- or -- simply use a fresh installation of Fiji making sure OMERO is not selected as an update site.

### Transmitted light image channels not yet supported
We are currently working on the script to allow transmitted light images to be described (e.g. DIC, Brightfield, Phase Contrast, Dark field). 

<br />

## Extensibility
It will be possible for imaging scientists and core facilities to customize the dialog boxes and output text ot better suit the needs of their users. Rather than make changes  in the python script, the information required to generate dialog boxes is found in a MethodsJ2 structure file, which is a JSON file stored in this github repository. 

For example, imaging scientists could add dialog boxes to select devices that are specific to their work, but which might not appear in Micro-Meta App, such as fluidics devices, stimulus projectors, electrophysiology pipettes and electrodes, etc. 

More information will be available soon, but the MJ2 json file can be downloaded, modified following the general structure of the file, and link that modified file either locally, or via a URL, provided it is publicly accessible.




