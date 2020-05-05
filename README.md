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

1. Title Page
	*Read in Map Units from HQT
	*Read in Project Name 
	*Use Report Title Layout
		* Update main Map Frame to extent of MUs
		* Update title
		* Update dynamic text w current conditions, size, etc. 
	*Export to PDF
2. Index Page
	*



### Outputs
**PDF with
1. report title
2. summary stats
3. specific management regime summaries
4. map series
5. summary table

## Tips


### TODO
*see code