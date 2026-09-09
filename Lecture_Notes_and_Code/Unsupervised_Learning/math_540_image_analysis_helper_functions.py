import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import io

# We need a tool that converts images into grayscale (i.e. all pixel values in [0, 1])
def gray_scale_convert(image):
    rescaled_image = np.zeros((image.shape[0], image.shape[1]))
    rescaled_image[:, :] = image
    rescaled_image -= np.min(rescaled_image)
    rescaled_image /= np.max(rescaled_image)
    return rescaled_image

# We need to be able to pass in a directory and build an image list
def file_builder(data_path):
    image_list = []
    image_paths = []
    labels = []

    # 2. Define uniform target dimensions
    IMG_WIDTH = 256
    IMG_HEIGHT = 256
    for root, dirs, files in os.walk(data_path):
        for file in files:
            # Ignore hidden system files like .DS_Store or READMEs
            if file.startswith('.') or file.endswith('.txt'):
                continue
                
            # Full path to the image
            full_path = os.path.join(root, file)
            image_paths.append(full_path)
            # Read the image in grayscale mode (0)
            img = cv2.imread(full_path, 0)
        
            if img is not None:
                # Resize image to uniform dimensions
                resized_img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                image_list.append(gray_scale_convert(resized_img))
                # Extract the label (e.g., 'subject01' from 'subject01.normal')
                # Adjust the splitting logic depending on how Kaggle names the files
                subject_label = file.split('.')[0] 
                labels.append(subject_label)
                
    return image_list, labels

# We would like to easily comapre different images to one another after we do various things to them.  
def image_comparison(original_image, reduced_image):
    gscale_reduced_image = gray_scale_convert(reduced_image) # note, we need to make sure skinny_puppy is grayscale
    difference = np.abs( original_image - gscale_reduced_image )

    fig, axes = plt.subplots(1, 3, figsize=(10, 5))
    ax = axes.ravel()
    ax[0].imshow(original_image, cmap=plt.cm.gray)
    ax[0].set_title("Original")
    ax[1].imshow(gscale_reduced_image, cmap=plt.cm.gray) 
    ax[1].set_title("Reduced")
    ax[2].imshow(difference, cmap=plt.cm.gray)
    ax[2].set_title("Difference")
    fig.tight_layout()

def zero_mean(mat):
    avg_mat = np.tile(np.mean(mat, axis=1).reshape(-1, 1), (1, mat.shape[1]))
    zero_avg_mat = mat - avg_mat
    return zero_avg_mat, avg_mat

def mode_builder(data_mat):
    zero_avg_data, _ = zero_mean(data_mat)
    u, s, vh = np.linalg.svd(zero_avg_data, full_matrices=False)
    return u, s

def mode_selector(u, s, thrshhld):
    indskp = np.log10(s/s[0]) >= -thrshhld
    return u[:, indskp]

def mode_projector(data_mat, u):
    return u @ (u.T @ data_mat)