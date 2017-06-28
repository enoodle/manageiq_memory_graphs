#! /usr/bin/python

import matplotlib.pyplot as plt


if __name__ == "__main__":
    time = []
    state = "new_record"
    pid_to_rss = {}
    f = open("manageiq_openshift_refresh_workers_memory", 'r')
    for line in f:
        if line.startswith("--"):
            state = "read_time"
            continue
        elif state == "read_time":
            time.append(line)
            state = "pid,rss"
            continue
        elif state == "pid,rss":
            state = "workers"
            continue
        elif state == "workers":
            pid, rss = line.strip().split(' ')
            if pid not in pid_to_rss:
                pid_to_rss[pid] = [0, ] * len(time)
            pid_to_rss[pid].append(rss)

    graph_lines = []
    for pid in pid_to_rss:
        pid_to_rss[pid].extend([0, ] * (len(time) - len(pid_to_rss[pid])))
        graph_lines.append(time)
        graph_lines.append(pid_to_rss[pid])

    plt.plot(*graph_lines)
    plt.show()

    raw_input("anykey to continue..")
