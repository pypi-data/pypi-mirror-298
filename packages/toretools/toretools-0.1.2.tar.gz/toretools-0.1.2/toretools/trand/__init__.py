import os


class RandSeedGen:
    def __init__(self):
        pass

    def _generate_random_seed(self):
        # Generate a random seed using os.urandom
        return int.from_bytes(os.urandom(4), "big")

    def generate_seed(self, num_bits: int | None = 128):
        if num_bits <= 0:
            raise ValueError("Number of bits must be positive.")

        # Generate a random seed
        seed = self._generate_random_seed()
        mt = MersenneTwister(seed)

        # Calculate the number of bytes needed
        num_bytes = (num_bits + 7) // 8
        long_integer = 0

        # Generate the specified number of bytes
        for _ in range(num_bytes):
            # Generate a random byte (0-255)
            random_byte = mt.extract_number() & 0xFF
            long_integer = (long_integer << 8) | random_byte  # Shift and add the byte

        # Ensure the result fits within the specified bit length
        return long_integer & ((1 << num_bits) - 1)


class MersenneTwister:
    def __init__(self, seed: int | RandSeedGen):
        # Constants for MT19937
        self.n = 624
        self.m = 397
        self.matrix_a = 0x9908B0DF  # Constant vector a
        self.upper_mask = 0x80000000  # Most significant w-r bits
        self.lower_mask = 0x7FFFFFFF  # Least significant r bits

        # State array to store the previous values
        self.mt = [0] * self.n
        self.index = self.n  # Correct initialization

        # Initialize with the seed
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, self.n):
            self.mt[i] = (
                0x6C078965 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i
            ) & 0xFFFFFFFF

    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                raise Exception("Generator was never seeded")

            self.twist()

        y = self.mt[self.index]
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18

        self.index += 1

        return y & 0xFFFFFFFF

    def twist(self):
        for i in range(self.n):
            y = (self.mt[i] & self.upper_mask) + (
                self.mt[(i + 1) % self.n] & self.lower_mask
            )
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ (y >> 1)
            if y % 2 != 0:  # y is odd
                self.mt[i] ^= self.matrix_a
        self.index = 0  # Reset index after twisting

    def randint(self, start, end):
        # Get a random number in the range [start, end]
        return start + self.extract_number() % (end - start + 1)
