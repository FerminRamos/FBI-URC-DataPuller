# FBI-URC-DataPuller
This repository contains data pulled from the [FBI's URC database](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi). 

It includes:
1. python code (for you to modify it according to your needs)
2. "List of ALL U.S. Agencies.csv" - List of ALL Law Enforcement Agencies in the U.S.
    * This file last updated w/ real data on 06/27/23
3. "My Agencies.csv" - A subset of *List of ALL U.S. Agencies.csv*. The file *List of Crimes per Agency.csv* gathers crime statistics on these agencies.
4. "List of Crimes per Agency.csv" - Statistics on all offenses documented per each agency, for any given year.
    * This file last updated w/ real data (for New Mexico) on 09/05/23

*Examples of these files can be seen in this repository*

<br>

### How do I run your code?
1. Download the "FBI Database Puller.py" python file
2. Get an API key to run this code (see section "How do I get an API key" below)
3. Copy/Paste your API key into the "FBI Database Puller.py" python file (where it says "INSERT_YOUR_API_KEY_HERE")
4. Make sure you have all the necessary CSV files
5. Run the program 👍

<br>

### You have a list of crimes per agency on all departments in NM, but I want to see the crime statistics from another state, how do I do this?
1. See section "How do I run your code" and make sure this works before moving on with this section.
2. Open a file called "List of ALL U.S. Agencies.csv" and COPY whatever agencies you want (i.e. all agencies that belong to Utah, Texas, Maine, etc.)
3. Open a file called "My Agencies.csv" and PASTE the agencies you just copied. (Make sure to include the header)
4. run the code with the function "getSummarizedData(startYear=2000, endYear=2006)" uncommented.
    * Feel free to change the years
5. Run the code (may take a few minutes)
6. Open a file called "List of Crimes per Agency.csv" and see your results 🙂

<br>

### How do I get an API key?
1. Go to the FBI developer's page and sign up for an API key: [https://api.data.gov/signup/](https://api.data.gov/signup/)
2. Enter your name, email, etc.
3. Check your inbox for an email containing your personal API key (do not share with anyone!)
