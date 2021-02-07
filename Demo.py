import secrets
import requests
import json
#when using debugger, wait a sec for everything to load
url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
outfile = open(r"api_data.txt", "w")

def get_data():
    #will retrieve:
        #school name
        #school city
        #2018 student size
        #2017 student size
        #2017 earnings (3 years after completion.overall count over poverty line)
        #2016 repayment (3 year repayment.overall)

    all_data = []
    #gets: 3203 elements and 20 per page. will need 161 pages
    #for page in range(162):
    page = 0
    NextPage = True

    #Stops if it hits a false
    while NextPage != False:
        #print(page)
        #put additional fields after &fields=
        response = requests.get(f"{url}school.degrees_awarded.predominant=2,3&fields=school.name,school.state,"
                                f"2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}&page={page}") #put the api url here
        if response.status_code != 200:
            print("Error getting data!")
            #exit(-1)
            #do not exit, continue
            page = page + 1
            continue

        #following code puts data in .json format
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
        NextPage = check_page(page_of_school_data)
        page=page+1
    print("Total number of pages is", page)
    return all_data

def check_page(page):
    if len(page) < 20:
        return False
    elif len(page) > 20:
        print("Entries exceed page!!!")
        pass
    else:
        pass

#takes the retrieved data and saves it to a .txt file
def main():
    demo_data = get_data()
    print(json.dumps(demo_data, indent=6), file=outfile)
    #will create a .txt file with 25626 lines. 25626/8 = 3203 entries as expected
    outfile.close()
    print("Data has been saved to a file")

if __name__ == '__main__':
    main()