package main

import (
	"fmt"
	"sync"
)

type Poll struct {
	Question string
	Options  map[string]int
	mu       sync.Mutex
}

type PollSystem struct {
	Polls map[string]*Poll
	mu    sync.Mutex
}

func NewPollSystem() *PollSystem {
	return &PollSystem{Polls: make(map[string]*Poll)}
}

func (ps *PollSystem) CreatePoll(id string, question string, options []string) {
	ps.mu.Lock()
	defer ps.mu.Unlock()

	optMap := make(map[string]int)
	for _, opt := range options {
		optMap[opt] = 0
	}

	ps.Polls[id] = &Poll{Question: question, Options: optMap}
}

func (ps *PollSystem) Vote(id, option string) {
	ps.mu.Lock()
	defer ps.mu.Unlock()

	if poll, exists := ps.Polls[id]; exists {
		poll.mu.Lock()
		defer poll.mu.Unlock()
		if _, ok := poll.Options[option]; ok {
			poll.Options[option]++
		} else {
			fmt.Println("Invalid option.")
		}
	} else {
		fmt.Println("Poll not found.")
	}
}

func (ps *PollSystem) GetResults(id string) {
	ps.mu.Lock()
	defer ps.mu.Unlock()

	if poll, exists := ps.Polls[id]; exists {
		fmt.Println("Poll Results for:", poll.Question)
		for opt, count := range poll.Options {
			fmt.Printf("%s: %d votes\n", opt, count)
		}
	} else {
		fmt.Println("Poll not found.")
	}
}

func main() {
	ps := NewPollSystem()
	ps.CreatePoll("1", "What's your favorite color?", []string{"Red", "Blue", "Green"})
	ps.Vote("1", "Blue")
	ps.Vote("1", "Red")
	ps.GetResults("1")
}
