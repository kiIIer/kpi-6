package game

import (
	"fmt"
	"hash/fnv"
	"math"
)

const BoardSize = 7

const (
	influenceRange = 3
	decayFactor    = 0.5
	clumpingFactor = 0.2
)

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
	fmt.Printf("Territories - Black: %.2f, White: %.2f\n", blackTerritory, whiteTerritory)
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

func (g *Game) CalculateTerritories() (float64, float64) {
	influence := make([][]float64, BoardSize)
	for i := range influence {
		influence[i] = make([]float64, BoardSize)
	}

	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if g.Board[i][j] != 0 {
				g.spreadInfluence(i, j, influence)
			}
		}
	}

	blackTerritory, whiteTerritory := 0.0, 0.0
	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if influence[i][j] > 0 {
				blackTerritory += influence[i][j]
			} else if influence[i][j] < 0 {
				whiteTerritory -= influence[i][j]
			}
		}
	}

	return blackTerritory, whiteTerritory
}

func (g *Game) spreadInfluence(x, y int, influence [][]float64) {
	stone := g.Board[x][y]

	nearbyStones := make([][]int, BoardSize)
	for i := range nearbyStones {
		nearbyStones[i] = make([]int, BoardSize)
	}

	for dx := -influenceRange; dx <= influenceRange; dx++ {
		for dy := -influenceRange; dy <= influenceRange; dy++ {
			nx, ny := x+dx, y+dy
			if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize && g.Board[nx][ny] != 0 {
				updateDensity(nearbyStones, nx, ny, BoardSize)
			}
		}
	}

	for dx := -influenceRange; dx <= influenceRange; dx++ {
		for dy := -influenceRange; dy <= influenceRange; dy++ {
			nx, ny := x+dx, y+dy
			if nx >= 0 && ny >= 0 && nx < BoardSize && ny < BoardSize {
				distance := math.Sqrt(float64(dx*dx + dy*dy))
				if distance <= float64(influenceRange) {
					decayedInfluence := (1.0 - decayFactor*distance) * float64(stone)
					clumpingDiscount := 1.0 - clumpingFactor*float64(nearbyStones[nx][ny])
					influence[nx][ny] += decayedInfluence * clumpingDiscount
				}
			}
		}
	}
}

func updateDensity(nearbyStones [][]int, x, y, size int) {
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			nx, ny := x+dx, y+dy
			if nx >= 0 && ny >= 0 && nx < size && ny < size {
				nearbyStones[nx][ny]++
			}
		}
	}
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
