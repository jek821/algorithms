# Algorithms

---

## Longest Palindrome Subsequence

**Language:** Python

This algorithm uses **dynamic programming** to find the longest palindromic subsequence in a given string. It fills a table with subsequence lengths and then backtracks to construct the palindrome.

### Key Components

1. **Dynamic Programming Table Construction**
   - Constructs a DP table where each cell stores the length of the longest palindromic subsequence within a given substring.
   - If two characters at the ends of a substring are equal, they can both be part of the subsequence, and the value is updated accordingly.
   - If the characters are not equal, the algorithm uses the maximum length from subproblems excluding either character.
   - By the end of this process, the top-right cell contains the length of the longest palindromic subsequence for the entire string.

2. **Backtracking to Find the Palindrome**
   - Starting from the cell representing the full substring, the algorithm backtracks through the table to construct the longest palindromic subsequence:
     - If two characters match, they are added to the result, and pointers move inward.
     - If they do not match, the algorithm moves toward the cell with the higher value.

3. **Constructing the Final Palindrome**
   - The characters collected from backtracking are mirrored to form the complete palindromic subsequence:
     - If the subsequence length is odd, a central character is retained in the middle.
     - If the length is even, the mirrored sequences are combined without a central character.

---

## Seam Carving for Image Compression

**Language:** Python

This project implements **seam carving**, an intelligent image resizing technique that removes the least noticeable pixels to reduce an image's dimensions with minimal visual impact. Using **dynamic programming** and **gradient-based energy maps**, this algorithm identifies and removes vertical and horizontal seams iteratively, each containing the pixels with the lowest cumulative energy values.

### Key Components

1. **Image to Array Conversion**
   - Converts the input image into an RGB array using the `image_to_array` function for easy processing.

2. **Energy Map Calculation**
   - Applies a Sobel filter to compute the horizontal and vertical gradients of each color channel, creating an energy map based on pixel "disruption" or intensity changes. This map indicates areas of high visual importance, such as edges, that are preserved during compression.

3. **Finding Optimal Seams**
   - Using dynamic programming, the algorithm finds the optimal vertical and horizontal seams:
     - **Vertical Seam**: Tracks and stores the minimum-energy path from bottom to top for a vertical seam.
     - **Horizontal Seam**: Tracks and stores the minimum-energy path from left to right for a horizontal seam.

4. **Seam Removal**
   - Each seam is removed iteratively:
     - **Vertical Seam Removal**: Deletes the lowest-energy path from the image vertically.
     - **Horizontal Seam Removal**: Deletes the lowest-energy path horizontally.

5. **Compression Execution**
   - The `compression` function performs a specified number of seam removals. For each iteration, it recalculates the energy map and identifies and removes the lowest-energy vertical and horizontal seams, progressively reducing the image's size.

---

## Inventory Planning Algorithm

**Language:** Python

This algorithm is designed to minimize the cost of meeting demand for inventory over a given period. Using **dynamic programming**, it optimizes production and holding costs by constructing a plan for each month based on demand and inventory.

### Key Components

1. **Cost Functions**
   - **Production Cost**: A per-unit cost applied to each machine produced above the free production allowance.
   - **Holding Cost**: A per-unit cost applied to each machine held in inventory at the end of each month.

2. **Dynamic Programming Table Construction**
   - Constructs a DP table where each cell represents the minimum cost of meeting monthly demand while managing inventory.
   - The algorithm iterates over possible inventory levels and calculates the optimal cost for each month, using a recurrence relation that considers three main cases:
     - **Exact Match**: When inventory and free production meet demand, resulting in no additional cost.
     - **Excess Demand**: When demand exceeds available inventory and free production, incurring additional production costs.
     - **Variable Production**: When demand is less than available resources, allowing the algorithm to explore production levels that minimize holding costs.

3. **Optimal Production Plan**
   - After filling the DP table, the algorithm backtracks to determine the optimal production quantity for each month based on minimum costs.
   - This provides a month-by-month production plan that meets demand at the lowest total cost.

4. **Result Output**
   - The algorithm outputs a production schedule for each month along with the total cost of meeting demand.

This method efficiently balances production and holding costs, providing a cost-effective solution to inventory planning.
