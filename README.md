# subunit_enrichment
Enriching gap junction cryoSPARC metadata that has been signal subtracted for a single subunit and 3D classified

These scripts rely on analyzing a .csv file with three columns using metadata extracted from a .cs file generated from CryoSPARC in a specific order: uid, sym_expand/idx and sym_expand/src_uid.

The intended input for these scripts is metadata that was extracted from a .cs file from gap junction particles that were symmetry expanded and signal subtracted to obtain a connexin monomer and that have gone through 3D classification. Each class’s .cs will need to have its metadata extracted to a .csv file and analyzed by the scripts individually.


########################################################################


Step # 1: Generate/acquire the necessary files to begin:

1) Extracted metadata .csv from the subunit state of interest
   - Start by following [Steps #1 - 7 in the subunit_analysis repository](https://github.com/reichow-lab/subunit_analysis/blob/main/README.md) to generate the required metadata .csv files

2) Exported .cs file from an unbinned consensus refinement
   - This refinement must contain all particles that eventually went into the symmetry expansion/signal subtraction/3D classification workflow


########################################################################


Using the Metadata_Enrichment.sh script

Step # 2: Load the script
```
./Metadata_Enrichment.sh
```
Enter a metadata .csv file of interest

After seeing the distribution, input the number of subunits that is wanted for enrichment

This will create a new "enriched_values" .csv file containing particle IDs that fit the selected criteria that is used with the Metadata_filter/py script

Optional: rename the the enriched_values.csv with # of enriched subunits (e.g. 10gated_enriched_values.csv) and repeat the script using another enrichment criteria. Repeat and concatenated enriched_values.csv (see below) files as necessary.
```
cat 10gated_enriched_values.csv 11gated_enriched_values.csv 12gated_enriched_values.csv > 10-12gated_enriched_values.csv
```


########################################################################


Using the Metadata_Filter.py script

Step # 3: Load the the script

```
python3 Metadata_Filter.py
```
Enter in the consensus refinement .cs file
Enter in the enriched_values.csv file

