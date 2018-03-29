#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           add_markers.py                    #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           26/03/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
#   This script .     #
#                                                                   #
#####################################################################


"""
add markers
fix question marks
add parameter for removing all punctuation except newline!


§wrenching sob stories, pleading, and such
move my third cousin flo very much.
are you broke? go to flo
with a sad tale of woe.
she's a do-gooder, bro, a soft touch.€

§while you're sleeping at night, you may dream,
and no matter how odd they may seem,
or how creepy they feel,
dreams seem perfectly real
till you wake yourself up with a scream.€

beginning: §
end: €


"""


########################################################################################################################
input_file          = 'data/limericks.txt'                                      # Read data from this file
output_file         = 'data/limericks_with_markers.txt'                 # Write new data into this file
########################################################################################################################


outfile = open(output_file,'w')

with open(input_file, 'r') as infile:                       # Open limericks file

    line_count = 0
    set_marker = True

    # Iterate over lines
    for line in infile:
        line_count += 1
        if set_marker == True:
            outfile.write("§\n")
            outfile.write(line.replace(" ?","?"))
            set_marker = False
        elif line_count % 6 == 0:
            outfile.write("€\n")
            set_marker = True
        else:
            outfile.write(line.replace(" ?","?"))


    # Also remove the blank space before a question mark that occurs sometimes:
    #if " ?" in line:
     # outfile.write(line.replace(" ?","?"))

infile.close()

print("Done!")