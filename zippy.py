#!/usr/bin/python3

import os
import sys
import argparse
import random
import string

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",help="Input directory", type=str, required=True)
    parser.add_argument("-p","--password", help="Password for zip file", type=str, required=False)
    parser.add_argument("-s","--size", help="Set max directory size in bytes (This is pre zip) Default is 25000000", type=str, required=False)
    parser.add_argument("-f","--force", help="Blat current zippy_output folder", action="store_true", required=False)
    #parser.add_argument("-d","--dontobsficate", help="FUTURE DEV: Will not nest the zip files to obsficate the filename", type=str, required=False)
    #parser.add_argument("-o","--optimise", help="FUTURE DEV: Will perform best fit logic. This will result in photos being out of order", type=str, required=False)
    args = parser.parse_args()
    return args

 #----------- Organuse files into directories of X size -----------#
def organise(_files, _maxsize):


	currentsize = 0

	#Initialise first folders to copy to.
	currentDir = "temp_"+str(random.randint(1000,9999))
	os.system("mkdir "+tempDirectory+"/"+currentDir)

	for file in _files:
		try:
		    if os.path.getsize(inputDirectory+"/"+file) > _maxsize:
		        #print(file + " is greater than the maximum attachment size and wont be included")
		        pass
		    else:
		        #Check if current folder we are sending to is > 25mb. If not, add it. If so, make new directory.
		        if currentsize + os.path.getsize(inputDirectory+"/"+file) > _maxsize:
		        	#print(currentDir + " is already "+str(currentsize)+" cannot add "+inputDirectory+"/"+file+" which is: "+str(os.path.getsize(inputDirectory+"/"+file)))
		        	currentDir = "temp_"+str(random.randint(1000,9999))
		        	os.system("mkdir "+tempDirectory+"/"+currentDir)

		        	#Put file in new folder
		        	os.system("cp "+inputDirectory+"/"+file+" "+tempDirectory+"/"+currentDir)
		        	currentsize = os.path.getsize(inputDirectory+"/"+file) 
		        else:
		            #Put file in current folder
		            os.system("cp "+inputDirectory+"/"+file+" "+tempDirectory+"/"+currentDir)
		            currentsize += os.path.getsize(inputDirectory+"/"+file)
		            #print("Current size: "+ str(currentsize))

		except Exception as e:
		    print(e)


 #----------- Zip folders into a nested format for Gmail/Gsec -----------#
def zip(_tempDirectory, _dirToZip, _password, _outputFile):
    
    try:
        #----------- Zip 1 -----------#
        
        intermediateFile = "intermediate"+str(random.randint(1000,9999))+".txt"

        #Check that the folder exists
        if os.path.isdir(_tempDirectory+"/"+_dirToZip):
            print("Creating first zip file " + intermediateFile)
            os.system("zip -0 -r " + intermediateFile + " "+_tempDirectory+"/"+_dirToZip)
        else:
            print("[!] The folder you want to zip does not exist...")
            exit(1)

       	#----------- Zip 2 -----------#

        if not os.path.exists("zippy_output/"+_outputFile):
        	print("Creating second zip file " + _outputFile)
        	os.system("zip -e -n -r --password "+_password+" zippy_output/"+_outputFile+" "+intermediateFile)

       		#Add file and the password to a list
       		passwords.append(_outputFile + "," +_password)

       		#Clean up intermediate file
       		cleanup(intermediateFile)

       	else:
        	print("[!] The output file you have specified already exists...")
        	cleanup(intermediateFile)
        	exit(1)

    except Exception as e:
        print("[!] Oh noooooo " + str(e))
        exit(1)

#----------- Delete file/directory given -----------#
def cleanup(_toDelete):
    try:
    	if os.path.isdir:
    		os.system("rm -r "+_toDelete)
    	else:
        	os.system("rm "+_toDelete)
    except:
        pass


if __name__ == "__main__":

	#----------- Init variables -----------#
    args = parse_args()

    inputDirectory = args.input
    tempDirectory = "temp_"+str(random.randint(1000,9999))
        
    if args.password:
        password = args.password
    else:
        password = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))

    if args.size:
    	maxsize = args.size
    else:
    	maxsize = 25000000

    #----------- Future use -----------#
    passwords =["folder,password"]
    
    #----------- Check and create output -----------#
    if os.path.exists("zippy_output") and not args.force:
    	print("The directory zippy_output already exists. Please delete it for run with --force.")
    	exit(1)
    elif os.path.exists("zippy_output") and args.force:
    	os.system("mv zippy_output zippy_output_"+str(random.randint(1000,9999)))
    	os.system("mkdir zippy_output")
    elif not os.path.exists("zippy_output"):
    	os.system("mkdir zippy_output")

    #----------- Create temp output folder ------------#
    if not os.path.isdir(tempDirectory):
    	os.system("mkdir " + tempDirectory)


    #----------- Organise input into folders  -----------#
    organise(os.listdir(inputDirectory), maxsize)

    #----------- Zip folders -----------#
    for index,dirToZip in enumerate(os.listdir(tempDirectory)):
    	zip(tempDirectory,dirToZip,password,"zip_"+str(index))


    print("\n[*] Cleaning up...")
    cleanup(tempDirectory)
    print("[*] Zipping complete. All zips are protected with password: " + password)
