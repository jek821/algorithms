import numpy as np
from scipy.ndimage import sobel
from PIL import Image

def calculate_energy(image_path):
    # Load image
    img = Image.open(image_path)
    img = img.convert("RGB")
    img_array = np.array(img, dtype=float)

    # Calculate the Sobel gradient for each channel
    energy_map = np.zeros((img_array.shape[0], img_array.shape[1]))

    for channel in range(3):  # R, G, B channels
        sobel_x = sobel(img_array[:, :, channel], axis=0)  # Horizontal gradient
        sobel_y = sobel(img_array[:, :, channel], axis=1)  # Vertical gradient
        energy_map += np.hypot(sobel_x, sobel_y)  # Combine gradients

    return energy_map

# print(np.shape(calculate_energy("test_image.jpg")))

def find_optimal_seam(array):
    # make np matrix of all zeros that is the same dimensions as the energy map of the image
    i = np.shape(array)[0] # height of the image
    j = np.shape(array)[1] # width of the image
    dp = np.zeros((i, j))

    # the bottom row of the image can just be those cell's disruption measurements
    for column in range(j):
        dp[i-1][column] = array[i-1][column]
    
    # Now we can move from the second to last row (left to right), up to the top of the dp matrix
    # filling in the potential seam values, we can then get the minimum total disruption in the top row
    # and backtrack from this cell to find the optimal seam path 
    for row in range((i-2), -1, -1):
        for column in range(j):
            #if at the left edge of the image we can only go right-down or straight-down
            if column == 0:
                minimum_disruption = min(dp[row+1,column],dp[row+1,column+1])
            #if at the right edge of the image we can only go left-down or straight-down
            if column == (j-1):
                minimum_disruption = min(dp[row+1,column],dp[row+1,column-1])
            else:
                # otherwise we get the minimum of all three possible directions 
                minimum_disruption = min(dp[row+1,column], dp[row+1,column-1], dp[row+1,column+1])
            # now we put the current cells disruption + the min previous cell disruption into the current cell
            dp[row][column] = (minimum_disruption + array[row][column])
    
    # now that the dp matrix is filled in we can find the minimum in the first row
    # this will give us the optimal starting point to backtrack from
    best_start = [0,0]
    for pixel in range(j):
        if best_start == [0,0]:
            best_start[1] = pixel
        else:
            if dp[0,pixel] < dp[0, best_start[1]]:
                best_start[1] = pixel

    # now best_start holds the best cell to start from so we can backtrack from here 
    # while backtracking we will store all of the cell locations in an array
    # this array can then get returned and passed into a remove seam function which will delete those cells in the image
    # and save a compressed copy of the original

    # Initialize variables for backtracking
    column = best_start[1]
    seam_cells = [(0, column)]  # Start at the top row with the best starting column

    # Backtrack downwards from top to bottom
    for row in range(1, i):
        # Check three possible moves and find the column with the minimum disruption
        if column == 0:  # Left edge
            # Only consider down and down-right
            if dp[row, column] > dp[row, column + 1]:
                column += 1
        elif column == j - 1:  # Right edge
            # Only consider down and down-left
            if dp[row, column] > dp[row, column - 1]:
                column -= 1
        else:
            # General case: choose the minimum of down-left, down, and down-right
            if dp[row, column - 1] <= dp[row, column] and dp[row, column - 1] <= dp[row, column + 1]:
                column -= 1
            elif dp[row, column + 1] <= dp[row, column] and dp[row, column + 1] <= dp[row, column - 1]:
                column += 1

        # Append the selected cell to seam_cells
        seam_cells.append((row, column))

    return seam_cells


def remove_seam(image_path, seam_cells):
    # Load image and convert to NumPy array
    img = Image.open(image_path)
    img_array = np.array(img)

    # Create a new array with one less column to store the image with the seam removed
    new_img_array = np.zeros((img_array.shape[0], img_array.shape[1] - 1, img_array.shape[2]), dtype=img_array.dtype)

    # Iterate over each row, removing the pixel in the specified column for that row
    for row, col in seam_cells:
        # Copy all pixels up to the seam pixel
        new_img_array[row, :col] = img_array[row, :col]
        # Skip the seam pixel and copy the rest of the row
        new_img_array[row, col:] = img_array[row, col + 1:]

    # Convert modified array back to an image and save it
    result_img = Image.fromarray(new_img_array)
    result_img.save("compressed_image.jpg")


for i in range(10):
    remove_seam("compressed_image.jpg", find_optimal_seam(calculate_energy("compressed_image.jpg")))
