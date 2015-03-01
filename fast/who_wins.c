#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <strings.h>
#include "xorshift.h"
#include <pthread.h>

#define PLAYER1_THRESHOLD 65
#define PLAYER2_THRESHOLD 55
#define ITERATIONS 1000000
#define THREADS 1 
#define spin() (5*(1+xor32()%20))

extern char *optarg;

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
typedef struct results_t { uint32_t totals[8]; } results_t;
typedef struct worker_args_t
{
	uint8_t player1_threshold;
	uint8_t player2_threshold;
	uint32_t iterations;
	results_t results;
} worker_args_t;

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

void worker(worker_args_t *args)
{
	int i;
	for (i = 0; i < args->iterations; ++i)
		(args->results.totals[who_wins(args->player1_threshold, args->player2_threshold)])++;
}

uint8_t main(int argc, char *argv[])
{
	results_t totals;
	worker_args_t *args;
	pthread_t *workers;

	uint32_t i, j;

	uint8_t player1_threshold = PLAYER1_THRESHOLD;
	uint8_t player2_threshold = PLAYER2_THRESHOLD;
	uint32_t threads = THREADS;
	uint32_t iterations = ITERATIONS;
	int opt;

	while ((opt = getopt(argc, argv, "1:2:n:t:")) != -1)
	{
		switch (opt)
		{
			case 'n':
				iterations = atoi(optarg);
				break;
			case '1':
				player1_threshold = atoi(optarg);
				break;
			case '2':
				player2_threshold = atoi(optarg);
				break;
			case 't':
				threads = atoi(optarg);
				break;
			default:
				fprintf(stderr, "Usage: %s [-n iterations] [-1 player1_threshold] [-2 player2_threshold]\n",
						argv[0]);
				exit(1);
		}
	}

	args = (worker_args_t *)malloc(sizeof(worker_args_t) * threads);
	workers = malloc(sizeof(pthread_t) * threads);
	for (i = 0; i < threads; i++)
	{
		args[i].player1_threshold = player1_threshold;
		args[i].player2_threshold = player2_threshold;
		args[i].iterations = iterations / threads;
		for (j = 0; j < 8; j++)
			args[i].results.totals[j] = 0;
		if (i == 0)
			args[i].iterations += iterations % threads;

		pthread_create(&workers[i], NULL, (void *)&worker, &args[i]);
	}

	bzero((void *)&totals, sizeof(totals));
	for (i = 0; i < threads; i++) 
	{
		pthread_join(workers[i], 0);
		for (j = 0; j < 8; j++)
			totals.totals[j] += args[i].results.totals[j];
	}

	for (i = 1; i < 8; i++)
		printf("%s: %3.2f\n", result_text[i], 100.0 * totals.totals[i] / iterations);
}
