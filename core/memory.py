import os
import json

# Define the path to the persistent memory file within the data directory with .id extension
MEMORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'memory.id')


def read_from_memory():
    """Reads and returns the persistent memory data as a dictionary from a plain text file with key=value lines."""
    data = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    data[key.strip()] = value.strip()
            return data
        except IOError:
            return {}
    return {}


def write_to_memory(data):
    """Writes the provided dictionary to persistent memory as plain text key=value pairs."""
    # Ensure the data directory exists
    data_dir = os.path.dirname(MEMORY_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    with open(MEMORY_FILE, 'w') as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")


def append_to_memory(key, value):
    """Reads current memory, updates with the given key-value pair, and writes back."""
    current_data = read_from_memory()
    current_data[key] = value
    write_to_memory(current_data) 