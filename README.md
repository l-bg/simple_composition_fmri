# Source code for [Bonnasse-Gahot, Bemis, Perez-Guevara, Dehaene, Pallier (2020). An fMRI study of composition in simple noun and verb phrases. (Preprint)](https://www.biorxiv.org/cgi/content/short/2025.12.17.694853v1)

Participants were scanned with fMRI while they were presented with short visual sequences (1 to 4 words long)
forming either meaningful grammatical phrases (e.g. `avec son beau clavier`
(`with his nice keyboard`) or unstructured lists `Adam son plus clavier` (`Adam
his more keyboard`)).

## Getting fMRI data

fMRI data can be obtained at openneuro.org.

The project is organized with the following structure:

```
├── code
├── derivatives
│   ├── figures
│   ├── fmriprep
│   │   ├── sub-01
│   │   │   ├── anat
│   │   │   └── func
│   │   ├── sub-02
│   │   └──  ...
│   ├── languagelocalizer_analysis
│   │   ├── contrasts
│   │   └── glm
│   ├── maindesign_model-anova_analysis
│   │   ├── events
│   │   └── glm
│   ├── maindesign_model-incremental_analysis
│   │   ├── contrasts
│   │   ├── events
│   │   └── glm
│   └── mask_simpcomp.nii
├── rawdata
│   ├── sub-01
│   │   ├── anat
│   │   └── func
│   ├── sub-02
│   └── ...
└── sourcedata
    └── roi_masks
    └── simpcomp_behavioral_data.csv
```

## Preprocessing  

In case you want to perform the preprocessing, you will need [fmriprep](https://github.com/poldracklab/fmriprep).

You must obtain a [freesurfer licence](https://surfer.nmr.mgh.harvard.edu/registration.html), and then create a variable FREESURFER_LICENCE pointing to the licence file:

---

    export FREESURFER_LICENCE=/home/lbg/freesurfer/licence.txt
    fmriprep-docker --fs-no-reconall --fs-license-file=$FREESURFER_LICENCE -w /tmp $SIMPCOMP/rawdata $SIMPCOMP/derivatives participant

---

## Check the required Python modules


Check that you have the modules listed in [requirement.txt](requirement.txt) by running


    python check_env.py


## Run the pipeline


1. you should set the `home_folder` variable in [simpcomp.py](simpcomp.py) to point to the directory of the study.

Alternatively, you can also set the home folder using the SIMPCOMP shell variable

    export SIMPCOMP=/home/lbg/research/cams/projects/simpcomp/

or

    export SIMPCOMP=/home/cp983411/git/simple_composition_fmri/

2. Launch `jupyter-notebook` and open the  notebook [main.ipynb](main.ipynb)
