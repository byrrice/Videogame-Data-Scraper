# Videogame Data Scraper, ikn3
# Future Improvements: Remove repeat games, merge companies, allow more flexibility for main line arguments, show more graphs, do more with data

# Import libraries
import urllib.request
from bs4 import BeautifulSoup
import re
import threading
import time
import argparse
import pandas as pd

# Establish the global variables as empty arrays
rating = []
name = []
company = []
date = []

# helper method to find the string in between different substrings
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

# collect data method
def collect_data(start, end):

    # declaring the global variables
    global company
    global name
    global rating
    global date

    # go through the range specified and scrape the range of pages
    for i in range(start, end + 1):

        # accessing the url with the specified page number of parsing it via BeautifulSoup
        url = "https://www.gamerankings.com/browse.html?page={}".format(i)
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        # Scraping the html data for the videogame name, its rating, the company, and the year it was created
        init_name = soup.find_all("tr")
        temp_name = []
        temp_rating = []
        temp_comp = []
        temp_year = []

        # Modifying the string to get the desired parts
        for node in init_name:
            nm, co = node.find_all('td')[2].text.strip().split('\r\n\t\t')
            yr = co[-4:]
            temp_name.append(nm)
            temp_rating.append(node.find_all('td')[3].text.split(r'%')[0])
            temp_comp.append(co[:-6])
            temp_year.append(yr)
        # print(list(map(len,[date, name, company, rating])))

        # Extending them onto the global variables list
        date.extend(temp_year)
        name.extend(temp_name)
        company.extend(temp_comp)
        rating.extend(temp_rating)

# Write data method which writes the data to a csv as well as txt files
def write_data():

    # The global variables
    global rating
    global name
    global company
    global date

    # Writing to the dataframe
    df = pd.DataFrame(
        {
            'name':name,
            'company':company,
            'rating':rating,
            'year':date,
        }
    )

    # Converting to csv
    df.to_csv("gamesdata.csv", index=False)

    # Writing to txt files
    namefile = open("name.txt", "w")
    ratingfile = open("rating.txt", "w")
    datefile = open("date.txt", "w")
    companyfile = open("company.txt", "w")
    for l in range(0, len(company)):
        namefile.write(name[l])
        ratingfile.write(rating[l])
        datefile.write(date[l])
        companyfile.write(company[l])
        namefile.write("\n")
        ratingfile.write("\n")
        datefile.write("\n")
        companyfile.write("\n")
    namefile.close()
    ratingfile.close()
    datefile.close()
    companyfile.close()


# Defining the thread class
class myThread (threading.Thread):

    # Has threadID, given name, starting page number, ending page number, time running)
    def __init__(self, threadID, name, start_int, end_int):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.start_int = start_int
        self.end_int = end_int
        self.time = 0

    # Collect the necessary data and time the process
    def run(self):
        print("Starting " + self.name)
        tic = time.clock()
        collect_data(self.start_int, self.end_int)
        toc = time.clock()
        self.time = round(toc - tic, 2)
        print("Exiting " + self.name)

# Main method takes nthreads and npages
def main(nthreads, npages):

    # Number of pages must be divisible by nthreads to work
    if npages % nthreads != 0:
        raise ValueError("Number of pages must be divisible by number of threads.")

    # Create list of threads with specified interval
    threads = []
    pagesper = npages//nthreads
    for i in range(nthreads):
        ub = min((i+1)*pagesper, npages) - 1
        lb = i * pagesper
        threads.append(myThread(i + 1, "Thread {}".format(i + 1), lb, ub))

    # Start the threads and open the time file
    timefile = open("time.txt", "w")
    for thread in threads:
        thread.start()

    # Write to the time file after joining to ensure all threads are measured correctly
    for thread in threads:
        thread.join()
        timefile.write("Thread {}: ".format(thread.threadID) + str(thread.time) + "\n")

    # Close file and write all the data
    timefile.close()
    write_data()

# Defining the arguments taken in by the main method
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input num of threads and num of pages.')
    parser.add_argument('nthreads', type=int,
                        help='Number of threads')
    parser.add_argument('npages', type=int,
                        help='Number of pages')

    args = parser.parse_args()
    main(args.nthreads, args.npages)





