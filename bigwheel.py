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

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("--iterations", "-n", type="int", default=10000)
	opts, args = parser.parse_args()

	for first_spin in range(5, 105, 5):
		print "%s,%s,%s" % (first_spin, win_pct(first_spin, False, opts.iterations), win_pct(first_spin, True, opts.iterations))
