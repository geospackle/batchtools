"""For ArcGIS Pro. Creates a list of figures to export and moves figures with existing figure number to old folder.
This script is designed for a layout with text "Figure [No]" and figure name as only element in 14.0 font."""

import os
import shutil
import arcpy
import re

arcpy.env.overwriteOutput = True
aprx = arcpy.mp.ArcGISProject("CURRENT")
layouts = aprx.listLayouts()

layouts_dict = {}
for lyt in layouts:
    layouts_dict[lyt.name] = lyt

exportFolder = arcpy.GetParameterAsText(0)
layouts_select = arcpy.GetParameterAsText(1).split(";")

if not os.path.exists(exportFolder + '\\zBatchOLD'):
    os.makedirs(exportFolder + '\\zBatchOLD')

for i in layouts_select:
    lyt = layouts_dict[i.strip("'")]
    txt_elms = lyt.listElements("TEXT_ELEMENT")
    figNumber = ""
    figName = i  # if no text size 14.0 in layout
    for elm in txt_elms:
        if "Figure" in elm.text:
            try:
                figNumber = re.search(r'Figure\s(.+)', elm.text).group(1)
            except Exception:
                figNumber = ""
        if elm.textSize == 14.0:
            figName = elm.text
            figName = figName.replace("\r", " ").replace("\n", " ")
    if "<dyn" in figName:       # in case dynamic field (map series)
        figName = i.strip("'")
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
                    except PermissionError:
                        continue

    exportPath = exportFolder + '\\' + 'Fig' + figNumber + ' - ' + figName + '.pdf'
    if os.path.exists(exportPath):
        try:
            os.remove(exportPath)
        except PermissionError:
            arcpy.AddError('Fig' + figNumber + ' - ' + figName + '.pdf in use! Saved as Fig' + figNumber + ' - ' + figName + '_1.pdf')
            exportPath_alt = exportFolder + '\\' + 'Fig' + figNumber + ' - ' + figName + '_1.pdf'
            lyt.exportToPDF(exportPath_alt, resolution=300)  # overwrites
    lyt.exportToPDF(exportPath, resolution=300)  # overwrites
del aprx
