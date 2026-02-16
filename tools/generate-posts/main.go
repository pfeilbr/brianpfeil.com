package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

func main() {
	log.SetPrefix("generate-posts: ")
	log.SetFlags(0)

	var (
		user  string
		dest  string
		cache bool
		debug bool
	)
	flag.StringVar(&user, "user", "", "GitHub username")
	flag.StringVar(&dest, "dest", "", "destination directory for generated posts")
	flag.BoolVar(&cache, "cache", false, "cache GitHub API responses locally")
	flag.BoolVar(&debug, "debug", false, "enable debug logging")
	flag.Parse()

	if user == "" || dest == "" {
		fmt.Fprintf(os.Stderr, "Usage: generate-posts -user=USER -dest=DIR [-cache] [-debug]\n")
		os.Exit(1)
	}

	cfg, err := LoadConfig()
	if err != nil {
		log.Fatalf("config: %v", err)
	}
	cfg.GithubUsername = user

	if err := run(cfg, dest, cache, debug); err != nil {
		log.Fatalf("fatal: %v", err)
	}
}

func run(cfg Config, destDir string, cache, debug bool) error {
	if cfg.GithubAccessToken == "" {
		return fmt.Errorf("github_access_token not set — create config.local.yaml with your token")
	}

	client := newGitHubClient(cfg.GithubAccessToken)

	repos, err := fetchRepos(client, cfg.GithubUsername, cache)
	if err != nil {
		return fmt.Errorf("fetch repos: %w", err)
	}
	if debug {
		log.Printf("fetched %d repos for %s", len(repos), cfg.GithubUsername)
	}

	filtered, err := filterRepos(repos, cfg.RepoFilters.Include, cfg.RepoFilters.Exclude)
	if err != nil {
		return fmt.Errorf("filter repos: %w", err)
	}
	if debug {
		log.Printf("matched %d repos after filtering", len(filtered))
	}

	wrote := 0
	for _, repo := range filtered {
		post, err := buildPost(repo, cfg)
		if err != nil {
			log.Printf("WARN: skipping %s: %v", repo.GetName(), err)
			continue
		}
		if err := writePostFile(post, destDir); err != nil {
			return fmt.Errorf("write %s: %w", post.FileName, err)
		}
		if debug {
			log.Printf("wrote %s", post.FileName)
		}
		wrote++
	}

	log.Printf("generated %d posts in %s", wrote, destDir)
	return nil
}
