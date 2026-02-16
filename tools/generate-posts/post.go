package main

import (
	"bytes"
	"embed"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"text/template"

	"github.com/adrg/frontmatter"
	"github.com/google/go-github/v68/github"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

//go:embed templates/post.md
var templateFS embed.FS

// RepoPost holds the data needed to render a blog post from a GitHub repo.
type RepoPost struct {
	Repo         *github.Repository
	Title        string
	Slug         string
	Tags         []string
	MarkdownBody string
	FileName     string
}

// buildPost creates a RepoPost by fetching and processing a repo's README.
func buildPost(repo *github.Repository, cfg Config) (*RepoPost, error) {
	branch := cfg.DefaultBranch
	if b := repo.GetDefaultBranch(); b != "" {
		branch = b
	}

	body, err := fetchReadme(repo.GetFullName(), branch)
	if err != nil {
		body = fmt.Sprintf("See repo at [%s](%s)", repo.GetFullName(), repo.GetHTMLURL())
	}

	// Parse frontmatter tags before stripping
	tags := postTags(repo, body, cfg)

	body = stripFrontMatterAndH1(body)
	body = convertRelativeLinksToAbsolute(body, repo.GetFullName(), repo.GetHTMLURL(), branch)

	title := postTitle(repo.GetName(), cfg)

	return &RepoPost{
		Repo:         repo,
		Title:        title,
		Slug:         postSlug(title),
		Tags:         tags,
		MarkdownBody: body,
		FileName:     "generated-" + repo.GetName() + ".md",
	}, nil
}

// postTitle generates a human-readable title from a repo name.
func postTitle(repoName string, cfg Config) string {
	// Check explicit mapping first
	if title, ok := cfg.TitleMappings[repoName]; ok {
		return title
	}

	// Build lowercase → corrected casing lookup
	casingMap := make(map[string]string, len(cfg.CasingCorrections))
	for _, word := range cfg.CasingCorrections {
		casingMap[strings.ToLower(word)] = word
	}

	// Strip "playground", clean up, title-case
	title := strings.ReplaceAll(repoName, "playground", "")
	title = strings.ReplaceAll(title, "-", " ")
	title = strings.TrimSpace(title)

	titleCaser := cases.Title(language.English)
	words := strings.Fields(strings.ToLower(title))

	result := make([]string, 0, len(words))
	for _, w := range words {
		if corrected, ok := casingMap[w]; ok {
			result = append(result, corrected)
		} else {
			result = append(result, titleCaser.String(w))
		}
	}

	return strings.Join(result, " ")
}

// postSlug creates a URL-friendly slug from a title.
func postSlug(title string) string {
	return strings.ToLower(strings.ReplaceAll(title, " ", "-"))
}

// postTags combines tags from multiple sources: auto-detected from repo name,
// explicit repo mappings, static tags, README frontmatter, and normalizes them.
func postTags(repo *github.Repository, body string, cfg Config) []string {
	repoWords := strings.Split(repo.GetName(), "-")

	// Auto-tags: intersection of repo name words with configured keywords
	autoSet := make(map[string]bool, len(cfg.Tags.AutoFromRepoName))
	for _, t := range cfg.Tags.AutoFromRepoName {
		autoSet[t] = true
	}
	var tags []string
	for _, w := range repoWords {
		if autoSet[w] {
			tags = append(tags, w)
		}
	}

	// Repo-specific tag mappings
	if mapped, ok := cfg.Tags.RepoMappings[repo.GetName()]; ok {
		tags = append(tags, mapped...)
	}

	// Static tags
	tags = append(tags, cfg.Tags.Static...)

	// Tags from README frontmatter
	var matter struct {
		Tags []string `yaml:"tags"`
	}
	if _, err := frontmatter.Parse(strings.NewReader(body), &matter); err == nil {
		tags = append(tags, matter.Tags...)
	}

	// Normalize, deduplicate, and remove empty tags
	seen := make(map[string]bool, len(tags))
	result := make([]string, 0, len(tags))
	for _, t := range tags {
		t = strings.TrimSpace(t)
		if t == "" {
			continue
		}
		if normalized, ok := cfg.Tags.Normalize[t]; ok {
			t = normalized
		}
		if !seen[t] {
			seen[t] = true
			result = append(result, t)
		}
	}

	return result
}

// stripFrontMatterAndH1 removes YAML front matter and the first H1 heading.
func stripFrontMatterAndH1(body string) string {
	lines := strings.Split(body, "\n")

	// Strip YAML front matter
	if len(lines) > 0 && lines[0] == "---" {
		for i := 1; i < len(lines); i++ {
			if lines[i] == "---" {
				lines = lines[i+1:]
				break
			}
		}
	}

	// Strip first H1
	for i, line := range lines {
		trimmed := strings.TrimSpace(line)
		if trimmed == "" {
			continue
		}
		if strings.HasPrefix(trimmed, "# ") {
			lines = append(lines[:i], lines[i+1:]...)
		}
		break
	}

	return strings.Join(lines, "\n")
}

// renderPost executes the embedded template with the post data.
func renderPost(post *RepoPost) (string, error) {
	data, err := templateFS.ReadFile("templates/post.md")
	if err != nil {
		return "", fmt.Errorf("read template: %w", err)
	}

	t, err := template.New("post").Parse(string(data))
	if err != nil {
		return "", fmt.Errorf("parse template: %w", err)
	}

	var buf bytes.Buffer
	if err := t.Execute(&buf, post); err != nil {
		return "", fmt.Errorf("execute template: %w", err)
	}
	return buf.String(), nil
}

// writePostFile renders and writes a post to the destination directory.
func writePostFile(post *RepoPost, destDir string) error {
	content, err := renderPost(post)
	if err != nil {
		return err
	}
	if err := os.MkdirAll(destDir, 0o755); err != nil {
		return fmt.Errorf("mkdir %s: %w", destDir, err)
	}
	path := filepath.Join(destDir, post.FileName)
	return os.WriteFile(path, []byte(content), 0o644)
}
