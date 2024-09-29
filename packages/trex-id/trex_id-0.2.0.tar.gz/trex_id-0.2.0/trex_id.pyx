import random
import time

cdef class Trex:
    """
    Trex is a singleton class used for generating unique IDs based on machine-specific and secret information.

    This class provides a secure and fast way to generate IDs. It uses 42 bits for the timestamp (in milliseconds),
    3 bits for the machine ID (for stronger servers), and 7 bits for randomness.
    """

    # Class-level Python attribute to store the singleton instance
    _instance = None  # This is a Python-level attribute

    cdef int MACHINE_ID
    cdef unsigned long long SECRET_KEY

    @staticmethod
    def get_instance(int machine_id, unsigned long long secret_key):
        """
        Static method to return the singleton instance. If no instance exists, it will create one.

        :param machine_id: Integer representing the machine ID (3 bits, 0-7)
        :param secret_key: Secret key provided by the user (masked to 52 bits)
        :return: The singleton instance of Trex
        """
        if Trex._instance is None:
            Trex._instance = Trex(machine_id, secret_key)
        return Trex._instance

    def __cinit__(self, int machine_id, unsigned long long secret_key):
        """
        Cython constructor for Trex.

        :param machine_id: Integer representing the machine ID (3 bits, 0-7)
        :param secret_key: Secret key provided by the user (masked to 52 bits)
        """
        # Mask the machine ID and secret key
        self.MACHINE_ID = machine_id & ((1 << 3) - 1)  # Mask to 3 bits
        self.SECRET_KEY = secret_key & ((1 << 52) - 1)  # Mask to 52 bits

    def generate_id(self):
        """
        Generates a unique ID using the machine ID, secret key, and current time.

        The custom ID consists of:
        - 42 bits for the current time in milliseconds, derived from nanoseconds.
        - 3 bits for the machine ID.
        - 7 bits for a random index to ensure uniqueness.
        - Finally, the 52-bit secret key is added and the result is masked to 53 bits.

        :return: A unique 53-bit integer ID.
        """
        cdef unsigned long long timestamp_ns, timestamp_ms, custom_id, final_id
        cdef int random_index

        # Get the current time in nanoseconds and convert to milliseconds by shifting right by 20 bits.
        timestamp_ns = time.perf_counter_ns()
        timestamp_ms = (timestamp_ns >> 20) & ((1 << 42) - 1)  # Mask to 42 bits of time

        # Generate a 7-bit random index.
        random_index = random.getrandbits(7)

        # Construct the custom ID: 42 bits of time + 3 bits machine ID + 7 bits random index.
        custom_id = (timestamp_ms << 10) | (self.MACHINE_ID << 7) | random_index

        # Add the secret key and mask the result to 53 bits.
        final_id = (custom_id + self.SECRET_KEY) & ((1 << 53) - 1)

        return final_id
