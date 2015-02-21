#!/usr/bin/python

import optparse
from random import randrange

def spin():
	return randrange(5,105,5)

def beats_next_player(my_score):
	their_score = spin()

	if their_score == my_score:
		return None

	if their_score > my_score:
		return False

	their_score = their_score + spin()

	if their_score > 100:
		return True
	if their_score == my_score:
		return None
	if their_score > my_score:
		return False

	return True

def score_wins(my_score):
	if beats_next_player(my_score):
		# still have to beat player 3
		if beats_next_player(my_score):
			return True
	return False

def did_i_win(first_spin, spin_again):
	score = first_spin
	if spin_again:
		score = score + spin()

	if score > 100:
		return False
	else:
		return score_wins(score)

def win_pct(first_spin, spin_again, iterations):
	wins = 0
	ties = 0
	for iteration in range(opts.iterations):
		result = did_i_win(first_spin, spin_again)
		if result is None:
			ties = ties + 1
		elif result is True:
			wins = wins + 1
	win_pct = wins * 100.0 / opts.iterations
	tie_pct = ties * 100.0 / opts.iterations
	return win_pct


def makePlot (filename, data):
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt

        x=[m[0] for m in data]
        stay = [m[1] for m in data]
        spin = [m[2] for m in data]

        fig = plt.figure()
        # plt.xkcd() # uncomment for xkcd style plots
        fig.suptitle("Price is Right Spin Strategy",
                     fontsize=14, fontweight='bold')
        ax = plt.subplot(111)                 # get default subplot to make it nice
        ax.set_ylim(0,100)                    # force the % to be 0-100
        ax.set_xlim(0,100.1)                  # force a grid line at 100
        ax.grid(True)                         # turn on the grid
        ax.spines['top'].set_visible(False)   # turn off top part of box (top spine)
        ax.spines['right'].set_visible(False) # turn off right part of box (right spine)
        ax.yaxis.set_ticks_position('left')   # turn off tick marks on right
        ax.xaxis.set_ticks_position('none')   # turn off tick marks on top and bottom
        ax.set_xticks(range(0,110,10))        # set ticks to be by 10s
        ax.set_yticks(range(0,110,10))        # set ticks to be by 10s

        plt.plot(x,stay,color="b",label="stay")
        plt.plot(x,spin,color="r",label="spin again")
        plt.fill_between(x,0,stay,alpha=0.2,color='b')
        plt.fill_between(x,0,spin,alpha=0.2,color='r')
        plt.ylabel("% chance of winning")
        plt.xlabel("first spin result")

        plt.legend(loc=2) # 2=upper-left (see pydoc matplotlib.pyplot.legend)

        fig.savefig(filename, format="png")

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("--iterations", "-n", type="int", default=10000)
        parser.add_option("--plot", "-p",
                          help="filename for plotted output (png)",
                          metavar="PLOTFILE")
	opts, args = parser.parse_args()

        allResults = []
	for first_spin in range(5, 105, 5):
                spinResults=[first_spin,
                             win_pct(first_spin, False, opts.iterations),
                             win_pct(first_spin, True, opts.iterations)]

                if opts.plot:
                        allResults.append(spinResults)
                else:
                        print ",".join([str(n) for n in spinResults])

        if opts.plot:
                makePlot(opts.plot, allResults)
