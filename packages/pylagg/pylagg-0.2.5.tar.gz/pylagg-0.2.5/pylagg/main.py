import typer
import os

import pylagg.cgr as cgr

app = typer.Typer()

@app.command()
def cgr_generate(
    input: str = typer.Option(
        None,
        "--input",
        "-i",
        help = "File name if using k-mer input you already have. Must be a .txt file for a single image.",
    ),
    accession_number: str = typer.Option(
        None,
        "--accession-number",
        "-a",
        help = 'Generate an image using an NCBI database accession number. If you would like to use more than one accession number, please list them in quotation marks, separated by commas, or put them in a .txt file with one accession number per line, and input the file name with this flag.',
    ),
    kmer: int = typer.Option(
        10,
        "--kmer",
        "-k",
        help = "Specify your desired k-mer number (Only used when generating from an accession number, if your input is already in k-mer form it will be detected)."
    ),
    output_path: str = typer.Option(
        os.getcwd(),
        "--output-path",
        "-o",
        help="Use this to specify an alternate save location for your generated images. If nothing is specified, the default location is where the terminal is located.",
    ),
    scale_size: int = typer.Option(
        100,
        "--scale-size",
        "-s",
        help = "Scale your image down by a percentage as a number between 1 and 100. Do not include any symbols (%)!",
    ),
    config: str = typer.Option(
        None,
        "--config",
        "-c",
        help = "Use a config file to specify your options. Please include only an input (accession number(s) or kmer file(s)) and the config file's name. If any other options are also specified they will be ignored."
        ),
):
    # INPUT ERROR CHECKING
    if input and accession_number:
        print("Please only include a file name OR an accession number(s).")
        print("If you need help, type 'lagg --help'.")
        exit()
    if not (input or accession_number):
        print("Please include an input, either an accession number(s) or the name of a file containing k-mer input(s).")
        print("If you need help, type 'lagg --help'.")
        exit()
    if scale_size > 100 or scale_size < 1:
        print("Please use a number between 1 and 100 for scale size.")
        print("If you need help, type 'lagg --help'.")
        exit()
    if kmer <= 0:
        print("Invalid k-mer count. Please use a k-mer count greater than 0.")
        print("If you need help, type 'lagg --help'.")
        exit()
    if not(os.path.exists(output_path)):
        print("The given output path does not exist. Please double check your path and try again.")
        print("If you need help, type 'lagg --help'.")
        exit()
    if input and not (os.path.exists(output_path +"/"+ input)):
        print("The input file name is invalid or does not exist. Please make sure your file name includes either '.txt'")
        print("If you need help, type 'lagg --help'.")
        exit()
    if input and not((input.rfind(".txt") != -1)):
        print("Your input is not a supported file type. Supported types are '.txt'. Please convert to a supported file type and try again.")
        print("If you need help, type 'lagg --help'.")
        exit()
        
    # END INPUT ERROR CHECKING
    
    # Pre Process Accession number
    if accession_number:
        
        #remove white spaces
        accession_number = accession_number.replace(" ", "")
        
        accession_list = accession_number.split(",")
            
        print(accession_list)
        
        if(kmer != 10):
            print("Using k-mer of " + str(kmer))
            print("Using a non default k-mer value (not yet implemented)")
        
        if(accession_number.rfind(".txt") != -1):
            print("detecting .txt of accession numbers (not implemented)")
        
        # Slice input if multiple numbers (DONE)
        # Check if .txt of numbers (DONE)
        # Error check for valid numbers (maybe done elsewhere tho?)
        
        # Image generation with accession number:
        print("Image generation with accession number not yet implemented")
        if scale_size != 100:
            print("scaling not yet implemented")
            
    if input:
        counts_file_path = output_path + "/" + input
        with open(counts_file_path) as f:
            
            # .txt case
            if(input.rfind(".txt") != -1):
                if scale_size != 100:
                    print("scaling single kmer input not yet implemented")
                else:
                    # Scale is 100% so generate normal full sized image
                    input = input.replace(".txt", "")
                    #print(input)
                    cgr.count_file_to_image_file(f, output_path + "/" + input + ".png")
                    print("\nSuccessfully created image called '" + input + ".png' at " + output_path)
            else:
                #this should never be hit since it's checked above...but just in case
                print("Error with file type")
                
def cli():
    app()
