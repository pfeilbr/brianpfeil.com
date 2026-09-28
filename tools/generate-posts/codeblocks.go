package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

// Code blocks longer than maxCodeBlockLines are cut to keepCodeBlockLines,
// with a link to the README for the rest. One README (aws-rekognition-
// playground) carried a 3,800-line JSON dump that made its post 445KB of
// highlighted HTML; nobody reads that inline. The limit sits well above the
// longest real script or config in any README (about 300 lines), so only
// dumps like that one are cut.
const (
	maxCodeBlockLines  = 500
	keepCodeBlockLines = 40
)

var fenceOpen = regexp.MustCompile("^(\\s*)(```+|~~~+)")

// truncateLongCodeBlocks shortens fenced code blocks over the limit. The
// fence keeps its indentation (blocks inside list items stay inside them)
// and the note after it links to the README on GitHub.
func truncateLongCodeBlocks(body, repoHTMLURL string) string {
	lines := strings.Split(body, "\n")
	out := make([]string, 0, len(lines))
	for i := 0; i < len(lines); i++ {
		m := fenceOpen.FindStringSubmatch(lines[i])
		if m == nil {
			out = append(out, lines[i])
			continue
		}
		indent, fence := m[1], m[2]
		end := -1
		for j := i + 1; j < len(lines); j++ {
			t := strings.TrimSpace(lines[j])
			if strings.HasPrefix(t, fence) && strings.Trim(t, fence[:1]) == "" {
				end = j
				break
			}
		}
		if end < 0 { // unclosed fence: leave the rest untouched
			out = append(out, lines[i:]...)
			break
		}
		n := end - i - 1
		if n <= maxCodeBlockLines {
			out = append(out, lines[i:end+1]...)
		} else {
			out = append(out, lines[i:i+1+keepCodeBlockLines]...)
			out = append(out, lines[end], "")
			out = append(out, fmt.Sprintf("%s*… %d more lines — see the [full README](%s#readme).*", indent, n-keepCodeBlockLines, repoHTMLURL))
		}
		i = end
	}
	return strings.Join(out, "\n")
}

var repoURLLine = regexp.MustCompile(`(?m)^repoHTMLURL = "([^"]+)"`)

// trimExisting applies truncateLongCodeBlocks to every generated-*.md in dir,
// so the rule reaches posts without re-fetching every README. Returns how
// many files changed.
func trimExisting(dir string) (int, error) {
	files, err := filepath.Glob(filepath.Join(dir, "generated-*.md"))
	if err != nil {
		return 0, err
	}
	changed := 0
	for _, f := range files {
		b, err := os.ReadFile(f)
		if err != nil {
			return changed, err
		}
		s := string(b)
		m := repoURLLine.FindStringSubmatch(s)
		if m == nil {
			continue
		}
		out := truncateLongCodeBlocks(s, m[1])
		if out == s {
			continue
		}
		if err := os.WriteFile(f, []byte(out), 0o644); err != nil {
			return changed, err
		}
		changed++
	}
	return changed, nil
}
