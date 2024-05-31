#! /usr/bin/env python3
'''
This is a utility to plot a daily periodic schedule.

Requirement
------------------

python3

matplotlib

numpy

'''


import argparse
import tomllib
import numpy as np
import matplotlib.pyplot as plt


def getargs():
    parser = argparse.ArgumentParser(description="plot daily periodic schedule")
    parser.add_argument("schedual", help="Assignment file")
    parser.add_argument("--conf", help="configuration file", required=True)
    parser.add_argument("--out", help="out file name",default='out')
    args = parser.parse_args()
    return args.conf, args.schedual, args.out


def read_conf(conf_file):
    conf = tomllib.load(open(conf_file, "rb"))
    return conf


def read_schedual(schedual_file):
    data = [line.rstrip().split('\t') for line in open(schedual_file)]
    return data


def calcu_theta_offset(start_time: str, end_time: str) -> tuple:
    '''
    Parameters
    -------------

    Returns
    -------------
    '''
    start_time = start_time.split(":")
    start_time = int(start_time[0]) + int(start_time[1]) / 60
    end_time = end_time.split(":")
    end_time = int(end_time[0]) + int(end_time[1]) / 60
    theta = start_time / 24 * np.pi * 2
    if end_time >= start_time:
        offset = (end_time - start_time) / 24 * np.pi * 2
    else:
        offset = (end_time + 24 - start_time) / 24 * np.pi * 2
    return (theta, offset)


def plot_ring(ax, ring_color):
    theta = [0] * 5
    height = [2] + [1] * 4
    bottom = [0] + list(range(2, 6))
    width = [np.pi * 2] * 5
    ring_id = ['r' + str(idx) for idx in range(5)]
    color = [ring_color[ele] for ele in ring_id]
    ax.bar(theta, height, bottom=bottom, width=width, color=color)


def plot_time_ticks(ax, n, ymin, ymax, color="black", lw=1, label=[]):
    vline_pos = np.arange(0, 1, 1 / n) * np.pi * 2
    ymin = [ymin] * n
    ymax = [ymax] * n
    ax.vlines(vline_pos, ymin, ymax, color=color, lw=lw)


def add_schedual(ax, schedual, sch_color):
    for sch in schedual:
        start_time, stop_time, sch_type = sch
        theta, offset = calcu_theta_offset(start_time, stop_time)
        theta = -theta - np.pi * .5
        offset = -offset
        ax.bar(theta, 1, width=offset, align="edge", bottom=6, color=sch_color[sch_type], label=sch_type)


def plot_time_label(ax):
    t = ax.text(.5 * np.pi, .7, 'Daily', verticalalignment='center', horizontalalignment='center', fontsize=15)
    t = ax.text(0, 0, 'Periodic', verticalalignment='center', horizontalalignment='center', fontsize=15)
    t = ax.text(1.5 * np.pi, .7, 'Schedule', verticalalignment='center', horizontalalignment='center', fontsize=15)
    t = ax.text(0, 2.5, '18', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(.5 * np.pi, 2.5, '12', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(np.pi, 2.5, '6', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(1.5 * np.pi, 2.5, ' 0/24', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(0.25 * np.pi, 3.5, '15', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(0.75 * np.pi, 3.5, '9', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(1.25 * np.pi, 3.5, '3', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')
    t = ax.text(1.75 * np.pi, 3.5, '21', verticalalignment='center', horizontalalignment='center', fontsize=13, color='white')


def modify_plot_add_legend(ax):
    ax.margins(0, 0)
    spins = ax.spines
    spins['polar'].set_visible(False)
    ax.grid(False)
    ax.set_xticks([],[])
    ax.set_yticks([], [])
    handles, labels = ax.get_legend_handles_labels()
    lab_dic = {}
    for ele in zip(labels, handles):
        lab_dic[ele[0]] = ele[1]
    labels = list(lab_dic.keys())
    handles = []
    for key in labels:
        handles.append(lab_dic[key])
    le = ax.legend(handles, labels, bbox_to_anchor=(.9, 1))
    le_patch = le.legendPatch
    le_patch.set_alpha(1)


def main():
    conf, schedual, out = getargs()
    conf = read_conf(conf)
    schedual = read_schedual(schedual)
    fig = plt.figure(figsize=(6, 6), layout='constrained', facecolor='#ffffff00')
    ax = fig.add_subplot(projection='polar')
    plot_ring(ax, conf["ticks-ring-color"])
    plot_time_ticks(ax, 4, ymin=2, ymax=6, lw=2.0)
    plot_time_ticks(ax, 8, ymin=3, ymax=6, lw=1.5)
    plot_time_ticks(ax, 24, ymin=4, ymax=6, lw=1.0)
    plot_time_ticks(ax, 24 * 4, ymin=5, ymax=6, lw=.5)
    add_schedual(ax, schedual, conf['schedual-type'])
    plot_time_label(ax)
    modify_plot_add_legend(ax)

    fig.savefig(out + ".svg")


if __name__ == "__main__":
    main()