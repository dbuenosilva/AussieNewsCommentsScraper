# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 3-lemmatization.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Figuring out the lemma of each word in sentencens.
#
#
##########################################################################
# Maintenance                            
# Author: 
# Date: 
# Description:  
#
##########################################################################>

import sys
import pathlib
import pandas as pd

path = str(pathlib.Path(__file__).resolve().parent) + "/"
sys.path.append(path)