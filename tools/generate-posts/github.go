package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"regexp"

	"github.com/google/go-github/v68/github"
	"golang.org/x/oauth2"
)

const tmpDir = "tmp"

func newGitHubClient(token string) *github.Client {
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(&oauth2.Token{AccessToken: token})
	tc := oauth2.NewClient(ctx, ts)
	return github.NewClient(tc)
}

// fetchRepos returns all repositories for a user. When cache is true,
// results are stored/loaded from a local JSON file to avoid API calls.
func fetchRepos(client *github.Client, user string, cache bool) ([]*github.Repository, error) {
	cachePath := filepath.Join(tmpDir, "repo-list-"+user+".json")

	if cache {
		if data, err := os.ReadFile(cachePath); err == nil {
			var repos []*github.Repository
			if err := json.Unmarshal(data, &repos); err == nil {
				return repos, nil
			}
		}
	}

	ctx := context.Background()
	opt := &github.RepositoryListOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	}

	var all []*github.Repository
	for {
		repos, resp, err := client.Repositories.List(ctx, user, opt)
		if err != nil {
			return nil, fmt.Errorf("list repos for %s: %w", user, err)
		}
		all = append(all, repos...)
		if resp.NextPage == 0 {
			break
		}
		opt.Page = resp.NextPage
	}

	if cache {
		os.MkdirAll(tmpDir, 0o755)
		if data, err := json.Marshal(all); err == nil {
			os.WriteFile(cachePath, data, 0o644)
		}
	}

	return all, nil
}

// filterRepos applies include/exclude regex patterns to a list of repos.
func filterRepos(repos []*github.Repository, include, exclude []string) ([]*github.Repository, error) {
	includeRes := make([]*regexp.Regexp, 0, len(include))
	for _, p := range include {
		re, err := regexp.Compile(p)
		if err != nil {
			return nil, fmt.Errorf("bad include filter %q: %w", p, err)
		}
		includeRes = append(includeRes, re)
	}

	excludeRes := make([]*regexp.Regexp, 0, len(exclude))
	for _, p := range exclude {
		if p == "" {
			continue
		}
		re, err := regexp.Compile(p)
		if err != nil {
			return nil, fmt.Errorf("bad exclude filter %q: %w", p, err)
		}
		excludeRes = append(excludeRes, re)
	}

	var result []*github.Repository
	for _, repo := range repos {
		name := repo.GetName()
		matched := false
		for _, re := range includeRes {
			if re.MatchString(name) {
				matched = true
				break
			}
		}
		for _, re := range excludeRes {
			if re.MatchString(name) {
				matched = false
				break
			}
		}
		if matched {
			result = append(result, repo)
		}
	}
	return result, nil
}

// fetchReadme downloads the raw README.md for a repo.
func fetchReadme(fullName, branch string) (string, error) {
	url := "https://raw.githubusercontent.com/" + fullName + "/" + branch + "/README.md"
	resp, err := http.Get(url)
	if err != nil {
		return "", fmt.Errorf("GET %s: %w", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("GET %s: status %d", url, resp.StatusCode)
	}

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("read body: %w", err)
	}
	return string(data), nil
}
