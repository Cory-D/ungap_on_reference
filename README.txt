# ungap_on_reference
Ungap_on_reference: Removal of FASTA alignment columns based upon gap locations in a selected sequence

Version: 1.0

----

Author:

Cory Dunn
Institute of Biotechnology
University of Helsinki
Email: cory.dunn@helsinki.fi

----

License:

GPLv3

----

Acknowledgements:

Funding received from the Sigrid Jusélius Foundation, the Academy of Finland, and the Jane and Aatos Erkko Foundation contributed to the development of this software.

----

Requirements:

ungap_on_reference is implemented in Python 3 (tested under version 3.9.1) 

Dependencies: 
Biopython (tested under version 1.78),
Pandas (tested under version 1.2.2),
Numpy (tested under version 1.20.1)

----

Usage:

python ungap_on_reference.py -i <INPUT_FILE> -o <OUTPUT_FILE> -r <REFERENCE_SEQUENCE>

----

Guidance: 

>1 AT--CGGAG
>2 A-AACGGAG
>3 -TAACGGAG

Ungap using 1 as reference:

ATCGGAG
A-CGGAG
-TCGGAG

Ungap using 2 as reference:

A--CGGAG
AAACGGAG
-AACGGAG

----

Example files included in repository:

mammal_ND5_protein_G_INS_i.fasta - an input alignment of ND5 protein sequences (mammalian, as well as a sequence from a single reptile, Anolis punctatus).

mammal_ND5_protein_ungap_NC_006853_1_Bos_taurus.fasta - the input alignment ungapped by the Bos taurus reference ("python ungap_on_reference.py -i mammal_ND5_protein_G_INS_i.fasta -o mammal_ND5_protein_ungap_NC_006853_1_Bos_taurus.fasta -r NC_006853_1_Bos_taurus")

mammal_ND5_protein_ungap_NC_012920_1_Homo_sapiens.fasta - the input alignment ungapped by the Homo sapiens reference ("python ungap_on_reference.py -i mammal_ND5_protein_G_INS_i.fasta -o mammal_ND5_protein_ungap_NC_012920_1_Homo_sapiens.fasta -r NC_012920_1_Homo_sapiens")

mammal_ND5_protein_ungap_NC_044125_1_Anolis_punctatus.fasta - the input alignment ungapped by the Anolis punctatus reference ("python ungap_on_reference.py -i mammal_ND5_protein_G_INS_i.fasta -o mammal_ND5_protein_ungap_NC_044125_1_Anolis_punctatus.fasta -r NC_044125_1_Anolis_punctatus")
