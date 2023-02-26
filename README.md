# pybinlog
Utility functions to parse Ardupilot's log file in bin format. 
Provides coomand line options to convert from bin file to csv. 
- ## bin2csv
  File converter from Ardupilot's log files in bin format to CSV files. 
 ### Usage
  `bin2csv [-h] [-m Messages] [-o output_directory] [filepath]`
  
  Convert bin file provided by `filepath` to csv files.
  #### Optional Arguments
  - -m Messages only converts the Messages provides, a comma separated string. 
  
  - -o output_directory Writes the csv files to provided output_directory. 
 - ## bin2csvgui
 Starts the gui application for converting the selected file to csv.
 
 ![image](https://user-images.githubusercontent.com/109569555/221422355-492ec4ff-5cd1-4053-aa5e-9a4eada940c3.png)

 Optionally select the required messages and output directory.
## Installation
 Install the [package](https://pypi.org/project/pybinlog/) using pip by running `pip install pybinlog`
 If you are running an older version, upgrade the package by running `pip install pybinlog --upgrade`
