#!/usr/bin/python

import optparse
from random import randrange

outcomes = [ "NaN",                #000
	     "player 1 wins",      #001
	     "player 2 wins",      #010
	     "players 1&2 tie",    #011
	     "player 3 wins",      #100
	     "players 1&3 tie",    #101
	     "players 2&3 tie",    #110
	     "three-way tie",      #111
	]

def spin():
	return randrange(5,105,5)

def who_wins(player1_threshold, player2_threshold):
	# player1 respins on 65 or less
	player1_score = spin()
	if player1_score <= player1_threshold:
		player1_score = player1_score + spin()

	if player1_score > 100:
		player1_score = 0

	# player2 respins on 60 or less or if losing
	player2_score = spin()
	if player2_score < player1_score or player2_score <= player2_threshold:
		player2_score = player2_score + spin()

	if player2_score > 100:
		player2_score = 0

	# player3 respins if losing
	player3_score = spin()
	if player3_score < player1_score or player3_score < player2_score:
		player3_score = player3_score + spin()

	if player3_score > 100:
		player3_score = 0

	# result
	best_score = max(player1_score, player2_score, player3_score)
	result = 0

	if player1_score == best_score:
		result = result | 1
	if player2_score == best_score:
		result = result | 2
	if player3_score == best_score:
		result = result | 4

	return result

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option("--iterations", "-n", type="int", default=10000)
	parser.add_option("--player-1-threshold", "-1", type="int", default=65)
	parser.add_option("--player-2-threshold", "-2", type="int", default=60)
	opts, args = parser.parse_args()

	results = [0, 0, 0, 0, 0, 0, 0, 0]
	for iteration in range(opts.iterations):
		outcome = who_wins(opts.player_1_threshold, opts.player_2_threshold)
		results[outcome] = results[outcome] + 1

	for result in range(1, len(results)):
		outcome_pct = results[result] * 100.0 / opts.iterations
		print "%s,%3.2f" % (outcomes[result], outcome_pct)
