package ai

import (
	"go-max/game"
	"math"
)

type MinimaxInput struct {
	Game      *game.Game
	Depth     int
	Alpha     float64
	Beta      float64
	MaxPlayer bool
}

type MinimaxResult struct {
	Eval float64
	Move game.Move
}

func MinimaxDecision(g *game.Game, tt *TranspositionTable) game.Move {
	initialDepth := 6
	alpha := -math.Inf(1)
	beta := math.Inf(1)

	input := MinimaxInput{
		Game:      g,
		Depth:     initialDepth,
		Alpha:     alpha,
		Beta:      beta,
		MaxPlayer: g.CurrentPlayer == 1,
	}

	_, bestMove := Minimax(input, tt)
	return bestMove
}

func Minimax(input MinimaxInput, tt *TranspositionTable) (float64, game.Move) {
	hash := input.Game.Hash()
	if result, found := tt.Load(hash); found {
		return result.Eval, result.Move
	}

	if input.Depth == 0 {
		eval := Evaluate(input.Game)
		return eval, game.Move{}
	}

	moves := input.Game.GenerateMoves()
	if len(moves) == 0 {
		return Evaluate(input.Game), game.Move{}
	}

	var bestMove game.Move
	var bestEval float64
	if input.MaxPlayer {
		bestEval = -math.Inf(1)
	} else {
		bestEval = math.Inf(1)
	}
	bestMove = moves[0]

	for _, move := range moves {
		newGame := input.Game.DeepCopy()
		if newGame.MakeMove(move) {
			newInput := MinimaxInput{
				Game:      newGame,
				Depth:     input.Depth - 1,
				Alpha:     input.Alpha,
				Beta:      input.Beta,
				MaxPlayer: !input.MaxPlayer,
			}
			eval, _ := Minimax(newInput, tt)
			if (input.MaxPlayer && eval > bestEval) || (!input.MaxPlayer && eval < bestEval) {
				bestEval = eval
				bestMove = move
				if input.MaxPlayer {
					input.Alpha = math.Max(input.Alpha, bestEval)
				} else {
					input.Beta = math.Min(input.Beta, bestEval)
				}
				//if input.Beta <= input.Alpha {
				//	break
				//}
			}
		}
	}

	tt.Store(hash, MinimaxResult{Eval: bestEval, Move: bestMove})
	return bestEval, bestMove
}

func noMoveEval(maxPlayer bool) float64 {
	if maxPlayer {
		return -math.Inf(1)
	}
	return math.Inf(1)
}

func Evaluate(g *game.Game) float64 {
	blackTerritory, whiteTerritory := g.CalculateTerritories()
	blackCaptures, whiteCaptures := 5*g.Captures[0], 5*g.Captures[1]
	score := blackTerritory - whiteTerritory + blackCaptures - whiteCaptures
	return float64(score)
}
