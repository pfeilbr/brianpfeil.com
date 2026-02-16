package main

import (
	"testing"

	"github.com/google/go-github/v68/github"
)

func ptr[T any](v T) *T { return &v }

func TestFilterRepos(t *testing.T) {
	repos := []*github.Repository{
		{Name: ptr("aws-cdk-playground")},
		{Name: ptr("aws-lambda-playground")},
		{Name: ptr("react-playground")},
		{Name: ptr("my-blog")},
		{Name: ptr("dotfiles")},
		{Name: ptr("alfred-utilities-workflow")},
		{Name: ptr("taco-playground")},
	}

	tests := []struct {
		name    string
		include []string
		exclude []string
		want    []string
	}{
		{
			name:    "Include playground repos",
			include: []string{".*-playground"},
			exclude: nil,
			want:    []string{"aws-cdk-playground", "aws-lambda-playground", "react-playground", "taco-playground"},
		},
		{
			name:    "Exclude overrides include",
			include: []string{".*-playground"},
			exclude: []string{"taco-playground"},
			want:    []string{"aws-cdk-playground", "aws-lambda-playground", "react-playground"},
		},
		{
			name:    "Multiple include patterns",
			include: []string{".*-playground", "alfred-utilities-workflow"},
			exclude: nil,
			want:    []string{"aws-cdk-playground", "aws-lambda-playground", "react-playground", "alfred-utilities-workflow", "taco-playground"},
		},
		{
			name:    "No matches",
			include: []string{"zzz-nonexistent"},
			exclude: nil,
			want:    nil,
		},
		{
			name:    "Empty include returns nothing",
			include: nil,
			exclude: nil,
			want:    nil,
		},
		{
			name:    "Exclude with empty string is ignored",
			include: []string{".*-playground"},
			exclude: []string{"", "taco-playground"},
			want:    []string{"aws-cdk-playground", "aws-lambda-playground", "react-playground"},
		},
		{
			name:    "Exclude all matched repos",
			include: []string{".*-playground"},
			exclude: []string{".*-playground"},
			want:    nil,
		},
		{
			name:    "Partial name exclude",
			include: []string{".*-playground"},
			exclude: []string{"aws-"},
			want:    []string{"react-playground", "taco-playground"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := filterRepos(repos, tt.include, tt.exclude)
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			var names []string
			for _, r := range got {
				names = append(names, r.GetName())
			}
			if len(names) != len(tt.want) {
				t.Fatalf("got %d repos %v, want %d repos %v", len(names), names, len(tt.want), tt.want)
			}
			for i, name := range names {
				if name != tt.want[i] {
					t.Errorf("repo[%d] = %q, want %q", i, name, tt.want[i])
				}
			}
		})
	}
}

func TestFilterReposInvalidRegex(t *testing.T) {
	repos := []*github.Repository{{Name: ptr("test")}}

	t.Run("Bad include pattern", func(t *testing.T) {
		_, err := filterRepos(repos, []string{"[invalid"}, nil)
		if err == nil {
			t.Error("expected error for invalid include regex, got nil")
		}
	})

	t.Run("Bad exclude pattern", func(t *testing.T) {
		_, err := filterRepos(repos, []string{".*"}, []string{"[invalid"})
		if err == nil {
			t.Error("expected error for invalid exclude regex, got nil")
		}
	})
}
