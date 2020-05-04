"""
Name:     sql connection
Author:   Kristen Boysen
Created:  1 April 2020
Revised:  
Version:  Created using Python 3 , ArcPro 2.5
Purpose: Connect to NV Database in SQL

"""
####Import packages
import numpy as np
import pandas as pd
import sqlite3



conn = sqlite3.connect('./data/test.db') ##connect to database

with conn:
    #create cursor to navigate
    c= conn.cursor()
    #read in content
    site_scale_score = pd.read_sql('SELECT * FROM site_scale_scores', conn)

