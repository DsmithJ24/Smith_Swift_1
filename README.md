# Smith_Swift_1

Daniel Smith
COMP490, MW 12:20-1:35

Must import the sqlite library, Typing from the Tuple library, json, sqlite3, pandas, and os in order to run this 
program. The used secrets.py files must be all lowercase. This program will begin by fetching data from the api 
data base including: 
    school.name
    school.city
    2018.student.size
    2017.student.size
    2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line
    2016.repayment.3_yr_repayment.overall
This totals 3203 entries which takes up 161 pages of 20 entries each. This data will be stored in an array.
Once successfully retrieved, the program will read the included 'state_M2019_dl.xlsx' file and copy select data.
About 1187 data entries should be saved and stored in json format. Once both sets of data have been read,
the program will then create an .sqlite database with the 6 parameters above.
After the database has been created, the program will take the arrays with the stored data and save it into the 
database. The api data will be stored first, then the Excel data. Once the data has been saved, a message will appear.

A few Automated Tests have been made. The first checks the data to see if at least 1000
entries have been retrieved from the api site. This test runs as intended.
The second test checks to see if jobs from all 50 states and 4 US territory jobs have been saved. 
The third tests check to see if BOTH the school table from Sprint 2 and the occupation table from Sprint 3
are both present in the database. The fourth and final test will input test entries into both files. One entry for the
schools table and three for the occupation table. The test will then check to see if the entry for the school
table has been correctly saved. The Excel part of the test will check to see if only 2 of the 3 entries
have been saved. The test will then check test to make sure the correct data has been saved.

The only thing that does not work is checking the api data for interger values that should be 0
instead of null.
