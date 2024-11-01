# algorithms
## Longest Palindrome Subsequence:
**Language:** Python

**Implementation:** Used dynamic programming to fill in table and then backtrack from cell with best length to find palindrome substring output. 


# Seam Carving for Image Compression

This project implements **seam carving**, an intelligent image resizing technique that removes the least noticeable pixels to reduce an image's dimensions with minimal visual impact. Using **dynamic programming** and **gradient-based energy maps**, this algorithm identifies and removes vertical and horizontal seams iteratively, each containing the pixels with the lowest cumulative energy values.

## Key Components

1. **Image to Array Conversion**
   - Converts the input image into an RGB array using the `image_to_array` function for easy processing.

2. **Energy Map Calculation**
   - The `calculate_energy` function applies a Sobel filter to compute the horizontal and vertical gradients of each color channel, creating an energy map based on pixel "disruption" or intensity changes. The resulting map indicates areas of high visual importance, such as edges, that are preserved during compression.

3. **Finding Optimal Seams**
   - Using dynamic programming, the algorithm finds the optimal vertical and horizontal seams:
     - **`vertical_seam`**: Tracks and stores the minimum-energy path from bottom to top for a vertical seam.
     - **`horizontal_seam`**: Tracks and stores the minimum-energy path from left to right for a horizontal seam.

4. **Seam Removal**
   - Each seam is removed iteratively:
     - **`remove_vertical_seam`**: Deletes the lowest-energy path from the image vertically.
     - **`remove_horizontal_seam`**: Deletes the lowest-energy path horizontally.

5. **Compression Execution**
   - The `compression` function performs a specified number of seam removals. For each iteration, it recalculates the energy map and identifies and removes the lowest-energy vertical and horizontal seams, progressively reducing the image's size.

## Example Usage

To compress an image by 20 seams (both vertical and horizontal):
compression(20, "test_image.jpg")
