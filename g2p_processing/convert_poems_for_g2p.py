#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################################################
# File:                           convert_poems_for_g2p.py          #
# Author:                         Aline Castendiek                  #
# Student ID:                     768297                            #
# Date:                           13/06/18                          #
# Operating system:               Mac OS X El Capitan [10.11.6]     #
# Python version:                 3.5.0                             #
#                                                                   #
# Convert poems from text file to a format that preserves their     #
# structure when using the G2P tool.                                #
#                                                                   #
#####################################################################

"""
The resulting structure will look like this:
<poem>
<line> i consider the froggy that fits </line>
<line> that my hammocks seem grown and interred </line>
<line> for the color i know </line>
<line> as i thought i am stuck </line>
<line> i have found a new human instead </line>
</poem>
"""

# Example call: python convert_poems_for_g2p.py input_poems/poems1.txt formatted_poems/formatted_poems1.txt

import sys

if len(sys.argv) != 3:
    print("Please specify an input and output file.")

else:
    with open(sys.argv[1]) as infile:

        out = open(sys.argv[2], "w")

        set_start_marker = True
        in_poem = False

        for line in infile:
            stripped_line = line.strip('\n')

            if set_start_marker:
                out.write("<poem>\n")
                set_start_marker = False

            if not set_start_marker and line not in ['\n', '\r\n']:
                out.write("<line> " + stripped_line + " </line>" + '\n')
                in_poem = True

            elif in_poem and line not in ['\n', '\r\n']:
                out.write("<line> " + stripped_line + " </line>" + '\n')

            if line in ['\n', '\r\n'] and in_poem:
                out.write("</poem>\n")
                in_poem = False
                set_start_marker = True

        out.write("</poem>\n")

    infile.close()
    out.close()
    print("Done. Saved formatted poems in '" + sys.argv[2] + "'.")