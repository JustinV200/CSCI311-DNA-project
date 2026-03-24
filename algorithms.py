class algorithms():
    def __init__(self):
        pass
    @staticmethod
    def edit_distance(s, t):
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0: dp[i][j] = j
                elif j == 0: dp[i][j] = i
                elif s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1]
                else: dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
        return dp[m][n]
    @staticmethod
    def longest_common_subsequence(s, t):
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]
    @staticmethod
    def longest_common_substring(s, t):
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        longest = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    if dp[i][j] > longest: longest = dp[i][j]
                else:
                    dp[i][j] = 0
        return longest

longest_common_substring = algorithms.longest_common_substring
longest_common_subsequence = algorithms.longest_common_subsequence
edit_distance = algorithms.edit_distance