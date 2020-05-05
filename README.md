#README

This package creates a summary output that can be used to communicate crediting and uplift options to landowners and credit developers. 

## Contents
**data** hypothetical and real data for the graphics
**outputs** PDF & other outputs


**credit_summary_tool_arcpro.py

### Inputs
** calculator
** map units from HQT
** map template with layouts, files

### Flow
Tool user inputs
1. Map Units from HQT
2. Project Name
3. Preferred Symbology 

1. Title Page
	*Read in Map Units from HQT
	*Read in Project Name 
	*Use Report Title Layout
		* Update main Map Frame to extent of MUs
		* Update title
		* Update dynamic text w current conditions, size, etc. 
	*Export to PDF
2. Index Page
	* Create grid based on MU
	* Optional: allow for user to input # of grids? 
	* Change 
		* Title
		* Delete Dynamic Text 
		* Add labels to grid
		* Use symbology from grid template
	* Export to PDF
3. Map Series 
	* Rely on map series layout template in arcpro 
	* Subsitute old index with new grid
	* Make grid invisible
	* Symbolize MU based on user input
	* Export all pages to PDF
4. Matplot Lib Graphs
	*Summary Stats- Current & Projected Credits from Credit Calculator by Map Unit
	*Management Regime Comparison: Which Management is best for which MUs? 
	*Management REgime Deep Dive
		*effort comparison
		*best MUs for that Management Regime
	*export all as pdfs
5. Use PDFOpen and PDFMerge to combine and export PDFs
	https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/pdfdocumentopen.htm



### Outputs
**PDF with
1. report title
2. summary stats
3. specific management regime summaries
4. map series
5. summary table

## Tips


### TODO
[ ] Expand ReadMe (KB) 
[ ] Finalize ArcPro Section / Map Series (KB) 
[ ] Clean up code (KB) 
[ ] Add in Scenario Outputs (EA) 
[ ] Review Matplotlib section and add comments (EA) 
[ ] Convert to arcDesktop 
[ ] Reimagine graphics, especially summary of management regimes (KB) 
[ ] Organize file inputs (KB) 
