# Algorithms

## Longest Palindrome Subsequence
**Language:** Python

This algorithm uses **dynamic programming** to find the longest palindromic subsequence in a given string. It fills a table with subsequence lengths and then backtracks to construct the palindrome.

### Key Components

1. **Dynamic Programming Table Construction**
   - The algorithm constructs a DP table where each cell stores the length of the longest palindromic subsequence within a given substring.
   - If two characters at the ends of a substring are equal, they can both be part of the subsequence, and the value is updated accordingly.
   - If the characters are not equal, the algorithm uses the maximum length from subproblems excluding either character, maintaining the longest subsequence found so far.
   - By the end of this process, the top-right cell contains the length of the longest palindromic subsequence for the entire string.

2. **Backtracking to Find the Palindrome**
   - Starting from the cell representing the full substring, the algorithm backtracks through the table to construct the longest palindromic subsequence:
     - If two characters match, they are added to the result and pointers move inward.
     - If they do not match, the algorithm moves toward the cell with the higher value, continuing along the path of the optimal solution.

3. **Constructing the Final Palindrome**
   - The characters collected from backtracking are mirrored to form the complete palindromic subsequence:
     - If the subsequence length is odd, a central character is retained in the middle.
     - If the length is even, the mirrored sequences are combined without a central character.
   
This method efficiently finds the longest palindromic subsequence and reconstructs it, balancing both time complexity and clarity in the output.


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
