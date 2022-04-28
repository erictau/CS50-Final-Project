# Project Budget Tracker
#### Video Demo:
#### Description:
##### Overview
The Project Budget Tracker is a web application that can be utilized by project managers as a simple budget tracking tool. Many project managers opt for spreadsheet softwares such as Excel or Google Sheets to manage their budgets, create dashboards, and organize their billing processes. This tool is built with the intention of replacing the standard spreadsheet systems to abstract away the logic from the end user. 

##### Benefits Over a Spreadsheet
Spreadsheets are highly customizable, however the data stored in cells are susceptible to accidental changes. Additionally, the equations built in to spreadsheet cells can become very complex when conditional statements and calculations are copied for entire columns or rows. This app is designed to only allow the user access to certain functions, such as setting up the project, adding a transaction, modifying an existing transaction, etc. Any actions they perform are handled through post requests to the back end, which take in the user input and update the database and browser automatically. All the logic is handled on the server side, so the user does not need to worry about inconsistencies in calculation methods or cell formulas. 

##### New Topics Learned
Below are several topics I had to research to develop this project:

###### Setup Local Development Environment
To prepare myself for life beyond CS50, I followed the "Developing Your Project Locally with VS Code" CS50 Seminar to set up a development environment on my Macbook Air M1. I had to install VS Code, the latest Python, Node.js, npm, Flask, and SQLite3. Setting up the development environment is a challenge in itself, as many of the tools used require command line installations rather than the traditional method of installing applications with .dmg or .exe files. Going through this process helped get me acquainted with using pip and npm to install modules and packages for use in my application.

###### Git & GitHub
Git and GitHub are known to be extremely popular version control tools. I was already familiar with the idea of Git, but setting up a remote repository and learning the command line functions to initiate, add files, commit, and push helps ingrain the process of using Git. Additionally, it was helpful to view my git commits on the VS Code timeline to quickly understand where I made changes since my last commit. 

###### Python Virtual Environment
When setting up my local development environment, I came across some Python "Best Practices" that suggested that a virtual environment is always used when developing Python apps. The virtual environmment is used so the project starts with a clean set of dependencies, independent of the global packages installed on the development machine. Any dependencies required in the application will be installed to the virtual environment, and a "pip freeze > requirements.txt" command line function will populate the requirements.txt file with all installed packages and version numbers so the environment can be recreated on any machine that runs this application. 

###### ChartJS
ChartJS is a data visualization tool for HTML pages. In developing a budget dashboard, a bar graph is essential in visualizing the budget remaining quickly. The ChartJS CDN is listed in the index.html (dashboard page) and the bar graph takes data passed in from Flask (via the database) to present the current budgets. The bar graph required some customization, such as labeling, bar colors, bar widths, and minimum values. 

###### Bootstrap Navbar and Modal
The Bootstrap Navbar and Modal were utilized in this project. The Navbar was set up in a layout.html page which allowed for the same Navbar to be shown on every webpage that extended layout.html. This Navbar is mobile responsive with a "-lg" breakpoint, meaning the Navbar becomes a collapsible dropdown menu once the screen is below 992px. Above 992px, the Navbar is a standard Navbar that shows links to the other pages in the web app. 


##### Description of Each File

###### app.py
This web application is developed with Flask, so an app.py file is required to configure and run the application. This file contains all the routes and back end logic for the application. 

###### helpers.py
Helpers.py is an additional python file to store miscellaneous functions used in app.py. 

###### layout.html
This layout file contains the HTML layout template for the rest of the web app. The HTML head and Navbar are coded in this file, and Jinja is used to allow other HTML files to "extend" this layout. The other HTML files only contain the "main" part of the HTML page.

###### index.html
The home page of the web app serves as the Project Dashboard. This is where you will find the Project Information such as Project Name, Project Owner, Start Date, End Date, and Project Duration. "Setup Project" and "Clear Project" buttons are also in this section, allowing the user to initialize a project budget with new descriptions and dollar amounts. Both of these buttons lead to modals which are pop ups that require clicking an additional button prior to the respective action to occur. The "Setup Project" button sends a post request to "/" with a value of "setup", and the "Clear Project" button sends a post request to "/" with a value of "clear". When posting "setup" to "/", the back end logic checks first to see if the project is already set up. If the project is already set up, the user is redirected back to "/". If it is not set up, the user is redirected to "/setup" to set the project up. When posting "clear" to "/", the back end logic clears the rows in each table in the database. Once the database tables are cleared, project setup is allowed. 

A bar graph and budget table are presented below the Project Information section. Data is passed in through Flask to populate the bar graph and budget table. The bar graph is created by utilizing ChartJS, a chart tool for HTML. The table is populated using a Jinja for loop that iterates through a list of dictionaries that was passed from Flask. This data is re-calculated and updated upon each "GET" request. 

###### transactions.html
The transactions page includes a "Add Transactions" section and a "Transaction History" section. The "Add Transactions" section is a form that posts to "/transactions" which contains 3 separate text inputs. The Letter, Amount, and Notes are user-inputted data, but the transaction number and date are auto-filled by SQLite. Once a transaction is added, the transaction shows up immediately in the "Transaction History" section below where all transactions are sorted by their transaction numbers. A Jinja for loop is used here to create the "Transaction History" table. 

###### setup.html
The setup page consists of a form to populate the project data and budget categories. All project information must be populated, but the budget categories do not all need to be filled. There are currently only 5 spots for categories, and this was hard coded in. Future features include user customizability for number of budget categories. The form posts to "/setup", which takes the data, validates the inputs, and updates the appropriate database tables. Once a project is set up, the setup page can no longer be accessed until the project is cleared. 

###### apology.html
This apology page is utilized for input validation. This project uses the same apology page as the finances pset. 

###### budget.db
This database is accessed through SQLite3. This database contains 4 tables: "info", "budgets", "transactions", and "original_budgets". Project data is stored here.

###### style.css
Custom CSS styling to overwrite Bootstrap classes or set defaults for specific tags are found in this file.

###### requirements.txt
Requirements.txt is a standard file to include with Python applications. This file contains a list of all packages and version numbers used by the application, and can be sent to any other machine to mimic the project dependencies such that the environment can be recreated. 
