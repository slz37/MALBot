## MALBot
Bot for myanimelist.net that automates some useful functions and ranks the anime on a user's PTW list. Currently supports adding tags an empty row, removing tags, updating tags without replacing, and replacing tags. PTW rankings are still under development. 

## Setup
User cannot must have a browser (chrome, firefox, or opera) with no processes open, and the user should be already logged in to MAL on that browser. The code selects a browser with no processes running, opens a driver with cookies found from the default location for the browser, and uses that for login. This avoids the user having to supply their own username and password to the program.

Currently supports chrome and opera. Firefox currently gets stuck trying to load the first page. 

Works with windows and python 3.

## To do:
Finish ranking algorithm.
Fix Firefox.
Add Linux support.
