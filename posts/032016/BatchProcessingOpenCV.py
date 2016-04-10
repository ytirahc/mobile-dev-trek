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
# using OpenCV and NumPy (developed with & tested against Python 3.5, OpenCV 3.1 and
# NumPy 1.10.4)
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
import numpy as np
import cv2



# *****
# SoftLight
#
# Description: Implements the soft light blending mode as per w3c
# https://en.wikipedia.org/wiki/Blend_modes#Soft_Light
#
# Parameters:
#    inTopImg : Open OpenCV image (top)
#    inBottomImg : Open OpenCV image (bottom)
# *****
def SoftLight(inTopImg,inBottomImg):
    
    # Normalize color values to between 0 and 1
    topImgArray = np.asarray(inTopImg) / 255.0
    bottomImgArray = np.asarray(inBottomImg) / 255.0
    
    softLightImgArray = SoftLightF(topImgArray, bottomImgArray)
    
    # Convert colors back to between 0 to 255
    softLightImgArray = softLightImgArray * 255.0
        
    return softLightImgArray


# *****
# SoftLightF
#
# Description: Implements f(bottom image, top image) portion of w3c soft light blending equation
#
# Parameters:
#    inTopImgArray : Top image as array
#    inBottomImgArray : Bottom image as array
# *****
def SoftLightF(inTopImgArray,inBottomImgArray):

    softLightFArray = np.where(inTopImgArray <= 0.5,inBottomImgArray - ((1 - (2 * inTopImgArray)) * inBottomImgArray * (1 - inBottomImgArray)),inBottomImgArray + (2 * inTopImgArray - 1) * (SoftLightG(inBottomImgArray) - inBottomImgArray))

    return softLightFArray


# *****
# SoftLightG
#
# Description: Implements f(bottom image) portion of w3c soft light blending equation
#
# Parameters:
#    inBottomImgArray : Bottom image as array
# *****
def SoftLightG(inBottomImgArray):
    
    softLightGArray = np.where(inBottomImgArray <= 0.25, ((16 * inBottomImgArray - 12) * inBottomImgArray + 4) * inBottomImgArray, np.sqrt(inBottomImgArray))
    
    return softLightGArray


# *****
# SepiaToneEffectAndSave
#
# Description: Applies sepia tone effect to input image and saves the result
#
# Parameters:
#    inImage : An OpenCV image
#    inSepiaImageFN : Output path and file name where the result is saved
# *****
def SepiaToneEffectAndSave(inImage, inSepiaImageFN):
    
    # Desaturate (but needs to be RGB for later operations)
    imgGrey = cv2.cvtColor(inImage,cv2.COLOR_BGR2GRAY)
    imgGrey = cv2.cvtColor(imgGrey,cv2.COLOR_GRAY2RGB)  # Need RGB for matrix math
    
    # Apply a slight blur
    imgSmooth = cv2.GaussianBlur(imgGrey,(5,5),0)

    # Blend the sepia tone color with the greyscale layer using soft light
    imgWidth, imgHeight, imgChannels = imgGrey.shape
    imgSepiaColor = np.zeros((imgWidth,imgHeight,3), np.uint8)
    imgSepiaColor[:,:] = (42,89,226)  # BGR
    
    imgSepia = SoftLight(imgSepiaColor, imgSmooth)
    
    cv2.imwrite(inSepiaImageFN,imgSepia)


# *****
# ResizeImageByPercentAndSave
#
# Description: Resizes image by specified percentage and saves the result
#
# Parameters:
#    inImage : An OpenCV image
#    inResizePercentage : Percentage by which to resize image as a non negative integer
#    inResizedImageFN : Output path and file name where the result is saved
# *****
def ResizeImageByPercentAndSave(inImage, inResizePercentage, inResizedImageFN):
    
    resizeFraction = inResizePercentage / 100
        
    imgResize = cv2.resize(inImage, (0,0), fx=resizeFraction, fy=resizeFraction)
    
    cv2.imwrite(inResizedImageFN,imgResize)



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
        img = cv2.imread(batchInImageFN)
            
        # Resize image by given percentages
        for resizePercentage in resizePercentages:
                
            batchOutImageFN = os.path.join(batchOutputImageDir, imageName + "_" + str(resizePercentage) + ".jpg")
            ResizeImageByPercentAndSave(img, resizePercentage, batchOutImageFN)
                
        # Apply the sepia tone effect
        batchOutImageFN = os.path.join(batchOutputImageDir, imageName + "_sepia.jpg")
        SepiaToneEffectAndSave(img, batchOutImageFN)
            
print("Finished processing all jpg images in input directory: " + batchInputImageDir)
print("Output images files located in the directory: " + batchOutputImageDir)
