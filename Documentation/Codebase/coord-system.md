# Coordinate System:

Three types of units are used; [pixels], [SQpixels], [squares]  
    ## Pixels:  
        exact location of clicks  
        defines size of app  
    ## SQpixels:  
        pixel location rounded to top left corner of square  
        calculated by x_sqpx = x_px - x_px%STEP_SIZE  
        exact location of sprites so that they fit into a square  
    ## Squares:  
        made up of STEP_SIZExSTEP_SIZE pixels  
        located at a position defined in SQpixels  
        calculated by SQpixels/STEP_SIZE  
