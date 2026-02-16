package main

import (
	"fmt"
	"regexp"
	"strings"
)

// convertRelativeLinksToAbsolute rewrites relative markdown and HTML links
// to point at the correct GitHub URLs. Images use raw.githubusercontent.com
// for direct rendering; other files use blob URLs.
func convertRelativeLinksToAbsolute(body, repoFullName, repoHTMLURL, branch string) string {
	if branch == "" {
		branch = "main"
	}

	rawBase := "https://raw.githubusercontent.com/" + repoFullName + "/" + branch
	blobBase := repoHTMLURL + "/blob/" + branch

	isAbsolute := func(url string) bool {
		return strings.HasPrefix(url, "http://") ||
			strings.HasPrefix(url, "https://") ||
			strings.HasPrefix(url, "mailto:") ||
			strings.HasPrefix(url, "//") ||
			strings.HasPrefix(url, "#")
	}

	cleanPath := func(url string) string {
		url = strings.TrimPrefix(url, "./")
		url = strings.TrimPrefix(url, "/")
		return url
	}

	imageExtRe := regexp.MustCompile(`\.(png|jpg|jpeg|gif|svg|webp)$`)

	// Markdown images: ![alt](path)
	imgRe := regexp.MustCompile(`!\[([^\]]*)\]\(([^)]+)\)`)
	body = imgRe.ReplaceAllStringFunc(body, func(match string) string {
		m := imgRe.FindStringSubmatch(match)
		if len(m) == 3 && !isAbsolute(m[2]) {
			return fmt.Sprintf("![%s](%s/%s)", m[1], rawBase, cleanPath(m[2]))
		}
		return match
	})

	// Markdown links: [text](path)
	linkRe := regexp.MustCompile(`\[([^\]]+)\]\(([^)]+)\)`)
	body = linkRe.ReplaceAllStringFunc(body, func(match string) string {
		m := linkRe.FindStringSubmatch(match)
		if len(m) == 3 && !isAbsolute(m[2]) {
			p := cleanPath(m[2])
			if imageExtRe.MatchString(strings.ToLower(p)) {
				return fmt.Sprintf("[%s](%s/%s)", m[1], rawBase, p)
			}
			return fmt.Sprintf("[%s](%s/%s)", m[1], blobBase, p)
		}
		return match
	})

	// HTML img tags: <img src="path">
	htmlImgRe := regexp.MustCompile(`<img\s+([^>]*\s+)?src="([^"]+)"([^>]*)>`)
	body = htmlImgRe.ReplaceAllStringFunc(body, func(match string) string {
		m := htmlImgRe.FindStringSubmatch(match)
		if len(m) == 4 && !isAbsolute(m[2]) {
			return fmt.Sprintf(`<img %ssrc="%s/%s"%s>`, m[1], rawBase, cleanPath(m[2]), m[3])
		}
		return match
	})

	return body
}
