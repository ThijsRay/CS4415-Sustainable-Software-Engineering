from argparse import ArgumentParser
from re import A
from experiment import get_browsers, get_sites
import numpy as np
import matplotlib.pyplot as plt
import sigfig

def main():
    sites = get_sites()

    parser = ArgumentParser(description='Run selenium tests with or without uBlock Origin')
    parser.add_argument('--date',type=int, default=1646053732, help="Which amount of seconds is used as date in results folders")
    parser.add_argument('--n_iterations', type=int, default=6, help="How many times the loop was executed")
    args = parser.parse_args()
    

    visualization_index = 0 # Core usage (0=core, 1=cpu, 2=duration)

    visualize(sites, args.date, args.n_iterations, visualization_index)

def read_result(site, date, i, adblocker_used):
    results = []
    with open(f"results/{date}-{i}/{site}_{adblocker_used}") as file:
        #Discard first line (header)
        file.readline()
        line = file.readline()
        while line != "":
            results.append(read_usage(line))
            line = file.readline()
    results = np.average(results, axis=0)
    return results

def read_usage(line):
    data = line.split(";")
    core, cpu_usage, duration, exit_code = data
    if int(exit_code) == 0:
        return [int(core) / 1000000.0, int(cpu_usage) / 1000000.0, int(duration)]
    else:
        return None

def visualize(sites, date, n, visualization_index):
    data = {}
    for site in sites:
        data[site] = {}
        for ad_blocker_used in [True, False]:
            print(f"Reading results for {n} iterations: {[read_result(site, date, i, ad_blocker_used) for i in range(n)]}")
            data[site][ad_blocker_used] = [read_result(site, date, i, ad_blocker_used) for i in range(n)]
    data["average"] = {}
    data["average"][True] = [np.average([data[site][True][i] for site in sites], axis=0) for i in range(n)]
    data["average"][False] = [np.average([data[site][False][i] for site in sites], axis=0) for i in range(n)]


    sites.append("average")
    for site in sites:
        generate_boxplot_per_site(data, site, visualization_index, n)

    generate_large_boxplot(data, sites, visualization_index, n)
    print_table(data, sites, visualization_index, n)

def extract_result_on_index(data, site, index_prop, n):
    return [[data[site][True][i][index_prop] for i in range(n)], [data[site][False][i][index_prop] for i in range(n)]]

def generate_boxplot_per_site(data, site, index_prop, n):
    fig = plt.figure(figsize =(10, 7))
    plt.boxplot(extract_result_on_index(data, site, index_prop, n))
    plt.title(f"Energy consumption {site}")
    plt.ylabel(f"Energy consumption (GJ")
    plt.xticks([1, 2], labels=["With adblocker", "Without adblocker"])
    plt.savefig(f"results/boxplot-{site}-{index_prop}")
    # plt.show()

#######################################################################################################
# Two-color boxplot, based on https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots  #
#######################################################################################################
# function for setting the colors of the box plots pairs
def generate_large_boxplot(data, sites, index_prop, n):
    def setBoxColors(bp):
        plt.setp(bp['boxes'][0], color='blue')
        plt.setp(bp['caps'][0], color='blue')
        plt.setp(bp['caps'][1], color='blue')
        plt.setp(bp['whiskers'][0], color='blue')
        plt.setp(bp['whiskers'][1], color='blue')
        plt.setp(bp['fliers'][0], color='blue')
        plt.setp(bp['fliers'][1], color='blue')
        plt.setp(bp['medians'][0], color='blue')

        plt.setp(bp['boxes'][1], color='red')
        plt.setp(bp['caps'][2], color='red')
        plt.setp(bp['caps'][3], color='red')
        plt.setp(bp['whiskers'][2], color='red')
        plt.setp(bp['whiskers'][3], color='red')
        plt.setp(bp['medians'][1], color='red')

    fig = plt.figure()
    ax1 = plt.axes()
    pos = [1, 2]
    for site in sites:
        bp = plt.boxplot(extract_result_on_index(data, site, index_prop, n), positions = pos, widths = 0.6)
        setBoxColors(bp)
        pos[0] += 3
        pos[1] += 3

    # set axes limits and labels
    plt.xlim(0,3*len(sites))
    ax1.set_xticklabels(sites)
    ax1.set_xticks([1.5 + 3*n for n in range(len(sites))])

    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('With adblocker', 'Without adblocker'))
    hB.set_visible(False)
    hR.set_visible(False)

    plt.ylabel(f"Energy consumption (GJ)")
    plt.title(f"Energy comparison of using adblocker (n={n})")
    plt.savefig('results/boxplot-complete.png')
    # plt.show()

def print_table(data, sites, index_prop, n):
    table_string = "| Website | Average Energy Consumption with adblocker (GJ) | Average Energy Consumption with adblocker (GJ)| Change |\n| --- | --- | --- | --- |"

    for site in sites:
        extracted = extract_result_on_index(data, site, index_prop, n)
        with_adblocker = np.average(extracted[0])
        without_adblocker = np.average(extracted[1])
        percentual_change = round(float(with_adblocker - without_adblocker) / float(without_adblocker) * 100.0, 2)
        table_string += f"\n| {site.capitalize()} | {sigfig.round(with_adblocker, sigfigs=4)} | {sigfig.round(without_adblocker, sigfigs=4)} | {percentual_change}% |"

    print(table_string)

if __name__ == "__main__":
    main()