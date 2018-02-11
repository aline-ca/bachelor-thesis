#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
# Remove double quotation mark style from file.

Example:

"a rather precocious young lad
asked mommy, ""if hell's for the bad
and those who have doubted,
won't hell be too  crowded?""
said mommy, ""uh?go ask your dad.""
"

becomes:
a rather precocious young lad
asked mommy, if hell's for the bad
and those who have doubted,
won't hell be too  crowded?"
said mommy, "uh?go ask your dad."

"""

########################################################################################################################
input_file  = 'limericks.txt'                 # Read data from this file
output_file = 'new_limericks.txt'             # Write new data into this file
########################################################################################################################


outfile = open(output_file,"w")

# Open limericks file
with open(input_file,'rb') as file:
  line_count = 0
  found_end_marker = False 

  # Iterate over lines
  for line in file:
    line_count += 1

    # Check whether all limericks consist of five lines:
    if (len(line) == 3) and (line_count % 6 != 0):
      print("Found problem in line " + str(line_count))
      break

    # Remove " at the beginning of limerick:  
    elif (line_count == 1) or (found_end_marker == True):
      # Also check for "" inside this line:
      if "\"\"" not in line:
        outfile.write(line[1:])
        found_end_marker = False
      else:
        new_line = line[1:]
        outfile.write(new_line.replace("\"\"","\""))
        found_end_marker = False

    # Line with " at the end of limerick becomes empty line as new end marker  
    elif (len(line) == 3):
      outfile.write("\n")
      found_end_marker = True

    # Convert "" to ":  
    elif "\"\"" in line:
      outfile.write(line.replace("\"\"","\""))

    # Also remove the blank space before a question mark that occurs sometimes:
    #if " ?" in line:
     # outfile.write(line.replace(" ?","?")) 

    else:
      outfile.write(line)  


  print("File consists of " + str(line_count) + " lines.")
  print("There are " + str(line_count/6) + " limericks in this file.")

outfile.close()







