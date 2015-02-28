#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <strings.h>

#define PLAYER1_THRESHOLD 65
#define PLAYER2_THRESHOLD 60
#define ITERATIONS 100000000
#define spin() (5*(1+random()%20))

char *result_text[] = {
	"NaN",
	"player 1 wins",
	"player 2 wins",
	"players 1&2 tie",
	"player 3 wins", 
	"players 1&3 tie",
	"players 2&3 tie",
	"three-way tie",
};

uint8_t who_wins(uint8_t player1_threshold, uint8_t player2_threshold)
{
	uint8_t player1_score = spin();
	if (player1_score <= player1_threshold)
		player1_score += spin();
	if (player1_score > 100)
		player1_score = 0;

	uint8_t best_score = player1_score;

	uint8_t player2_score = spin();
	if (player2_score < player1_score || player2_score <= player2_threshold)
		player2_score += spin();
	if (player2_score > 100)
		player2_score = 0;

	if (player2_score > best_score)
		best_score = player2_score;

	uint8_t player3_score = spin();
	if (player3_score < player1_score || player3_score < player2_score)
		player3_score += spin();
	if (player3_score > 100)
		player3_score = 0;

	if (player3_score > best_score)
		best_score = player3_score;

	/* printf("1: %d, 2: %d, 3: %d, B: %d\n", player1_score, player2_score, player3_score, best_score); */
	return((player1_score == best_score ? 1 : 0) | (player2_score == best_score ? 2 : 0) | (player3_score == best_score ? 4 : 0));
}

uint8_t main(int argc, char *argv[])
{
	srandom(time(NULL));
	uint32_t results[8];
	uint32_t i;

	bzero(results, sizeof(results));

	for (i = 0; i < ITERATIONS; ++i)
		results[who_wins(PLAYER1_THRESHOLD, PLAYER2_THRESHOLD)]++;

	for (i = 1; i < 8; i++)
		printf("%s: %3.2f\n", result_text[i], 100.0 * results[i] / ITERATIONS);
}
