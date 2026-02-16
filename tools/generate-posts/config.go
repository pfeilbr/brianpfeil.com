package main

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

// Config holds all settings for post generation.
type Config struct {
	GithubUsername    string `yaml:"github_username"`
	GithubAccessToken string `yaml:"github_access_token"`
	DefaultBranch    string `yaml:"default_branch"`

	RepoFilters struct {
		Include []string `yaml:"include"`
		Exclude []string `yaml:"exclude"`
	} `yaml:"repo_filters"`

	TitleMappings    map[string]string `yaml:"title_mappings"`
	CasingCorrections []string         `yaml:"casing_corrections"`

	Tags struct {
		AutoFromRepoName []string            `yaml:"auto_from_repo_name"`
		Static           []string            `yaml:"static"`
		RepoMappings     map[string][]string `yaml:"repo_mappings"`
		Normalize        map[string]string   `yaml:"normalize"`
	} `yaml:"tags"`
}

// LoadConfig reads config.yaml and merges config.local.yaml if present.
func LoadConfig() (Config, error) {
	var cfg Config

	data, err := os.ReadFile("config.yaml")
	if err != nil {
		return cfg, fmt.Errorf("read config.yaml: %w", err)
	}
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return cfg, fmt.Errorf("parse config.yaml: %w", err)
	}

	// Merge local overrides (secrets)
	if localData, err := os.ReadFile("config.local.yaml"); err == nil {
		var local Config
		if err := yaml.Unmarshal(localData, &local); err != nil {
			return cfg, fmt.Errorf("parse config.local.yaml: %w", err)
		}
		if local.GithubAccessToken != "" {
			cfg.GithubAccessToken = local.GithubAccessToken
		}
		if local.GithubUsername != "" {
			cfg.GithubUsername = local.GithubUsername
		}
		if local.DefaultBranch != "" {
			cfg.DefaultBranch = local.DefaultBranch
		}
	}

	// Defaults
	if cfg.DefaultBranch == "" {
		cfg.DefaultBranch = "main"
	}
	if cfg.TitleMappings == nil {
		cfg.TitleMappings = make(map[string]string)
	}
	if cfg.Tags.RepoMappings == nil {
		cfg.Tags.RepoMappings = make(map[string][]string)
	}
	if cfg.Tags.Normalize == nil {
		cfg.Tags.Normalize = make(map[string]string)
	}

	return cfg, nil
}
