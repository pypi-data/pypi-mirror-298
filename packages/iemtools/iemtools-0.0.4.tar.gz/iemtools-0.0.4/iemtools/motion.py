from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
import matplotlib.lines as lines
import numpy as np
import os, sys
import time
import glob
import cv2

def video_to_frames( vid_path , output_path , output_fps ):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        vid_path: src video file path
        output_fps: desired frame rate
    Returns:
        None
    """
    extention = "."+vid_path[-3:]
    folder = os.path.basename( vid_path ).replace( extention , "" )
    output_loc = output_path + folder
    if folder not in glob.glob( output_path ):
        try:
            os.mkdir( output_loc )
            print("[Video to frames: creating output folder ... \t done" )
        except OSError:
            pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture( vid_path )
    # Find the number of frames
    video_length = int( cap.get( cv2.CAP_PROP_FRAME_COUNT ) ) - 1
    cap.set( cv2.CAP_PROP_FPS , output_fps )
    print("[Video to frames]: FPS reset to: \t\t" , output_fps )
    count = 0
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        cv2.imwrite( output_loc + "/%#05d.jpg" % (count+output_fps), frame )
        count += 1
        cap.set( cv2.CAP_PROP_POS_FRAMES , count )
        # If there are no more frames left
        if ( count > ( video_length-1) ):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            break
    print("[Video to frames]: done" )

def colored_line(x, y, c, ax, **lc_kwargs):
    """
    Plot a line with a color specified along the line by a third value.

    It does this by creating a collection of line segments. Each line segment is
    made up of two straight lines each connecting the current (x, y) point to the
    midpoints of the lines connecting the current point with its two neighbors.
    This creates a smooth line with no gaps between the line segments.

    Parameters
    ----------
    x, y : array-like
        The horizontal and vertical coordinates of the data points.
    c : array-like
        The color values, which should be the same size as x and y.
    ax : Axes
        Axis object on which to plot the colored line.
    **lc_kwargs
        Any additional arguments to pass to matplotlib.collections.LineCollection
        constructor. This should not include the array keyword argument because
        that is set to the color argument. If provided, it will be overridden.

    Returns
    -------
    matplotlib.collections.LineCollection
        The generated line collection representing the colored line.
    """
    if "array" in lc_kwargs:
        warnings.warn('The provided "array" keyword argument will be overridden')

    # Default the capstyle to butt so that the line segments smoothly line up
    default_kwargs = {"capstyle": "butt"}
    default_kwargs.update(lc_kwargs)

    # Compute the midpoints of the line segments. Include the first and last points
    # twice so we don't need any special syntax later to handle them.
    x = np.asarray(x)
    y = np.asarray(y)
    x_midpts = np.hstack((x[0], 0.5 * (x[1:] + x[:-1]), x[-1]))
    y_midpts = np.hstack((y[0], 0.5 * (y[1:] + y[:-1]), y[-1]))

    # Determine the start, middle, and end coordinate pair of each line segment.
    # Use the reshape to add an extra dimension so each pair of points is in its
    # own list. Then concatenate them to create:
    # [
    #   [(x1_start, y1_start), (x1_mid, y1_mid), (x1_end, y1_end)],
    #   [(x2_start, y2_start), (x2_mid, y2_mid), (x2_end, y2_end)],
    #   ...
    # ]
    coord_start = np.column_stack((x_midpts[:-1], y_midpts[:-1]))[:, np.newaxis, :]
    coord_mid = np.column_stack((x, y))[:, np.newaxis, :]
    coord_end = np.column_stack((x_midpts[1:], y_midpts[1:]))[:, np.newaxis, :]
    segments = np.concatenate((coord_start, coord_mid, coord_end), axis=1)

    lc = LineCollection(segments, **default_kwargs)
    lc.set_array(c)  # set the colors of each segment

    return ax.add_collection(lc)