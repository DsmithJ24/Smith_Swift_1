import Secrets
import requests
#when using debugger, wait a sec for everything to load
url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?"
outfile = open(r"api_data.txt", "w")

def get_data():
    #will need:
        #school name
        #school city
        #2018 student size
        #2017 student size
        #2017 earnings (3 years after completion.overall count over poverty line)
        #2016 repayment (3 year repayment.overall)

    all_data = []
    #test url: https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=school.state,2018.student.size&api_key=QIht2JJOGAwBJal0uCKw8bURSlaHd5gOGxmlbP3g
    #add parameters between {url} and &api_key=

    #will need to figure out how much data there is and how to walk through it all
    #gets: 3203 elements and 20 per page. will need 161 pages
    for page in range(162):
        #put additional fields after &fields=
        response = requests.get(f"{url}school.degrees_awarded.predominant=2,3&fields=school.name,school.state,"
                                f"2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall&api_key={Secrets.api_key}&page={page}") #put the api url here
        if response.status_code != 200:
            print("Error getting data!")
            #exit(-1)
            #do not exit, continue
            continue

        #following code puts data in .json format
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
        #print(page)

    return all_data

#need function to save data in a document

def main():
    demo_data = get_data()
    print(demo_data, file=outfile)
    outfile.close()
    print("Data has been saved to a file")

if __name__ == '__main__':
    main()