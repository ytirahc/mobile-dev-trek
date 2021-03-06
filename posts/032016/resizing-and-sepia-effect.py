#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2016, ytirahc, www.mobiledevtrek.com
# All rights reserved. Copyright holder cannot be held liable for any damages. 
# 
# Distributed under the Apache License (ASL). 
# http://www.apache.org/licenses/
# *****
# Description: This file is a script for Adobe Photoshop (tested with Photoshop CC 2015). 
# The current active image in Photoshop will be resized by the specified percentages
# in the array scaleFactor and will save those files to the specified directory,  
#
# Usage:	Filters -> MDT -> Create Scaled Versions in Batch (to select an input directory of multiple images)
#			Filters -> MDT -> Create Scaled Versions (for current image)
#			Filters -> MDT -> Create Sepia Effect
# *****


import os
from gimpfu import * 
import ntpath
import string


# *****
# create_sepia_effect
#
# Description: Applies sepia tone effect to current image
#
# Parameters:
# 		inGimpImg : Current image
#		inLayerinGimpImg : Current layer in current image
# *****
def create_sepia_effect(inGimpImg, inLayerinGimpImg):
		
	try:
		
		# Convert image to greyscale
		pdb.gimp_desaturate_full(inLayerinGimpImg, DESATURATE_LUMINOSITY)
		
		# Blur the greyscale image
		pdb.plug_in_gauss_iir(inGimpImg, inLayerinGimpImg, 2, True, True)
		
		# Add color layer with soft light mode
		sepiaColorLayer = gimp.Layer(inGimpImg, "sepia color layer", inLayerinGimpImg.width, inLayerinGimpImg.height, inLayerinGimpImg.type, 100, SOFTLIGHT_MODE)
		inGimpImg.add_layer(sepiaColorLayer, 0) 
		pdb.gimp_context_set_background((226,89,42))
		pdb.gimp_edit_fill(sepiaColorLayer, BACKGROUND_FILL)
		
	except Exception as err:
		gimp.message("Unexpected error: " + str(err))


# *****
# create_scaled_versions
#
# Description: Resize current image to 25%, 50% and 75% of original
#
# Parameters:
# 		inGimpImg : Current image
#		inLayerinGimpImg : Current layer in current image (not used)
#		inOutputDir : Directory to save resized images
# *****
def create_scaled_versions(inGimpImg, inLayerinGimpImg, inOutputDir):
	resizePercentageArray = [75, 50, 25]  # Percentages to scale input image
	
	gimpImgRFN = get_root_name_from_filepath(inGimpImg.filename) 
	
	for resizePercentage in resizePercentageArray:
		scaledHeight = int(inGimpImg.height * resizePercentage / 100)
		scaledWidth = int(inGimpImg.width * resizePercentage / 100)
		outputImgFN = os.path.join(inOutputDir, gimpImgRFN) + "_" + str(resizePercentage) + "percent.jpg"
		scale_and_save_image(inGimpImg, scaledWidth, scaledHeight, outputImgFN)


# *****
# create_scaled_versions_batch
#
# Description: Processes a directory of images to resize and save the results
#
# Parameters:
# 		inGimpImg : Current image (not used)
#		inLayerinGimpImg : Current layer in current image (not used)
#		inInputDir : Directory with images to be resized
#		inOutputDir : Directory to save resized images
# *****
def create_scaled_versions_batch(inGimpImg, inLayerinGimpImg, inInputDir, inOutputDir):
	
	for fileInDir in os.listdir(inInputDir):   # Look at all files in the input directory
	
		try:
			
			inputImgFN = os.path.join(inInputDir, fileInDir)
			
			# Process only images that are jpgs
			inputImage = None
			if(inputImgFN.lower().endswith(('.jpeg', '.jpg'))):
				inputImage = pdb.file_jpeg_load(inputImgFN, inputImgFN)
			
			# Scale and save jpgs images
			if(inputImage != None):
				if(len(inputImage.layers) > 0):
					create_scaled_versions(inputImage, inputImage.layers[0], inOutputDir)
		
		except Exception as err:
			gimp.message("Unexpected error: " + str(err))


# *****
# scale_and_save_image
#
# Description: Scales and input image and saves the result
#
# Parameters:
# 		inImg : Image to be resized
#		inWidth : Resize width
#		inHeight : Resize height
#		inFilePathName : Path and filename to save resized image
# *****
def scale_and_save_image(inImg, inWidth, inHeight, inFilePathName):

	# Duplicate the image & resize
	scaledImg = pdb.gimp_channel_ops_duplicate(inImg)  # use currently loaded image
	pdb.gimp_image_scale(scaledImg, inWidth, inHeight)
	
	# Save the resized image as a jpg
	flattenedImgLayer = pdb.gimp_image_flatten(scaledImg)
	pdb.file_jpeg_save(scaledImg, flattenedImgLayer, inFilePathName, inFilePathName, 0.9, 0, 0, 0, "Created with GIMP", 0, 0, 0, 0)	


# *****
# get_root_name_from_filepath
#
# Description: Extract filename (without extension) from full file path and name
#
# Parameters:
# 		inFullFP : Path and filename
# *****
def get_root_name_from_filepath(inFullFP):

	fullFN = ntpath.basename(inFullFP)	
	
	fileName, fileExt = os.path.splitext(fullFN)
	
	return fileName


# *****
# Description: Registration of resize and sepia tone functions
# *****
register(
	"create_sepia_effect",
	"Create Sepia Effect",
	"Adds a sepia effect to an image",
	"ytirahc",
	"Proprietary",
	"2016",
	"<Image>/Filters/MDT/Create Sepia Effect",
	"*",
	[],
	[],
	create_sepia_effect)


register(
	"create_scaled_versions",
	"Create Scaled Versions",
	"Creates different scaled versions of an image",
	"ytirahc",
	"Proprietary",
	"2016",
	"<Image>/Filters/MDT/Create Scaled Versions",
	"*",
	[
		(PF_DIRNAME, "outputFolder", "Output directory", "")
	],
	[],
	create_scaled_versions)


register(
	"create_scaled_versions_batch",
	"Create Scaled Versions in Batch",
	"Creates different scaled versions of images in a directory",
	"ytirahc",
	"Proprietary",
	"2016",
	"<Image>/Filters/MDT/Create Scaled Versions in Batch",
	"*",
	[
		(PF_DIRNAME, "inputFolder", "Input directory", ""),
		(PF_DIRNAME, "outputFolder", "Output directory", "")
	],
	[],
	create_scaled_versions_batch)


main()
