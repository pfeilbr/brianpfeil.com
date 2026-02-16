package main

import "testing"

func TestConvertRelativeLinksToAbsolute(t *testing.T) {
	const (
		fullName = "pfeilbr/test-playground"
		htmlURL  = "https://github.com/pfeilbr/test-playground"
		branch   = "main"
	)

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Relative markdown link to file",
			input:    `See [config.json](config.json) for details`,
			expected: `See [config.json](https://github.com/pfeilbr/test-playground/blob/main/config.json) for details`,
		},
		{
			name:     "Relative markdown link with path",
			input:    `Check [README](docs/README.md)`,
			expected: `Check [README](https://github.com/pfeilbr/test-playground/blob/main/docs/README.md)`,
		},
		{
			name:     "Relative markdown image",
			input:    `![Screenshot](images/demo.png)`,
			expected: `![Screenshot](https://raw.githubusercontent.com/pfeilbr/test-playground/main/images/demo.png)`,
		},
		{
			name:     "Relative path with leading ./",
			input:    `[File](./src/main.go)`,
			expected: `[File](https://github.com/pfeilbr/test-playground/blob/main/src/main.go)`,
		},
		{
			name:     "Absolute URL unchanged",
			input:    `[AWS](https://aws.amazon.com)`,
			expected: `[AWS](https://aws.amazon.com)`,
		},
		{
			name:     "Anchor link unchanged",
			input:    `[Top](#heading)`,
			expected: `[Top](#heading)`,
		},
		{
			name:     "HTML img tag with relative path",
			input:    `<img src="images/logo.png" width="100">`,
			expected: `<img src="https://raw.githubusercontent.com/pfeilbr/test-playground/main/images/logo.png" width="100">`,
		},
		{
			name:     "Multiple relative links",
			input:    `See [file1](a.txt) and [file2](b.txt)`,
			expected: `See [file1](https://github.com/pfeilbr/test-playground/blob/main/a.txt) and [file2](https://github.com/pfeilbr/test-playground/blob/main/b.txt)`,
		},
		{
			name:     "Mixed relative and absolute",
			input:    `[Local](data.json) and [Remote](https://example.com)`,
			expected: `[Local](https://github.com/pfeilbr/test-playground/blob/main/data.json) and [Remote](https://example.com)`,
		},
		{
			name:     "Relative image link with extension gets raw URL",
			input:    `[Download](screenshot.png)`,
			expected: `[Download](https://raw.githubusercontent.com/pfeilbr/test-playground/main/screenshot.png)`,
		},
		{
			name:     "Empty alt text in image",
			input:    `![](diagram.svg)`,
			expected: `![](https://raw.githubusercontent.com/pfeilbr/test-playground/main/diagram.svg)`,
		},
		{
			name:     "Path with leading slash",
			input:    `[Root file](/README.md)`,
			expected: `[Root file](https://github.com/pfeilbr/test-playground/blob/main/README.md)`,
		},
		{
			name:     "Protocol relative URL unchanged",
			input:    `[Link](//example.com/page)`,
			expected: `[Link](//example.com/page)`,
		},
		{
			name:     "Mailto link unchanged",
			input:    `[Email](mailto:test@example.com)`,
			expected: `[Email](mailto:test@example.com)`,
		},
		{
			name:     "HTML img without attributes before src",
			input:    `<img src="test.png">`,
			expected: `<img src="https://raw.githubusercontent.com/pfeilbr/test-playground/main/test.png">`,
		},
		{
			name:     "Real example from test README",
			input:    "users are stored in aws secrets manager and sourced from [`users.json`](users.json)",
			expected: "users are stored in aws secrets manager and sourced from [`users.json`](https://github.com/pfeilbr/test-playground/blob/main/users.json)",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := convertRelativeLinksToAbsolute(tt.input, fullName, htmlURL, branch)
			if result != tt.expected {
				t.Errorf("\nInput:    %s\nExpected: %s\nGot:      %s", tt.input, tt.expected, result)
			}
		})
	}
}

func TestConvertRelativeLinksWithMainBranch(t *testing.T) {
	input := `[Config](config.yaml)`
	expected := `[Config](https://github.com/pfeilbr/modern-repo/blob/main/config.yaml)`

	result := convertRelativeLinksToAbsolute(input, "pfeilbr/modern-repo", "https://github.com/pfeilbr/modern-repo", "main")
	if result != expected {
		t.Errorf("\nExpected: %s\nGot:      %s", expected, result)
	}
}

func TestConvertRelativeLinksEdgeCases(t *testing.T) {
	const (
		fullName = "pfeilbr/test-playground"
		htmlURL  = "https://github.com/pfeilbr/test-playground"
		branch   = "main"
	)

	rawBase := "https://raw.githubusercontent.com/" + fullName + "/" + branch
	blobBase := htmlURL + "/blob/" + branch

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Empty branch defaults to main",
			input:    `[File](test.go)`,
			expected: `[File](` + blobBase + `/test.go)`,
		},
		{
			name:     "Link with fragment after relative path",
			input:    `[Section](README.md#section)`,
			expected: `[Section](` + blobBase + `/README.md#section)`,
		},
		{
			name:     "Image with uppercase extension",
			input:    `![Logo](logo.PNG)`,
			expected: `![Logo](` + rawBase + `/logo.PNG)`,
		},
		{
			name:     "Image with jpeg extension",
			input:    `![Photo](photo.jpeg)`,
			expected: `![Photo](` + rawBase + `/photo.jpeg)`,
		},
		{
			name:     "Image with webp extension",
			input:    `![Img](hero.webp)`,
			expected: `![Img](` + rawBase + `/hero.webp)`,
		},
		{
			name:     "Link to non-image file is blob URL",
			input:    `[Script](deploy.sh)`,
			expected: `[Script](` + blobBase + `/deploy.sh)`,
		},
		{
			name:     "http:// link is unchanged",
			input:    `[Old](http://example.com)`,
			expected: `[Old](http://example.com)`,
		},
		{
			name:     "Nested path with many segments",
			input:    `[Deep](src/main/java/com/example/App.java)`,
			expected: `[Deep](` + blobBase + `/src/main/java/com/example/App.java)`,
		},
		{
			name:     "HTML img with attributes before src",
			input:    `<img class="screenshot" src="demo.png" alt="demo">`,
			expected: `<img class="screenshot" src="` + rawBase + `/demo.png" alt="demo">`,
		},
		{
			name:     "HTML img with absolute URL unchanged",
			input:    `<img src="https://example.com/logo.png">`,
			expected: `<img src="https://example.com/logo.png">`,
		},
		{
			name:     "Multiple images on same line",
			input:    `![A](a.png) and ![B](b.svg)`,
			expected: `![A](` + rawBase + `/a.png) and ![B](` + rawBase + `/b.svg)`,
		},
		{
			name:     "Empty input",
			input:    ``,
			expected: ``,
		},
		{
			name:     "No links at all",
			input:    `Just plain text with no links.`,
			expected: `Just plain text with no links.`,
		},
		{
			name:     "Link to directory (no extension)",
			input:    `[Examples](examples)`,
			expected: `[Examples](` + blobBase + `/examples)`,
		},
		{
			name:     "GIF image uses raw URL",
			input:    `![Demo](demo.gif)`,
			expected: `![Demo](` + rawBase + `/demo.gif)`,
		},
		{
			name:     "Markdown link to .png uses raw URL",
			input:    `[Screenshot](screenshot.png)`,
			expected: `[Screenshot](` + rawBase + `/screenshot.png)`,
		},
		{
			name:     "Code block contents should still be processed",
			input:    "See [file](src/index.ts) for implementation",
			expected: "See [file](" + blobBase + "/src/index.ts) for implementation",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := convertRelativeLinksToAbsolute(tt.input, fullName, htmlURL, branch)
			if result != tt.expected {
				t.Errorf("\nInput:    %s\nExpected: %s\nGot:      %s", tt.input, tt.expected, result)
			}
		})
	}
}

func TestConvertRelativeLinksEmptyBranch(t *testing.T) {
	input := `[File](test.go)`
	// Empty branch should default to "main"
	expected := `[File](https://github.com/user/repo/blob/main/test.go)`

	result := convertRelativeLinksToAbsolute(input, "user/repo", "https://github.com/user/repo", "")
	if result != expected {
		t.Errorf("\nExpected: %s\nGot:      %s", expected, result)
	}
}
