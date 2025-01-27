import numpy as np
from scipy.ndimage import sobel
from PIL import Image
from typing import Tuple, Union, Literal
from pathlib import Path

def calculate_energy(img_array: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    """Calculate energy map with improved gradient calculation and color coherence"""
    if img_array.ndim != 3:
        raise ValueError("Input image must have 3 dimensions (height, width, channels)")
        
    height, width = img_array.shape[:2]
    energy_map = np.zeros((height, width))
    
    # RGB to grayscale weights (human perception)
    weights = np.array([0.299, 0.587, 0.114])
    
    for y in range(1, height):
        for x in range(width):
            if x == 0:
                left_cost = float('inf')
            else:
                left_cost = np.sum(np.abs(img_array[y, x] - img_array[y, x-1])) + \
                           np.sum(np.abs(img_array[y-1, x] - img_array[y, x-1]))
                
            if x == width-1:
                right_cost = float('inf')
            else:
                right_cost = np.sum(np.abs(img_array[y, x] - img_array[y, x+1])) + \
                            np.sum(np.abs(img_array[y-1, x] - img_array[y, x+1]))
                
            straight_cost = np.sum(np.abs(img_array[y-1, x] - img_array[y, x]))
            
            energy_map[y, x] = min(left_cost, straight_cost, right_cost)
    
    for channel, weight in enumerate(weights):
        sobel_x = sobel(img_array[:, :, channel], axis=0)
        sobel_y = sobel(img_array[:, :, channel], axis=1)
        energy_map += weight * np.hypot(sobel_x, sobel_y)
    
    for channel in range(3):
        grad_x = np.gradient(img_array[:, :, channel], axis=1)
        grad_y = np.gradient(img_array[:, :, channel], axis=0)
        color_coherence = 0.02 * (np.abs(grad_x) + np.abs(grad_y))
        energy_map += color_coherence
    
    energy_range = np.max(energy_map) - np.min(energy_map)
    if energy_range > eps:
        energy_map = (energy_map - np.min(energy_map)) / energy_range
    else:
        energy_map = np.zeros_like(energy_map)
    
    return energy_map

def find_vertical_seam(energy_map: np.ndarray) -> np.ndarray:
    """Find vertical seam with improved handling of flat regions and edges"""
    height, width = energy_map.shape
    dp = np.copy(energy_map)
    backtrack = np.zeros((height, width), dtype=np.int32)
    
    dp += np.random.random(dp.shape) * 1e-5
    
    for i in range(1, height):
        for j in range(width):
            if j == 0:
                neighbors = dp[i-1, j:j+2]
                min_idx = np.argmin(neighbors)
                backtrack[i, j] = min_idx
                dp[i, j] += neighbors[min_idx]
            elif j == width-1:
                neighbors = dp[i-1, j-1:j+1]
                min_idx = np.argmin(neighbors)
                backtrack[i, j] = min_idx - 1
                dp[i, j] += neighbors[min_idx]
            else:
                neighbors = dp[i-1, j-1:j+2]
                min_idx = np.argmin(neighbors)
                backtrack[i, j] = min_idx - 1
                dp[i, j] += neighbors[min_idx]
    
    seam = np.zeros(height, dtype=np.int32)
    seam[-1] = np.argmin(dp[-1])
    
    for i in range(height - 2, -1, -1):
        offset = backtrack[i + 1, seam[i + 1]]
        seam[i] = np.clip(seam[i + 1] + offset, 0, width - 1)

    
    return seam

def remove_seam(img_array: np.ndarray, seam: np.ndarray, axis: int = 1) -> np.ndarray:
    """Remove seam with color blending at removal points."""
    if axis not in (0, 1):
        raise ValueError("Axis must be 0 (horizontal) or 1 (vertical)")
    
    height, width, channels = img_array.shape
    
    if axis == 1:  # Vertical seam
        new_array = np.zeros((height, width-1, channels), dtype=img_array.dtype)
        
        for i in range(height):
            # Blend colors if the seam pixel isn't at the edge
            if 0 < seam[i] < width - 1:
                left_color = img_array[i, seam[i]-1].astype(float)
                right_color = img_array[i, seam[i]+1].astype(float)
                blend_color = ((left_color + right_color) / 2).astype(img_array.dtype)
            else:
                blend_color = img_array[i, seam[i]].astype(img_array.dtype)
            
            # Copy pixels left of the seam
            new_array[i, :seam[i]] = img_array[i, :seam[i]]
            # Place the blended color at the seam position
            if seam[i] < width - 1:
                new_array[i, seam[i]-1] = blend_color
            # Copy pixels right of the seam
            new_array[i, seam[i]:] = img_array[i, seam[i]+1:]
        
        return new_array
    
    else:  # Horizontal seam
        return remove_seam(img_array.transpose(1, 0, 2), seam, axis=1).transpose(1, 0, 2)


def compress_image(
    image_path: Union[str, Path],
    num_seams: int,
    direction: Literal['both', 'vertical', 'horizontal'] = 'both',
    min_dimension: int = 2
) -> Image.Image:
    """Compress image without logging"""
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img = np.array(Image.open(image_path))
    original_aspect = img.shape[1] / img.shape[0]
    
    if direction == 'both':
        aspect_weight = min(max(original_aspect - 1.0, 0), 1)
        v_seams = int(num_seams * (0.5 + 0.2 * aspect_weight))
        h_seams = num_seams - v_seams
    elif direction == 'vertical':
        v_seams, h_seams = num_seams, 0
    else:
        v_seams, h_seams = 0, num_seams
    
    recalc_interval = 10
    
    for i in range(v_seams):
        if img.shape[1] <= min_dimension:
            break
        
        if i % recalc_interval == 0:
            energy_map = calculate_energy(img)
        
        seam = find_vertical_seam(energy_map)
        img = remove_seam(img, seam, axis=1)
    
    for i in range(h_seams):
        if img.shape[0] <= min_dimension:
            break
        
        if i % recalc_interval == 0:
            energy_map = calculate_energy(img)
        
        seam = find_vertical_seam(energy_map.T)
        img = remove_seam(img, seam, axis=0)
    
    return Image.fromarray(img)

if __name__ == "__main__":
    input_path = "dory.png"
    output_path = "compressed_output.jpg"
    
    try:
        image = compress_image(
            image_path=input_path,
            num_seams=120,
            direction='both',
            min_dimension=2
        )
        image.save(output_path, quality=95)
        print(f"Successfully saved compressed image to {output_path}")
    except Exception as e:
        print(f"Error during image compression: {str(e)}")
