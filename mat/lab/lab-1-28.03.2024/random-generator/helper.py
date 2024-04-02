n = 120000  # Total number of bits
n1 = n0 = n / 2  # Number of 1s and 0s, assuming they are about equal

# Calculate the expected number of runs for a truly random sequence
expected_runs = 1 + (2 * n1 * n0) / n
print(expected_runs)