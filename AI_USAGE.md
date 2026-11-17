AI Usage Report: Job Application Tracker
What AI was used for
Code development: Generating and organizing code for the Flask app, the MySQL database scripts, the Job Match feature and the automated tests, based on the assignment requirements.
Troubleshooting: Explaining error messages from the terminal and VS Code, and suggesting fixes during setup on Windows.
Documentation: Shortening and updating the README and organizing the troubleshooting log.
Problems that occurred
VS Code could not find Python or pytest. No virtual environment had been set up, and VS Code was using Python 3.15, which had none of the required packages installed.
PowerShell didn't recognize commands. Commands like -m pip and test were typed incompletely instead of python -m pip and python -m pytest.
MySQL "Access denied" (using password: NO). The .env file with the database password hadn't been created, so the app connected without a password.
"'Interview Scheduled' is not among the defined enum values." The database had been built from an earlier script that used a status the assignment doesn't allow. It was rebuilt from the project's schema.sql and seed.sql.
All four problems were resolved. The app runs with all pages connected to MySQL, and all 25 automated tests pass.

Other Common Problems (General)
These problems didn't happen in this project, but they come up often when building Flask + MySQL websites like this one.

Deleting a record that other records depend on. Deleting a company that still has jobs or contacts linked to it is blocked by the database's foreign keys. The app needs to show a clear message instead of crashing.
Port already in use. Starting the app while another copy is still running causes an "Address already in use" error.
Virtual environment not activated. Opening a new terminal and running the app without activating the venv causes "No module named flask".
MySQL service stopped. After a restart, MySQL may not be running, which causes "Can't connect to MySQL server".
Invalid or empty form input. Users can leave required fields blank or type text into number fields, so input has to be checked on the server before saving.
Duplicate records. Double-clicking Save or refreshing the page can submit a form twice unless the app redirects after saving.
SQL injection and special characters. Putting user text straight into a query can break on an apostrophe and lets attackers run their own SQL. Parameterized queries prevent this.
Secrets committed to GitHub. Uploading the .env file shares the database password publicly. It should be listed in .gitignore.
Debug mode left on. Running Flask with debug mode in production shows error details and an interactive console to anyone.
Date and time format issues. Dates entered in the browser may not match the format MySQL expects, causing save errors or wrong dates.
Character encoding problems. Names with accents or emojis can show up garbled unless the database uses utf8mb4.
Browser caching old CSS or JavaScript. Style or script changes don't appear until the page is hard-refreshed with Ctrl + F5.
Layout breaking on phones. Tables and forms that look fine on a laptop can overflow on small screens without responsive styling.
What Worked Well
Pasting exact error messages. Giving the AI the full terminal output, not just "it doesn't work", led to quick and accurate explanations.
Automated tests. Running python -m pytest after each fix made it easy to confirm nothing else had broken.
Keeping the password in .env. Once the file was set up, the app connected to MySQL every time without changing any code.
Building the database from the project's SQL files. Re-running schema.sql and seed.sql gave a clean, consistent database in under a minute.
Updating the README as problems came up. The setup steps now match what actually works on Windows.
Lessons Learned
AI suggestions have to be checked on my own computer. Its first setup steps assumed a different Python version than the one I had.
Errors are often about the setup or the data, not the code. Three of the four problems had nothing to do with the app's code.
Small details in error messages matter, such as "using password: NO" versus "YES".
The database and the code have to match exactly, including allowed values like application statuses.
A virtual environment should be created and activated before anything else in a Python project.
Writing problems down as they happen makes the final documentation much easier.