import numpy as np 

def return_longest_palindrome(s):
    n = len(s)
    dp = np.zeros((len(s), len(s)), dtype=int)

    # fill in values for each character being a palindrome of length 1 
    for i in range(n):
        dp[i,i] = 1 

    # iterate backwards from (n-2, second to last row), through the first row 0
    for i in range((n-2), -1, -1):
        #iterate j from left to right on each row (goes to n because it needs to go through the last cell)
        for j in range(i + 1, n):
            # If s[i] == s[j], it means these characters can be part of a palindromic subsequence.
            # We then look at the longest palindromic subsequence within the substring s[i+1:j]
            # (which is stored in dp[i+1][j-1]) and add 2 to include s[i] and s[j].
            if s[i] == s[j]:
                dp[i, j] = dp[i+1, j-1] + 2
            # If s[i] and s[j] do not match, we take the maximum of the two subproblems:
            # dp[i][j-1] (excluding s[j]) and dp[i+1][j] (excluding s[i]),
            # keeping the longest possible subsequence found so far.
            else:
                dp[i, j] = max(dp[i, j-1], dp[i+1, j])

    # Now that we have filled in the table the answer will be in the top right of the table
    # the logic behind this is that since we filled it in from bottom left to top right
    # the last sell is dependent on the optimal solution of all its subproblems which is every possible palindrome
    
    j = n - 1 
    i = 0 
    output = []

    # to backtrack we move until we get to the base case of j being equal to i (middle of the palindrome) 
    while i <= j:
        # if we find a match where s[i] == s[j] we append the character to the output
        # then move both pointers inward (i + 1, j - 1)
        if s[i] == s[j]:
            output.append(s[i])
            i += 1 
            j -= 1 
    # if we don't find a match we check the optimal subproblem of the current cell dp[i,j]
    # if the palindrome length is higher at dp[i, j-1] we decrement j 
    # if the palindrome length is higher at dp[i+1, j] we increment i 
        elif dp[i,j-1] > dp[i+1,j]:
            j -= 1
        else:
            i += 1

    # once this loop finishes we will either be halfway through the palindrome (if its even in length)
    # or we will be at the middle character if it is odd
    # if it is even we just add its mirrored self to the output and return this 
    # if it is odd we just mirror everything but the middle char and add that to the output
    if dp[0, n-1] % 2 != 0:
        left = "".join(output)
        right = (left[::-1])[1:] # reverse left and then cut off first letter (middle)
        return (left+right)
    else:
        left = "".join(output)
        right = left[::-1]
        return (left+right)

print(return_longest_palindrome("CHARACTER"))

