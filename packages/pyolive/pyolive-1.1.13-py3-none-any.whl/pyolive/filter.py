import fnmatch

class Filter:
    def __init__(self, pattern, filename):
        self.pattern = pattern
        self.filename = filename

    def match(self):
        print(f"KIRO> pattern = {self.pattern}")
        if self.pattern == '':
            return True

        pattern = self.pattern.split("^")

        # exclude pattern
        if pattern[1]:
            elems = pattern[1].split(",")
            for elem in elems:
                if self._match_simple(elem, self.filename):
                    return False

        # include pattern
        if pattern[0]:
            elems = pattern[0].split(",")
            for elem in elems:
                if self._match_wildcard(elem, self.filename):
                    return True
            return False

        return True

    def _match_simple(self, pattern, string):
        if pattern in string:
            return True
        return False

    def _match_wildcard(self, pattern, string):
        p_len = len(pattern)
        s_len = len(string)

        # dp[i][j] is True if pattern[0..i-1] matches string[0..j-1]
        dp = [[False] * (s_len+1) for _ in range(p_len+1)]

        # Empty pattern matches empty string
        dp[0][0] = True

        # Handle the cases where pattern starts with '*' (can match empty string)
        for i in range(1, p_len+1):
            if pattern[i-1] == '*':
                dp[i][0] = dp[i-1][0]

        # Build the table for all other characters
        for i in range(1, p_len+1):
            for j in range(1, s_len+1):
                if pattern[i-1] == string[j-1] or pattern[i-1] == '?':
                    dp[i][j] = dp[i-1][j-1]
                elif pattern[i-1] == '*':
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]

        return dp[p_len][s_len]

if __name__ == '__main__':
    p = Filter("ac_123.txt^.bin", "ac_123.txt")
    print(p.match())