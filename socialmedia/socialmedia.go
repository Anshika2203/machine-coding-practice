package main

import (
	"fmt"
	"sync"
)

type Post struct {
	ID      string
	User    string
	Content string
}

type SocialMedia struct {
	Posts     map[string]Post
	Followers map[string]map[string]bool
	mu        sync.Mutex
}

func NewSocialMedia() *SocialMedia {
	return &SocialMedia{
		Posts:     make(map[string]Post),
		Followers: make(map[string]map[string]bool),
	}
}

func (sm *SocialMedia) CreatePost(user, id, content string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	sm.Posts[id] = Post{ID: id, User: user, Content: content}
}

func (sm *SocialMedia) DeletePost(id string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	delete(sm.Posts, id)
}

func (sm *SocialMedia) Follow(follower, followee string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	if _, exists := sm.Followers[follower]; !exists {
		sm.Followers[follower] = make(map[string]bool)
	}
	sm.Followers[follower][followee] = true
}

func (sm *SocialMedia) Unfollow(follower, followee string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	delete(sm.Followers[follower], followee)
}

func (sm *SocialMedia) GetFeed(user string) {
	sm.mu.Lock()
	defer sm.mu.Unlock()
	fmt.Println("Feed for:", user)
	for _, post := range sm.Posts {
		if user == post.User || sm.Followers[user][post.User] {
			fmt.Println(post.Content)
		}
	}
}

func main() {
	sm := NewSocialMedia()
	sm.CreatePost("user1", "101", "Hello World!")
	sm.CreatePost("user2", "102", "Golang is awesome!")
	sm.Follow("user1", "user2")
	sm.GetFeed("user1")
}
