#!/usr/bin/python
import math 
import random
import os
import re
from Phy_to_Nex import Phy_to_Nex

## I have 72 genes to perform automodel on and then build a paup block for, so I keep this counter variable
count = 0

#set stopping condition, which should be the number of files you have to run seperately
stop = 2

## Go through each file, I will add to count as I go through files
while count < stop:
	
	## pull out first file and open for reading
	phylip_file = "dataset_" + str(count) +".phy"
	output_nex_file = "dataset_" + str(count) +".nex"
	Phy_to_Nex(phylip_file, output_nex_file)
	os.system("./paup4a165_osx -n " + output_nex_file)
	
	count = count + 1
