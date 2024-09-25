from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
import matplotlib.lines as lines
from skimage import exposure
from skimage import feature
import skimage as ski
import scipy.stats as stat
import numpy as np
import os, sys
import time
import glob


def analyse_sequnce( positions ):
    """
    Takes a Spontaneous alteration sequence and returns the SA index
    """
    alternation_count = 0
    i = 0
    while i < len(positions)-2:
        #check if 3 consecutive positions are all different, i++ if so
        if ( positions[ i ] != positions[ i + 1 ] ) and ( positions[ i ] != positions[ i + 2 ] ) and ( positions[ i + 1 ] != positions[ i + 2 ] ):
            alternation_count += 1
        else: pass
        i += 1
    #do the maths, prepared for div by 0
    try: index = alternation_count / ( len(positions) - 2 )
    except ZeroDivisionError:
        index = 0
    return index , alternation_count


def ymaze_positions( subfolder , fps , rescale_low , rescale_hi , sigma ):
    """
    Spontaneous alternation analysis tool. Returns subfolder path (ie subject name), positions detected, and respective timestamps.
    1) loads .jpg frames from a subfolder, assumes .png masks for Y maze arms are in "/mask" subfolder
    2) makes sure all images are 2D arrays and masks are binary, rescales intensity (low=0, hi=5, sigma=5)
    3) each frame is multiplied by masks and results are compared - largest array sum assumed to be mouse's position
    4) position and respective timestamp (assuming framerate set to fps arg) are saved to list
    """
    #load images and masks
    image_list = []
    mask_list = []
    for frame in glob.glob(subfolder+"*.jpg"):
        im = np.sum( ski.io.imread( frame ) , axis=2 )
        image_list.append( im )
    for file in glob.glob( subfolder + "/masks/*.png" ):
        #load masks and threshold them
        mask_list.append( np.where( np.sum( ski.io.imread( file ) , axis=2) < 1000 , 0 , 1 ) )
    #IMAGE PROCESSING
    sequence = []
    overlaps = []
    timestamps = []
    positions = ["A","B","C","D"]
    position = "x"
    timestamp = 0
    #load one frame from image list
    for frame in image_list:
        #increment timestamp by fps of the video
        timestamp += fps
        #rescale intensity, in our case low=0, hi=5
        s_low, s_hi = np.percentile( frame , ( rescale_low , rescale_hi ) )
        rescaled = exposure.rescale_intensity( frame, in_range=( s_low, s_hi ) )
        #find edges in current rescaled img, in our case sigma=7
        edges = feature.canny( rescaled, sigma=sigma )
        #overlap (1*1) between image and arms' masks, outside mask = 0 ie 1*0 or 0*0
        indices = []        
        for mask in mask_list:
            indices.append( np.sum( edges * mask ) )
        #find greatest overlap, ie highest area ratio
        index_max = sorted( indices )[ 3 ]
        i = 0
        for index in indices:
            if all( [ index == index_max , ( sum(indices)-index_max ) == 0 ] ) == True:
                position = positions[ i ]
            elif indices[3] == index_max:
                position = "D"
            else: pass
            i += 1
        #save position if previous frame different
        if ( len(sequence) == 0 ) or position != sequence[ len(sequence)-1 ]:
            sequence.append( position )
            timestamps.append( timestamp )
        else: pass
    try: sequence.remove("x")
    except: pass
    #remove all Ds and respective timestamps
    respective_tstamp = 0
    for p in sequence:
        if p == "D":
            sequence.remove("D")
            timestamps.remove( timestamps[ respective_tstamp ] )
        else:
            pass
        respective_tstamp += 1
    return subfolder , sequence , timestamps