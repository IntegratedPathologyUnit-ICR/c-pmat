import os
import random
import shutil

# Directory containing the images to divide
source_directory = r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\TWF_Process - Copy"
# List of 5 directories to create for the random assignments
output_directories = [r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\230912TWF_process_run1", r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\230912TWF_process_run2", r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\230912TWF_process_run3", r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\230912TWF_process_run4", r"D:\AMY\01_09_2K3_TWF_ORIG_TEST\230912TWF_process_run5"]

# Create the output directories if they don't exist
for directory in output_directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# List all files in the source directory
all_files = os.listdir(source_directory)

# Shuffle the list of files randomly
random.shuffle(all_files)

# Calculate the number of files to place in each directory
num_files_per_directory = len(all_files) // len(output_directories)

# Distribute the files evenly among the output directories
for i, output_directory in enumerate(output_directories):
    start_index = i * num_files_per_directory
    end_index = (i + 1) * num_files_per_directory if i < len(output_directories) - 1 else len(all_files)
    files_to_copy = all_files[start_index:end_index]

    for filename in files_to_copy:
        source_path = os.path.join(source_directory, filename)
        output_path = os.path.join(output_directory, filename)
        shutil.copy(source_path, output_path)
        print(f"Copied {filename} to {output_directory}")

print("Copying completed.")
