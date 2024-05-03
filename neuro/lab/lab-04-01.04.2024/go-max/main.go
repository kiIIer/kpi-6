package main

import (
	"bufio"
	"fmt"
	"go-max/ai"
	"go-max/game"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

func clearConsole() {
	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("cmd", "/c", "cls")
	} else {
		cmd = exec.Command("clear")
	}
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func promptForMove(g *game.Game, tt *ai.TranspositionTable) {
	reader := bufio.NewReader(os.Stdin)
	var x, y int

	for {
		fmt.Print("Enter move (x y) or type 'a' for AI to make a move: ")
		input, err := reader.ReadString('\n')
		if err != nil {
			fmt.Println("Error reading input. Please try again.")
			continue
		}

		input = strings.TrimSpace(input)

		if input == "a" {

			makeAIMove(g, tt)
			return
		}

		_, err = fmt.Sscanf(input, "%d %d", &x, &y)
		if err != nil {
			fmt.Println("Invalid input format. Please enter coordinates as 'x y'.")
			continue
		}

		if g.MakeMove(game.Move{X: x, Y: y}) {
			break
		} else {
			fmt.Println("Invalid move, try again.")
		}
	}
}

func makeAIMove(g *game.Game, tt *ai.TranspositionTable) {
	bestMove := ai.MinimaxDecision(g, tt)
	if !g.MakeMove(bestMove) {
		fmt.Println("AI made an invalid move, which should never happen.")
	} else {
		fmt.Println("AI has made its move.")
	}
}

func main() {
	g := game.NewGame()
	tt := ai.NewTranspositionTable()

	for {
		clearConsole()
		g.PrintBoard()
		printPossibleMoves(g)
		promptForMove(g, tt)
	}
}

//func main() {
//	g := game.NewGame()
//	tt := ai.NewTranspositionTable()
//	start := time.Now()
//
//	bestMove := ai.MinimaxDecision(g, tt)
//
//	duration := time.Since(start)
//	fmt.Printf("Best Move: %v\n", bestMove)
//	fmt.Printf("Time taken: %v\n", duration)
//}

func printPossibleMoves(g *game.Game) {
	moves := g.GenerateMoves()
	fmt.Println("Possible Moves:")
	for _, move := range moves {
		fmt.Printf("(%d, %d) ", move.X, move.Y)
	}
	fmt.Println()
}
