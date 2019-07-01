
# create list of figures to export and move figures with same figure number to OLD

import os
import shutil
import arcpy
import re

arcpy.env.overwriteOutput = True

sourceFolder = arcpy.GetParameterAsText(0)
exportFolder = arcpy.GetParameterAsText(1)

if not os.path.exists(exportFolder + '\\zBatchOLD'):
    os.makedirs(exportFolder + '\\zBatchOLD')

for filename in os.listdir(sourceFolder):
    fullpath = os.path.join(sourceFolder, filename)
    if os.path.isfile(fullpath):
        basename, extension = os.path.splitext(fullpath)
        if extension.lower() == ".mxd":
            mxd = arcpy.mapping.MapDocument(fullpath)
            figName = filename[:-4]  # in case does not find 14.0 text size
            figNumber = ""
            for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
                if "Figure" in elm.text:
                    try:
                        figNumber = re.search(r'Figure\s(.+)', elm.text).group(1)
                    except AttributeError:
                        figNumber = ""
                if elm.fontSize == 14.0:	#looks for font size to get figure name
                    figName = elm.text
                    figName = figName.replace("\r", " ").replace("\n", "")      # new line in text field results in \r\n

            if "<dyn" in figName:
                figName = filename[:-4]
            if "<dyn" in figNumber:
                figNumber = ""

            for f in os.listdir(exportFolder):
                if f.startswith('Fig' + figNumber + ' '):
                    fullpath = os.path.join(exportFolder, f)
                    if os.path.isfile(fullpath):
                        basename, extension = os.path.splitext(fullpath)
                        if extension.lower() == ".pdf":
                            shutil.copy2(fullpath, exportFolder + '\\zBatchOLD')
                            try:
                                os.remove(fullpath)
                            except Exception:
                                pass

            exportPath = exportFolder + '\\' + 'Fig' + figNumber + ' - ' + figName + '.pdf'
            if os.path.exists(exportPath):
                os.remove(exportPath)
            arcpy.mapping.ExportToPDF(mxd, exportPath)
            del mxd
