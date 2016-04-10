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
# Description: Python script to resize images by percentage and apply sepia tone effect 
# using ImageMagick via Wand (developed with & tested against Python 3.5, Wand 0.4.2)
# Resize
# The jpg image files of the specified input directory are resized by the specified percentages
# in the array resizePercentages and saved to the specified output directory.   
# Sepia
# The jpg image files of the specified input directory have the sepia tone effect applied and saved 
# to the specified output directory.
# 
# Usage: Running the script will both resize and apply the sepia tone effect to the jpg images in the
# input directory, saving the results to the output directory
# *****


import os
from wand.image import Image
from wand.color import Color


# *****
# SepiaToneEffectAndSave
#
# Description: Applies sepia tone effect to input image and saves the result
#
# Parameters:
#    inImage : An image opened using Wand
#    inSepiaImageFN : Output path and file name where the result is saved
# *****
def SepiaToneEffectAndSave(inImage, inSepiaImageFN):

    colorStr = '#e2592a'    # Sepia tone effect color

    # Apply the effect on a copy of the input image
    with inImage.clone() as imgClone:
        
        # Convert image to greyscale
        imgClone.type = 'grayscale'
        
        # Apply a slight blur
        imgClone.gaussian_blur(0,1)
        
        # Blend the sepia tone color with the greyscale layer using soft light
        fillColor = Color(colorStr)
        with Image(width=img.width, height=img.height, background=fillColor) as fillImg:
        
            imgClone.composite_channel('default_channels', fillImg, 'soft_light', 0, 0 )
        
        imgClone.save(filename=inSepiaImageFN)


# *****
# ResizeImageByPercentAndSave
#
# Description: Resizes image by specified percentage and saves the result
#
# Parameters:
#    inImage : An image opened using Wand
#    inResizePercentage : Percentage by which to resize image as a non negative integer
#    inResizedImageFN : Output path and file name where the result is saved
# *****
def ResizeImageByPercentAndSave(inImage, inResizePercentage, inResizedImageFN):
    
    with inImage.clone() as imgClone:
        
        resizeHeight = int(inResizePercentage * imgClone.height / 100)
        resizeWidth = int(inResizePercentage * imgClone.width / 100)
        
        imgClone.resize(resizeWidth, resizeHeight)
        
        imgClone.save(filename=inResizedImageFN)



batchInputImageDir = os.path.join("..","images","in")       # Input directory where jpg files reside
batchOutputImageDir = os.path.join("..","images","out")     # Output directory where results are saves as jpg image files
resizePercentages = [75, 50, 25]    # Percentages to by which to resize input images

# Iterate through all jpgs in the input directory 
for jpgFile in os.listdir(batchInputImageDir):
    
    if jpgFile.endswith(".jpg"):    # Process jpg files only
    
        # Determine full path and filename
        imageName, imageExt = os.path.splitext(jpgFile)
        batchInImageFN = os.path.join(batchInputImageDir, jpgFile)

        print("Currently processing image: " + batchInImageFN)

        # Open the input image to process
        with Image(filename=batchInImageFN) as img:
            
            # Resize image by given percentages
            for resizePercentage in resizePercentages:
                
                batchOutImageFN = os.path.join(batchOutputImageDir, imageName + "_" + str(resizePercentage) + ".jpg")
                ResizeImageByPercentAndSave(img, resizePercentage, batchOutImageFN)
                
            # Apply the sepia tone effect
            batchOutImageFN = os.path.join(batchOutputImageDir, imageName + "_sepia.jpg")
            SepiaToneEffectAndSave(img, batchOutImageFN)
            
print("Finished processing all jpg images in input directory: " + batchInputImageDir)
print("Output images files located in the directory: " + batchOutputImageDir)