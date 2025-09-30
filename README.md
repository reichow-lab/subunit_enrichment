# subunit_enrichment

The purpose of this workflow is to generete gap junction particle.cs files that have been enriched for a desired state that can be imported back into CryoSPARC for high resolution refinement.


IMPORTANT:
These scripts rely on analyzing a .csv file with three columns using metadata extracted from a .cs file generated from CryoSPARC in a specific order: uid, sym_expand/idx and sym_expand/src_uid.

The intended input for these scripts is metadata that was extracted from a .cs file from gap junction particles that were symmetry expanded and signal subtracted to obtain a connexin monomer and that have gone through 3D classification. Each class’s .cs will need to have its metadata extracted to a .csv file and analyzed by the scripts individually.

########################################################################



Step # 1: Generate/acquire the necessary files to begin:

1) Extracted metadata .csv from the subunit state of interest
- Start by following [Steps #1 - 7 in the subunit_analysis repository](https://github.com/reichow-lab/subunit_analysis/blob/main/README.md) to generate the required metadata .csv files

2) Exported particles_exported.cs file from an unbinned consensus refinement
- This refinement must contain all particles that eventually went into the symmetry expansion/signal subtraction/3D classification workflow



########################################################################



Using the Metadata_Enrichment.sh script

Step # 2: Load the script
```
./Metadata_Enrichment.sh
```
 - Enter the path to the metadata .csv file of interest

 - After seeing the distribution, input the number of subunits that is wanted for enrichment

IMPORTANT: Make note of the number of particles of the selected criteria it will be needed later in this workflow

 - This will create a new "enriched_values" .csv file containing particle IDs that fit the selected criteria that is used with the Metadata_filter/py script

Optional: rename the the enriched_values.csv with # of enriched subunits (e.g. 10gated_enriched_values.csv) and repeat the script using another enrichment criteria.

 - Typical use case is to generate several enriched_values.csv files of different amounts of the desired state to be enriched that get independently used in the script below. 

 - The end goal being several particles.cs files with varying amounts of the desired state in gap junction particles.
    - 10gated_enriched_values.csv
    - 11gated_enriched_values.csv
    - 12gated_enriched_values.csv


########################################################################



Using the Metadata_Filter.py script

Step # 3: Load the the script

```
python3 Metadata_Filter.py
```
 - Enter the path to the consensus refinement partilces_exported.cs file
 - Enter the path to the enriched_values.csv file

 - This script will create a new gap junction particle.cs file named "filtered_particles.cs" that can be imported into CryoSPARC

Step # 4: Rename the filtered_particles.cs file with an unique identifier
```
mv fitlered_particles.cs 10gated_particles.cs
```
Step # 5: Repeat Steps # 3 & 4 for each enriched_values.csv file
 - 10gated_particles.cs
 - 11gated_particles.cs
 - 12gated_particles.cs

########################################################################


Importing the filtered_particles.cs file into CryoSPARC

Step # 6: Move the filtered_particle.cs file(s) to the exported consensus particle.cs directory
```
scp *gated_filtered_particles.cs user@xxx.edu:/.../exports/jobs/J350_nonuniform_refine_new/J350_particles/)
```
Step # 7: Make a copy of the particle.csg file that will get edited to point at the new 10gated_filtered_particles.cs file
```
cp J350_particles_exported.csg 10gated_filtered_particles.csg
```
Step # 8: Use Vim or something similar to edit the 10gated_filtered_particles.csg file
```
vi 10gated_filtered_particles.csg
```
- The file should look something similar to below
```
created: xxxx-xx-xx xx:xx:xx.xxxxxx
group:
  description: All particles that were processed, including alignments
  name: particles
  title: All particles
  type: particle
results:
  alignments2D:
    metafile: '>J350_particles_exported.cs'
    num_items: 456024
    type: particle.alignments2D
  alignments3D:
    metafile: '>J350_particles_exported.cs'
    num_items: 456024
    type: particle.alignments3D
  blob:
    metafile: '>J350_particles_exported.cs'
    num_items: 456024
    type: particle.blob
  ctf:
    metafile: '>J350_particles_exported.cs'
    num_items: 456024
    type: particle.ctf
  location:
    metafile: '>J350_particles_exported.cs'
    num_items: 456024
    type: particle.location
  pick_stats:
    metafile: '>350_particles_exported.cs'
    num_items: 456024
    type: particle.pick_stats
version: v4.4.1
```


Step # 9: Change metadata file from the old .cs file to the new enriched .cs file and the num_items (number of particles)
 - In this example:
    - The old .cs file = "J350_particles_exported.cs" with 456024 particles
    - The new enriched .cs file = "10gated_filtered_particles.cs" with 12345 particles
```
created: xxxx-xx-xx xx:xx:xx.xxxxxx
group:
  description: All particles that were processed, including alignments
  name: particles
  title: All particles
  type: particle
results:
  alignments2D:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.alignments2D
  alignments3D:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.alignments3D
  blob:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.blob
  ctf:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.ctf
  location:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.location
  pick_stats:
    metafile: '>10gated_filtered_particles.cs'
    num_items: 12345
    type: particle.pick_stats
version: v4.4.1
```
Step # 10: Save and quit
```
:wq
```

Step # 11: Repeat Steps # 6-10 for each filtered_particles.cs file
 - 10gated_filtered_particles.csg
 - 11gated_filtered_particles.csg
 - 12gated_filtered_particles.csg

Step # 12: Import the new .csg files into CryoSPARC using the import result group job type and make sure the number of particles imported matches the expected number of partilces.

Step # 13: Provided the consensus map still has extracted partilces attached to it, then the particles are ready for 3D refinement. 
