import arcpy, os, sys
relPath = os.path.dirname(sys.argv[0])

def setMF(mf):
  ext = mf.camera.getExtent()
  fieldValue = "[" + str(round(mf.elementPositionX, 2)) + "," + str(round(mf.elementPositionY, 2)) + \
               "," + str(round(mf.elementWidth, 2)) + "," + str(round(mf.elementHeight, 2)) + \
               "," + str(int(round(ext.XMin, -2))) + "," + str(int(round(ext.YMin, -2))) + \
               "," + str(int(round(ext.XMax, -2))) + "," + str(int(round(ext.YMax, -2))) + \
               "," + str(int(round(mf.camera.scale, -2))) + "]"
  arcpy.AddMessage(mf.name + ": " + fieldValue)
  return fieldValue

############################ MAIN SCRIPT STARTS HERE ##############################

#REFERENCE PROJECT, DMS OBJECT, AND LAYOUT ELEMENTS
p = arcpy.mp.ArcGISProject("current")  #CURRENT
lyt = p.listLayouts('MultipleInsets')[0]
ms = lyt.mapSeries

#pageName = ms.pageRow.getValue(ms.pageNameField.name) #doesn't work in PRO
pageName = ms.pageRow.SUB_REGION          #temp fix for above
title = lyt.listElements("TEXT_ELEMENT", "Title")[0]
northArrow = lyt.listElements("MAPSURROUND_ELEMENT", "NorthArrow")[0]

#REFERENCE PAGELAYOUT TABLE
mainMap = p.listMaps('MainMap')[0]
pageLayoutTable = mainMap.listTables('PageLayoutElements')[0]

#UPDATE INFORMATION FROM PAGELAYOUT TABLE
pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "\"Name\" = '" + pageName + "'")
pageLayoutRow = pageLayoutCursor.next()

if pageLayoutRow == None:               #INSERT A NEW ROW - INSERT CURSOR
  arcpy.AddMessage("Adding New Row: " + pageName)
  pageInsertCursor = arcpy.InsertCursor(pageLayoutTable.dataSource)
  pageInsertRow = pageInsertCursor.newRow()
  pageInsertRow.Name = pageName
  

  #Set Data Frame information
  for mf in lyt.listElements("MAPFRAME_ELEMENT"):
    if mf.elementPositionX > 0 and mf.elementPositionX < 11:  #don't set values if MF is off the page
      pageInsertRow.setValue(mf.name, setMF(mf))

  #Set Locator and North Arrow
  pageInsertRow.Title_NorthArrow = "[" + str(round(title.elementPositionX,2)) + "," + str(round(title.elementPositionY,2)) + "," + \
                                   str(round(northArrow.elementPositionX,2)) + "," + str(round(northArrow.elementPositionY,2)) + "]"              
  
  pageInsertCursor.insertRow(pageInsertRow)
  del pageInsertCursor, pageInsertRow

else:                                   #UPDATE EXISTING ROW - UPDATE CURSOR
  arcpy.AddMessage("Updating Existing Row: " + pageName)
  pageUpdateCursor = arcpy.UpdateCursor(pageLayoutTable.dataSource, "\"Name\" = '" + pageName + "'")
  pageUpdateRow = pageUpdateCursor.next()

  #Set Data Frame information
  for mf in lyt.listElements("MAPFRAME_ELEMENT"):
    if mf.elementPositionX > 0 and mf.elementPositionX < 11:  #don't set values if DF is off the page
      pageUpdateRow.setValue(mf.name, setMF(mf))

  #Set Locator and North Arrow
  pageUpdateRow.Title_NorthArrow = "[" + str(round(title.elementPositionX,2)) + "," + str(round(title.elementPositionY,2)) + "," + \
                                   str(round(northArrow.elementPositionX,2)) + "," + str(round(northArrow.elementPositionY,2)) + "]"             
  
  pageUpdateCursor.updateRow(pageUpdateRow)
  del pageUpdateCursor, pageUpdateRow
  
del pageLayoutCursor, pageLayoutRow
