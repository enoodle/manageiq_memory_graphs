#! /usr/bin/python

import matplotlib.pyplot as plt
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Displays graphs from ErezGraph format')
    parser.add_argument(
            'filename',
            help="name of the graph file")
    args = parser.parse_args()

    time = []
    state = "new_record"
    ems_names = {}
    f = open(args.filename, 'r')
    for line in f:
        if line.startswith("--"):
            state = "read_time"
            continue
        elif state == "read_time":
            time.append(line)
            state = "pid,rss,command"
            continue
        elif state == "pid,rss,command":
            state = "workers"
            continue
        elif state == "workers":
            details = line.strip().split(' ')
            rss = details[1]
            ems = details[-1]
            # import pdb; pdb.set_trace()
            if ems not in ems_names:
                ems_names[ems] = [0, ] * len(time)
            ems_names[ems].append(rss)

    graph_lines = []
    for ems in ems_names:
        ems_names[ems].extend([0, ] * (len(time) - len(ems_names[ems])))
        graph_lines.append(time)
        graph_lines.append(ems_names[ems])

    plt.plot(*graph_lines)
    plt.show()

    raw_input("anykey to continue..")
