#!/usr/bin/env python
# coding: utf-8

# Author: Cory Dunn
# Github: 
# License: GPLv3
# Version 1.31


import numpy as np
from Bio import SeqIO
import argparse
import logging

if __name__ == "__main__" : 

    version = '1.31'

    # Collect input from user

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input_file', required = True, type = str, help = 'Input alignment in FASTA format.\n')
    ap.add_argument('-o', '--output_file', required = True, type = str, help = 'Output alignment in FASTA format.\n')
    ap.add_argument('-r', '--reference_sequence', required = True, type = str, help = 'Reference seqeunce used for alignment ungapping. Note that spaces are converted to underscores in accession names when loading input alignment.\n')

    args = vars(ap.parse_args())

    # Selected input file and reference to variables

    selected_accession = args['reference_sequence']
    alignfile = args['input_file']
    output_file = args['output_file']

    input_strip = alignfile.split('.', 1)[0]
    log_outputfilename = input_strip + '_ungap_on_reference.log'

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
    mylogs.info('Version: ' + version + '\n')
    mylogs.info('This software removes alignment columns from a FASTA multiple sequence alignment based upon gap locations within the reference sequence.\n')
    mylogs.info('Author: Cory Dunn')
    mylogs.info('Email: cory.david.dunn@gmail.com')
    mylogs.info('Input FASTA: ' + str(alignfile))
    mylogs.info('Selected reference sequence: ' + str(selected_accession))

    # Find reference sequence location in FASTA

    reference_index = -1
    count = 0

    for record in SeqIO.parse(alignfile, 'fasta'):

        reference_name = record.name
        reference_name_underscore = reference_name.replace(' ', '_')
        if selected_accession == reference_name_underscore:
            reference_sequence = list(record.seq)
            reference_sequence_NP = np.array(reference_sequence, dtype = 'str')
            reference_index = count
            break
        count += 1

    if reference_index == -1:
        mylogs.info('Reference accession ' + selected_accession + ' not found.')
        quit()

    # Find gap indices

    gap_index = np.where(reference_sequence_NP == '-')

    # Save new FASTA alignment

    ofile = open(output_file, 'w')

    for record in SeqIO.parse(alignfile, 'fasta'):

        accession_name = str(record.name)
        accession_name_underscore = accession_name.replace(' ', '_')
        accession_sequence = list(record.seq)
        accession_sequence_NP = np.array(accession_sequence, dtype = 'str')
        accession_sequence_ungapped_NP = np.delete(accession_sequence_NP, gap_index)
        accession_sequence_back_to_str = accession_sequence_ungapped_NP.astype('|S1').tobytes().decode('utf-8')
        ofile.write('>' + accession_name_underscore + '\n' + accession_sequence_back_to_str + '\n')
        
    ofile.close()
