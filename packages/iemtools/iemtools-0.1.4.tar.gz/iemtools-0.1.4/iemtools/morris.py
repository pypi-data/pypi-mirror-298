from skimage.measure import label, regionprops, regionprops_table
from skimage.feature import canny
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage import filters
from skimage import exposure
from skimage import feature
from skimage.color import rgb2gray
from skimage.draw import disk, polygon
import skimage as ski
import scipy.stats as stat
import numpy as np
import os, sys
import time
import glob


def find_edges( image_to_process , rescale_percentile_low , rescale_percentile_hi , sigma ):
    """
    1) take raw image, rescale at low and high bounds
    2) return edges
    """
    s_low , s_hi = np.percentile( image_to_process , ( rescale_percentile_low , rescale_percentile_hi ) )
    rescaled = exposure.rescale_intensity( image_to_process , in_range=( s_low , s_hi ) )
    return canny( rescaled , sigma=sigma )


def rescale( image_to_process , rescale_percentile_low , rescale_percentile_hi ):
    """
    1) take raw image, rescale at low and high bounds
    """
    s_low , s_hi = np.percentile( image_to_process , ( rescale_percentile_low , rescale_percentile_hi ) ) 
    return exposure.rescale_intensity( image_to_process , in_range=( s_low , s_hi ) )


def platform_mask( edges , radius_low , radius_hi ):
    """
    1) take a source Morris Water Maze image and find a circle of radius in the low-to-hi interval px
    --> to estimate the interval plot an image of your MWM pool and see approximately how large in px the MWM platform radius is
    --> in our case the interval was low=15, hi=40
    2) return a 2D mask array
    """
    # Detect two radii
    hough_radii = np.arange( radius_low , radius_hi , 1 )
    hough_res = hough_circle( edges , hough_radii )
    # Select the most prominent 3 circles
    accums , cx , cy , radii = hough_circle_peaks( hough_res , hough_radii , total_num_peaks=1 )
    cx = sorted( cx )
    cy = sorted( cy )
    radii = sorted( radii )
    mask = np.zeros( ( len(edges) , len(edges[0]) , 3 ) )
    rr , cc = disk( ( cy[ 0 ] , cx[ 0 ] ) , radii[ 0 ] , shape=mask.shape )
    mask[ rr , cc ] = ( 1 , 1 , 0 )
    return rgb2gray(mask) , radii[0]


def pool_mask( edges , radius_low , radius_hi ):
    """
    1) take a source Morris Water Maze image and find a circle of radius in the low-to-hi interval px
    --> to estimate the interval plot an image of your MWM pool and see approximately how large in px the MWM platform radius is
    --> in our case the interval was low=300, hi=550
    2) return a 2D mask array
    """
    # Detect two radii
    hough_radii = np.arange( radius_low , radius_hi , 50 )
    hough_res = hough_circle( edges , hough_radii )
    # Select the most prominent 3 circles
    accums , cx , cy , radii = hough_circle_peaks( hough_res , hough_radii , total_num_peaks=1 )
    cx = sorted( cx )
    cy = sorted( cy )
    radii = sorted( radii )
    mask = np.zeros( ( len(edges) , len(edges[0]) , 3 ) )
    rr , cc = disk( ( cy[ 0 ] , cx[ 0 ] ) , radii[ 0 ] , shape=mask.shape )
    mask[ rr , cc ] = ( 1 , 1 , 0 )
    return rgb2gray(mask) , radii[0] , cx[0] , cy[0]


def find_coordinates( img ):
        """
        take source image, find coords of the prominent edges object
        """
        label_img = label( img )
        regions = regionprops( label_img )
        for props in regions:
            centroid_y , centroid_x = props.centroid
        return centroid_x , centroid_y


def movement_stats( list_of_x_coordinates , list_of_y_coordinates , platform_diameter_cm , platform_radius , fps ):
    """
    1) define the diameter of the platform in cm; give x, y coordinates of the mouse's trace
    3) take the platform radius from the platform mask global variable and calculate the px to cm conversion
    2) return the distance and duration of the swim
    """
    platform_diameter_px = platform_radius * 2 #because d=2r
    distance_index = platform_diameter_cm / platform_diameter_px
    i = 0
    distance = 0
    while i < len(list_of_x_coordinates)-1:
        a = ( list_of_x_coordinates[ i ] - list_of_x_coordinates[ i + 1 ] )
        b = ( list_of_y_coordinates[ i ] - list_of_y_coordinates[ i + 1 ] )
        distance += np.sqrt( a**2 + b**2 )
        i += 1
    distance_cm = np.round( distance * distance_index , 0 ).astype(int)
    print( distance_cm , "cm swum in" , len(list_of_x_coordinates )/fps , "s")
    return distance_cm , len(list_of_x_coordinates )/fps


def trim_start( list_of_video_frames , pool_mask , rescale_percentile_low , rescale_percentile_hi ):
    """
    1) take list of water maze frames, rescale intensity (in our case set to low=60, hi=70)
    2) take sums of the pixel values in each frame (masked for pool)
    3) find global minimum - assuming that's the maximum overlap between hands in gloves and the pool
    4) find the 1st value above the median of the list between the minimum and the list end - assuming that's where the hands are fully retracted
    5) return trimmed list 
    """
    print("[Video trimmer]: WARNING - for short swims manual selection of frames is advised")

    vals = []
    for img in list_of_video_frames:
        current_frame = img * pool_mask
        current_rescaled = rescale( current_frame , 60 , 70 )
        vals.append( np.sum(current_rescaled) )
    print("[Video trimmer]: rescaling frames ... \t\t done")

    if len(vals) <= 700:
        counts, bins = np.histogram(vals,bins=10)
    elif len(vals) > 400:
        counts, bins = np.histogram(vals[ : np.round( len(vals)*0.5 , 0 ).astype(int) ],bins=10)
    else: pass    
    start = ""
    start_index = 0
    while ( start != "found" ) and ( start_index < len(vals)-1 ):
        lower_bound = np.round( bins[ np.argmax(counts)-2 ] , 0 )
        upper_bound = np.round( np.mean( [ bins[ np.argmax(counts)+2 ] , bins[ np.argmax(counts)+3 ] ] ) , 0 )
        reasonable_range = np.arange( lower_bound , upper_bound )
        current_val = np.round( vals[ start_index ] , 0 )
        consecutive_vals = np.round( vals[ start_index : start_index+30 ] , 0 )
        bool_list = []
        for val in consecutive_vals:
            if val in reasonable_range:
                bool_list.append(True)
            else: bool_list.append(False)
        if all(bool_list) == True:
            start = "found"
            trimmed_list = list_of_video_frames[ start_index : ]
        else: start_index += 1
    print("[Video trimmer]: \n\t\t trim start sum of pixels:\t" , current_val ,
          "\n\t\t median pixel sum:\t\t" , np.round( np.median(vals) , 0 ) ,
          "\n\t\t video trimmed at frame:\t" , start_index , "; is" , len(trimmed_list) , "frames long")
    return trimmed_list