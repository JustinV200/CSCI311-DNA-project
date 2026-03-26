class algorithms():
    def __init__(self):
        pass

    @staticmethod
    def edit_distance(s, t):
        # Edit Distance (Levenshtein Distance) calculates the minimum number of
        # single-character operations (insert, delete, substitute) needed to
        # transform string s into string t. A lower score means the strings are
        # more similar.

        # Get the lengths of both input sequences
        m, n = len(s), len(t)

        # Create a 2D table (matrix) with (m+1) rows and (n+1) columns.
        # The extra row and column represent the empty string base cases.
        # dp[i][j] will hold the edit distance between the first i characters
        # of s and the first j characters of t.
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill in every cell of the table row by row
        for i in range(m + 1):
            for j in range(n + 1):

                # BASE CASE: If s is empty (i == 0), the only option is to
                # insert all j characters of t, so the cost is j.
                if i == 0: dp[i][j] = j

                # BASE CASE: If t is empty (j == 0), the only option is to
                # delete all i characters of s, so the cost is i.
                elif j == 0: dp[i][j] = i

                # If the current characters match (s[i-1] == t[j-1]), no
                # operation is needed for this pair. Carry forward the edit
                # distance from the previous characters (diagonal cell).
                elif s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1]

                # If the characters don't match, we pick the cheapest of three
                # possible operations and add 1 for the cost of that operation:
                #   dp[i][j-1]   = INSERT a character into s to match t[j-1]
                #   dp[i-1][j]   = DELETE s[i-1] from s
                #   dp[i-1][j-1] = SUBSTITUTE s[i-1] with t[j-1]
                else: dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

        # The bottom-right cell contains the final answer: the minimum edit
        # distance between the full strings s and t.
        return dp[m][n]

    @staticmethod
    def longest_common_subsequence(s, t):
        # Longest Common Subsequence (LCS) finds the length of the longest
        # sequence of characters that appear in both s and t in the same
        # relative order, but not necessarily contiguously. Characters can be
        # spread apart with gaps between them.

        # Get the lengths of both input sequences
        m, n = len(s), len(t)

        # Create a 2D table with (m+1) rows and (n+1) columns.
        # dp[i][j] will hold the length of the LCS between the first i
        # characters of s and the first j characters of t.
        # Row 0 and column 0 are implicitly 0 (comparing anything against an
        # empty string yields an LCS of length 0).
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Iterate through every character pair, starting from (1,1) since
        # the 0th row/column are the empty-string base cases (already 0).
        for i in range(1, m + 1):
            for j in range(1, n + 1):

                # If the current characters match, this character extends the
                # LCS. Take the LCS length without these two characters
                # (diagonal cell dp[i-1][j-1]) and add 1.
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1

                # If the characters don't match, we can't extend the LCS here.
                # Take the better of two options:
                #   dp[i-1][j] = skip the current character of s
                #   dp[i][j-1] = skip the current character of t
                # This is what allows gaps in the subsequence.
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        # The bottom-right cell holds the length of the LCS of the full
        # strings s and t.
        return dp[m][n]

    @staticmethod
    def longest_common_substring(s, t):
        # Longest Common Substring finds the length of the longest CONTIGUOUS
        # block of characters that appears identically in both s and t.
        # Unlike subsequence, there can be no gaps — the matching characters
        # must be consecutive in both strings.

        # Get the lengths of both input sequences
        m, n = len(s), len(t)

        # Create a 2D table with (m+1) rows and (n+1) columns.
        # dp[i][j] will hold the length of the longest common substring that
        # ENDS at s[i-1] and t[j-1]. This is different from LCS — here each
        # cell only tracks substrings ending at that specific position.
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Track the global maximum substring length found so far
        longest = 0

        # Iterate through every character pair
        for i in range(1, m + 1):
            for j in range(1, n + 1):

                # If the current characters match, extend the contiguous
                # substring that ended at the previous position in both
                # strings (diagonal cell dp[i-1][j-1]) by 1.
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1

                    # Update the global max if this substring is the longest
                    # one we've found so far
                    if dp[i][j] > longest: longest = dp[i][j]

                # If the characters dont match, reset to 0. The substring
                # must be contiguous, so any mismatch breaks the chain
                # entirely. This is the key difference from LCS, which would
                # carry forward the best prior result instead of resetting.
                else:
                    dp[i][j] = 0

        # Return the length of the longest contiguous match found anywhere
        # in the two strings.
        return longest

longest_common_substring = algorithms.longest_common_substring
longest_common_subsequence = algorithms.longest_common_subsequence
edit_distance = algorithms.edit_distance