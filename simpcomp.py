import os
import numpy as np
import pandas as pd
import seaborn as sns
import os.path as op

from nistats.second_level_model import SecondLevelModel
import nibabel as nib

from nilearn.masking import apply_mask, intersect_masks
from nilearn.image import resample_to_img

home_folder = '/home/lbg/research/cams/projects/simpcomp/'
# home_folder = '/home/cp983411/git/simple_composition_fmri/'

try:
    home_folder
except NameError:
    home_folder = os.getenv('SIMPCOMP')

assert home_folder != None, "You must set the home directory of the simpcomp study; either in python with 'home_folder=/path/to/study', or in the shell with 'export SIMPCOMP=/path/to/study'"

assert op.exists(home_folder)

fmri_data = op.join(home_folder, 'derivatives', 'fmriprep')
events_folder = op.join(home_folder, 'rawdata')
model_incremental_folder = op.join(home_folder, 'derivatives', 'maindesign_model-incremental_analysis')
model_anova_folder = op.join(home_folder, 'derivatives', 'maindesign_model-anova_analysis')
localizer_folder = op.join(home_folder, 'derivatives', 'languagelocalizer_analysis')
roi_masks = op.join(home_folder, 'sourcedata', 'roi_masks')
figures_folder = op.join(home_folder, 'derivatives', 'figures')

# three subjects were rejected because of their low (below 80%) performance on
# the probe detection task
REJECTED_SUBJECTS = [3, 6, 12]
N_SUBJECTS = 18
subject_list = ['sub-{:02d}'.format(k) for k in np.setdiff1d(np.arange(1,N_SUBJECTS+1),
                                                          REJECTED_SUBJECTS)]

color = np.vstack((sns.color_palette('Reds_r', 5)[0:3],
                   sns.color_palette('Blues_r', 5)[0:3],
                   [0.95]*3,
                   [0.6]*3,
                   [0.3]*3,))

# helpers
def make_dir(directory):
    if not op.exists(directory):
        os.makedirs(directory)

def create_one_sample_t_test(name, maps, output_dir, smoothing_fwhm=6.0):
    if not op.isdir(output_dir):
        op.mkdir(output_dir)
    model = SecondLevelModel(smoothing_fwhm=smoothing_fwhm)
    design_matrix = pd.DataFrame([1] * len(maps),
                                 columns=['intercept'])
    model = model.fit(maps,
                      design_matrix=design_matrix)
    z_map = model.compute_contrast(output_type='z_score')
    nib.save(z_map, op.join(output_dir, "{}_group_zmap.nii.gz".format(name)))

def pvalue2str(pvalue):
    if pvalue <= 0.001:
        return '***'
    elif pvalue <= 0.01:
        return '**'
    elif pvalue <= 0.05:
        return '*'
    else:
        return 'ns'

def binarize_img(img, threshold):
    mask = img.get_data().copy()
    mask[mask < threshold] = 0.
    mask[mask >= threshold] = 1.
    return nib.Nifti1Image(mask, img.affine)

def create_bestvoxels_mask(roi_img, localizer_img, n_voxels=100):
    """ select voxels within roi_img having the largest values in localizer_img """
    masked_data = apply_mask(localizer_img, roi_img)
    threshold = -np.sort(-masked_data)[min(n_voxels, masked_data.size)-1]
    mask = binarize_img(localizer_img, threshold)
    return intersect_masks((roi_img, mask), threshold=1)

def prepare_masks(sub_id, roi_imgs, n_best):
    mask_imgs = []
    localizer_img = nib.load(op.join(localizer_folder,
                                     'contrasts/sentence_pseudo_{}_effsize.nii.gz'.format(sub_id)))
    for roi_img in roi_imgs:
        roi_img = binarize_img(resample_to_img(roi_img, localizer_img), 0.5)
        mask_imgs.append(create_bestvoxels_mask(roi_img, localizer_img, n_best))
    return mask_imgs
