README - DATS 6401-10 Final Project					
									
Benjamin Lee								
								    	
--------------------------------------------------------------------------------------------------------
How to Load Webpages							
								
- Open up VSCode and open the base folder containing all folders associated with this project.

- Open the "code" folder, and then and open "home.html" in VSCode and type the following in Terminal:

python -m http.server 9000

This will open a HTTP server on port 9000 using Python. "home.html" is the homepage for this project.

- Feel free to navigate around the webpages as you please!

--------------------------------------------------------------------------------------------------------
How to find the Presentation Video and PowerPoint Presentation

- Go to the "powerpoint" folder to find the PowerPoint presentation (.PPT) file.

- Go to the "presentation" folder to find the video presentation (.mp4) file.

--------------------------------------------------------------------------------------------------------
How to Download and Clean Most Recent Version of Data

- For infections data, go to "https://ourworldindata.org/coronavirus-source-data" and download the 
data in CSV format.

- For vaccination data, go to "https://www.kaggle.com/gpreda/covid-world-vaccination-progress" and 
download the 3 MB zip folder. Extract all files to the "raw" folder, which can be found in the 
"data" folder included in this project's files, and delete "country_vaccinations_by_manufacturer.csv."

- Open up the IDE of your choosing (i.e. PyCharm) and run "preprocessing.py", which can be found in the 
"code" folder included in this project's files. This will clean most files, but some may have to be 
formatted in VSCode using regular expressions and find/replace. Many of the cleaned files were uploaded
to Google Drive to be used with the Google Charts API. The link can be found below:

https://docs.google.com/spreadsheets/d/19iZ-MP7LdHa9Hbjxd2nCYokMOP-WaU-RNFSQjFbIDx0/edit?usp=sharing

Please email bml72@gwu.edu for edit access.

- The base datasets (i.e. the cleaned versions of what was downloaded from OWiD and Kaggle) can be 
found in the "base_data" folder of the "cleaned" folder, while datasets specific to certain 
visualizations that were later uploaded to Google Drive can be found in the "visualization_data"
folder.