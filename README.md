# Project WiCCED Data Core GitHub Page ![image](https://user-images.githubusercontent.com/58920927/124919410-39b9e400-dfc4-11eb-873d-67593678e8f8.PNG)

This repository was created to provide a basic api (wicced.py or wicc.R) and documentation for researchers working with data on the Project WiCCED Data Core systems.

# Where to go to start

 There is a getting started page that can help with understanding the purpose of this
 GitHub page called [Getting Started](https://github.com/mshatley/epscor/wiki/Getting-Started)

# List of Contents 

* Why
* Installation
* [Wiki](https://github.com/mshatley/epscor/wiki)
* Usage
* What can you do?

# Why
To create a wiki documentation with use-cases for users to understand and use the Python API.
There is a lot of data that is gathered when monitoring/researching and the purpose of this
Wiki, GitHub repo is to assist researchers with being able to access/manipulate the data while
having no programming/CS background

# Installation
What is needed is an application that can be used to run Python code

(For example: Download Anaconda Navigator to have access to Jupyter Notebook, Jupyter Lab,
Google Collab can work as well)

Pandas and Geopandas are libraries inside of Jupyter Notebook/Lab that can be used to access,
read data that need to be installed and saved.

# Wiki
We have created a wiki to help support researchers accessing the system.

Within the wiki you will find the following pages:

Getting Started (First Steps) - This will help you get all configurations set and ready to access the data.

Methods:

addDate - to help format requested dates into the proper format
addDataType - to get specific type of data out of a list
Get_full_query_by_month - used to specify data grabs by month
addBox- specify a bounding box to return data only falling inside the box
addDateRange - specify a date range and return data inside that date range
changeFormat - specify data format for the data returned
buildURL- creates the fully parameterized url for call to geoserver
Seperate_by_location- returns data by location (and time)
Features/Information in Documentation:

Instantiate wicced.py
Define URL for data access
List features or data available
Specify data type of interest
Specify a date or date range
Define a bounding box
Export to CSV or JSON file types
Project Contributors This code was developed for researchers working with Project WiCCED Data Core.

For questions, please contact tina.callahan@udel.edu

The Wiki has the different tools that can be used when accessing the data and what kind of data
is accessed. The Wiki has instructions as to how to get started. How to use the Python code
to get a selected date, or coordinates or data type. It also goes in depth with each feature
and explains the params, use and what should the output look like.

Goals for this documentation

Make it easier for user to understand how everything works.
Be able to make folders and clone repositories on GitHub
Show how to put together the code to print out specific outputs.
Help new comers have access to the program.

Contents of the wiki

1. [addDate](https://github.com/mshatley/epscor/wiki/addDate)
2. [addDataType](https://github.com/mshatley/epscor/wiki/addDataType)
3. [get_full_query_by_month](https://github.com/mshatley/epscor/wiki/get_full_query_by_month)
4. [addBox](https://github.com/mshatley/epscor/wiki/addBox)
5. [addDateRange](https://github.com/mshatley/epscor/wiki/addDateRange)
6. [changeFormat](https://github.com/mshatley/epscor/wiki/changeFormat)
7. [buildURL](https://github.com/mshatley/epscor/wiki/buildURL)
8. [separate_by_location](https://github.com/mshatley/epscor/wiki/separate_by_location)

# Usage

* Be able to have large sets of data displayed regardless of what is being looked at/researched.
* Be able to access data from different data sources.


# What can users do

The user can change the data source to see where the data should be taken from. There is a way to
see the data for a particular data type. The date can be printed in many different formats. The
date can also have a range in there which will access the data all in between the two dates selected.
The format can also be changed as to how someone can extract the data whether it is json or csv. A URL
can be built to send the user to another tab with the data there. There is an option to get the data for
a full month using the get full query function and the data can be isolated and used for machine learning
using the separate by location function



