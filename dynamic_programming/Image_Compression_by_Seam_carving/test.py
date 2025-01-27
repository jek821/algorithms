import numpy as np
from scipy.ndimage import sobel
from PIL import Image

def calculate_energy(img_array):
    """Calculate energy map with improved gradient calculation and normalization"""
    energy_map = np.zeros((img_array.shape[0], img_array.shape[1]))
    weights = [0.299, 0.587, 0.114]
    
    for channel, weight in enumerate(weights):
        sobel_x = sobel(img_array[:, :, channel], axis=0)
        sobel_y = sobel(img_array[:, :, channel], axis=1)
        energy_map += weight * np.hypot(sobel_x, sobel_y)
    
    energy_map = (energy_map - np.min(energy_map)) / (np.max(energy_map) - np.min(energy_map))
    
    for channel in range(3):
        grad_x = np.gradient(img_array[:, :, channel], axis=1)
        grad_y = np.gradient(img_array[:, :, channel], axis=0)
        energy_map += 0.05 * (np.abs(grad_x) + np.abs(grad_y))
    
    return energy_map

def find_vertical_seam(energy_map):
    """Find vertical seam with bounds-checked backtracking"""
    height, width = energy_map.shape
    dp = np.copy(energy_map)
    backtrack = np.zeros((height, width), dtype=np.int32)
    
    # Fill dp table
    for i in range(1, height):
        for j in range(width):
            # Get the possible previous positions
            prev_cols = slice(max(0, j-1), min(width, j+2))
            min_idx = np.argmin(dp[i-1, prev_cols])
            min_energy = dp[i-1, prev_cols][min_idx]
            
            # Store the relative offset (-1, 0, or 1) in backtrack
            backtrack[i, j] = min_idx - (1 if j > 0 else 0)
            dp[i, j] += min_energy
    
    # Backtrack to find optimal seam
    seam = np.zeros(height, dtype=np.int32)
    seam[-1] = np.argmin(dp[-1])
    
    for i in range(height-2, -1, -1):
        offset = backtrack[i+1, seam[i+1]]
        seam[i] = min(max(seam[i+1] + offset, 0), width-1)
    
    return seam

def remove_seam(img_array, seam, axis=1):
    """Remove seam with proper array handling"""
    if axis == 1:  # vertical seam
        height, width, channels = img_array.shape
        new_array = np.zeros((height, width-1, channels), dtype=img_array.dtype)
        
        for i in range(height):
            new_array[i, :seam[i]] = img_array[i, :seam[i]]
            new_array[i, seam[i]:] = img_array[i, seam[i]+1:]
            
        return new_array
    else:  # horizontal seam
        return remove_seam(img_array.transpose(1, 0, 2), seam, 1).transpose(1, 0, 2)

def compress_image(image_path, num_seams, direction='both'):
    """Main compression function with improved seam removal strategy"""
    img = np.array(Image.open(image_path))
    
    if direction == 'both':
        v_seams = h_seams = num_seams // 2
    elif direction == 'vertical':
        v_seams, h_seams = num_seams, 0
    else:
        v_seams, h_seams = 0, num_seams
    
    # Remove vertical seams
    for i in range(v_seams):
        if img.shape[1] <= 2:  # Check if image is too narrow
            print(f"Stopping vertical compression: image width ({img.shape[1]}) too small")
            break
            
        energy_map = calculate_energy(img)
        seam = find_vertical_seam(energy_map)
        img = remove_seam(img, seam, axis=1)
        if (i + 1) % 10 == 0:
            print(f"Removed {i + 1}/{v_seams} vertical seams")
            
    # Remove horizontal seams
    for i in range(h_seams):
        if img.shape[0] <= 2:  # Check if image is too tall
            print(f"Stopping horizontal compression: image height ({img.shape[0]}) too small")
            break
            
        energy_map = calculate_energy(img)
        seam = find_vertical_seam(energy_map.T)
        img = remove_seam(img, seam, axis=0)
        if (i + 1) % 10 == 0:
            print(f"Removed {i + 1}/{h_seams} horizontal seams")
    
    return Image.fromarray(img)

# Example usage
image = compress_image("dory.png", 120, direction='both')
image.save("compressed_output.jpg")