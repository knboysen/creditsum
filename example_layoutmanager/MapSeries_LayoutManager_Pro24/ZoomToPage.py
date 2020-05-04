import arcpy, json, os, sys, time

#Set up relative paths
relPath = os.path.dirname(sys.argv[0])

#Get input page value from GP dialog
pageName = str(arcpy.GetParameterAsText(0))

#Function that arranges data frames based on the field info within the PageLayoutElements table
def arrangeMFs(row, lyt, mfName):
  rowInfo = json.loads(row.getValue(mfName))
  mf = lyt.listElements('MAPFRAME_ELEMENT', mfName)[0]
  mf.elementPositionX = rowInfo[0]
  mf.elementPositionY = rowInfo[1]
  mf.elementWidth = rowInfo[2]
  mf.elementHeight = rowInfo[3]
  newExtent = mf.camera.getExtent()
  newExtent.XMin = rowInfo[4]
  newExtent.YMin = rowInfo[5]
  newExtent.XMax = rowInfo[6]
  newExtent.YMax = rowInfo[7]
  mf.camera.setExtent(newExtent)
  mf.scale = rowInfo[8]

############################ MAIN SCRIPT STARTS HERE ##############################

arcpy.AddMessage("Processing map: " + str(pageName))

#Reference Project and Layout
p = arcpy.mp.ArcGISProject("current")  #CURRENT
lyt = p.listLayouts('MultipleInsets')[0]

#Use MapSeries object when not resetting the page back to the default template
if pageName != "Default Template":
  ms = lyt.mapSeries
  pageNum = ms.getPageNumberFromName(pageName)
  ms.currentPageNumber = pageNum
else:
  pageName = "Default Template"

#Reference pageLayoutTable
mainMap = p.listMaps('MainMap')[0]
pageLayoutTable = mainMap.listTables('PageLayoutElements')[0]

#Build list of map frames for current region
pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "Name = '" + pageName + "'")
pageLayoutRow = pageLayoutCursor.next()
mfList = []
for mf in lyt.listElements('MAPFRAME_ELEMENT'):
  if not pageLayoutRow.isNull(mf.name):
    mfList.append(mf.name)

#Reference Layout CIM (new at Pro 2.4) to control visibility of extent indicators
#Get/set CIM needs to happen BEFORE arrangeMFs, otherwise setCIM resets the MS extent
lyt_cim = lyt.getDefinition('V2')
for elm in lyt_cim.elements:
  if elm.name == "MainMF":
    #Turn off all indicators
    for ei in elm.extentIndicators:
      ei.isVisible = False
    #Turn on only needed indicators
    for ei in elm.extentIndicators:
      for mfName in mfList:
        if ei.name == 'Extent of ' + mfName + ' Map Frame':
          ei.isVisible = True
lyt.setDefinition(lyt_cim)

#Move all map frames off the layout and into their default positions
pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "Name = 'Default Template'")
pageLayoutRow = pageLayoutCursor.next()
for mf in lyt.listElements('MAPFRAME_ELEMENT'):
  arrangeMFs(pageLayoutRow, lyt, mf.name)

#Move appropriate map frames onto the layout and build list of MF names
pageLayoutCursor = arcpy.SearchCursor(pageLayoutTable.dataSource, "Name = '" + pageName + "'")
pageLayoutRow = pageLayoutCursor.next()
mfList = []
for mf in lyt.listElements('MAPFRAME_ELEMENT'):
  if not pageLayoutRow.isNull(mf.name):
    arrangeMFs(pageLayoutRow, lyt, mf.name)
    mfList.append(mf.name)

#Arrange other layout elements
title = lyt.listElements("TEXT_ELEMENT", "Title")[0]
title.text = "Capitol Cities for Region: \n " + pageName
title.elementPositionX = json.loads(pageLayoutRow.getValue("Title_NorthArrow"))[0]
title.elementPositionY = json.loads(pageLayoutRow.getValue("Title_NorthArrow"))[1]
nArrow = lyt.listElements("MAPSURROUND_ELEMENT", "NorthArrow")[0]
nArrow.elementPositionX = json.loads(pageLayoutRow.getValue("Title_NorthArrow"))[2]
nArrow.elementPositionY = json.loads(pageLayoutRow.getValue("Title_NorthArrow"))[3]
