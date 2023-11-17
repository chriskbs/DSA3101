# DSA3101_library_frontend

## Introduction
This folder comprises Python scripts corresponding to each page of the web interface under development. The assets folder contains the images and icons that were used in the various pages. The data folder stores the data files generated from the input page as well as data files required for the simulation page.

## Requirements
The web interface is developed using Python Dash, alongside HTML and CSS concepts to enhance the visual appeal of the interface. Addtionally, interactive graphs will be generated using Plotly to enhance the user experience. 

## To run Docker Container 
1. Navigate to this folder via `cd` command in terminal
2. Build image using `docker build -t mydash .`
3. Run container using `docker run -d -p 9002:8050 mydash`
4. Navigate to http://localhost:9002 to view the interface

 
