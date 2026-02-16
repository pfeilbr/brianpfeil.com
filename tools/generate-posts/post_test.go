package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/google/go-github/v68/github"
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

func TestPostTitleEdgeCases(t *testing.T) {
	cfg := Config{
		TitleMappings:     map[string]string{},
		CasingCorrections: []string{"AWS", "CDK", "Diagrams as Code", "JavaScript", "to", "with", "for", "and"},
	}

	tests := []struct {
		repoName string
		want     string
	}{
		// No -playground suffix
		{"alfred-utilities-workflow", "Alfred Utilities Workflow"},
		// Very long repo name
		{"aws-glue-pyspark-fetch-databases-and-tables-metadata-playground", "AWS Glue Pyspark Fetch Databases and Tables Metadata"},
		// Multi-word casing correction — "Diagrams as Code" is a single entry
		// but postTitle splits on hyphens so each word is looked up individually;
		// "as" is not in casing corrections, so it gets title-cased to "As"
		{"diagrams-as-code-playground", "Diagrams As Code"},
		// Repo name is just "playground"
		{"playground", ""},
		// Single word repo
		{"react", "React"},
		// Consecutive hyphens
		{"aws--cdk-playground", "AWS CDK"},
		// Lowercase connectors
		{"aws-cdk-to-javascript-playground", "AWS CDK to JavaScript"},
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

func TestPostSlugEdgeCases(t *testing.T) {
	tests := []struct {
		title string
		want  string
	}{
		{"", ""},
		{"AWS CDK Step Functions", "aws-cdk-step-functions"},
		{"A", "a"},
		{"Already lowercase", "already-lowercase"},
		// Multiple spaces become multiple hyphens (current behavior)
		{"Double  Space", "double--space"},
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

func TestStripFrontMatterAndH1EdgeCases(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  string
	}{
		{
			name:  "H1 preceded by blank lines",
			input: "\n\n# Heading\nBody text",
			// stripFrontMatterAndH1 only strips the H1 line itself,
			// preceding blank lines are preserved
			want:  "\n\nBody text",
		},
		{
			name:  "H1 with no trailing content",
			input: "# Heading",
			want:  "",
		},
		{
			name:  "Only frontmatter",
			input: "---\ntitle: Test\n---",
			want:  "",
		},
		{
			name:  "Frontmatter then blank lines then H1",
			input: "---\ntitle: Test\n---\n\n# Heading\nBody",
			want:  "\nBody",
		},
		{
			name:  "H2 not stripped",
			input: "## Not an H1\nBody text",
			want:  "## Not an H1\nBody text",
		},
		{
			name:  "--- in body is not frontmatter",
			input: "Some text\n---\nMore text",
			want:  "Some text\n---\nMore text",
		},
		{
			name:  "Empty input",
			input: "",
			want:  "",
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

func TestPostTags(t *testing.T) {
	cfg := Config{
		Tags: struct {
			AutoFromRepoName []string            `yaml:"auto_from_repo_name"`
			Static           []string            `yaml:"static"`
			RepoMappings     map[string][]string `yaml:"repo_mappings"`
			Normalize        map[string]string   `yaml:"normalize"`
		}{
			AutoFromRepoName: []string{"aws", "lambda", "cdk", "react", "python", "go"},
			Static:           nil,
			RepoMappings: map[string][]string{
				"aws-cdk-playground": {"infrastructure-as-code"},
			},
			Normalize: map[string]string{
				"c++": "cpp",
				"js":  "javascript",
				"go":  "golang",
			},
		},
	}

	tests := []struct {
		name     string
		repoName string
		body     string
		wantTags []string
	}{
		{
			name:     "Auto-tags from repo name",
			repoName: "aws-lambda-playground",
			body:     "Some content",
			wantTags: []string{"aws", "lambda"},
		},
		{
			name:     "Repo mapping tags added",
			repoName: "aws-cdk-playground",
			body:     "Some content",
			wantTags: []string{"aws", "cdk", "infrastructure-as-code"},
		},
		{
			name:     "Tags from README frontmatter",
			repoName: "no-auto-match",
			body:     "---\ntags:\n  - docker\n  - kubernetes\n---\nContent here",
			wantTags: []string{"docker", "kubernetes"},
		},
		{
			name:     "Deduplication",
			repoName: "aws-cdk-playground",
			body:     "---\ntags:\n  - aws\n  - cdk\n---\nContent",
			wantTags: []string{"aws", "cdk", "infrastructure-as-code"},
		},
		{
			name:     "Normalization",
			repoName: "go-playground",
			body:     "---\ntags:\n  - c++\n  - js\n---\nContent",
			wantTags: []string{"golang", "cpp", "javascript"},
		},
		{
			name:     "Empty tags when nothing matches",
			repoName: "totally-unrelated",
			body:     "No frontmatter here",
			wantTags: nil,
		},
		{
			name:     "Empty and whitespace tags are filtered",
			repoName: "no-match",
			body:     "---\ntags:\n  - \"\"\n  - \"  \"\n  - valid\n---\nContent",
			wantTags: []string{"valid"},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			repo := &github.Repository{Name: strPtr(tt.repoName)}
			got := postTags(repo, tt.body, cfg)

			if len(got) != len(tt.wantTags) {
				t.Fatalf("got %d tags %v, want %d tags %v", len(got), got, len(tt.wantTags), tt.wantTags)
			}
			for i, tag := range got {
				if tag != tt.wantTags[i] {
					t.Errorf("tag[%d] = %q, want %q", i, tag, tt.wantTags[i])
				}
			}
		})
	}
}

func TestPostTagsWithStaticTags(t *testing.T) {
	cfg := Config{
		Tags: struct {
			AutoFromRepoName []string            `yaml:"auto_from_repo_name"`
			Static           []string            `yaml:"static"`
			RepoMappings     map[string][]string `yaml:"repo_mappings"`
			Normalize        map[string]string   `yaml:"normalize"`
		}{
			AutoFromRepoName: []string{"aws"},
			Static:           []string{"blog", "generated"},
			RepoMappings:     map[string][]string{},
			Normalize:        map[string]string{},
		},
	}

	repo := &github.Repository{Name: strPtr("aws-playground")}
	got := postTags(repo, "content", cfg)

	want := []string{"aws", "blog", "generated"}
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i, tag := range got {
		if tag != want[i] {
			t.Errorf("tag[%d] = %q, want %q", i, tag, want[i])
		}
	}
}

func strPtr(s string) *string { return &s }

func TestRenderPost(t *testing.T) {
	created := time.Date(2023, 6, 15, 0, 0, 0, 0, time.UTC)
	ts := github.Timestamp{Time: created}
	lang := "Go"

	post := &RepoPost{
		Repo: &github.Repository{
			Name:      strPtr("aws-cdk-playground"),
			FullName:  strPtr("pfeilbr/aws-cdk-playground"),
			HTMLURL:   strPtr("https://github.com/pfeilbr/aws-cdk-playground"),
			Language:  &lang,
			CreatedAt: &ts,
		},
		Title:        "AWS CDK",
		Slug:         "aws-cdk",
		Tags:         []string{"aws", "cdk"},
		MarkdownBody: "## Getting Started\n\nSome content here.",
		FileName:     "generated-aws-cdk-playground.md",
	}

	content, err := renderPost(post)
	if err != nil {
		t.Fatalf("renderPost() error: %v", err)
	}

	// Verify TOML frontmatter structure
	if !strings.HasPrefix(content, "+++\n") {
		t.Error("expected content to start with TOML frontmatter delimiter +++")
	}
	if !strings.Contains(content, `title = "AWS CDK"`) {
		t.Error("expected title in frontmatter")
	}
	if !strings.Contains(content, `slug = "aws-cdk"`) {
		t.Error("expected slug in frontmatter")
	}
	if !strings.Contains(content, `tags = ["aws","cdk"]`) {
		t.Error("expected tags in frontmatter")
	}
	if !strings.Contains(content, `date = 2023-06-15`) {
		t.Error("expected date in frontmatter")
	}
	if !strings.Contains(content, `categories = ["Go", "playground"]`) {
		t.Error("expected categories in frontmatter")
	}
	if !strings.Contains(content, `repoFullName = "pfeilbr/aws-cdk-playground"`) {
		t.Error("expected repoFullName in frontmatter")
	}
	if !strings.Contains(content, `repoHTMLURL = "https://github.com/pfeilbr/aws-cdk-playground"`) {
		t.Error("expected repoHTMLURL in frontmatter")
	}
	if !strings.Contains(content, `truncated = true`) {
		t.Error("expected truncated = true in frontmatter")
	}

	// Verify HTML banner
	if !strings.Contains(content, `class="alert alert-info small bg-info"`) {
		t.Error("expected HTML banner with alert classes")
	}
	if !strings.Contains(content, `pfeilbr/aws-cdk-playground`) {
		t.Error("expected repo full name in banner link")
	}

	// Verify markdown body is included
	if !strings.Contains(content, "## Getting Started") {
		t.Error("expected markdown body in output")
	}
}

func TestRenderPostNilLanguage(t *testing.T) {
	created := time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	ts := github.Timestamp{Time: created}

	post := &RepoPost{
		Repo: &github.Repository{
			Name:      strPtr("drawio-playground"),
			FullName:  strPtr("pfeilbr/drawio-playground"),
			HTMLURL:   strPtr("https://github.com/pfeilbr/drawio-playground"),
			Language:  nil, // No language detected
			CreatedAt: &ts,
		},
		Title:        "Drawio",
		Slug:         "drawio",
		Tags:         []string{"drawio"},
		MarkdownBody: "Content",
		FileName:     "generated-drawio-playground.md",
	}

	content, err := renderPost(post)
	if err != nil {
		t.Fatalf("renderPost() error: %v", err)
	}

	// When Language is nil, GetLanguage() returns "" — verify it doesn't produce "<nil>"
	if strings.Contains(content, "<nil>") {
		t.Error("nil language should not produce literal '<nil>' in output")
	}
	// Should have empty string category
	if !strings.Contains(content, `categories = ["", "playground"]`) {
		t.Error("expected categories with empty string for nil language")
	}
}

func TestRenderPostEmptyTags(t *testing.T) {
	created := time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	ts := github.Timestamp{Time: created}
	lang := "Shell"

	post := &RepoPost{
		Repo: &github.Repository{
			Name:      strPtr("test-repo"),
			FullName:  strPtr("user/test-repo"),
			HTMLURL:   strPtr("https://github.com/user/test-repo"),
			Language:  &lang,
			CreatedAt: &ts,
		},
		Title:        "Test Repo",
		Slug:         "test-repo",
		Tags:         nil,
		MarkdownBody: "Content",
		FileName:     "generated-test-repo.md",
	}

	content, err := renderPost(post)
	if err != nil {
		t.Fatalf("renderPost() error: %v", err)
	}

	if !strings.Contains(content, `tags = []`) {
		t.Errorf("expected empty tags array, got content containing tags line: %s",
			extractLine(content, "tags ="))
	}
}

func TestRenderPostSpecialCharsInTitle(t *testing.T) {
	created := time.Date(2023, 1, 1, 0, 0, 0, 0, time.UTC)
	ts := github.Timestamp{Time: created}
	lang := "Go"

	post := &RepoPost{
		Repo: &github.Repository{
			Name:      strPtr("test"),
			FullName:  strPtr("user/test"),
			HTMLURL:   strPtr("https://github.com/user/test"),
			Language:  &lang,
			CreatedAt: &ts,
		},
		Title:        `C++ "Templates" & Generics`,
		Slug:         "cpp-templates-generics",
		Tags:         []string{"cpp"},
		MarkdownBody: "Content",
		FileName:     "generated-test.md",
	}

	// Should not panic or error — template may not escape correctly for TOML,
	// but it should at least render without error.
	_, err := renderPost(post)
	if err != nil {
		t.Fatalf("renderPost() error with special chars: %v", err)
	}
}

func TestWritePostFile(t *testing.T) {
	created := time.Date(2023, 6, 15, 0, 0, 0, 0, time.UTC)
	ts := github.Timestamp{Time: created}
	lang := "Go"

	post := &RepoPost{
		Repo: &github.Repository{
			Name:      strPtr("test-playground"),
			FullName:  strPtr("user/test-playground"),
			HTMLURL:   strPtr("https://github.com/user/test-playground"),
			Language:  &lang,
			CreatedAt: &ts,
		},
		Title:        "Test",
		Slug:         "test",
		Tags:         []string{"go"},
		MarkdownBody: "Hello world",
		FileName:     "generated-test-playground.md",
	}

	dir := t.TempDir()

	// Write to a subdirectory that doesn't exist yet — should create it
	destDir := filepath.Join(dir, "output", "posts")
	if err := writePostFile(post, destDir); err != nil {
		t.Fatalf("writePostFile() error: %v", err)
	}

	// Verify file exists with correct name
	path := filepath.Join(destDir, "generated-test-playground.md")
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read output file: %v", err)
	}

	content := string(data)

	// Verify it starts with TOML frontmatter
	if !strings.HasPrefix(content, "+++\n") {
		t.Error("output file should start with +++ TOML delimiter")
	}

	// Verify it contains the markdown body
	if !strings.Contains(content, "Hello world") {
		t.Error("output file should contain the markdown body")
	}

	// Verify file is not empty
	if len(data) == 0 {
		t.Error("output file should not be empty")
	}
}

// extractLine returns the first line containing substr, or "" if not found.
func extractLine(content, substr string) string {
	for _, line := range strings.Split(content, "\n") {
		if strings.Contains(line, substr) {
			return line
		}
	}
	return ""
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
