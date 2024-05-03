package ai

import "sync"

type TranspositionTable struct {
	store map[uint64]MinimaxResult
	mutex sync.RWMutex
}

func NewTranspositionTable() *TranspositionTable {
	return &TranspositionTable{
		store: make(map[uint64]MinimaxResult),
	}
}

func (tt *TranspositionTable) Store(hash uint64, result MinimaxResult) {
	//tt.mutex.Lock()
	//defer tt.mutex.Unlock()
	//tt.store[hash] = result
}

func (tt *TranspositionTable) Load(hash uint64) (MinimaxResult, bool) {
	tt.mutex.RLock()
	defer tt.mutex.RUnlock()
	result, found := tt.store[hash]
	return result, found
}
