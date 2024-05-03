package game

import (
	"fmt"
	"hash/fnv"
)

const BoardSize = 5

type Game struct {
	Board            [BoardSize][BoardSize]int
	CurrentPlayer    int
	MoveNumber       int
	Captures         [2]int
	LastCapturePoint Move
	LastCaptureValid bool
}

type Move struct {
	X, Y int
}

func (g *Game) DeepCopy() *Game {
	newGame := &Game{
		CurrentPlayer: g.CurrentPlayer,
		MoveNumber:    g.MoveNumber,
		Captures:      [2]int{g.Captures[0], g.Captures[1]},
	}
	copy(newGame.Board[:], g.Board[:])
	return newGame
}

func NewGame() *Game {
	return &Game{
		CurrentPlayer: 1,
		MoveNumber:    1,
	}
}

func (g *Game) MakeMove(move Move) bool {
	x, y := move.X, move.Y
	if x < 0 || y < 0 || x >= BoardSize || y >= BoardSize || g.Board[x][y] != 0 {
		return false
	}

	if g.LastCaptureValid && move == g.LastCapturePoint {
		return false
	}

	originalState := g.Board[x][y]
	g.Board[x][y] = g.CurrentPlayer

	capturedStones := g.removeCapturedStones(x, y)
	if capturedStones == 0 && !g.hasLiberty(x, y) {
		g.Board[x][y] = originalState
		return false
	}

	if capturedStones != 1 {
		g.LastCaptureValid = false
	}

	g.CurrentPlayer = -g.CurrentPlayer
	g.MoveNumber++
	return true
}

func (g *Game) removeCapturedStones(x, y int) int {
	directions := []struct{ x, y int }{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	totalCaptures := 0
	for _, d := range directions {
		nx, ny := x+d.x, y+d.y
		if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize && g.Board[nx][ny] == -g.CurrentPlayer {
			if !g.hasLiberty(nx, ny) {
				capturedStones := g.captureGroup(nx, ny)
				totalCaptures += capturedStones
				if g.CurrentPlayer == 1 {
					g.Captures[0] += capturedStones
				} else {
					g.Captures[1] += capturedStones
				}
			}
		}
	}
	if totalCaptures == 1 {
		g.LastCaptureValid = true
	} else {
		g.LastCaptureValid = false
	}
	return totalCaptures
}

func (g *Game) anyAdjacentEnemyCaptured(x, y int) bool {
	directions := []struct{ x, y int }{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}
	for _, d := range directions {
		nx, ny := x+d.x, y+d.y
		if nx >= 0 && nx < BoardSize && ny >= 0 && ny < BoardSize {
			if g.Board[nx][ny] == -g.CurrentPlayer && !g.hasLiberty(nx, ny) {
				return true
			}
		}
	}
	return false
}

func (g *Game) hasLiberty(x, y int) bool {
	visited := make([][]bool, BoardSize)
	for i := range visited {
		visited[i] = make([]bool, BoardSize)
	}
	return g.checkLiberty(x, y, visited)
}

func (g *Game) checkLiberty(x, y int, visited [][]bool) bool {
	if visited[x][y] {
		return false
	}
	visited[x][y] = true

	directions := []struct{ x, y int }{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	for _, d := range directions {
		nx, ny := x+d.x, y+d.y
		if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize {
			if g.Board[nx][ny] == 0 {
				return true
			} else if g.Board[nx][ny] == g.Board[x][y] {
				if g.checkLiberty(nx, ny, visited) {
					return true
				}
			}
		}
	}
	return false
}

func (g *Game) captureGroup(x, y int) int {
	group := g.collectGroup(x, y)
	for _, s := range group {
		g.Board[s.x][s.y] = 0
		g.LastCapturePoint = Move{X: s.x, Y: s.y}
	}
	return len(group)
}

func (g *Game) collectGroup(x, y int) []struct{ x, y int } {
	group := []struct{ x, y int }{}
	stack := []struct{ x, y int }{{x, y}}
	visited := make([][]bool, BoardSize)
	for i := range visited {
		visited[i] = make([]bool, BoardSize)
	}
	color := g.Board[x][y]

	for len(stack) > 0 {
		p := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if visited[p.x][p.y] {
			continue
		}
		visited[p.x][p.y] = true
		group = append(group, p)

		directions := []struct{ x, y int }{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
		for _, d := range directions {
			nx, ny := p.x+d.x, p.y+d.y
			if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize && g.Board[nx][ny] == color {
				stack = append(stack, struct{ x, y int }{nx, ny})
			}
		}
	}
	return group
}

func (g *Game) GenerateMoves() []Move {
	var moves []Move
	for x := 0; x < BoardSize; x++ {
		for y := 0; y < BoardSize; y++ {
			if g.Board[x][y] == 0 {
				if g.isMoveLegal(x, y) {
					moves = append(moves, Move{X: x, Y: y})
				}
			}
		}
	}
	return moves
}

func (g *Game) isMoveLegal(x, y int) bool {
	move := Move{X: x, Y: y}

	if g.LastCaptureValid && move == g.LastCapturePoint {
	}

	originalState := g.Board[x][y]
	g.Board[x][y] = g.CurrentPlayer

	isLegal := g.hasLiberty(x, y) || g.anyAdjacentEnemyCaptured(x, y)

	g.Board[x][y] = originalState
	return isLegal
}

func (g *Game) PrintBoard() {
	blackTerritory, whiteTerritory := g.CalculateTerritories()
	fmt.Println("Move number:", g.MoveNumber)
	currentPlayerName := "White"
	if g.CurrentPlayer == 1 {
		currentPlayerName = "Black"
	}
	fmt.Println(currentPlayerName, "'s turn")
	fmt.Printf("Captures - Black: %d, White: %d\n", g.Captures[0], g.Captures[1])
	fmt.Printf("Territories - Black: %d, White: %d\n", blackTerritory, whiteTerritory)
	fmt.Print("  ")
	for i := 0; i < BoardSize; i++ {
		fmt.Printf("%d ", i)
	}
	fmt.Println()

	for i, row := range g.Board {
		fmt.Printf("%d ", i)
		for _, cell := range row {
			switch cell {
			case 1:
				fmt.Print("X ")
			case -1:
				fmt.Print("O ")
			default:
				fmt.Print(". ")
			}
		}
		fmt.Println()
	}
}

func (g *Game) CalculateTerritories() (blackTerritory, whiteTerritory int) {
	visited := make([][]bool, BoardSize)
	for i := range visited {
		visited[i] = make([]bool, BoardSize)
	}

	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if g.Board[i][j] == 0 && !visited[i][j] {
				territory, isBlack, isWhite := g.FloodFill(i, j, &visited)
				if isBlack && !isWhite {
					blackTerritory += territory
				} else if isWhite && !isBlack {
					whiteTerritory += territory
				}
			}
			//if g.Board[i][j] == 1 {
			//	blackTerritory++
			//} else if g.Board[i][j] == -1 {
			//	whiteTerritory++
			//}
		}
	}
	return
}

func (g *Game) FloodFill(x, y int, visited *[][]bool) (territorySize int, touchesBlack, touchesWhite bool) {
	directions := []struct{ x, y int }{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	stack := []struct{ x, y int }{{x, y}}
	territorySize = 0

	for len(stack) > 0 {
		p := stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		if (*visited)[p.x][p.y] {
			continue
		}
		(*visited)[p.x][p.y] = true
		territorySize++

		for _, d := range directions {
			nx, ny := p.x+d.x, p.y+d.y
			if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize {
				if g.Board[nx][ny] == 0 {
					stack = append(stack, struct{ x, y int }{nx, ny})
				} else if g.Board[nx][ny] == 1 {
					touchesBlack = true
				} else if g.Board[nx][ny] == -1 {
					touchesWhite = true
				}
			}
		}
	}
	return
}

func (g *Game) Hash() uint64 {
	h := fnv.New64a()

	for x := 0; x < BoardSize; x++ {
		for y := 0; y < BoardSize; y++ {

			val := byte(g.Board[x][y] + 2)
			h.Write([]byte{val})
		}
	}

	currentPlayer := byte(0)
	if g.CurrentPlayer == 1 {
		currentPlayer = 1
	} else if g.CurrentPlayer == -1 {
		currentPlayer = 2
	}
	h.Write([]byte{currentPlayer})

	return h.Sum64()
}
