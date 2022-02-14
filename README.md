# WMGTSS-QA-1942818

# All Python was written in 3.7

# GitHub link: https://github.com/OHammond1-th/WMGTSS-QA-1942818

### MAKE SURE TO RUN ANY PYTHON SCRIPT FROM THE VENV LOCATED IN <Directory where download/git-clone is>\WMGTSS-QA-1942818\Source\QA_Board ###
### OTHERWISE WINDOWS WILL TRY TO USE YOUR LOCAL INSTALLATION										  ###


Get the following dependancies online:
https://www.pgadmin.org/download/
https://www.postgresql.org/download/

When you are in pgAdmin setup a user and create two databases named:

WMGTSS_QA
WMGTSS_QA_TEST

Inside of one of the databases right-click the name in the explorer and select "Query Tool", then paste the code from the file "WMGTSS-QA-1942818\DB_Schema\users_and_roles.sql" and hit run.
Then go to both databases and using the query tool manually copy and paste the schema code from "WMGTSS-QA-1942818\DB_Schema\WMGTSS_QA_SCHEMA.sql" and run it.


From the given directory run this command with the tags replaced by your Postgres username and password:

directory: <Directory where download/git-clone is>\WMGTSS-QA-1942818\Source\QA_Board\Setup
script: python3 setup_dbs.py <your_username> <your_password>
-- please note that on some installations of python you need to replace python3 with py


If you would like to inject some test data there are some scripts that will do this for users, courses and their association known as enrollments.
These can be found here:

<Directory where download/git-clone is>\WMGTSS-QA-1942818\Source\QA_Board\Testing\Database\Scripts


You can also manually input the data either using the WMG_admin_tool(WIP) or by running the create_<db_table_row> scripts that can be found in the
main QA_BOARD directory.

Admin-tool password = warwickuni22


To run the website open a command window in the QA_BOARD directory and perform this command:

python3 main.py
-- please note that on some installations of python you need to replace python3 with py

-- please note that all web styling was performed on a 2560x1440 monitor so visuals may vary, this would be updated on the final product