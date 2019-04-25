#!/usr/bin/python
import math 
import random
import os
import re
	
def Phy_to_Nex(phylip, output):
	
	## open phylip file for reading
	phylipFile = open(phylip, 'r+')
	
	## store all lines; create list objects for taxon ids and seqeunces
	all_lines = phylipFile.readlines()
	ids = []
	seqs = []
	
	## first line in phylip file has two pieces of information; number of taxa and length of sequences
	first_line_info = all_lines[0].split()
	num_taxa = int(first_line_info[0])
	seq_length = int(first_line_info[1])
	
	## Phylip files are weird, where the sequences are divided into chunks, and only the first chunk bares the sequence ID
	## to handle this, index the rows + 1 blank line
	indexing_range = list(range(0, num_taxa + 1))
	seq_index = indexing_range * int(len(all_lines)/num_taxa)
	seq_index =  [1] + seq_index
	
	## start at 1 because first line in file was number of taxa and sequence length
	## first for loop goes through first phylip chunk with ids
	for i in range(1, num_taxa + 1):
		id = all_lines[i][0:5].rstrip()	
		sequence = all_lines[i][6:int(seq_length)-1]
		sequence = re.sub(' +', '', sequence)		
		ids.append(id)
		seqs.append(sequence.rstrip())
	
	## add at end to cover blank line
	ids.append("blank")
	seqs.append("blank")

	## go throughs all additional phylip chunks
	for k in range(num_taxa + 1, len(all_lines)):
		if not all_lines[k].strip():
			print("line "+ str(k)+ " empty ")
		else:
			sequence = all_lines[k][0:int(seq_length)-1]
			sequence = re.sub(' +', '', sequence)
			index = seq_index[int(k)]
			seqs[index] = seqs[index] + sequence.rstrip()
			
	## close the phylip file
	phylipFile.close()
	
	## open the output file for writing
	nexusFile = open(output, 'w')
	
	## start at the top of the file and write the header for a nexus file while filling in the correct info on length
	## of locus and number of taxa
	nexusFile.seek(0)
	nexusFile.write("#NEXUS\n\nBEGIN DATA;\n\tDIMENSIONS  NTAX="+str(num_taxa)+" NCHAR="+str(seq_length)+";\nFORMAT DATATYPE=DNA  MISSING=-;\nMATRIX\n")

	## write out all of the sequence data stored in seqs, except for last blank object
	for i in range(0, len(seqs)-1):
		#print(ids[i]+"\t" + listseqs[i])
		nexusFile.write(ids[i]+"\t"+seqs[i]+"\n")

	## close the data portion with end
	nexusFile.write(";\nEND;\n\n")
	
	## write out the paup block for model selection
	## HERE is where you can change the params for auto model in paup!!
	nexusFile.write("begin paup;\nlog start;\nSet criterion=distance;\nDset distance=logDet;\nNJ;\nAutoModel AICc=yes BIC=no DT=no;\nlog stop;\nend;\n")

	## close file
	nexusFile.close()	