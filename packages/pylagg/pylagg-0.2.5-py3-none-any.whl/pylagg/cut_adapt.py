from cutadapt.cli import main
import os
import toml

def trim(input_file: str):

    config_file = "config.toml"

    if os.path.isfile(config_file):
        print(f"The file '{config_file}' exists.")
    else:
        print(f"The file '{config_file}' does not exist.")
        exit(0)

    # Read the TOML file
    config = toml.load(config_file)

    command = []  # Initialize an empty list to hold the commands

    # Check if the 'arguments' section exists
    if 'arguments' in config:
        arguments = config['arguments']
        
        # Iterate through each key and its associated list
        for key, value in arguments.items():
            if isinstance(value, list):
                for item in value:
                    command.append(f"{key}")
                    if item != "":
                        command.append(f"{item}")
            else:
                command.append(f"{key}")
                if value != []:
                    command.append(f"{value}")
    else:
        print("No 'arguments' section found in the config file.")
    
    if '-o' not in command:
        # Automatically generate the output file name by adding "_trimmed" before the extension
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_trimmed{ext}"
        command.append('-o')
        command.append(output_file)

    command.append(input_file)

    print(f"Running command: {' '.join(command)}")

    main(command)
    #os.remove(input_file)