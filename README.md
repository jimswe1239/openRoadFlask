FLASK APP README

This application is connected to Heroku via the master branch of Github. Any changes that you commit and push to master will be loaded in Heroku.

When developing on a local device, create a branch so that you don't accidentally push any changes to github.
Clone the repo to your local machine. Make sure that you have Flask installed. If you don't have Flask, install via:

pip install flask
(on Windows. May be different on Mac, please verify)

Then, you can run the file by executing the following commands in command prompt, where YOUR_DIRPATH_HERE is the path to the folder containing the codebase, for example C:\Users\You\Documents\GitHub\openRoadFlask
And #### represents the Google Maps API Key

On Windows:

cd YOUR_DIRPATH_HERE
set apiKey = ####
set FLASK_APP=flaskApp.py
flask run

On Mac:
(someone with Mac please verify)

cd YOUR_DIRPATH_HERE
export apiKey = ####
export FLASK_APP=flaskApp.py
flask run
