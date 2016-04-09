// Copyright (c) 2016, ytirahc, www.mobiledevtrek.com
// All rights reserved. Copyright holder cannot be held liable for any damages. 
// 
// Distributed under the Apache License (ASL). 
// http://www.apache.org/licenses/
// *****
// Description: This file is a script for Adobe Photoshop (tested with Photoshop CC 2015). 
// The current active image in Photoshop will be resized by the specified percentages
// in the array scaleFactor and will save those files to the specified directory, saveDir.  
//
// Usage: File -> Scripts -> Browse... to locate the script and execute it
// *****

var scaleFactor = [75, 50, 25];  // Scale factor as percentage of original image
var saveDir = "~/Documents/work/"; // Directory in which to save resized images

// Create resized image for all specified scale factors
for (var scaleFactorIndex in scaleFactor) 
{
	ResizeToScaleFactor(saveDir, scaleFactor[scaleFactorIndex])
}

// *****
// ResizeToScaleFactor
//
// Description: Resizes an image according to specified scale factor and saves it
//
// Parameters:
// 		inSaveDir: Directory in which to save resized image
//		inScaleFactor: Scale factor as a percentage in which to resize image
// *****
function ResizeToScaleFactor(inSaveDir, inScaleFactor) 
{

	var doc;  // Reference to the active document
	var duplicateDoc;  // Reference to a copy of the active document
	var imageName; // The name of the current document, without extension
	var saveFN; // The full file path and name of the image to be saved
	var saveFNOptions; // The save options

	// Reference to current, active document
	doc = app.activeDocument;
	
	// Duplicate document
	duplicateDoc = doc.duplicate();

	// Resize image according to specified scale factor
	duplicateDoc.resizeImage(UnitValue(inScaleFactor,"%"),null,null,ResampleMethod.BICUBIC);

	// Save the resized image as a jpg
	imageName = (doc.name).split(".")[0];
	saveFN = new File(inSaveDir + imageName + "_" + inScaleFactor + "percent.jpg" );
	saveFNOptions = new JPEGSaveOptions();
	saveFNOptions.embedColorProfile = true;
	saveFNOptions.formatOptions = FormatOptions.STANDARDBASELINE;
	saveFNOptions.matte = MatteType.NONE;
	saveFNOptions.quality = 9;
	duplicateDoc.saveAs(saveFN, saveFNOptions, true, Extension.LOWERCASE);

	// Close the duplicate image view without a save as dialog box
	duplicateDoc.close(SaveOptions.DONOTSAVECHANGES)

}





