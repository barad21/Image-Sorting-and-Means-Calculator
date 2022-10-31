#%% Author:
"""
Created on Sun Sep  4 15:29:16 2022

@author: 1bora
"""

#%% Libraries:
import pandas as pd
import numpy as np
from PIL import Image as im
from PIL import ImageChops
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import image
from scipy import ndimage
import os
import pyometiff
import re
import seaborn as sns
import imagehash
from tqdm import tqdm
from skimage.metrics import structural_similarity as compare_ssim
import argparse
import imutils
import cv2
#%% Sorting function:

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#%% Creating the export lists and dictionary:
First_obs_dir = r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Unprocessed Images/1st Obs Only TIFF"
Second_obs_dir = r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Unprocessed Images/2nd Obs Only TIFF"
Third_obs_dir = r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Unprocessed Images/3rd Obs Only TIFF"
Fourth_obs_dir = r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Unprocessed Images/4th Obs Only TIFF"

Observation_dir_list = [First_obs_dir, Second_obs_dir, Third_obs_dir, Fourth_obs_dir]

First_obs_contents = os.listdir(Observation_dir_list[0]) 
Second_obs_contents = os.listdir(Observation_dir_list[1])
Third_obs_contents = os.listdir(Observation_dir_list[2])
Fourth_obs_contents = os.listdir(Observation_dir_list[3])

First_obs_contents.sort(key= natural_keys)
Second_obs_contents.sort(key= natural_keys)
Third_obs_contents.sort(key= natural_keys)
Fourth_obs_contents.sort(key= natural_keys)

Observation_dict = {"FO": [], "SO": [], "TO": [], "FourthO": []}

#%% Importing the images.
for i in tqdm(range(len(Observation_dir_list))):
    
    if i == 0:
        
        for j in range(len(First_obs_contents)):
            
            image_array = im.open(Observation_dir_list[0]+"/%s" % First_obs_contents[j])
            
            Observation_dict["FO"].append(image_array)
            
            
    elif i == 1:
        
        for k in range(len(Second_obs_contents)):
            
            image_array = im.open(Observation_dir_list[1]+"/%s" % Second_obs_contents[k])
            
            Observation_dict["SO"].append(image_array)
            
            
    elif i == 2:
        
        for l in range(len(Third_obs_contents)):
            
            image_array = im.open(Observation_dir_list[2]+"/%s" % Third_obs_contents[l])
            
            Observation_dict["TO"].append(image_array)
    
    elif i == 3:
        
        for m in range(len(Fourth_obs_contents)):
            
            image_array = im.open(Observation_dir_list[3]+"/%s" % Fourth_obs_contents[m])
            
            Observation_dict["FourthO"].append(image_array)
            
    else:
        pass
    
#%% Exporting the images for later use:
    
#Observation_dict["FO"][0].save("C:/Users/1bora/OneDrive/Masaüstü/2209-A/Exported_Images/test1.tif")
 
for i in range(len(Observation_dict["FO"])):
    
    Observation_dict["FO"][i].save(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Exported_Images/First_Ob/%d.tiff" % i)

for j in range(len(Observation_dict["SO"])):
    
    Observation_dict["SO"][j].save(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Exported_Images/Second_Ob/%d.tiff" % j)

for k in range(len(Observation_dict["TO"])):
    
    Observation_dict["TO"][k].save(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Exported_Images/Third_Ob/%d.tiff" % k)

for l in range(len(Observation_dict["FourthO"])):
    
    Observation_dict["FourthO"][l].save(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Exported_Images/Fourth_Ob/%d.tiff" % l)
           
#%% Comparing Images - First with Others:
    
hash_1_2 = []
hash_1_3 = []
hash_1_4 = []

for i in tqdm(range(len(Observation_dict["FO"]))):
    
    init_hash = imagehash.average_hash(Observation_dict["FO"][i])
    
    for j in range(len(Observation_dict["SO"])):
        
        secondary_hash = imagehash.average_hash(Observation_dict["SO"][j])
        
        res = init_hash - secondary_hash
        
        if res < 10:
            
            hash_1_2.append([res, i, j])
        
        else:
            pass
        
    for k in range(len(Observation_dict["TO"])):
        
        third_hash = imagehash.average_hash(Observation_dict["TO"][k])
        
        res = init_hash - third_hash
        
        if res < 10:
            
            hash_1_3.append([res, i, k])
        
        else:
            pass
    
    for l in range(len(Observation_dict["FourthO"])):
        
        fourth_hash = imagehash.average_hash(Observation_dict["FourthO"][l])
        
        res = init_hash - fourth_hash
        
        if res < 10:
            
            hash_1_4.append([res, i, l])
        
        else:
            pass

#%% Comparing Images - 2 with 3 and 4:

hash_2_3 = []
hash_2_4 = []

for i in tqdm(range(len(Observation_dict["SO"]))):
    
    init_hash = imagehash.average_hash(Observation_dict["SO"][i])
    
    for j in range(len(Observation_dict["TO"])):
        
        third_hash = imagehash.average_hash(Observation_dict["TO"][j])
        
        res = init_hash - third_hash
        
        if res < 10:
            
            hash_2_3.append([res, i, j])
        
        else:
            pass
    
    for k in range(len(Observation_dict["FourthO"])):
        
        fourth_hash = imagehash.average_hash(Observation_dict["FourthO"][j])
        
        res = init_hash - fourth_hash
        
        if res < 15:
            
            hash_2_4.append([res, i, k])
        
        else:
            pass
        
#%% Comparing Images - 3 with 4:
    
hash_3_4 = []

for i in tqdm(range(len(Observation_dict["TO"]))):
    
    init_hash = imagehash.average_hash(Observation_dict["TO"][i])
    
    for j in range(len(Observation_dict["FourthO"])):
        
        fourth_hash = imagehash.average_hash(Observation_dict["FourthO"][j])
        
        res = init_hash - fourth_hash
        
        if res < 10:
            
            hash_3_4.append([res, i, j])
        
        else:
            pass

#%% Plotting the Similar or Same Images in Subplots:

i = 31
j = 46
k = 36
l = 51

fig, axs = plt.subplots(1,4)

axs[0].imshow(Observation_dict["FO"][i])
axs[0].set_title("İlk Gözlem")

axs[1].imshow(Observation_dict["SO"][j])
axs[1].set_title("3 Ay sonra")
axs[1].set_yticks([])

axs[2].imshow(Observation_dict["TO"][k])
axs[2].set_title("6 Ay sonra")
axs[2].set_yticks([])

axs[3].imshow(Observation_dict["FourthO"][l])
axs[3].set_title("9 Ay sonra")
axs[3].set_yticks([])

#%% Match List

"""
Match List(Index):
    
    Write the images with hash level of 1 to the area below.

 FO SO TO FourthO (Ob1 vs Ob2, Ob3, Ob4)
 ----------------
 26 40 47 -
 
 26 44 47 -
 
 31 46 45 -
 
 31 47 46 -
 
 27 41 42 -
 
 28 41 42 -
 
 27 37 42
 
 28 37 42
 
 28 41 46 -
 
 33 16 -  -
 
 47 30 -  -
 
 --------------------------
 
 FO SO TO FourthO (Ob2 vs Ob3, Ob4)
 ----------------
    36 33
    
    36 43
    
    37 34
    
    37 38
    
    37 42
    
    38 37
    
    40 33
    
    42 41
    
    46 45
    
    45 46
    
To be honest, evaluate the fourth obs. manually and focus on how much degredation there are rather than signal.

 --------------------------
 
 FO SO TO FourthO   -   Manual.
 ----------------

For this part, None of the images will be used in comparing observations because
degredation is far too much and the hash values calculated from it are significantly
larger than the other images. That is why a comparison cannot be made.

Analyse these images' means.
    
"""

#%% Notes:
    
"""
There are several things you can do with the means.

First is to compare them image by
image, which would give you an accurate idea on the amount of photobleach that occured for similar
images.

Second is to get the means of each individual observation, this would prove the 
general amount of photobleach that occured.

Definetly do these two and explain the method of your anaylsis in your result 
report. Unfortunately in Turkish.

Note: keep in mind that due to the files being in .tiff format does not mean it accurately
gives you the signal. Unfortunately only the relative signal intensity or light intensity
can be calculated due to how the Zeiss program gives us that image. 
Fortunately we have the ZEISS output as well, so we can make a comparison on that.


Improvements:
    
    add a way that you can identify the image from the slice (writable_image)
    you can do this via sorting the folder that contains the snaps, then using the 
    indices of the slices folder. Something like:
        
        slice_ind_and_img = []
        
        original_snaps_folder.sort(key=natural_keys)
        
        for i in range(len(slice_folder_contents)):
            
            slice_ind_and_img.append([original_snaps_folder[i], slice_folder_contents[i]])
            
    
    From this you can identify the images by their wavelenght excitation and from there
    you can decide on which ones to use and which ones to discard.
"""

#%% Means Analysis Part-1 Getting individual means of each image:

Means_1 = []
Means_2 = []
Means_3 = []
Means_4 = []

Means_1_with_names = []
Means_2_with_names = []
Means_3_with_names = []
Means_4_with_names = []

for i in tqdm(range(len(Observation_dict["FO"]))):
    
    mean_Val = np.mean(Observation_dict["FO"][i])
    
    Means_1.append(mean_Val)
    
    Means_1_with_names.append([First_obs_contents[i],mean_Val])

for i in tqdm(range(len(Observation_dict["SO"]))):
    
    mean_Val = np.mean(Observation_dict["SO"][i])
    
    Means_2.append(mean_Val)
    
    Means_2_with_names.append([Second_obs_contents[i],mean_Val])

for i in tqdm(range(len(Observation_dict["TO"]))):
    
    mean_Val = np.mean(Observation_dict["TO"][i])
    
    Means_3.append(mean_Val)
    
    Means_3_with_names.append([Third_obs_contents[i],mean_Val])

for i in tqdm(range(len(Observation_dict["FourthO"]))):
    
    mean_Val = np.mean(Observation_dict["FourthO"][i])
    
    Means_4.append(mean_Val)
    
    Means_4_with_names.append([Fourth_obs_contents[i],mean_Val])



General_Means = []

General_Means.append([np.mean(Means_1), np.mean(Means_2), np.mean(Means_3), np.mean(Means_4)])

Std_Dev_Gen_Means = []

Std_Dev_Gen_Means.append([np.std(Means_1),np.std(Means_2),np.std(Means_3),np.std(Means_4)])

#%% Making the Comparison Plots:

indices_1 = pd.read_csv(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Ob1_vs_Ob2_Ob3_Ob4.csv",header=None,sep=" ")
indices_2 = pd.read_csv(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Ob2_vs_Ob3_Ob4.csv", header= None, sep= " ")

sns.set_context("paper")

Means_df = pd.DataFrame()

for i in tqdm(range(len(indices_1))):
    
    
    if indices_1[0][i] != 0 and indices_1[1][i] != 0 and indices_1[2][i] != 0:
        
        fig0, axs0 = plt.subplots(1,3)
        
        #fig.suptitle("Gözlem 1-%d, Gözlem 2-%d, Gözlem3-%d Karşılaştırması" % (indices_1[0][i], indices_1[1][i], indices_1[2][i]))
    
        axs0[0].imshow(Observation_dict["FO"][indices_1[0][i]])
        axs0[0].set_title("İlk Gözlem - indeks: %d" % indices_1[0][i])
    
        axs0[1].imshow(Observation_dict["SO"][indices_1[1][i]])
        axs0[1].set_title("3 Ay sonra - indeks: %d" % indices_1[1][i])
        axs0[1].set_yticks([])
    
        axs0[2].imshow(Observation_dict["TO"][indices_1[2][i]])
        axs0[2].set_title("6 Ay sonra - indeks: %d" % indices_1[2][i])
        axs0[2].set_yticks([])
        
        fig0.savefig(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Result_Report/Obs_1_vs_Others_Plots/FO_%d_SO_%d_TO_%d" % (indices_1[0][i],indices_1[1][i],indices_1[2][i]), dpi= 1000)
        
    
    elif indices_1[0][i] != 0 and indices_1[1][i] != 0 and indices_1[2][i] == 0:
        
        fig1, axs1 = plt.subplots(1,2)
        
        #fig.suptitle("Gözlem 1-%d  Gözlem 2-%d Karşılaştırması" % (indices_1[0][i], indices_1[1][i]))
    
        axs1[0].imshow(Observation_dict["FO"][indices_1[0][i]])
        axs1[0].set_title("İlk Gözlem - indeks: %d" % indices_1[0][i])
    
        axs1[1].imshow(Observation_dict["SO"][indices_1[1][i]])
        axs1[1].set_title("3 Ay sonra - indeks: %d" % indices_1[1][i])
        axs1[1].set_yticks([])
        
        fig1.savefig(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Result_Report/Obs_1_vs_Others_Plots/FO_%d_SO_%d" % (indices_1[0][i],indices_1[1][i]), dpi= 1000)

    else:
        print(i, "This one did not work.")
    
        
    #fig.savefig(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Result_Report/Obs_1_vs_Others_Plots/FO_%d_SO_%d_TO_%d" % (indices_1[0][i],indices_1[1][i],indices_1[2][i]), dpi= 1000)
"""
Improvements:
    
    * Adjust this part in a way that it would only make the required amounts of subplots
    for each of the indices in indices_1 list, After that functionalize it for indices 2.
    Then hand select the images from the folder that you'll be uploading these into.
    
    * Make a saving algorithm for each of these subplots.

"""
#%% Getting the means of ind. images from the image comparison into a dataframe

Means_df = {}


for i in tqdm(range(len(indices_1))):
    
    if indices_1[0][i] != 0 and indices_1[1][i] != 0 and indices_1[2][i] != 0:
        
        Means_df["Images_%d" % i] = {Means_1_with_names[indices_1[0][i]][0]:[Means_1_with_names[indices_1[0][i]][1], indices_1[0][i]], Means_2_with_names[indices_1[1][i]][0]: [Means_2_with_names[indices_1[1][i]][1], indices_1[1][i]], Means_3_with_names[indices_1[2][i]][0]: [Means_3_with_names[indices_1[2][i]][1], indices_1[2][i]]}
    
    elif indices_1[0][i] != 0 and indices_1[1][i] != 0 and indices_1[2][i] == 0:
        
        Means_df["Images_%d" % i] = {Means_1_with_names[indices_1[0][i]][0]: [Means_1_with_names[indices_1[0][i]][1], indices_1[0][i]], Means_2_with_names[indices_1[1][i]][0]:[ Means_2_with_names[indices_1[1][i]][1], indices_1[1][i]]}

    else:
        print(i)


#%% Making the histograms:
    
    
for i in range(len(indices_1)):

    fig, axs = plt.subplots(1,3)
    
    if indices_1[0][i] == 0:
        pass
    else:
        axs[0].hist()
        axs[0].set_title("İlk Gözlem")
    
    if indices_1[1][i] == 0:
        pass
    else:
        axs[1].imshow(Observation_dict["SO"][indices_1[1][i]])
        axs[1].set_title("3 Ay sonra")
        axs[1].set_yticks([])
    
    if indices_1[2][i] == 0:
        print("Make subplots with 2 figures with index: %d" % i)
    else:
        axs[2].imshow(Observation_dict["TO"][indices_1[2][i]])
        axs[2].set_title("6 Ay sonra")
        axs[2].set_yticks([])


#%% Testing Plots:

plt.figure("4. Gözlem", dpi=1000, figsize=(30,25))

fig, axs = plt.subplots()

axs.set_facecolor("lightgray")

image_id = [x for x in range(len(Means_4))]

for i in range(len(Means_4)):
    plt.bar(image_id[i], height= Means_4[i])#(image_id,Means_1)
plt.xticks(np.arange(0,47,3),np.arange(0,47,3))

plt.xlabel("Görüntü Numaraları (i)", fontsize= 12)
plt.ylabel("Ortalama Işık Şiddeti (Cd)", fontsize= 12)

plt.grid(visible=True)

plt.title("4. Gözlem Görüntü Numaraları (i) - Işık Şiddeti (Cd)", fontsize= 14)
plt.savefig(r"C:/Users/1bora/OneDrive/Masaüstü/2209-A/Result_Report/Histogram_Plots/Gözlem_4_Histogram.jpeg", dpi= 1000)

#%% General Mean Testing Plot:
    
fig, ax = plt.subplots(figsize=(15,10))

plt.suptitle("Gözlemlerin Ortalama Işık Şiddeti (Cd)", fontsize= 30)

obs_id = [x for x in range(len(General_Means[0]))]

ax.set_facecolor("lightgray")

for i in range(len(obs_id)):    
    ax.bar(obs_id[i], General_Means[0][i], yerr=Std_Dev_Gen_Means[0][i], align='center', alpha=0.5, ecolor='black', capsize=10)

ax.set_xticks(np.arange(0,4,1),["Gözlem-1", "Gözlem-2", "Gözlem-3", "Gözlem-4"], fontsize= 28)
ax.set_yticks(np.arange(0,111,10), np.arange(0,111,10), fontsize=28)

plt.grid(visible=True)

ax.set_xlabel("Gözlem Numaraları (i)", fontsize= 28)
ax.set_ylabel("Ortalama Işık Şiddeti (Cd)", fontsize= 28)

fig.savefig(r"Gözlemlerin_Ortalama_Işık_Şiddeti.jpeg", dpi= 1000)












