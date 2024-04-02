class LFSRWithCustomPolynomial:
    def __init__(self, seed, taps):
        self.state = seed & 0xFFF
        self.taps = [tap - 1 for tap in taps]

    def step(self):
        new_bit = 0
        for tap in self.taps:
            new_bit ^= (self.state >> tap) & 1
        non_linear_bit = (self.state >> 5 & 1) & (self.state >> 3 & 1)
        new_bit ^= non_linear_bit
        self.state = ((self.state << 1) | new_bit) & 0xFFF
        return self.state


class SynchronizedLFSR:
    def __init__(self, main_seed, sync_seed, main_taps, sync_taps):
        self.main_lfsr = LFSRWithCustomPolynomial(main_seed, main_taps)
        self.sync_lfsr = LFSRWithCustomPolynomial(sync_seed, sync_taps)
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def step(self):
        if not self.running:
            return None

        while self.running:
            main_output = self.main_lfsr.step()
            sync_output = self.sync_lfsr.step()

            if bin(sync_output).count('1') % 2 == 0:
                return main_output


def frequency_test(sequence):
    n = len(sequence)
    frequency = sum(sequence) / n
    return frequency


def differential_test(sequence):
    n = len(sequence)
    changes = sum(sequence[i] ^ sequence[i - 1] for i in range(1, n))
    return changes / (n - 1)


def runs_test(sequence):
    runs = 1
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i - 1]:
            runs += 1
    return runs


def berlekamp_massey(sequence):
    n = len(sequence)
    L = 0
    C = [0] * n
    B = [0] * n
    C[0], B[0] = 1, 1
    m = 1
    b = 1
    for N in range(n):
        d = sequence[N]
        for i in range(1, L + 1):
            d ^= (C[i] & sequence[N - i])
        if d == 1:
            temp = C.copy()
            for i in range(N + 1 - m, n):
                if B[i - (N + 1 - m)] == 1:
                    C[i] ^= 1
            if L <= N // 2:
                L = N + 1 - L
                B = temp
                m = N + 1
        if N % 1000 == 0:
            print(f"Progress: {N / n * 100}%")
    linear_complexity = L
    return linear_complexity


def calculate_lfsr_cycle_length(sequence):
    for cycle_length in range(1, len(sequence)):
        is_repeating = True
        for i in range(len(sequence) - cycle_length):
            if sequence[i] != sequence[i + cycle_length]:
                is_repeating = False
                break

        if is_repeating:
            return cycle_length

    return len(sequence)


main_taps = [12, 6, 4, 1]
sync_taps = [12, 6, 4, 1]
main_seed = 0xACE
sync_seed = 0xBEE
main_lfsr = SynchronizedLFSR(main_seed, sync_seed, main_taps, sync_taps)
main_lfsr.start()

lfsr_values = []
while len(lfsr_values) < 10000:
    lfsr_values.append(main_lfsr.step())

binary_sequence = [bit for number in lfsr_values for bit in [(number >> i) & 1 for i in range(11, -1, -1)]]

frequency_result = frequency_test(binary_sequence)
differential_result = differential_test(binary_sequence)
runs_result = runs_test(binary_sequence)
complexity_result = berlekamp_massey(binary_sequence)
cycles_result = calculate_lfsr_cycle_length(binary_sequence)

print(binary_sequence)
print(f"Frequency Test Result: {frequency_result}")
print(f"Differential Test Result: {differential_result}")
print(f"Runs Test Result: {runs_result}")
print(f"Complexity Test Result: {complexity_result}")
print(f"Cycle Length: {cycles_result}")
