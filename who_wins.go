package main

import (
	"fmt"
	"math/rand"
)

func spin() (score int) {
        return 5 * (1 + rand.Intn(20))
}

func who_wins(player1_threshold int, player2_threshold int) (bitmask int) {
	var player1_score = spin()
	if player1_score <= player1_threshold {
		player1_score += spin()
	}
	if player1_score > 100 {
		player1_score = 0
	}

	player2_score := spin()
	if player2_score < player1_score || player2_score <= player2_threshold {
		player2_score = player2_score + spin()
	}
	if player2_score > 100 {
		player2_score = 0
	}

	player3_score := spin()
	if player3_score < player1_score || player3_score < player2_score {
		player3_score = player3_score + spin()
	}
	if player3_score > 100 {
		player3_score = 0
	}

	best_score := player1_score
	if player2_score > best_score {
		best_score = player2_score
	}
	if player3_score > best_score {
		best_score = player3_score
	}

	bitmask = 0
	if player1_score == best_score {
		bitmask |= 1
	}
	if player2_score == best_score {
		bitmask |= 2
	}
	if player3_score == best_score {
		bitmask |= 4
	}
	return bitmask
}
		
func main() {
	var results[8]int
	iterations := 10000000

	text := [8]string{ "NaN", "player1 wins", "player2 wins", "player1 & player2 tie", "player3 wins", "player3 & player1 tie", "player3 & player2 tie", "three-way tie" }

	for i := 1; i < iterations; i++ {
		outcome := who_wins(65, 60)
		results[outcome]++
	}

	for i := 1; i < 8; i++ {
		fmt.Printf("%s,%3.2f\n", text[i], float64(results[i]) * 100.0 / float64(iterations))
	}
}
