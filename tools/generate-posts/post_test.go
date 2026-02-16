package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

type expectedResults struct {
	Title string `json:"title"`
}

func TestPostTitle(t *testing.T) {
	cfg := Config{
		TitleMappings: map[string]string{
			"aws-well-architected-playground":                      "AWS Well-Architected",
			"aws-assume-role-using-custom-oidc-provider-playground": "AWS Assume Role Using Custom OIDC Provider",
		},
		CasingCorrections: []string{"CloudWatch", "CloudFront", "CloudFormation", "AWS", "CLI", "CDK"},
	}

	tests := []struct {
		repoName string
		want     string
	}{
		{"aws-cdk-playground", "AWS CDK"},
		{"aws-well-architected-playground", "AWS Well-Architected"},
		{"react-playground", "React"},
		{"docker-playground", "Docker"},
	}

	for _, tt := range tests {
		t.Run(tt.repoName, func(t *testing.T) {
			got := postTitle(tt.repoName, cfg)
			if got != tt.want {
				t.Errorf("postTitle(%q) = %q, want %q", tt.repoName, got, tt.want)
			}
		})
	}
}

func TestPostSlug(t *testing.T) {
	tests := []struct {
		title string
		want  string
	}{
		{"AWS CDK", "aws-cdk"},
		{"React", "react"},
		{"Docker Compose", "docker-compose"},
	}

	for _, tt := range tests {
		t.Run(tt.title, func(t *testing.T) {
			got := postSlug(tt.title)
			if got != tt.want {
				t.Errorf("postSlug(%q) = %q, want %q", tt.title, got, tt.want)
			}
		})
	}
}

func TestStripFrontMatterAndH1(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "With frontmatter and H1",
			input: "---\ntitle: Test\n---\n# Heading\nBody text",
			want:  "Body text",
		},
		{
			name:  "H1 only",
			input: "# Heading\nBody text",
			want:  "Body text",
		},
		{
			name:  "No frontmatter or H1",
			input: "Just body text\nMore text",
			want:  "Just body text\nMore text",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := stripFrontMatterAndH1(tt.input)
			if got != tt.want {
				t.Errorf("got %q, want %q", got, tt.want)
			}
		})
	}
}

// TestAllRepos runs testdata-driven title tests from the original test suite.
func TestAllRepos(t *testing.T) {
	cfg := Config{
		TitleMappings: map[string]string{
			"aws-well-architected-playground": "AWS Well-Architected",
		},
		CasingCorrections: []string{
			"CloudWatch", "CloudFront", "CloudFormation", "OpenCV", "AWS", "CLI", "PHP",
			"HTTP", "SDK", "CDK", "API", "HLS", "SAM", "YouTube", "SDL2",
			"GoReleaser", "TailwindCSS", "GLib", "XRay", "URL", "AKS", "JS",
			"ARM", "WebSocket", "GatsbyJS", "fswatch", "UI", "WebSockets",
			"CodePipeline", "JFrog", "ECR", "CPP", "CMake", "VueJS",
			"WebAssembly", "JSON", "GitHub", "GraphQL", "IoT", "IAM", "ECS",
			"and", "KMS", "webpack", "NextJS", "KeystoneJS", "GitBook",
			"TypeScript", "OData", "OSX", "WebdriverIO", "HTML", "ES6",
			"NWjs", "iOS", "JSForce", "EventBridge", "SFML", "MacOS",
			"AppFlow", "MDX", "PowerShell", "Diagrams as Code", "AppConfig",
			"JavaScript", "to", "with", "DynamoDB", "SES", "APIs", "for",
			"CFN", "RDS", "CDKTF", "SurveyJS", "EC2", "EMR", "ALB", "R",
			"RStudio", "SageMaker", "SSO", "EFS", "OpenSearch", "VectorDB",
			"MemoryDB", "DuckDB", "LangChain", "PyTorch", "ChromaDB", "OpenAI",
		},
	}

	testdataDir := "testdata"
	userDir := filepath.Join(testdataDir, "repos", "pfeilbr")

	entries, err := os.ReadDir(userDir)
	if err != nil {
		t.Fatalf("read testdata dir: %v", err)
	}

	for _, entry := range entries {
		if !entry.IsDir() || strings.HasPrefix(entry.Name(), ".") {
			continue
		}
		name := entry.Name()

		t.Run("title/"+name, func(t *testing.T) {
			expectPath := filepath.Join(userDir, name, "expect.json")
			data, err := os.ReadFile(expectPath)
			if err != nil {
				t.Fatalf("read expect.json: %v", err)
			}
			var expect expectedResults
			if err := json.Unmarshal(data, &expect); err != nil {
				t.Fatalf("parse expect.json: %v", err)
			}

			got := postTitle(name, cfg)
			if got != expect.Title {
				t.Errorf("postTitle(%q) = %q, want %q", name, got, expect.Title)
			}
		})
	}
}
