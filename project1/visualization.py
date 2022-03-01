from argparse import ArgumentParser
from distutils.command.sdist import sdist
from re import A
from experiment import get_browsers, get_sites
import numpy as np
import matplotlib.pyplot as plt
import sigfig

RESULT_FOLDER = "results"
PLOT_FOLDER = "img"
UNIT_OF_METRICS = {
    "power of core": "W",
    "power of cpu": "W",
    "energy consumption of core": "J",
    "energy consumption of cpu": "J",
    "duration": "s"
}

def main():
    sites = [key for key in get_sites().keys()]

    parser = ArgumentParser(description='Run selenium tests with or without uBlock Origin')
    parser.add_argument('--date',type=int, default=1646053732, help="Which amount of seconds is used as date in results folders")
    parser.add_argument('--n_iterations', type=int, default=6, help="How many times the loop was executed")
    parser.add_argument('--metric', type=str, default="power of core", choices=UNIT_OF_METRICS.keys(), help="What metric to visualize")
    args = parser.parse_args()

    visualize(sites, args.date, args.n_iterations, args.metric)

def read_result(site, date, i, adblocker_used):
    results = []
    with open(f"{RESULT_FOLDER}/{date}-{i}/{site}_{adblocker_used}") as file:
        #Discard first line (header)
        file.readline()
        line = file.readline()
        while line != "":
            usage = read_usage(line)
            if usage is not None:
                results.append(usage)
            line = file.readline()
    if results != []:
        return np.average(results, axis=0)
    return None

def read_usage(line):
    data = line.split(";")
    core, cpu_usage, duration, exit_code = data
    if int(exit_code) == 0:
        return [int(core), int(cpu_usage), int(duration)]
    else:
        print("exit code -1")
        return None

def visualize(sites, date, n, metric):
    data = {}
    for site in sites:
        data[site] = {}
        for ad_blocker_used in [True, False]:
            data[site][ad_blocker_used] = [read_result(site, date, i, ad_blocker_used) for i in range(n) if read_result(site, date, i, ad_blocker_used) is not None]
    data["average"] = {}
    data["average"][True] = [np.average([data[site][True][i] for site in sites if len(data[site][True]) > i and len(data[site][False]) > i], axis=0) for i in range(n)]
    data["average"][False] = [np.average([data[site][False][i] for site in sites if len(data[site][True]) > i and len(data[site][False]) > i], axis=0) for i in range(n)]


    sites.append("average")
    for site in sites:
        generate_boxplot_per_site(data, site, n, metric)

    generate_large_boxplot(data, sites, n, metric)
    print_table(data, sites, n, metric)

def extract_metric(site_data, metric):
    if metric == "power of core":
        return [float(sd[0]) / float(sd[2]) for sd in site_data]
    elif metric == "duration":
        return [int(sd[2]) / 1000000.0 for sd in site_data]
    elif metric == "power of cpu":
        return [float(sd[1]) / float(sd[2]) for sd in site_data]
    elif metric == "energy consumption of core":
        return [float(sd[0]) / 1000000.0 for sd in site_data]
    elif metric == "energy consumption of cpu":
        return [float(sd[1]) / 1000000.0 for sd in site_data]


def extract_metric_of_site(data, site, metric):
    return [extract_metric(data[site][True], metric), extract_metric(data[site][False], metric)]

def generate_boxplot_per_site(data, site, n, metric):
    fig = plt.figure(figsize=(10, 7))
    plt.boxplot(extract_metric_of_site(data, site, metric))
    plt.title(f"Energy comparison of {site}")
    plt.ylabel(f"{metric.capitalize()} ({UNIT_OF_METRICS[metric]})")
    plt.xticks([1, 2], labels=["With adblocker", "Without adblocker"])
    plt.savefig(f"{PLOT_FOLDER}/boxplot-{site}-{metric}")
    # plt.show()

#######################################################################################################
# Two-color boxplot, based on https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots  #
#######################################################################################################
# function for setting the colors of the box plots pairs
def generate_large_boxplot(data, sites, n, metric):
    def setBoxColors(bp):
        plt.setp(bp['boxes'][0], color='blue')
        plt.setp(bp['caps'][0], color='blue')
        plt.setp(bp['caps'][1], color='blue')
        plt.setp(bp['whiskers'][0], color='blue')
        plt.setp(bp['whiskers'][1], color='blue')
        # plt.setp(bp['fliers'][0], color='blue')
        # plt.setp(bp['fliers'][1], color='blue')
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
        # if metric == "duration":
        #     bp = plt.scatter(extract_metric_of_site(data, site, metric), lineoffsets=pos, linewidth=0.75, orientation="vertical")
        # else:
        bp = plt.boxplot(extract_metric_of_site(data, site, metric), positions = pos, widths = 0.6)
        setBoxColors(bp)
        pos[0] += 3
        pos[1] += 3

    # set axes limits and labels
    plt.xlim(0,3*len(sites))
    ax1.set_xticklabels(sites)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_xticks([1.5 + 3*n for n in range(len(sites))])

    # draw temporary red and blue lines and use them to create a legend
    hB, = plt.plot([1,1],'b-')
    hR, = plt.plot([1,1],'r-')
    plt.legend((hB, hR),('With adblocker', 'Without adblocker'))
    hB.set_visible(False)
    hR.set_visible(False)

    plt.ylabel(f"{metric.capitalize()} ({UNIT_OF_METRICS[metric]})")
    plt.title(f"Energy comparison of using adblocker (n={n})")
    plt.tight_layout()
    plt.savefig(f'{PLOT_FOLDER}/boxplot-complete-{metric}.png')
    # plt.show()

def print_table(data, sites, n, metric):
    table_string = f"| Website | Average {metric} with adblocker ({UNIT_OF_METRICS[metric]}) | Average {metric} without adblocker ({UNIT_OF_METRICS[metric]})| Change |\n| --- | --- | --- | --- |"

    for site in sites:
        extracted = extract_metric_of_site(data, site, metric)
        with_adblocker = np.average(extracted[0])
        without_adblocker = np.average(extracted[1])
        percentual_change = round(float(with_adblocker - without_adblocker) / float(without_adblocker) * 100.0, 2)
        table_string += f"\n| {site.capitalize()} | {sigfig.round(with_adblocker, sigfigs=4)} | {sigfig.round(without_adblocker, sigfigs=4)} | {percentual_change}% |"

    print(table_string)

if __name__ == "__main__":
    main()