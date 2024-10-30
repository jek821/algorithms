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

def find_optimal_seam(array):
    # Initialize a DP array to store the minimum energy cost to reach each pixel
    i, j = array.shape
    dp = np.zeros((i, j))
    # Set the bottom row of the DP array to the energy map's bottom row values
    dp[-1, :] = array[-1, :]
    # Fill DP table from bottom to top to find minimum seam cost
    for row in range(i-2, -1, -1):
        for col in range(j):
            # Calculate minimum energy for each possible move
            min_prev = dp[row + 1, col]
            if col > 0:
                min_prev = min(min_prev, dp[row + 1, col - 1])
            if col < j - 1:
                min_prev = min(min_prev, dp[row + 1, col + 1])
            dp[row, col] = array[row, col] + min_prev
    # Backtrack to find the optimal seam path
    seam_cells = []
    col = np.argmin(dp[0])  # Starting point with minimum energy in the top row
    seam_cells.append((0, col))
    # For each row, track the path by moving to the minimum energy column in the next row
    for row in range(1, i):
        if col > 0 and dp[row, col - 1] <= dp[row, col] and (col == j - 1 or dp[row, col - 1] <= dp[row, col + 1]):
            col -= 1
        elif col < j - 1 and dp[row, col + 1] <= dp[row, col] and dp[row, col + 1] <= dp[row, col - 1]:
            col += 1
        seam_cells.append((row, col))
    return seam_cells

def remove_seam(img_array, seam_cells):
    # Create a new array with one less column for the compressed image
    new_img_array = np.zeros((img_array.shape[0], img_array.shape[1] - 1, img_array.shape[2]), dtype=img_array.dtype)
    # For each row, remove the pixel in the seam
    for row, col in seam_cells:
        new_img_array[row, :col] = img_array[row, :col]  # Copy all pixels up to seam
        new_img_array[row, col:] = img_array[row, col + 1:]  # Skip seam and copy the rest
    return new_img_array

def compression(num_reductions, img_path):
    # Convert image to array and apply seam carving for the specified number of reductions
    img_array = image_to_array(img_path)
    for i in range(num_reductions):
        energy_map = calculate_energy(img_array)  # Generate energy map
        seam = find_optimal_seam(energy_map)  # Find optimal seam based on energy map
        img_array = remove_seam(img_array, seam)  # Remove the optimal seam
        print(str(i+1) + "/" + str(num_reductions))
    # Save the compressed image after all seams are removed
    result_img = Image.fromarray(img_array)
    result_img.save("compressed_image.jpg")



compression(50, "test_image.jpg")
