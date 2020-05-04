"""
Name:     toolpractice_v2.py
Author:   Kristen Boysen
Created:  14 Feb 2020
Revised:  
Version:  Created using Python 3 , ArcPro 2.5

"""


###import packages
import arcpy
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as path_effects
import sqlite3

###import table calculator

conn = sqlite3.connect('./data/test.db') ##connect to database

with conn:
    #create cursor to navigate
    c= conn.cursor()
    #read in content
    site_scale_score = pd.read_sql('SELECT * FROM site_scale_scores', conn)


site_scale_score

site_scale_score.to_csv(r'./data/database_crawford.csv')

### Read in 

b_boxplot = site_scale_score.boxplot(column=['b_sage_cover', 'b_shrub_cover',
       'b_forb_cover', 'b_forb_rich'])

fig = plt.figure(figsize=(7, 1))
text = fig.text(0.5, 0.5, 'This text stands out because of\n'
                          'its black border.', color='white',
                          ha='center', va='center', size=30)
text.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'),
                       path_effects.Normal()])
plt.show()

#######

import pandas as pd
from IPython.core.display import HTML

df = pd.DataFrame([['A231', 'Book', 5, 3, 150], 
                   ['M441', 'Magic Staff', 10, 7, 200]],
                   columns = ['Code', 'Name', 'Price', 'Net', 'Sales'])

# your images
images = ['https://vignette.wikia.nocookie.net/2007scape/images/7/7a/Mage%27s_book_detail.png/revision/latest?cb=20180310083825',
          'https://i.pinimg.com/originals/d9/5c/9b/d95c9ba809aa9dd4cb519a225af40f2b.png'] 


df['image'] = images

# convert your links to html tags 
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

pd.set_option('display.max_colwidth', -1)

HTML(df.to_html(escape=False ,formatters=dict(image=path_to_image_html)))


# #### This is the beautiful graph I made earlier

# #Map_unit_id is a unique identifier
# #merge to merge things together

# # Bring in excel table
# #shapefile = arcpy.GetParameterAsText(0)

# #attribute_table = arcpy.da.TableToNumPyArray(shapefile, (‘FIRE_ID’, ‘FIRENAME’))

# training_data= pd.read_excel("E:/kboysen_gis/toolpractice02142020/example_table.xlsx")

# melt= pd.melt(training_data, id_vars= ['map unit'],  var_name ='Type', value_name ='Func_Acres')

# merge = pd.merge(melt, training_data[['map unit', 'acres']], how= "left", on= "map unit")
# merge = merge[merge.Type != 'acres']

# merge[['season','pre_post', 'fun']] = merge.Type.str.split("_", expand=True) 
# merge = merge.drop(['fun'], axis = 1)
# merge['Func_Acres'] = merge['Func_Acres'].astype(float)
# merge= merge.rename(columns={'map unit': 'map_unit'})

# #### now we try to graph

# ##Explore Group By 
# grouped = merge.groupby('map_unit')
# mapunits = []
# pre = []
# post = []
# for site,group in grouped:
#     print(site)
#     print(group)

# #########define colors
# ##use this function

# def pltcolor(lst):
#     cols=[]
#     for l in lst:
#         if l=='summer':
#             cols.append('red')
#         elif l=='transition':
#             cols.append('blue')
#         else:
#             cols.append('green')
#     return cols

# ### Mapping
# #######################################

# fig, ax = plt.subplots(figsize=(7, 5))

# # Set up list to track sites
# mapunits = []
# i = 1.0
# for site, group in grouped: 
#     mapunits.append(site)
#     # Get the values for healthy and disease patients
#     h = group.query('pre_post == "pre"')['Func_Acres'].values
#     h_c = group.query('pre_post == "pre"')['season'].values
#     d = group.query('pre_post == "post"')['Func_Acres'].values 
#     d_c = group.query('pre_post == "pre"')['season'].values
#     # Set up the x-axis values
#     x1 = i - 0.2
#     x2 = i + 0.2

#     #set up colors
#     color_h = pltcolor(h_c)
#     color_d = pltcolor(d_c)

#     # Plot the lines connecting the dots
#     for hi, di in zip(h, d):
#         ax.plot([x1, x2], [hi, di], c='gray')

#     # Plot the points
#     ax.scatter(len(h)*[x1-0.01], h, c = color_h,
#                s=25, label='pre')
#     ax.scatter(len(d)*[x2+0.01], d, c= color_d,
#                s=25, label='post')


#     # Update x-axis
#     i += 1

# ax.set_xticks([1, 2, 3, 4, 5])
# ax.set_xticklabels(['MU 1', '2', '3', '4', 'Full Project'], fontsize='x-large')
# ax.set_ylabel('Functionality')
# ax.set_xlabel('Map Unit')
# ax.set_title('Map Unit Functionality Change From Pre- to Post-Project')

# ##legend
# legend_elements = [Line2D([0], [0], marker='o', color='gray', label='Summer',
#                           markerfacecolor='red', markersize=10),
#                     Line2D([0], [0], marker='o', color='gray', label='Transition',
#                           markerfacecolor='green', markersize=10), 
#                     Line2D([0], [0], marker='o', color='gray', label='Winter',
#                           markerfacecolor='blue', markersize=10)]
# ax.legend(handles=legend_elements, loc='upper right')


# num2= arcpy.GetParameterAsText(1)
# arcpy.AddMessage("This is the number you entered " +str(num2))

# string_try = "this is a number {}".format(num2)

# fig.text(1, 0.8, string_try,
#                 ha='left', va='center', size=10, 
#                 bbox=dict(facecolor='red', alpha=0.5))
# #text.set_path_effects([path_effects.Normal()])
        
# ##save file

# fig.savefig(r"E:\kboysen_gis\toolpractice02142020\foo1.pdf", bbox_inches='tight')



# ##############Define extent

# mu_shapefile = arcpy.GetParameterAsText(2)

# shape1 = r'E:\kboysen_gis\toolpractice02142020\Crawford_Map_Units_Dissolve\Crawford_Map_Units_Dissolve.shp'
# arcpy.env.extent = arcpy.Describe(mu_shapefile).extent
# print(arcpy.env.extent)

# ##### Print exisiting layout
# aprx = arcpy.mp.ArcGISProject("CURRENT")
# for lyt in aprx.listLayouts():
#   lyt.exportToPDF(r'E:\kboysen_gis\toolpractice02142020\test.pdf')


# ################## Play with Attribute Table

# in_table = shape1[0:-3]+"dbf" 
# outLocation = r"E:\kboysen_gis\toolpractice02142020"
# try1= arcpy.TableToTable_conversion(in_table, outLocation, 'crawford1.csv') 

# #read in attribute table as pandas

# mu_att = pd.read_csv('E:\\kboysen_gis\\toolpractice02142020\\crawford1.csv')

# ### create table


# clust_data = mu_att[['OBJECTID', 'Acres', 'Current_Av', 'Current_Br', 'Current_LB', 'Current_Wi']]
# clust_data= clust_data.round(2) ##round
# columns = ('MapUnit', 'Acres', 'Average \n Functionality', 'Breeding \nFunctionality', 'Leking \n Func', 'Winter Func')



# fig, ax = plt.subplots()

# # hide axes
# plt.axis('off')
# plt.grid('off')

# table = ax.table(cellText=clust_data.values, colLabels=columns, loc='center')

# fig.tight_layout()

# plt.title("Summary of Map Units", pad= 8)


# plt.gcf().canvas.draw()
# # get bounding box of table
# points = table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
# # add 10 pixel spacing
# points[0,:] -= 10; points[1,:] += 10
# # get new bounding box in inches
# nbbox = matplotlib.transforms.Bbox.from_extents(points/plt.gcf().dpi)
# # save and clip by new bounding box
# plt.savefig(r'E:\kboysen_gis\toolpractice02142020\test3.pdf', bbox_inches=nbbox, )

# plt.show()


# ###########
# #### just pandas

# mu_att.groupby('OBJECTID')['Current_Wi']


# #### merge PDFS

# pdfDoc1 = arcpy.mp.PDFDocumentOpen(r"E:\kboysen_gis\toolpractice02142020\foo1.pdf")
# pdfDoc2 = arcpy.mp.PDFDocumentOpen(r"C:\Users\KristenBoysen\Downloads\Resource_Conserving_Crops_for_Crop_Rotation.pdf")
# pdfDoc3 = arcpy.GetParameterAsText(0)
# pdfDoc4 = arcpy.mp.PDFDocumentOpen(r'E:\kboysen_gis\toolpractice02142020\test.pdf')
# pdfDoc5 = arcpy.mp.PDFDocumentOpen(r'E:\kboysen_gis\toolpractice02142020\table.pdf')

# pdfDoc1.appendPages(pdfDoc2)
# pdfDoc1.appendPages(pdfDoc3)
# pdfDoc1.appendPages(pdfDoc4)
# pdfDoc1.appendPages(pdfDoc5)



# pdfDoc1.saveAndClose()



####
###########from the web
### https://cduvallet.github.io/posts/2018/03/slopegraphs-in-python

#%matplotlib inline

# # Set up the data
# data = np.concatenate(
#     [[np.random.normal(loc=1, size=15), 15*['site1'], 15*['healthy']],
#      [np.random.normal(loc=3, size=15), 15*['site2'], 15*['healthy']],
#      [np.random.normal(loc=0, size=15), 15*['site3'], 15*['healthy']],
#      [np.random.normal(loc=1, size=15), 15*['site1'], 15*['disease']],
#      [np.random.normal(loc=1, size=15), 15*['site2'], 15*['disease']],
#      [np.random.normal(loc=3, size=15), 15*['site3'], 15*['disease']]],
#     axis=1)
# df = pd.DataFrame(columns=['value', 'site', 'label'], data=data.T)
# df['value'] = df['value'].astype(float)

# # Show every ninth row
# df.iloc[::9]

# fig, ax = plt.subplots(figsize=(4, 3))

# # Set up list to track sites
# sites = []
# i = 1.0
# for site, subdf in df.groupby('site'):
#     sites.append(site)
#     # Get the values for healthy and disease patients
#     h = subdf.query('label == "healthy"')['value'].values
#     d = subdf.query('label == "disease"')['value'].values

#     # Set up the x-axis values
#     x1 = i - 0.2
#     x2 = i + 0.2

#     # Plot the lines connecting the dots
#     for hi, di in zip(h, d):
#         ax.plot([x1, x2], [hi, di], c='gray')

#     # Plot the points
#     ax.scatter(len(h)*[x1-0.01], h, c='k',
#                s=25, label='healthy')
#     ax.scatter(len(d)*[x2+0.01], d, c='k',
#                s=25, label='disease')


#     # Update x-axis
#     i += 1

# # Fix the axes and labels
# ax.set_xticks([1, 2, 3])
# _ = ax.set_xticklabels(sites, fontsize='x-large')