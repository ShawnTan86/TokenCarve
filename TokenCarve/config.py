import os
import shutil
import site

# Define the path to the source file
modeling_llama_source_file = os.path.join(os.path.dirname(__file__), 'modeling_llama.py')
configuration_llama_source_file = os.path.join(os.path.dirname(__file__), 'configuration_llama.py')

# Get the site-packages directory of the current Conda environment
site_packages_dir = site.getsitepackages()[0]

# Construct the path to the destination file
modeling_llama_destination_file = os.path.join(site_packages_dir, 'transformers', 'models', 'llama', 'modeling_llama.py')
configuration_llama_destination_file = os.path.join(site_packages_dir, 'transformers', 'models', 'llama', 'configuration_llama.py')

print(f"Current Conda environment's site-packages directory: {site_packages_dir}")

# Check if the destination file exists
if not os.path.exists(modeling_llama_destination_file):
    print(f"The destination file does not exist. Please check the path: {modeling_llama_destination_file}")
    exit(1)

if not os.path.exists(configuration_llama_destination_file):
    print(f"The destination file does not exist. Please check the path: {configuration_llama_destination_file}")
    exit(1)

# Copy the source file to the destination file
shutil.copyfile(modeling_llama_source_file, modeling_llama_destination_file)
print(f"modeling_llama successfully replaced: {modeling_llama_source_file} -> {modeling_llama_destination_file}")
shutil.copyfile(configuration_llama_source_file, configuration_llama_destination_file)
print(f"configuration_llama successfully replaced: {configuration_llama_source_file} -> {configuration_llama_destination_file}")
