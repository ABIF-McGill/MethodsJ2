########################################################################################################
#
#
#	MethodsJ2: A Software Tool to Improve Microscopy Methods Reporting
#
#
#	Joel Ryan 1, Thomas Pengo 2, Alex Rigano 3, Paula Montero Llopis 4, Michelle S. Itano 5,
#   Lisa Cameron 6, Guillermo Marqués 7, Caterina Strambio-De-Castillia 3,
#   Mark A. Sanders 7,*  Claire M. Brown 1,*
#
#	Based on MethodsJ Blurb generator by Thomas Pengo (2019)
#
#
#
#	1. Advanced BioImaging Facility (ABIF) &amp; Department of Physiology, McGill University,
#	Montreal, Quebec, Canada, H4W 2R2
#	2. University of Minnesota Informatics Institute, University of Minnesota, 55455, United States
#	3. Program in Molecular Medicine, University of Massachusetts Medical School, Worcester,
#	MA 01605, USA
#	4. MicRoN, Department of Microbiology, Harvard Medical School, Boston, Massachusetts,
#	02115, USA
#	5. Neuroscience Microscopy Core, University of North Carolina, Chapel Hill, North Carolina,
#	27599, USA
#	6. Light Microscopy Core Facility, Duke University, Durham, North Carolina, 27708, USA
#	7. University Imaging Centers and Department of Neuroscience, University of Minnesota,
#	55455, United States
#
#	* Corresponding Authors, equal contributions: msanders@umn.edu, claire.brown@mcgill.ca
#
#
#
# 	August 06 2021
#
#	See biorxiv preprint:
#	MethodsJ2: A Software Tool to Improve Microscopy Methods Reporting
#	doi: https://doi.org/10.1101/2021.06.23.449674
#
########################################################################################################


# Version 1.2 
# developed with structure file: MJ2_structure_file_001.json


##########################################################
# import packages and modules
##########################################################


mj2_version = "v1.2"

import time
import datetime
from ij.gui import NonBlockingGenericDialog
import os
from java.io import File
from ij import IJ
from ij.gui import GenericDialog, NonBlockingGenericDialog
from fiji.util.gui import GenericDialogPlus
from ij import WindowManager as WindowManager

from loci.plugins import BF
from loci.plugins. in import ImporterOptions

import urllib2
import json

from __builtin__ import any as b_any



#@ OMEXMLService omeservice
#@ LogService logger
#@ Context context


from org.python.core import codecs

codecs.setDefaultEncoding('utf-8')

import sys
from org.scijava.ui.swing.console import LoggingPanel
from loci.formats import ImageReader

from ome.units import UNITS

import csv

def showText(text, title="Model output", hint="This is an example"):
	from javax.swing import JDialog, JEditorPane, BoxLayout, JLabel, JPanel, JScrollPane
	from java.awt import Dimension

	a = JDialog(None, title)

	p = JPanel()
	b = BoxLayout(p, BoxLayout.Y_AXIS)
	p.setLayout(b)

	t = JEditorPane("text/plain", text)

	p.add(JLabel(hint))
	p.add(JScrollPane(t))

	a.add(p)

	a.setPreferredSize(Dimension(500, 300))
	a.setLocationRelativeTo(None)
	a.pack()

	t.selectAll()
	t.copy()

	a.show()

	return a




def textCleanUp(string):
	string = string.replace('CCD.json', 'CCD camera')
	string = string.replace('CMOS.json', 'sCMOS camera')
	string = string.replace('IntensifiedCamera.json', 'intensified CCD camera')
	string = string.replace('gain set to and', '')
	string = string.replace(', with the assistance of . (', '. (')
	string = string.replace('(RRID: ).', '')
	string = string.replace('.json', '')
	string = string.replace('wide field', 'widefield')
	string = string.replace('Mineral Oil', 'oil')
	string = string.replace('  ', ' ')
	string = string.replace('  ', ' ')
	string = string.replace('..', '.')
	string = string.replace('The time interval between frames was n/a s','')


	return (string)


# The whole script is wrapped in this "main()" function. At the moment, this is only to allow to have functional "Cancel" buttons
# With each "showDialog()" command, an if statement if gui.wasCanceled(): return None exits the script

def main():
	mj1_errors = ''
	MMtext = ''
	BLURB = ""
	acknowledgement_blurb = ''

	gui = NonBlockingGenericDialog("")
	MJ2_structure_file_URL = 'https://raw.githubusercontent.com/ABIF-McGill/MethodsJ2/main/MJ2_structure_files/MJ2_structure_file_001.json'
	page_to_retrieve = urllib2.urlopen(
MJ2_structure_file_URL)
	settingsDialogJSON = json.load(page_to_retrieve)
	settings = settingsDialogJSON['settings']


	def print_and_log(a, b, c):
		print(a + " " + b)
		IJ.log(a +" " + b)
		writer.writerow([a, c, b])
		

	def welcomeBox():

		gui = GenericDialogPlus("MethodsJ2")

		gui.addMessage(
			"Welcome to MethodsJ2 - a tool to help write materials and methods sections for imaging experiments \n")
		gui.addMessage("")
		gui.addMessage(
			"First, the script will extract as much information as possible from the metadata of an image file. \n \n")
		gui.addFileField("Please select an image representative of your imaging experiments", "")
		gui.addMessage("")
		# gui.addFileField("Please select a MethodsJ2 settings structure file ", "")
		# gui.addMessage("")
		gui.addCheckbox("Display original metadata (recommended)", True) 
		gui.addCheckbox("Display Bio-Formats OME-XML metadata (recommended)", True)
		gui.addMessage("\n")

		gui.addRadioButtonGroup("Save output: \n", ["Save methods data in same folder as image ", "Select a folder to save methods data"], 1, 2, "Save methods data in same folder as image ")
		
		
		
		
		gui.showDialog()
		if gui.wasCanceled():
			return None
		filename = gui.getNextString()
		# componentsJson = gui.getNextString()
		componentsJson = ''

		# scopeJSONFile = 0 #gui.getNextString()
		showBioFormatsMetadata = gui.getNextBoolean()
		showOrigMetadata = gui.getNextBoolean()
		choice = gui.getNextRadioButton()
		return [filename, componentsJson, showBioFormatsMetadata, showOrigMetadata, choice]

	# return [filename, showBioFormatsMetadata, showOrigMetadata]

	# just retrieve info from things that will only exist in one instance (e.g. microscope stand, software)

	def getInfo_noDialogBox(settings, i):
		blurble = ''
		if settings[i].get('Information') == "MicroscopeStand":
			if microscope_stand.get('Schema_ID') == settings[i].get('Schema_ID'):
				list_attribute_elements = []
				for j in range(0, len(settings[i]['attributes'])):
					list_attribute_elements.append(microscope_stand.get(settings[i]['attributes'][j], ''))
				blurble = settings[i].get('blurb', '') % tuple(list_attribute_elements)

		return (blurble)

	def dialog_adder(settings, i):
		if settings[i].get('Add_to_same_row') == 1:
			gui.addToSameRow()

		if settings[i].get('Dialog_Type') == 'addCheckbox':
			gui.addCheckbox(settings[i]['Setting'], False)

		if settings[i].get('Dialog_Type') == 'addStringField':
			gui.addStringField(settings[i]['Setting'], settings[i].get('metadata value'), settings[i].get('width', 12))

		if settings[i].get('Dialog_Type') == 'addMessage':
			gui.addMessage(settings[i].get('message'))
			gui.addMessage(" \n ")

		if settings[i].get('Dialog_Type') == 'addChoice':
			settings[i]['tempList'] = []
			for l in range(0, len(components)):
				if components[l].get('Schema_ID') in settings[i].get('Schema_ID'):
					settings[i]['tempList'].append(components[l]['Name'])

			if len(settings[i]['tempList']) == 0:
				gui.addMessage(str(settings[i]['Setting']) + 'not found')
			else:
				gui.addChoice(settings[i]['Setting'], settings[i]['tempList'], '')

		if settings[i].get('Dialog_Type') == 'addChoiceInternal':
			gui.addChoice(settings[i]['Setting'], settings[i]['choices'], '')

	# gui.showDialog()

	def dialog_getter(settings, i):
		if settings[i].get('Dialog_Type') == 'addCheckbox':
			settings[i]['userInput'] = str(gui.getNextBoolean())
			print_and_log(settings[i].get('Setting'), (settings[i]['userInput']), settings[i].get('metadata value', ''))

		if settings[i].get('Dialog_Type') == 'addStringField':
			settings[i]['userInput'] = gui.getNextString()
			print_and_log(settings[i].get('Setting'), (settings[i]['userInput']), settings[i].get('metadata value', ''))

		if settings[i].get('Dialog_Type') == 'addChoice':
			if len(settings[i]['tempList']) > 0:
				settings[i]['userInput'] = gui.getNextChoice()
				print_and_log(settings[i].get('Setting'), (settings[i]['userInput']), settings[i].get('metadata value', ''))
			else:
				settings[i]['blurb'] = "not found"

		if settings[i].get('Dialog_Type') == 'addChoiceInternal':
			settings[i]['userInput'] = gui.getNextChoice()
			print_and_log(settings[i].get('Setting'), (settings[i]['userInput']), settings[i].get('metadata value', ''))
		return (settings[i].get('userInput'))

	def getInfoAndBlurb(userInput, settings, i):
		list_attribute_elements = []

		if settings[i].get('Dialog_Type') == "addStringField":
			if settings[i].get('userInput') == 'n/a':
				blurble = ''
			else:
				blurble = settings[i].get('blurb', '') % str(userInput)
		elif settings[i].get('Dialog_Type') == "addMessage":
			blurble = ''
		elif settings[i].get('Dialog_Type') == "addChoiceInternal":
			blurble = settings[i].get('blurb', '') % str(userInput)

		else:
			blurble = ' '
			if settings[i].get('blurb') == "not found":
				blurble = ' '
			if len(settings[i].get('tempList', [])) > 0:
				for l in range(0, len(components)):
					checkComp = components[l].get('Schema_ID')
					checkSetting = settings[i].get('Schema_ID', 0)
					if (checkComp in checkSetting) and (components[l].get('Name') == userInput):

						for j in range(0, len(settings[i]['attributes'])):
							list_attribute_elements.append(components[l].get(settings[i]['attributes'][j], ''))
				blurble = settings[i].get('blurb', '') % tuple(list_attribute_elements)

		return (blurble)


	image_check = False
	while image_check == False:
		initial = welcomeBox()
	
		# get welcome box values
		filename = initial[0]
		# scopeJSONFile = initial[1]
		showBioFormatsMetadata = initial[2]
		showOrigMetadata = initial[3]

		# open image and display OME-XML metadata (if selected)
		options = ImporterOptions()
		options.setShowMetadata(showBioFormatsMetadata)
		options.setShowOMEXML(showBioFormatsMetadata)
		options.setId(filename)
		try: 
			imps = BF.openImagePlus(options)
			for imp in imps:
				imp.show()
			image_check = True
		except:
			print("Selected file: ")
			print(filename)
			print("File could not be read by BioFormats")
			gui = GenericDialogPlus("Not a readable image")
			gui.addMessage("The selected file cannot be read by BioFormats in Fiji/Image. \n")
			gui.addMessage("Please run the script again and select a different image file.")
			gui.showDialog()
			IJ.log("Selected file: " + filename)
			IJ.log("File could not be read by BioFormats")
			continue
			#sys.exit() 

	# display image original metadata from acquisition software (if selected)
	if showOrigMetadata == True:
		var = IJ.run("Show Info...")

	# time interval stuff - need to find more cohesive method
	current_imp = WindowManager.getCurrentImage()
	calibration = current_imp.getCalibration()

	# Collect and store metadata using ImageReader
	# Adapted from https://github.com/ome/bioformats/blob/develop/components/formats-gpl/utils/GetPhysicalMetadata.java
	ir = ImageReader()
	m = omeservice.createOMEXMLMetadata()
	ir.setMetadataStore(m)
	ir.setId(filename)



	# set csv save directory
	folder_path_button = initial[4]
	if folder_path_button == "Select a folder to save methods data":
		folder_path = IJ.getDirectory('Choose a folder to save your data');
	else:
		folder_path = os.path.dirname(os.path.abspath(initial[0])) + os.path.sep

	print(folder_path)
	imagefilename_no_extension = os.path.basename(filename.split(".",1)[0])
	
	counter = 0
	file_check = True
	
	while file_check == True:
		file_to_create = (folder_path + "MethodsJ2_methods_text_" + imagefilename_no_extension + "_" + "%03d" % (counter,)  +".csv")
		file_check = os.path.isfile(file_to_create)
	
		if file_check == True:
			counter = counter + 1

	print(file_to_create)
	
	
	f = open(file_to_create, 'wb')
	writer = csv.writer(f)
	writer.writerow(['Label', 'Image metadata value', 'User input value'])

	
	print_and_log("Script", "MethodsJ2 " + mj2_version, '')
	print_and_log("Date", str(datetime.datetime.now()), '')

	print_and_log("Image file: ", str(initial[0]), '')
	print_and_log("MJ2 structure file: ", MJ2_structure_file_URL, '')


	
	time.sleep(0.25)

	##################################
	################################## mix mj1 and mj2
	##################################

	# Some checks
	ninstruments = m.getInstrumentCount()
	if ninstruments > 1:
		# logger.error("More than one instrument found. Automatic generation will not work...")
		mj1_errors += (
" More than one instrument found in the image metadata - image metadata may be incomplete, or inaccessible by bio-formats")
	if ninstruments == 0:
		# logger.error("No instrument in metadata - image metadata may be incomplete, or inaccessible by bio-formats")
		mj1_errors += (" No instrument in metadata - image metadata may be incomplete, or inaccessible by bio-formats")

	# Metadata text generation bits from mj1

	TEMPLATE_IMG_DIM = "The selected image has a width of {dim_X} pixels, a height of {dim_Y} pixels, {dim_C} channel(s), {dim_Z} slice(s), and {dim_T} frame(s), with a dimensional order of {dim_order}. "
	TEMPLATE_PIXEL_SIZE = "The lateral pixel size is {pxx_microns} microns. "
	TEMPLATE_GENERAL = "Imaging data was acquired on a {ID} system, using a {objective} {NA} NA objective. "
	TEMPLATE_CHANNEL = "The excitation and emission wavelengths for channel {ch} were {ex} and {em} and the exposure time was {et}. "
	TEMPLATE_3D = "A series of slices was collected with a step size of {pzz_microns} microns. "
	TEMPLATE_TIME = "Images were acquired with a time interval of {timeInterval} {timeIntervalUnits}. "

	BLURB = ""
	blurb = ''
	blurb_dim = ''

	# get image dimensions, dimension order

	dim_X = m.getPixelsSizeX(0)
	dim_Y = m.getPixelsSizeY(0)
	dim_C = int(str(m.getPixelsSizeC(0)))  ### java-element thing? -> to integer...
	dim_Z = m.getPixelsSizeZ(0)
	dim_T = m.getPixelsSizeT(0)
	dim_order = m.getPixelsDimensionOrder(0)

	
	temp_img_dim = TEMPLATE_IMG_DIM.format(dim_X=dim_X, dim_Y=dim_Y, dim_C=dim_C, dim_Z=dim_Z, dim_T=dim_T,
									 dim_order=dim_order)

	BLURB += temp_img_dim

	###
	### MJ1: get pixel size, z-step size, time interval
	###

	pxx_microns = "UNKNOWN"
	if ninstruments == 1:
		try:
			pxx_microns = "{:.2f}".format(m.getPixelsPhysicalSizeX(0).value(UNITS.MICROMETER))
			BLURB += TEMPLATE_PIXEL_SIZE.format(pxx_microns=pxx_microns)
		except:
			# logger.error(sys.exc_info()[0])
			msg = " Could not extract physical pixel size! The image might be missing some crucial metadata."
			# logger.error(msg)
			mj1_errors += (msg)
			pxx_microns = "n/a"

	# Is it 3D?
	is3D = ir.getSizeZ() > 1

	pzz_microns = "UNKNOWN"
	if ninstruments == 1:
		try:
			pzz_microns = "{:.2f}".format(m.getPixelsPhysicalSizeZ(0).value(UNITS.MICROMETER))
			BLURB += TEMPLATE_3D.format(pzz_microns=pzz_microns)
		except:
			# logger.error(sys.exc_info()[0])
			msg = " No physical step size detected. The image might be missing some crucial metadata."
			mj1_errors += (msg)

			pzz_microns = "n/a"
	# get time interval, if timelapse (from Jython FRAP example on imagej.net)

	time_interval = "n/a"
	time_units = ''
	time_interval_blurb = "n/a"

	if str(dim_T) != '1':
		time_interval = calibration.frameInterval
		time_units = calibration.getTimeUnit()
		# print ("time int " + str(frame_interval) + " " + str(time_units))
		time_interval_blurb = TEMPLATE_TIME.format(timeInterval=str(time_interval), timeIntervalUnits=str(time_units))
		BLURB += TEMPLATE_TIME.format(timeInterval=str(time_interval), timeIntervalUnits=str(time_units))

	

	for i in range(0, len(settings)):
		if settings[i].get('metadata key') == 'getPixelsSizeX':
			settings[i]['metadata value'] = str(dim_X)
		if settings[i].get('metadata key') == 'getPixelsSizeY':
			settings[i]['metadata value'] = str(dim_Y)
		if settings[i].get('metadata key') == 'getPixelsSizeC':
			settings[i]['metadata value'] = str(dim_C)
		if settings[i].get('metadata key') == 'getPixelsSizeZ':
			settings[i]['metadata value'] = str(dim_Z)
		if settings[i].get('metadata key') == 'getPixelsSizeT':
			settings[i]['metadata value'] = str(dim_T)
		if settings[i].get('metadata key') == 'getPixelsDimensionOrder':
			settings[i]['metadata value'] = str(dim_order)
		if settings[i].get('metadata key') == 'getPixelsPhysicalSizeX':
			settings[i]['metadata value'] = str(pxx_microns)
		if settings[i].get('metadata key') == 'getPixelsPhysicalSizeZ':
			settings[i]['metadata value'] = str(pzz_microns)
		if settings[i].get('metadata key') == 'frameInterval':
			settings[i]['metadata value'] = (str(time_interval) + ' ' + str(time_units))

	
	#############################
	### experiment dialog box
	############################

	blurb_prep = ''

	gui = NonBlockingGenericDialog("Sample Preparation Information")
	gui.addMessage("\n")

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Experiment description":
			dialog_adder(settings, i)
	gui.showDialog()
	if gui.wasCanceled():
		return None

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Experiment description":
			user_input = str(dialog_getter(settings, i))
			blurb_prep += '\n' + getInfoAndBlurb(user_input, settings, i)

	######
	## img dimensions dialog box
	######

	gui = NonBlockingGenericDialog("Image dimensions")
	gui.addMessage("According to the metadata, you have selected an image with the following dimensions: \n")

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Image dimensions":
			dialog_adder(settings, i)
	gui.showDialog()
	if gui.wasCanceled():
		return None
	# blurb =''
	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Image dimensions":
			user_input = str(dialog_getter(settings, i))
			blurb_dim += ' ' + getInfoAndBlurb(user_input, settings, i)

	###
	### MJ1: get microscope information from metadata
	###

	# Manufacturer and modalities

	ID = None

	if ninstruments == 1:
		try:
			ID = m.getMicroscopeManufacturer(0)
		except:
			# logger.error(sys.exc_info()[0])
			ID = None

	if ID == None:
		ff = str(ir.getFormat())
		if "Zeiss" in ff:
			ID = "Zeiss"
		elif "Nikon" in ff:
			ID = "Nikon"

			tID = ir.getMetadataValue("m_sMicroscopePhysFullName")
			if tID is not None:
				ID = tID

		elif "Olympus" in ff:
			ID = "Olympus"
		else:
			ID = "manufacturer not found"

	for ic in range(ir.getSizeC()):
		mode = m.getChannelAcquisitionMode(0, ic)

		if ic > 0 and mode != mode0:
			# logger.warn("WARNING : Not all channels were acquired with the same modality..")
			mj1_errors += ("WARNING : Not all channels were acquired with the same modality..")
		else:
			mode0 = mode

	if mode == None:
		mode_with_spaces = "UNKNOWN"
	else:
		mode_with_spaces = ""
		if str(mode) == "TIRF":
			mode_with_spaces = str(mode)
		else:
			for letter in str(mode):
				if letter.isupper():
					mode_with_spaces += " " + letter.lower()
				else:
					mode_with_spaces += letter
	
	scopeManuMetadata = ID
	ID += " " + str(mode_with_spaces.strip())
	

	
	#########################################
	######## MJ2 Check instrument dialog box
	#########################################
	check_manufacturer = "Select a new hardware file"
	
	while check_manufacturer == "Select a new hardware file":
		gui = GenericDialogPlus("Microscope hardware: select the Micro-Meta App Microscope.json file")
		gui.addMessage("According to the metadata: \n" + temp_img_dim + "\n")
		gui.addMessage("This image appears to have been acquired on a: \n")
		gui.addMessage(ID + "\n")
		gui.addFileField("Please select a Micro-Meta App json file corresponding to this system", "")

		gui.showDialog()
		if gui.wasCanceled():
			return None
		scopeJSONFile = gui.getNextString()
		
	#print_and_log("\n" + "Micro-Meta App json file: " + str(scopeJSONFile) + "\n")
		print_and_log("Micro-Meta App json file: ", str(scopeJSONFile), '')
	

	###################################
	####### MJ2 load json file to data
	###################################

	# load json file
		# if json file isn't valid:
		# ValueError: No JSON object could be decoded 
		with open(scopeJSONFile) as json_file:
			try:
				data = json.load(json_file)
				

				microscope_stand = data['MicroscopeStand']
				scopeHandle = data.get('Name' ,'')
				scopeManu = microscope_stand.get('Manufacturer', '')
				scopeModel = microscope_stand.get('Model','')
				scopeType = microscope_stand.get('Type', '')
				scopeTextCSV = scopeManu + ' ' + scopeModel + ' '+ scopeType + ' ' + '(' + scopeHandle + ')'
				scopeText = "You have selected a Micro-Meta App file for a \n {scopeHandle},\n an {scopeType} system made by {scopeManu}. \n".format(
					scopeHandle=scopeHandle, scopeType=scopeType, scopeManu=scopeManu)

				
			except ValueError:
				print('value error')
				gui = NonBlockingGenericDialog("Not a valid json file")
				gui.addMessage("The selected file is not a valid json file. Please select a valid json file created in Micro-Meta App")
				gui.showDialog()
				continue

			except KeyError:
				print('value error')
				gui = NonBlockingGenericDialog("Not a valid Micro-Meta App file")
				gui.addMessage("The selected file is not a valid hardware file - it might be corrupted or missing critical information. Please select a valid json file created in Micro-Meta App")
				gui.showDialog()
				continue
				
				
	
		
	########################################
	### Check microscope manufacturer
	#######################################
	
		if scopeManu.lower().strip() != scopeManuMetadata.lower().strip():
			gui = NonBlockingGenericDialog("Microscope manufacturer doesn't match")
			gui.addMessage("It looks like the selected microscope.json might not match the microscope used to acquire the selected image.")
			gui.addMessage("Microscope manufacturer according to image metadata: "+ scopeManuMetadata + "\n")
			gui.addMessage("Microscope manufacturer according to microscope.json hardware file: "+ scopeManu + "\n")
			gui.addRadioButtonGroup("Please choose:", ["Continue with this hardware file", "Select a new hardware file"], 1, 2, "Continue with this hardware file")
			gui.showDialog()
			choice = gui.getNextRadioButton()
			print(choice)
			if choice == "Continue with this hardware file":
				check_manufacturer = "Continue with this hardware file"
		else:
			check_manufacturer = "Continue with this hardware file"
			
		
	
	##### FIRST hardware json text and string formatting (eg. TRUE to "DIC", etc)

	components = data['components']

	for i in range(0, len(components)):
		if components[i].get('DIC') == True:
			components[i]['DIC'] = 'DIC'
		if components[i].get('DIC') == False:
			components[i]['DIC'] = ''
		if components[i].get('CorrectionCollar', '') == True:
			components[i]['CorrectionCollar'] = "(with a correction collar for " + components[i].get(
				'CorrectionCollarType', '') + ")"
		if components[i].get('CorrectionCollar', '') == False:
			components[i]['CorrectionCollar'] = ''
		if components[i].get('ContrastModulation') == "None":
			components[i]['ContrastModulation'] = ''
		if "ExcitationFilter" in components[i]:
			if (components[i].get('ExcitationFilter')) != 'na':
				target_id = (components[i]['ExcitationFilter']).split("/", 1)[1]
				for j in range(0, len(components)):
					if components[j]['ID'] == target_id:
						components[i]['ExcitationFilter'] = components[j]['Name']

		if "StandardDichroic" in components[i]:
			if (components[i].get('StandardDichroic')) != 'na':
				target_id = (components[i]['StandardDichroic']).split("/", 1)[1]
				for j in range(0, len(components)):
					if components[j]['ID'] == target_id:
						components[i]['StandardDichroic'] = components[j]['Name']

		if "EmissionFilter" in components[i]:
			if (components[i].get('EmissionFilter')) != 'na':
				target_id = (components[i]['EmissionFilter']).split("/", 1)[1]
				for j in range(0, len(components)):
					if components[j]['ID'] == target_id:
						components[i]['EmissionFilter'] = components[j]['Name']

	### get Schema_ID values for all components, in order to identify them later
	schema_ID = []
	for i in range(0, len(components)):
		schema_ID.append(components[i]['Schema_ID'])

	### generate list of unique schema_id values, easier for iterating later
	schema_ID_unique = list(set(schema_ID))

	scopeBlurb = ''
	for i in range(0, len(settings)):
		scopeBlurb += getInfo_noDialogBox(settings, i)


	print_and_log("Microscope: ", scopeTextCSV, ID)

	print(scopeManu.lower().strip())
	print('-----------------')
	print(scopeManuMetadata.lower().strip())


	

	gui = NonBlockingGenericDialog("Microscope system overview")
	gui.addMessage("According to the metadata, this image was acquired on a: \n")
	gui.addMessage(ID + "\n")
	gui.addMessage(scopeText + "\n")

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Microscope description":
			dialog_adder(settings, i)

	gui.showDialog()
	if gui.wasCanceled():
		return None

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Microscope description":
			user_input = str(dialog_getter(settings, i))
			scopeBlurb += ' ' + getInfoAndBlurb(user_input, settings, i)

	### unstable variable !!!!! Rethink structure...

	descriptor = user_input

	scopeText2 = "{scopeManu} {scopeModel} {scopeType} {descriptor}".format(scopeManu=scopeManu, scopeModel=scopeModel,
																			scopeType=scopeType, descriptor=descriptor)

	print(ir.getSizeC())
	
	###
	### MJ1: get objective information from metadata
	###

	if ninstruments == 1:
		nobjectives = m.getObjectiveCount(0)
		if nobjectives > 1:
			# logger.error("More than one objective found. Automatic generation will generate information for the first objective only.")
			mj1_errors += (
				"More than one objective found. Automatic generation will generate information for the first objective only.")
	objective = "UNKNOWN"
	if ninstruments == 1 and nobjectives > 0:
		try:
			magnification1 = m.getObjectiveNominalMagnification(0, 0)

			if magnification1 != None:
				objective = "{:.0f}x".format(magnification1)
		except:
			# logger.error(sys.exc_info()[0])
			msg = " Could not extract information about the objective! The image might be missing some crucial metadata."
			# logger.error(msg)
			mj1_errors += msg

	if objective == "UNKNOWN":
		if "Nikon" in ff:
			objective0 = str(ir.getMetadataValue("sObjective"))
			if objective0 is not None:
				objective = objective0

	NA = "UNKNOWN"
	if ninstruments == 1 and nobjectives > 0:
		try:
			NA1 = m.getObjectiveLensNA(0, 0)

			if NA1 != None:
				NA = str(NA1)
		except:
			msg = " Could not extract information about the objective! The image might be missing some crucial metadata."
			# logger.error(msg)
			mj1_errors += msg

	NAm = ir.getMetadataValue("Numerical Aperture")
	if NA == "UNKNOWN" and "Nikon" in ff and NAm is not None:
		NA = str(NAm)

	
	# Pixel size
	nimages = m.getImageCount()
	

	
	BLURB += TEMPLATE_GENERAL.format(ID=ID, objective=objective, NA=NA)
	##########################################
	########### Check objective dialog box
	###########################################

	objectiveBlurb = ''

	gui = NonBlockingGenericDialog("Select objective")
	objective_string = objective + " NA " + NA
	gui.addMessage("The metadata suggests that the following objective was used \n" + objective_string + "\n")
	#
	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Objective":
			# dialog_adder_attributes(settings, i, objective_string)
			settings[i]['metadata value'] = objective_string
			dialog_adder(settings, i)
	gui.showDialog()
	if gui.wasCanceled():
		return None
	# blurb =''
	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Objective":
			user_input = str(dialog_getter(settings, i))
			objectiveBlurb += ' ' + getInfoAndBlurb(user_input, settings, i)

	###################
	# Channels...
	####################
	for ic in range(ir.getSizeC()):
		try:
			ex0 = m.getChannelExcitationWavelength(0, ic)

			if ex0 == None:
				ex = "UNKNOWN"
			else:
				ex = "{:.0f} nm".format(ex0.value(UNITS.NANOMETER))
		except:
			# logger.error(sys.exc_info()[0])
			# logger.error("Wasn't able to extract channel wavelength information for channel {}.".format(ic+1))
			mj1_errors += (" Wasn't able to extract channel wavelength information for channel {}.".format(ic + 1))
			continue

		try:
			em0 = m.getChannelEmissionWavelength(0, ic)

			if em0 == None:
				em = "UNKNOWN"
			else:
				em = "{:.0f} nm".format(em0.value(UNITS.NANOMETER))
		except:
			# logger.error(sys.exc_info()[0])
			# logger.error("Wasn't able to extract channel wavelength information for channel {}.".format(ic+1))
			mj1_errors += (" Wasn't able to extract channel wavelength information for channel {}.".format(ic + 1))
			continue

		# try:
		ix = ir.getIndex(0, ic, 0)  # NOTE : First z plane, first timepoint only
		et = m.getPlaneExposureTime(0, ix)

		if et == None:
			et = "UNKNOWN"
		else:
			etms = et.value(UNITS.MILLISECOND)
			if "CZI" in ff:  # TODO Check if error is across other images
				# logger.warn("The exposure time was divided by 1000 to account for ms mistaken as s in CZI files")
				mj1_errors += (
					" The exposure time was divided by 1000 to allow reporting in seconds in .czi file format for channel {}.".format(ic + 1))

				etms = etms / 1000

			if etms < 1000:
				et = str("{:.2f} ms".format(etms))
			else:
				et = str("{} s".format(etms / 1000))

				if etms / 1000 > 600:
					# logger.warn("Exposure time for channel {} is {}s. That's longer than 10m, please double check metadata to make sure it's correct".format(ic+1,etms/1000))
					mj1_errors += (
						"Exposure time for channel {} is {}s. That's longer than 10m, please double check metadata to make sure it's correct".format(
							ic + 1, etms / 1000))
		try:
			pinholeSizeMetadata = m.getChannelPinholeSize(0, ic).value(UNITS.MICROMETER)
		except:
			pinholeSizeMetadata = 'UNKNOWN'
		try:
			cameraBinningMetadata = m.getDetectorSettingsBinning(0, 0)
		except:
			cameraBinningMetadata = 'UNKNOWN'

		# print("pinhole: " + str(pinholeSizeMetadata) + ", binning: " + str(cameraBinningMetadata))
		for i in range(0, len(settings)):
			if settings[i].get('Setting') == "Exposure time: ":
				settings[i]['metadata value'] = et

		BLURB += TEMPLATE_CHANNEL.format(ch=ic + 1, ex=ex, em=em, et=et)

		imp.setC(ic + 1)
		gui = GenericDialogPlus("Channel " + str(ic + 1) + ": Excitation, wavelength and detector selection ")
		gui.addMessage("\n The image metadata suggests that the excitation wavelength for channel " + str(
			ic + 1) + " is " + ex + " and the emission wavelength is " + em + ".")

		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == "Channel Settings" and settings[i].get('category') == "general":
				dialog_adder(settings, i)
		gui.showDialog()
		if gui.wasCanceled():
			return None

		print("Channel " + str(ic + 1) + " settings: ")
		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == "Channel Settings" and settings[i].get('category') == "general":
				user_input = str(dialog_getter(settings, i))
				blurb += ' ' + getInfoAndBlurb(user_input, settings, i)
				if settings[i].get('Setting') == "Detector:":
					detector = user_input

		for i in range(0, len(components)):
			if components[i].get('Schema_ID') in ["CCD.json", "IntensifiedCamera.json", "CMOS.json",
												  "AnalogVideo.json"]:
				channel_settings_template = "camera"
			if components[i].get('Schema_ID') in ["PhotoDiode.json", "PhotoMultiplierTube.json",
												  "HybridPhotoDetector.json"]:
				channel_settings_template = "scanning"

		gui = GenericDialogPlus("Channel " + str(ic + 1) + ': ' + channel_settings_template + " settings")

		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == "Channel Settings" and settings[i].get(
					'camera_vs_scanning') == channel_settings_template:
				dialog_adder(settings, i)
		gui.showDialog()
		if gui.wasCanceled():
			return None

		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == "Channel Settings" and settings[i].get(
					'camera_vs_scanning') == channel_settings_template:
				user_input = str(dialog_getter(settings, i))
				blurb += ' ' + getInfoAndBlurb(user_input, settings, i)

	##########################
	### Optional devices
	##########################

	gui = GenericDialogPlus("Select optional devices")
	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Toggle optional devices":
			for j in range(0, len(components)):
				if components[j].get('Schema_ID') == settings[i].get('Schema_ID'):
					dialog_adder(settings, i)
	gui.showDialog()
	if gui.wasCanceled():
		return None

	for i in range(0, len(settings)):
		if settings[i].get('Dialog_Box') == "Toggle optional devices":
			for j in range(0, len(components)):
				if components[j].get('Schema_ID') == settings[i].get('Schema_ID'):
					user_input = str(dialog_getter(settings, i))

	list_toggle_on = []

	for i in range(0, len(settings)):
		if (settings[i].get('Dialog_Box') == 'Toggle optional devices' and settings[i].get('userInput') == 'True'):
			list_toggle_on.append(settings[i].get('if_true_dialog_box'))
	
	

	for j in range(0, len(list_toggle_on)):
		gui = GenericDialogPlus(list_toggle_on[j])
		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == list_toggle_on[j]:
				dialog_adder(settings, i)
		gui.showDialog()
		if gui.wasCanceled():
			return None

		for i in range(0, len(settings)):
			if settings[i].get('Dialog_Box') == list_toggle_on[j]:
				user_input = str(dialog_getter(settings, i))
				blurb += ' ' + getInfoAndBlurb(user_input, settings, i)
		##########################
		### Acknowledgement
		##########################

	acknowledgement_blurb = '\n \nAcknowledgements: \n'

	gui = NonBlockingGenericDialog("Acknowledgements")

	for j in range(0, len(settings)):
		if settings[j].get('Dialog_Box') == 'Acknowledgements':
			dialog_adder(settings, j)
	gui.showDialog()
	if gui.wasCanceled():
		return None
	# blurb =''
	for j in range(0, len(settings)):
		if settings[j].get('Dialog_Box') == 'Acknowledgements':
			user_input = str(dialog_getter(settings, j))
			acknowledgement_blurb += ' ' + getInfoAndBlurb(user_input, settings, j)

	#print_and_log("\n *** MethodsJ1 warnings: \n" + mj1_errors + "n")
	print_and_log("MethodsJ1 warnings:", mj1_errors, '')

	print_and_log("MethodsJ1 text generation based on the metadata: ", textCleanUp(BLURB), '')

	#print_and_log(textCleanUp(BLURB))

	#print_and_log(scopeBlurb + objectiveBlurb)

	# print(blurb_prep)

	#print_and_log(blurb_dim)

	# blurb = blurb.replace('  ', ' ')
	# blurb = blurb.replace('..', '.')
	# blurb = blurb.replace('.json', '')
	#blurb += acknowledgement_blurb
	#blurb = textCleanUp(blurb)
	

	disclaimer = '\n Methods and acknowledgement sections text generated with MethodsJ2 - please verify for accuracy and grammatical correctness' 
	concat_text = scopeBlurb + objectiveBlurb + blurb_dim + '\n' + blurb + acknowledgement_blurb +'\n' + disclaimer
	concat_text = textCleanUp(concat_text)
	
	print_and_log("MethodsJ2 text generation based on user input and on a Micro-Meta App hardware file:", concat_text,'')

	#print_and_log(concat_text)

	showText(concat_text, "MethodsJ2 output",
			 "MethodsJ2 text generation based on user input and on a Micro-Meta App hardware file")

	f.close()


main()



