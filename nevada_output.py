"""
Name:     toolpractice_v2.py
Author:   Kristen Boysen
Created:  14 Feb 2020
Revised:  
Version:  Created using Python 3 , ArcPro 2.5

"""

###Import packages
import arcpy
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from numpy.random import rand
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec
import sqlite3


####
### READ IN DATA
##this data should be read in from the calculator/databasefile uploaded into the GIS tool
current_data = pd.read_csv('../database/nvccs-database/data/processed/current_credits.csv') 
proj_data = pd.read_csv('../database/nvccs-database/data/processed/projected_credits.csv')
fakedata= pd.read_csv('./data/scenario_mock.csv')
projcredits = fakedata[['map_unit_id', 'credits']]
projcredits.rename(columns = {'credits': 'proj_credits'}, inplace= True) 

###

###autolabels
def autolabel(rects):
    '''
    creates & places labels for horizontal bar charts
    '''
    (x_bottom, x_top) = ax.get_xlim()
    x_height = x_top - x_bottom
    for rect in rects:
        width = round(rect.get_width())
        label_position = width + (x_height * 0.03)
        ax.annotate('{}'.format(width),
                    xy=(label_position, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, -3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

###### FIGURE 1
# bar chart of MU current conditions


##Data Wrangling

#merge projected credits & current credits 
plotmu = current_data.merge(proj_data[['map_unit_id', 'credits']].rename(columns = {'credits': 'proj_credits'}), on = 'map_unit_id')

#ID Max Credits (whether current or projected)
plotmu['maxcredits'] = plotmu[['credits', 'proj_credits']].max(axis =1) ###identify maximum credits 


### sort by maxcredits
plotmu = plotmu.sort_values(by=['maxcredits'], ascending = True, na_position = 'first')
plotmu['map_unit_id'] = plotmu['map_unit_id'].astype(str)
## drop 0s
plotmu = plotmu[plotmu['maxcredits'] != 0]
##drop Na in max credits
plotmu.dropna(subset=['maxcredits'], inplace=True)

##define caption
t= ("This graph shows the current and projected uplift on each Map Unit \n as entered in the Credit Calculator. The labels indicate the max number \nof credits,"
    " regardlesss of it they are current on predicted. \n As shown, Map Unit 19 has the greatest"
    " total number of credits, with \n 817 current credits") 
##TODO: Figure out how to make this dynamic text

##plot
fig, ax = plt.subplots(figsize = (7,9))
fig.set_size_inches(7, 9, forward=True)

p0= ax.barh(plotmu['map_unit_id'], width = plotmu['maxcredits'])
p1 = ax.barh(plotmu['map_unit_id'], width = plotmu['proj_credits'])
p2 = ax.barh(plotmu.map_unit_id, width = plotmu.credits)
ax.text(-1,-8, t, family = 'serif', ha = 'left', wrap = True)
#txt._get_wrap_line_width = lambda : 600.
ax.set_ylabel('Map Unit #')
ax.set_xlabel('Credits')
ax.set_title('Credits Per Map Unit')
ax.legend((p1[0], p2[0]), ('Predicted', 'Current'))

autolabel(p0)
fig.tight_layout()
plt.figure()

fig.savefig(r"./outputs/full_summary_chart.pdf", bbox_inches='tight')


###Projected conditions
####functional acres vary by season: so stick with credits
### how to normalize by acre? 
    ## bring to the set. 

##2. Summary graph showing best mngmt action

##Use Fake Data
functionality = fakedata.drop(['map_unit_area'], axis =1)

###find max credits generated for each MU and associated management regime
functionality['max'] = functionality.iloc[:,2:].max(axis = 1)
functionality['idmax'] = functionality.iloc[:,2:].idxmax(axis = 1)


##reshape data 
# TODO: this is super clunky; needs streamlining

functionality.set_index(['map_unit_id', 'credits'])
plotmu1 = functionality.sort_values(by=['max'], ascending = True, na_position = 'first')
plotmu1 = plotmu1[plotmu1['max'] != 0] ##drop where no credits are created


##reshape for plotting
plotmu2 = pd.melt(plotmu1, id_vars=["map_unit_id", "credits", "max", "idmax"], var_name = "Mngmt_Scenario", value_name = "optimal_credits")

plotmu2 = plotmu2.sort_values(by=['max'], ascending = False, na_position = 'first', ignore_index= True)
plotmu2['map_unit_id'] = plotmu2['map_unit_id'].astype(str)

#list of Management Options Included
management_options = plotmu2.idmax.unique() 

##define colors for bars
colorlist = ('b', 'r', 'g', 'c', 'm','y', 'purple', 'salmon', 'yellowgreen', 'silver', 'darkgreen', 'khaki', 'darkorange', 'lightsteelblue', 'brown' ) ## this is not the right way to do this

color_dict = dict(zip(management_options, colorlist[:len(management_options)])) #create a dictionary that is the list of the total best management options
plotmu2['color'] = plotmu2['idmax'].map(color_dict)
plotmu2 = plotmu2.sort_values(by=['max'], ascending = True, na_position = 'first')

##set caption
#TODO change to dynamic text
t= ("This graph shows the projected credits for each Map Unit based on the \n ideal management regime. \n These 'idealized' credits are compared to the maximum credits in the calcualator \n (either predicted or current). As shown, Map Unit 19 has the greatest total number \n of credits, with  902 current credits, if Restoration Management Scenarion 5 \n(High Effort Level) is used") 


###########
##Figure 2. Scenarios Compared to Calculator
#####

##graph it
fig, ax = plt.subplots(figsize = (7,9))

p= ax.barh(plotmu2['map_unit_id'], width = plotmu2['max'], color = plotmu2['color'])
autolabel(p)
##Erik- the only way I could figure out how to put a label on this graph was to create this invisible graph below. unfortunately it iterates over each of the colors and takes a while. please help. 

for i, j in color_dict.items(): #Loop over color dictionary
    ax.barh(plotmu2['map_unit_id'], width = 0 ,color=j,label=i) #Plot invisible bar graph but have the legends specified


p1 = ax.barh(plotmu['map_unit_id'], width = plotmu['maxcredits'], color = 'gray', label = "Max Credits \n from Calc")

ax.text(-1,-9, t, family = 'serif', ha = 'left', wrap = True)

ax.set_ylabel('Map Unit #')
ax.set_xlabel('Credits')
ax.set_title('Credits Per Map Unit Based on Ideal Management Regime')
ax.legend()
fig.tight_layout()
plt.figure()

fig.savefig(r"./outputs/managementregime_summary_chart.pdf", bbox_inches='tight')
#####

####
#Deep Dive into Management Options##
# 1/2 page per scenario
## for each management scenario


regimes = ['rest1', 'rest2', 'rest3', 'rest4', 'rest5'] ## Fake Data; this needs to be changed to match scenario tool

## Add in Projected Credits to Fake Data
plotmu1 = plotmu1.merge(projcredits, on = 'map_unit_id')


for i in regimes: 

    ####comparison charts wrangling
    current_regime = []
    current_scenario = []
    t = "Management Regime #{}".format(i[-1])
    current_regime.append('{}_l'.format(i))
    current_regime.append('{}_m'.format(i))
    current_regime.append('{}_h'.format(i))
    current_scenario = plotmu1[['map_unit_id', 'credits', 'max', 'idmax', current_regime[0], current_regime[1], current_regime[2]]]
    current_scenario = current_scenario.merge(projcredits, on = 'map_unit_id')
  
    totals = plotmu1[['credits', 'proj_credits', current_regime[0], current_regime[1], current_regime[2]]].sum(axis = 0)

    ##set caption
    graph1cap= "The  graph above compares current, predicted, and modelled credit creation opportunities across \n the project site. The left-most bars represent different levels of effort of this management regime \n \n The table below captures the Map Units that will be most improved by this  management regime, and \n shows the number of credits predicted under each effort level. \n \n The barchart below shows the same information, but in credits per acre in order to normalize the effect of \n total number of acres."
### Table information

#Table Top 5-10 MUs that show the greatest increase - functional acre uplift per acre
    acres = fakedata[['map_unit_id', 'map_unit_area']]
    current_scenario=current_scenario.merge(acres, on = 'map_unit_id')

    #current_scenario['low_increase_per_acre'] = (current_scenario['{}_l'.format(i)] - current_scenario['proj_credits']) / current_scenario['map_unit_area'] * 100

    #current_scenario['m_increase_per_acre'] = (current_scenario['{}_m'.format(i)] - current_scenario['proj_credits']) / current_scenario['map_unit_area'] * 100

#    current_scenario['h_increase_per_acre'] = (current_scenario['{}_h'.format(i)] - current_scenario['proj_credits']) / current_scenario['map_unit_area'] * 100

    current_scenario['low_increase_per_acre'] = (current_scenario['{}_l'.format(i)] / current_scenario['map_unit_area'])

    current_scenario['m_increase_per_acre'] = (current_scenario['{}_m'.format(i)] / current_scenario['map_unit_area'])

    current_scenario['h_increase_per_acre'] = (current_scenario['{}_h'.format(i)] / current_scenario['map_unit_area'])

###straight numbers for table
    subtable = current_scenario[['map_unit_id', 'credits','proj_credits', '{}_l'.format(i),'{}_m'.format(i), '{}_h'.format(i)]]

    col_name_dict1 = {'map_unit_id':'MU', 'credits': 'Current Credits', 'proj_credits': 'Projected Creds', 'low_increase_per_acre': 'Percent Increase/Acre: LOW', 'm_increase_per_acre': 'Percent Increase/Acre: MEDIUM', 'h_increase_per_acre':'Percent Increase/Acre: HIGH', '{}_l'.format(i): 'Low Effort', '{}_m'.format(i): 'Medium Effort', '{}_h'.format(i): 'High Effort'}

    subtable = subtable.rename(columns = col_name_dict1).round(decimals =2)
    subtable = subtable[subtable["High Effort"] > subtable['Projected Creds']].sort_values(by = "High Effort", ascending = False)

    if len(subtable) >10: 
        subtable= subtable[0:10]

######
    table = current_scenario[['map_unit_id', 'credits', 'low_increase_per_acre', 'm_increase_per_acre', 'h_increase_per_acre']].sort_values(by = "h_increase_per_acre", ascending = False)

    col_name_dict = {'map_unit_id':'MU', 'credits': 'Current Credits', 'low_increase_per_acre': 'Percent Increase/Acre: LOW', 'm_increase_per_acre': 'Percent Increase/Acre: MEDIUM', 'h_increase_per_acre':'Percent Increase/Acre: HIGH'}
    
    table = table.rename(columns = col_name_dict)

    table1= table[['MU','Current Credits', 'Percent Increase/Acre: LOW', 'Percent Increase/Acre: MEDIUM', 'Percent Increase/Acre: HIGH']].round(decimals=2)
    table1 = table1[table1["Percent Increase/Acre: HIGH"] > 0]
###Try bar chart
##transpose for bar chart

    table2 = table.copy()
    #table2.set_index("MU", inplace= True)
    table2 = table2[table2["Percent Increase/Acre: HIGH"] > table2['Percent Increase/Acre: HIGH'].median()]
    
    width = 0.5      # the width of the bars: can also be len(x) sequence
    colors = plt.cm.YlGnBu(np.linspace(0, 0.5, 3))

##GRAPH
    fig = plt.figure(figsize = (8,11))    
    ax1 = plt.subplot2grid((5,2), (0, 0), colspan=2, rowspan =2)

    ax1.bar(['Current Credits', 'Projected Creds', 'Low Effort', "Medium Effort", 'High Effort'], totals)
    ax1.set_title(t, fontsize = 18)
    ax1.set_xlabel('Management Regime \n ')
    ax1.set_ylabel('Total Number of Credits')

    #fig.tight_layout()
    #plt.figure()
    ##NARATIVE
    ax2 = plt.subplot2grid((5,2), (2, 0), colspan=2)
    ax2.axis('off')
    ax2.axis('tight')
    text= fig.text(.05,.5, graph1cap, family = 'serif', ha = 'left', wrap = True)

#### TABLE
   
    # hide axes
    #fig.patch.set_visible(False)
    ax3 = plt.subplot2grid((5,2), (3, 0), rowspan=2)
    ax3.axis('off')
    ax3.axis('tight')

    the_table = ax3.table(cellText=subtable.values, colLabels=subtable.columns, loc='center', colColours= ['0.5', '0.4', '0.3', colors[2], colors[1], colors[0]])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    the_table.scale(1.8, 1.3)
    ax3.set_title('Map Unit and Percent Increase\nBased on Effort Level')

#### comparison bar
    ax4 = plt.subplot2grid((5,2), (3, 1), rowspan =2)
    ax4.bar(table2['MU'].astype(str), table2['Percent Increase/Acre: HIGH'], width, label='High', color = colors[0])
    
    ax4.bar(table2['MU'].astype(str), table2['Percent Increase/Acre: MEDIUM'], width, label='Medium', color = colors[1])

    ax4.bar(table2['MU'].astype(str), table2['Percent Increase/Acre: LOW'], width, label='Low', color = colors[2])
    
    ax4.set_ylabel('Credits/Acre')
    ax4.set_xlabel('Map Units')
    ax4.set_title('Credits/Acre Created for Each Effort Level')
    ax4.legend()


    fig.tight_layout(pad = 2)
    plt.show()
    ##save page
    fig.savefig("./outputs/{}_summarypage1.pdf".format(i), bbox_inches='tight', papertype = 'letter')
###END Page
    

##########################

###GIS FUN

##
##############Define extent

##tasks
##cover page
    ##inputs: layout, shape file, project title

    ##outputs: single page, full map, title change, dynamic text



##grid index
    ##inputs: layout, shapefile, project title
    ##output: grid on map, labeled


###map series
    # input: grid, shapefile, layout
    #output: multiple map pages

    
#mu_shapefile = arcpy.GetParameterAsText(0)
shape1 = r'E:\kboysen_gis\toolpractice02142020\Crawford_Map_Units_Dissolve\Crawford_Map_Units_Dissolve.shp'
extent = arcpy.Describe(shape1).extent
print(extent)

##### Print exisiting layout
aprx = arcpy.mp.ArcGISProject("CURRENT")
for lyt in aprx.listLayouts(): ##this is going to be hard to convert to desktop
  lyt.exportToPDF(r'E:\kboysen_gis\toolpractice02142020\test.pdf')

#create grid
arcpy.GridIndexFeatures_cartography('E:\kboysen_gis\toolpractice02142020\toolpratice_NVOutput\toolpratice_NVOutput.gdb\gridgridgrid', shape1, number_rows = 4, number_columns = 4)


###

##print using 