#!/usr/bin/python3

import os
import argparse
import random
import string


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input directory", type=str, required=True
    )
    parser.add_argument(
        "-p", "--password", help="Password for zip file", type=str, required=False
    )
    parser.add_argument(
        "-s",
        "--size",
        help="Set max directory size in bytes (This is pre zip) Default is 25000000",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Blat current zippy_output folder",
        action="store_true",
        required=False,
    )
    args = parser.parse_args()
    return args


# Seperate out files into temp folders per max file size
def organise(_files, _max_size):
    current_size = 0

    # Initialise first folders to copy to.
    current_directory = "temp_" + str(random.randint(1000, 9999))
    os.system("mkdir " + temp_directory + "/" + current_directory)

    for file in _files:
        try:
            if os.path.getsize(input_directory + "/" + file) > _max_size:
                print(
                    file
                    + " is greater than the maximum attachment size and wont be included"
                )
                pass
            else:
                # Check if current folder we are sending to is > 25mb. If not, add it.
                # If so, make new directory.
                if (
                    current_size + os.path.getsize(input_directory + "/" + file)
                    > _max_size
                ):
                    current_directory = "temp_" + str(random.randint(1000, 9999))
                    os.system("mkdir " + temp_directory + "/" + current_directory)

                    # Put file in new folder
                    os.system(
                        "cp "
                        + input_directory
                        + "/"
                        + file
                        + " "
                        + temp_directory
                        + "/"
                        + current_directory
                    )
                    current_size = os.path.getsize(input_directory + "/" + file)
                else:
                    # Put file in current folder
                    os.system(
                        "cp "
                        + input_directory
                        + "/"
                        + file
                        + " "
                        + temp_directory
                        + "/"
                        + current_directory
                    )
                    current_size += os.path.getsize(input_directory + "/" + file)

        except Exception as e:
            print(e)


# Create zip files
def zip(_temp_directory, _dir_to_zip, _password, _outputFile):
    try:
        # Process zip 1
        intermediate_file = "intermediate" + str(random.randint(1000, 9999)) + ".txt"

        if os.path.isdir(_temp_directory + "/" + _dir_to_zip):
            print("Creating first zip file " + intermediate_file)
            os.system(
                "zip -0 -r -j "
                + intermediate_file
                + " "
                + _temp_directory
                + "/"
                + _dir_to_zip
            )
        else:
            print("[!] The folder you want to zip does not exist...")
            exit(1)

        # Process zip 2
        if not os.path.exists("zippy_output/" + _outputFile):
            print("Creating second zip file " + _outputFile)
            os.system(
                "zip -e -n -r --password "
                + _password
                + " zippy_output/"
                + _outputFile
                + " "
                + intermediate_file
            )

            cleanup(intermediate_file)

        else:
            print("[!] The output file you have specified already exists...")
            cleanup(intermediate_file)
            exit(1)

    except Exception as e:
        print("[!] Oh noooooo " + str(e))
        exit(1)


# Clean up temporary files
def cleanup(_toDelete):
    try:
        if os.path.isdir:
            os.system("rm -r " + _toDelete)
        else:
            os.system("rm " + _toDelete)
    except:
        pass


if __name__ == "__main__":
    print(
        """\
  ______ _                      
 |___  /(_)                     
    / /  _  _ __   _ __   _   _ 
   / /  | || '_ \ | '_ \ | | | |
  / /__ | || |_) || |_) || |_| |
 /_____||_|| .__/ | .__/  \__, |
           | |    | |      __/ |
           |_|    |_|     |___/ 
"""
    )

    args = parse_args()

    if os.path.isdir(args.input):
        input_directory = args.input
    else:
        print("[!] The input must me a directory")
        exit(1)

    temp_directory = "temp_" + str(random.randint(1000, 9999))

    if args.password:
        password = args.password
    else:
        password = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))

    if args.size:
        max_size = args.size
    else:
        max_size = 25000000

    if os.path.exists("zippy_output") and not args.force:
        print(
            "The directory zippy_output already exists. Please delete it for run with --force."
        )
        exit(1)
    elif os.path.exists("zippy_output") and args.force:
        os.system("mv zippy_output zippy_output_" + str(random.randint(1000, 9999)))
        os.system("mkdir zippy_output")
    elif not os.path.exists("zippy_output"):
        os.system("mkdir zippy_output")

    if not os.path.isdir(temp_directory):
        os.system("mkdir " + temp_directory)

    organise(os.listdir(input_directory), max_size)

    for index, dir_to_zip in enumerate(os.listdir(temp_directory)):
        zip(temp_directory, dir_to_zip, password, "zip_" + str(index))

    print("\n[*] Cleaning up...")
    cleanup(temp_directory)
    print("[*] Zipping complete. All zips are protected with password: " + password)
