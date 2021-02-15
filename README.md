# Smith_Swift_1

Daniel Smith
COMP490, MW 12:20-1:35

Must import the sqlite library and Typing from the Tuple library in order to run this program. 
The used secrets.py files must be all lowercase. This program will fetch data from the api data base including: 
    school.name
    school.city
    2018.student.size
    2017.student.size
    2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line
    2016.repayment.3_yr_repayment.overall
This totals 3203 entries which takes up 161 pages of 20 entries each. This data will be stored in an array.
Once successfully retrieved, the data will be checked to determine if at least 1000 entries have been obtained.
If not, the program will end. Note that the data takes a while to retrieve. 
The program will print out a message detailing the number of entries obtained if the minimum requirement has been met.
If enough data has been confirmed the program will then create an .sqlite database with the 6 parameters above.
After the database has been created, the program will take the array with the stored data and save it into the database.
Any expected integer entries with a 'None' will be saved as 0 instead.
Once the data has been saved, a message will appear.
