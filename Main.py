import numpy as np
import matplotlib.pyplot as plt
import Scraper
import re
import argparse
from Plot import plotit

# Graphing all the times
def main(nthreads1, nthreads2, nthreads3, nthreads4, nthreads5, npages):

    # Scraping the pages using the requisite number of threads
    Scraper.main(nthreads1, npages)
    avg1 = findtime()
    Scraper.main(nthreads2, npages)
    avg2 = findtime()
    Scraper.main(nthreads3, npages)
    avg3 = findtime()
    Scraper.main(nthreads4, npages)
    avg4 = findtime()
    Scraper.main(nthreads5, npages)
    avg5 = findtime()

    # Adding data to numpy arrays for further processing
    threads = np.array([nthreads1, nthreads2, nthreads3, nthreads4, nthreads5])
    times = np.array([avg1, avg2, avg3, avg4, avg5])

    # Writing to txt files
    txtfile = open("{}pages.txt".format(npages), "w")
    for i in range(len(threads)):
        txtfile.write("Average time for {} thread(s): {}\n".format(threads[i], round(times[i], 2)))
    txtfile.close()

    # Graph the necessary data
    plt.figure(1)
    plt.title("For {} Pages".format(npages))
    plt.xlabel("Number of Threads")
    plt.ylabel("Average Time(s)")
    plt.plot(threads, times, 'ko-')
    plt.xticks(np.arange(min(threads), max(threads)+1, 1.0))
    plt.yticks(np.arange(0, int(max(times))+1, 1.0))
    plt.grid(b=True, which='major', color='k', linestyle='-')
    plt.savefig("{}img.png".format(npages))
    plotit()
    plt.show()

# Helper method for finding the average time
def findtime():
    file = open("time.txt", "r").read().splitlines()
    total = 0
    for i in range(len(file)):
        file[i] = float(file[i].split(": ", 1)[1])
        total += file[i]
    return total/len(file)

# Main method that takes in all inputs
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input num of threads (5 iterations) and num of pages (MUST BE DIVISIBLE BY NUMTHREAD).')
    parser.add_argument('nthreads1', type=int,
                        help='Number of threads for 1st iteration')
    parser.add_argument('nthreads2', type=int,
                        help='Number of threads for 2nd iteration')
    parser.add_argument('nthreads3', type=int,
                        help='Number of threads for 3rd iteration')
    parser.add_argument('nthreads4', type=int,
                        help='Number of threads for 4th iteration')
    parser.add_argument('nthreads5', type=int,
                        help='Number of threads for 5th iteration')
    parser.add_argument('npages', type=int,
                        help='Number of pages')

    args = parser.parse_args()
    main(args.nthreads1, args.nthreads2, args.nthreads3, args.nthreads4, args.nthreads5, args.npages)