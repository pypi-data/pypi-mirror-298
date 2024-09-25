# IEM CAS toolset
This library contains functions for the analysis of behavioural tests such as Morris Water Maze, offering an open-source non-DeepL/ML alternative to existing proprietary software.
This is an experimental version. Created by Sely Papan.

## Documentation
### Morris package: iemtools.morris
This package includes all functions needed for a Morris Water Maze analysis.

- **find_edges**( image_to_process , rescale_percentile_low , rescale_percentile_hi , sigma )
    - Using *rescale* and *canny* from **scikit-image**, takes a raw image, rescales the intensity using given low and high percentile bounds.
    - Returs an outline of the mouse as an array

- **rescale**( image_to_process , rescale_percentile_low , rescale_percentile_hi )
    - Using scikit-image, function takes a raw image and rescales the intensity using given low and high percentile bounds.
    - Returns a rescaled image as array.

- **platform_mask**( edges , radius_low , radius_hi )
    - Takes a source Morris Water Maze image and finds a circle of radius in the low-to-hi interval in px.
    - *To estimate the interval plot an image of your MWM pool and see approximately how large in px the MWM platform radius is. In our case the interval was low=15, hi=40*
    - Returns a 2D mask array, and the radius of the platform

- **pool_mask**( edges , radius_low , radius_hi )
    - Takes a source Morris Water Maze image and finds a circle of radius in the low-to-hi interval in px.
    - *To estimate the interval plot an image of your MWM pool and see approximately how large in px the MWM platform radius is. In our case the interval was low=300, hi=550*
    - Returns a 2D mask array, the x and y coordinate of its centre and its radius.

- **find_coordinates**( img )
    - Takes a processed image, i.e. an array produced by **find_edges** function. Using scikit-image returns the x , y coordinates of the silhouette's centroid.

- **movement_stats**( list_of_x_coordinates , list_of_y_coordinates , platform_diameter_cm , platform_mask )
    - Define the diameter of the platform in cm; give x, y coordinates of the mouse's trace. Take the platform radius from the platform mask global variable and calculate the px to cm conversion in order to calculate the swimming distance.
    - Returns the distance and duration of the swim.

- **trim_start**( list_of_video_frames , pool_mask , rescale_percentile_low , rescale_percentile_hi )
    - Takes a list of images as arrays, rescales intensity (in our case set to low=60, hi=70), multiplies by the unit matrix created by **pool_mask** function and summs the pixel values of each frame.
    - Finds the first frame, whose sum is within median+-200 units range, which is also followed by frames conforming to this rule. 
    - Returns a trimmed list of video frames.
    - The assumption is that there will be a significant drop in the sum of pixel values once gloved hands with the mouse appear in the frame / pool mask area. To find the frame where hands retract and the mouse is in the water, we look for a frame which has sum of pixels about the median. To start at the point of hand retraction and not hand extention to the pool, the following images must also be within the given limit.


### Y-maze package: iemtools.ymaze
This package includes all functions necessary for Y-maze spontaneous alternation test analysis

- **analyse_sequnce**( positions )
    - Takes a spontaneous alteration sequence created by ymaze_positions (or created manually) and returns the SA index and number of alternations

- **ymaze_positions**( subfolder , fps , rescale_low , rescale_hi , sigma ):
    - Requires jpg frames from vid-to-frame function to be stored in *subfolder* (name=subject_code), and requires manually drawn png masks for Y maze arms in "subfolder/mask" sub-subfolder. Mask is white on black/transparent background. Processes images using *skimage.rescale* funcction (percentiles set by **rescale_low** and **rescale_hi** (low=0, hi=5 in our case), and *skimage.canny*. Each frame is multiplied by masks and results are compared - largest array sum assumed to be mouse's position.
    - Returns lists of positions, respective timestamps assuming framerate=fps

    
### Motion package: iemtools.motion
This package includes functions for video-to-frames conversion and for movement visualisation

- **video_to_frames**( vid_path , output_path , output_fps )
    - Takes video's path (including filename), saves jpg frames (at desired *output_fps*) in a dedicated subfolder (derived from filename) in *output_path* location.

- **colored_line**(x, y, c, ax, **lc_kwargs)
    - From **matplotlib**:
    >Plot a line with a color specified along the line by a third value. It does this by creating a collection of line segments. Each line segment ismade up of two straight lines each connecting the current (x, y) point to the midpoints of the lines connecting the current point with its two neighbors. This creates a smooth line with no gaps between the line segments.
    >Parameters:
    >x, y : array-like - The horizontal and vertical coordinates of the data points.
    >c : array-like - The color values, which should be the same size as x and y.
    >ax : Axes - Axis object on which to plot the colored line.
    >**lc_kwargs - Any additional arguments to pass to matplotlib.collections.LineCollection constructor
    - Returns *matplotlib.collections.LineCollection* - the generated line collection representing the colored line.