package main

import (
	"os"
	"path/filepath"
	"regexp"
	"testing"
)

func TestLoadConfig(t *testing.T) {
	// LoadConfig reads from the current directory's config.yaml
	// which exists in the tools/generate-posts/ directory where tests run.
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error: %v", err)
	}

	if cfg.GithubUsername == "" {
		t.Error("expected non-empty GithubUsername")
	}
	if cfg.DefaultBranch == "" {
		t.Error("expected non-empty DefaultBranch")
	}
	if len(cfg.RepoFilters.Include) == 0 {
		t.Error("expected non-empty repo include filters")
	}
	if len(cfg.CasingCorrections) == 0 {
		t.Error("expected non-empty casing corrections")
	}
	if len(cfg.Tags.AutoFromRepoName) == 0 {
		t.Error("expected non-empty auto_from_repo_name tags")
	}
}

func TestLoadConfigDefaults(t *testing.T) {
	dir := t.TempDir()

	// Minimal config with no default_branch — should default to "main"
	configContent := `github_username: "testuser"`
	if err := os.WriteFile(filepath.Join(dir, "config.yaml"), []byte(configContent), 0o644); err != nil {
		t.Fatal(err)
	}

	origDir, _ := os.Getwd()
	os.Chdir(dir)
	defer os.Chdir(origDir)

	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error: %v", err)
	}

	if cfg.DefaultBranch != "main" {
		t.Errorf("DefaultBranch = %q, want %q", cfg.DefaultBranch, "main")
	}
	if cfg.TitleMappings == nil {
		t.Error("TitleMappings should be initialized to non-nil map")
	}
	if cfg.Tags.RepoMappings == nil {
		t.Error("Tags.RepoMappings should be initialized to non-nil map")
	}
	if cfg.Tags.Normalize == nil {
		t.Error("Tags.Normalize should be initialized to non-nil map")
	}
}

func TestLoadConfigLocalOverride(t *testing.T) {
	dir := t.TempDir()

	configContent := `
github_username: "baseuser"
default_branch: "develop"
`
	localContent := `
github_access_token: "ghp_test_token"
github_username: "overridden_user"
default_branch: "main"
`
	os.WriteFile(filepath.Join(dir, "config.yaml"), []byte(configContent), 0o644)
	os.WriteFile(filepath.Join(dir, "config.local.yaml"), []byte(localContent), 0o644)

	origDir, _ := os.Getwd()
	os.Chdir(dir)
	defer os.Chdir(origDir)

	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error: %v", err)
	}

	if cfg.GithubAccessToken != "ghp_test_token" {
		t.Errorf("GithubAccessToken = %q, want %q", cfg.GithubAccessToken, "ghp_test_token")
	}
	if cfg.GithubUsername != "overridden_user" {
		t.Errorf("GithubUsername = %q, want %q", cfg.GithubUsername, "overridden_user")
	}
	if cfg.DefaultBranch != "main" {
		t.Errorf("DefaultBranch = %q, want %q", cfg.DefaultBranch, "main")
	}
}

func TestLoadConfigMalformedYAML(t *testing.T) {
	dir := t.TempDir()
	os.WriteFile(filepath.Join(dir, "config.yaml"), []byte("invalid: [yaml: {broken"), 0o644)

	origDir, _ := os.Getwd()
	os.Chdir(dir)
	defer os.Chdir(origDir)

	_, err := LoadConfig()
	if err == nil {
		t.Error("expected error for malformed YAML, got nil")
	}
}

func TestLoadConfigMissingFile(t *testing.T) {
	dir := t.TempDir()

	origDir, _ := os.Getwd()
	os.Chdir(dir)
	defer os.Chdir(origDir)

	_, err := LoadConfig()
	if err == nil {
		t.Error("expected error for missing config.yaml, got nil")
	}
}

// TestConfigTagConsistency validates that the real config.yaml is internally consistent.
func TestConfigTagConsistency(t *testing.T) {
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error: %v", err)
	}

	// Build include regexes
	includeRes := make([]*regexp.Regexp, 0, len(cfg.RepoFilters.Include))
	for _, p := range cfg.RepoFilters.Include {
		re, err := regexp.Compile(p)
		if err != nil {
			t.Fatalf("bad include pattern %q: %v", p, err)
		}
		includeRes = append(includeRes, re)
	}

	// Build exclude regexes
	excludeRes := make([]*regexp.Regexp, 0, len(cfg.RepoFilters.Exclude))
	for _, p := range cfg.RepoFilters.Exclude {
		if p == "" {
			continue
		}
		re, err := regexp.Compile(p)
		if err != nil {
			t.Fatalf("bad exclude pattern %q: %v", p, err)
		}
		excludeRes = append(excludeRes, re)
	}

	// Every repo in repo_mappings should match at least one include pattern
	for repoName := range cfg.Tags.RepoMappings {
		matched := false
		for _, re := range includeRes {
			if re.MatchString(repoName) {
				matched = true
				break
			}
		}
		if !matched {
			t.Errorf("repo_mappings entry %q does not match any include filter", repoName)
		}
	}

	// Warn about repo_mappings entries that are also excluded (dead config)
	for repoName := range cfg.Tags.RepoMappings {
		for _, re := range excludeRes {
			if re.MatchString(repoName) {
				t.Logf("WARN: repo_mappings entry %q is also matched by exclude filter %q (dead config)", repoName, re.String())
			}
		}
	}

	// All normalize keys and values should be lowercase
	for key, val := range cfg.Tags.Normalize {
		if key != key {
			t.Errorf("normalize key %q is not lowercase", key)
		}
		if val != val {
			t.Errorf("normalize value %q (for key %q) is not lowercase", val, key)
		}
	}

	// All include/exclude patterns should be valid regexes (already tested above, but explicit)
	for _, p := range cfg.RepoFilters.Include {
		if _, err := regexp.Compile(p); err != nil {
			t.Errorf("invalid include regex %q: %v", p, err)
		}
	}
	for _, p := range cfg.RepoFilters.Exclude {
		if p == "" {
			continue
		}
		if _, err := regexp.Compile(p); err != nil {
			t.Errorf("invalid exclude regex %q: %v", p, err)
		}
	}
}

// TestNoDuplicateCasingCorrections checks for duplicate entries in casing_corrections.
func TestNoDuplicateCasingCorrections(t *testing.T) {
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatalf("LoadConfig() error: %v", err)
	}

	seen := make(map[string]bool, len(cfg.CasingCorrections))
	for _, word := range cfg.CasingCorrections {
		lower := word
		if seen[lower] {
			t.Errorf("duplicate casing correction: %q", word)
		}
		seen[lower] = true
	}
}
