import numpy as np
from scipy.ndimage import sobel
from PIL import Image

def image_to_array(image_path):
    # Open the image and convert it to an array
    img = Image.open(image_path)
    img_array = np.array(img)
    return img_array

def calculate_energy(img_array):
    # Calculate the energy map by finding the Sobel gradient for each RGB channel
    energy_map = np.zeros((img_array.shape[0], img_array.shape[1]))

    for channel in range(3):  # For R, G, B channels
        sobel_x = sobel(img_array[:, :, channel], axis=0)  # Horizontal gradient
        sobel_y = sobel(img_array[:, :, channel], axis=1)  # Vertical gradient
        energy_map += np.hypot(sobel_x, sobel_y)  # Combine gradients for energy map
    return energy_map

def vertical_seam(array):
    # Initialize a DP array to store the minimum energy cost to reach each pixel
    i, j = array.shape
    dp = np.zeros((i, j))
    # Set the bottom row of the DP array to the energy map's bottom row values
    dp[-1, :] = array[-1, :]
    # Fill DP table from bottom to top to find minimum seam cost
    for row in range(i-2, -1, -1):
        for col in range(j):
            # Calculate minimum energy for each possible move
            min_prev = dp[row + 1, col] #direct up will always be possible
            if col > 0:
                min_prev = min(min_prev, dp[row + 1, col - 1]) #if not at left edge then check for left-down case vs current min
            if col < j - 1:    
                min_prev = min(min_prev, dp[row + 1, col + 1]) #if not at right edge then check for right-down case vs current min
           #add the min path we found to the distruction value at the current cell and add it to the current dp matrix cell (total destruction up to this point)
            dp[row, col] = array[row, col] + min_prev 
    # Backtrack to find the optimal seam path
    seam_cells = []
    col = np.argmin(dp[0,:])  # Starting point with minimum energy in the top row
    seam_cells.append((0, col))                
    # For each row, track the path by moving to the minimum energy column in the next row
    for row in range(1,i):
        if col == j-1:
            if dp[row,col-1] < dp[row,col]:
                col-=1
        elif col == 0:
            if dp[row,col+1] < dp[row,col]:
                col+=1
        elif col > 0 and col < j-1:
            if dp[row,col-1] < dp[row,col] and dp[row,col-1] < dp[row,col+1]:
                col-=1
            elif dp[row,col+1] < dp[row,col] and dp[row,col+1] < dp[row,col-1]:
                col+=1
        seam_cells.append([row,col])
    return seam_cells

def horizontal_seam(array):
    i, j = array.shape
    dp = np.zeros((i,j))
    # set left side of dp matrix to energy map's left side values (j = 0)
    dp[ : , 0] = array[ : , 0]
    # Now fill in the DP matrix from left to right
    for column in range(1, j - 1):
        #for each column (left to right, skipping previously filled in first), go through each row, top to bottom
        for row in range(0, i-1):
            #we can always go straight to the right so lets set min_prev to that first
            min_prev = dp[row,column+1] 
            #check if not at top of table (then we can go right-up)
            if row > 0: 
                min_prev = min(min_prev, dp[row-1,column+1])
            #check if not at bottom of table (then we can go right-down)
            if row < i - 1:
                min_prev = min(min_prev, dp[row+1,column+1])
            #now add the min prev to the distruction at the current pixel and put this in the curr cell of the dp matrix
            #this is the total destruction up to this cell
            dp[row,column] = array[row, column] + min_prev
    #once the matrix is filled in, the ideal starting pixel will be the cell with the smallest value in the last column
    start_row = np.argmin(dp[:, j-1])
    #lets make an array to keep track of ideal seam's pixels to delete later
    seam_cells = []
    # put the optimal start_cell in the seam_cell array 
    seam_cells.append([start_row, j-1])
    #move from second to last column down to the first following ideal path from start pixel
    for col in range(j-2,0,-1):
        if row == 0:
            if dp[row+1,col] < dp[row,col]:
                row+=1
        elif row==i-1:
            if dp[row-1,col] < dp[row,col]:
                row-=1
        elif row > 0 and row < i-1:
            if dp[row-1,col] < dp[row,col] and dp[row-1,col] < dp[row+1,col]:
                row-=1
            elif dp[row+1,col] < dp[row,col] and dp[row+1, col] < dp[row-1,col]:
                row+=1
        seam_cells.append([row,col])
    return seam_cells

def remove_vertical_seam(img_array, seam_cells):
    # Create a new array with one less column for the compressed image
    new_img_array = np.zeros((img_array.shape[0], img_array.shape[1] - 1, img_array.shape[2]), dtype=img_array.dtype)
    # For each row, remove the pixel in the seam
    for row, col in seam_cells:
        new_img_array[row, :col] = img_array[row, :col]  # Copy all pixels up to seam
        new_img_array[row, col:] = img_array[row, col + 1:]  # Skip seam and copy the rest
    return new_img_array

def remove_horizontal_seam(img_array, seam_cells):
    # Create new array with one less row for the compressed image
    new_img_array = np.zeros((img_array.shape[0] - 1, img_array.shape[1], img_array.shape[2]), dtype=img_array.dtype)
    # for each column, remove the pixel in the seam
    for row, col in seam_cells:
        new_img_array[:row, col] = img_array[:row, col] #copy all pixels up to seam
        new_img_array[row:, col] = img_array[row + 1:, col] #skip seam cell and copy the rest
    return new_img_array

def compression(num_reductions, img_path):
    # Convert image to array and apply seam carving for the specified number of reductions
    img_array = image_to_array(img_path)
    for i in range(num_reductions):
        # remove vertical seam
        energy_map = calculate_energy(img_array)  # Generate energy map
        seam = vertical_seam(energy_map)  # Find optimal seam based on energy map
        img_array = remove_vertical_seam(img_array, seam)  # Remove the optimal seam
        # now remove horizontal seam
        energy_map = calculate_energy(img_array)
        seam = horizontal_seam(energy_map)
        img_array = remove_horizontal_seam(img_array, seam)
        print(str(i+1) + "/" + str(num_reductions))
    # Save the compressed image after all seams are removed
    result_img = Image.fromarray(img_array)
    result_img.save("compressed_image.jpg")



compression(20, "test_image.jpg")
