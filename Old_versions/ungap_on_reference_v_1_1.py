#!/usr/bin/env python
# coding: utf-8 

# Funding received from the Sigrid Jusélius Foundation, the Academy of Finland, and the Jane and Aatos Erkko Foundation contributed to the development of this software.
# Author: Cory Dunn
# Institution: University of Helsinki
# Author Email: cory.dunn@helsinki.fi
# License: GPLv3
# Version: 1.1

# Load dependencies

import pandas as pd
import numpy as np
from Bio import SeqIO
import argparse
import logging

if __name__ == "__main__" :

    # Collect input from user

    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input_file',required=True,type=str,help='Input alignment in FASTA format.\n')
    ap.add_argument('-o','--output_file',required=True,type=str,help="Output alignment in FASTA format.\n")
    ap.add_argument('-r','--reference_sequence',required=True,type=str,help='Reference sequence used for alignment ungapping.\n')

    args = vars(ap.parse_args())

    # Selected reference and file for ungapping

    selected_accession = args['reference_sequence']
    alignfile = args['input_file']
    output_file = args['output_file']
    
    sep = '.'
    input_strip = alignfile.split(sep, 1)[0]
    log_outputfilename = input_strip+'_ungap_on_reference.log'
    
    # Logging and streaming to console

    mylogs = logging.getLogger(__name__)
    mylogs.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    streamformat = logging.Formatter("%(message)s")
    stream.setFormatter(streamformat)
    mylogs.addHandler(stream)

    logfile = logging.FileHandler(log_outputfilename)
    mylogs.addHandler(logfile)
    
    mylogs.info('\nUngap_on_reference')
    version = '1.1'
    mylogs.info('Version: ' + version +'\n')
    mylogs.info('This software removes alignment columns from a FASTA multiple sequence alignment based upon gap locations within the reference sequence.\n')
    mylogs.info('Cory Dunn')
    mylogs.info('University of Helsinki')
    mylogs.info('cory.dunn@helsinki.fi')
    mylogs.info('Please cite (DOI): 10.5281/zenodo.4633159\n')
    mylogs.info('Input FASTA: ' + str(alignfile))
    mylogs.info('Selected reference sequence: ' + str(selected_accession))

    # Initialize lists for FASTA information

    record_x_toward_seq_dataframe = []
    sequence_records = []
    alignment_record_name_list = []

    # Load input FASTA into dataframe

    for record in SeqIO.parse(alignfile,"fasta"):
        alignment_record_name_list.append(record.name)
        record_x_toward_seq_dataframe = list(record.seq)
        record_x_toward_seq_dataframe_UPPER = [x.upper() for x in record_x_toward_seq_dataframe] 
        sequence_records.append(record_x_toward_seq_dataframe_UPPER)

    accession_name_dataframe = pd.DataFrame(alignment_record_name_list, columns=['Accession'])
    sequence_dataframe = pd.DataFrame(sequence_records)

    # Select row with chosen accession

    my_accession_row = accession_name_dataframe[accession_name_dataframe['Accession'] == selected_accession].index[0]
    my_accession_sequence = sequence_dataframe.iloc[my_accession_row,:]

    # Ungap based upon chosen accession

    sequence_dataframe_series_remove = my_accession_sequence == '-'
    sequence_dataframe_index_remove = sequence_dataframe_series_remove[sequence_dataframe_series_remove].index
    sequence_dataframe = sequence_dataframe.drop(sequence_dataframe_index_remove,axis=1)

    sequence_dataframe_concat = sequence_dataframe.apply(''.join, axis=1)
    sequence_dataframe_final_seq_list = sequence_dataframe_concat.values.tolist()

    # Write FASTA ungapped based upon chosen accession

    ofile = open(output_file, "w")
    for seqi in range(len(alignment_record_name_list)):
        ofile.write(">" + alignment_record_name_list[seqi] + "\n" + sequence_dataframe_final_seq_list[seqi] + "\n")
    ofile.close()
    mylogs.info('Output FASTA: ' + str(output_file))