import sys
from PyQt4 import QtGui

from file_selector_class import *


file_list = FileSelector.select()



# check whether a file was selected
if len(file_list)>0:
    # create list of same length to store data per file
    file_arr = []
    column_arr = []
    value_arr = []
    # do something with each file
    for file in file_list:
        print (file) #prints the full filename
        file_arr.append(column_arr)
        # open each file:
        with open(file) as myfile:
            # read each line:
            data = myfile.readlines()
            # cut first 3 characters from line 1; is % sign
            data[0] = data[0][3:]
            # do something with first line
            for line in data[0:1]:
                # read each word, multiple spaces are automagically disregarded
                cl_titles = line.split()
                # do something with each word from line1
                # for word in columns:
                #     print(word)
            column_arr.append(value_arr)
            # do something with remaining lines
            for line in data[1:2]:
                values = line.split()
                # do something with each word from remaining lines
                for value in values:
                    value_arr.append(value)
                    print(value)



else:
    print ("no file selected")




