# Close-Take-Home

## Script logic:
More detailed logic about what each function does can be found in the comments in the script, but the first thing that it does is creates the two custom "Company Founded" and "Company Revenue" fields on your Close dashboard. From there, it reads your csv file and formats the data so that it is in an acceptable shape for your Close dashboard to receive it and to place it properly. After the leads are formatted, the script sends them to the Close Dashboard via the Close API. After all of the leads are available on your Close dashboard, the script makes a request for lead id's that are filtered by companies that were founded between 01/01/1980 and 01/01/2023. It then goes on to fetch all of the leads that match the id's that have been acquired. From there, it formats the leads and only saves the data that is relevant to the values that we want for the output csv, before finally writing it.

## Invalid data
There were a few different cells in the csv that contained invalid data. The data that was particularly useless were leads that didn't have a contact attached to them. Those leads were bypassed from import altogether, though they may have later been added if a row contained the same lead name with a contact. Otherwise, the two types of data that were invalid were emails an phone numbers. The script uses a regex validating function to check wether or not an email could potentially be valid and it bypasses any emails that are clearly invalid. For validating phone numbers, since the csv only contains US leads, and 10 digits is the number of digits required to make a US phone call, any digits that proceeds the last 10 digits are discarded.

## Finding all leads
In Close, a lead is a company name, and each row of the input csv contained a contact from the lead, matched to the lead name. The script finds all unique lead names and sends any lead that has at least one contact to your dashboard, along with all associated contacts.

## Segmenting leads by state
Leads were segmented by state by saving them to a data structure in Python, the coding language used for the script, called a "dictionary". Dictionaries make it easy to lookup values associated with specific key, which in the case of the script were the state name abbreviations. To find the lead in the state with the most revenue, all of the lead totals for each state were stored together and compared to find both the lead with the most revenue, and then the median lead in the state.

## Clone this repository:
Look for the green box that says "Code" near the upper left hand corner of the Github page that contains this README, click on it and copy the url that is revealed. Then open a terminal and write `git clone <paste link here>`. From there, type `cd <file containing link>` and once you're in the directory that contains the script, enter `code .` in the terminal and your code editor should open and give you access to the script.

## Once the repository is cloned, create a file so that you don't push your API key to Github:
run `pip install python-dotenv`
Create a .env file by running `touch .env`
in your .env file, store your API key as:
  `API_KEY=<put you api key here>`

## Install Close Python wrapper:
`pip install closeio`

## Install package to convert state abbreviations to state name:
`pip install us`

## Run script:
`python3 close-script.py`

# And that's it!
The script should generate a file called "output.py" that will be visible in your file tree in your code editor
