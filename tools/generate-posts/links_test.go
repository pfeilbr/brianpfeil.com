package main

import "testing"

func TestConvertRelativeLinksToAbsolute(t *testing.T) {
	const (
		fullName = "pfeilbr/test-playground"
		htmlURL  = "https://github.com/pfeilbr/test-playground"
		branch   = "master"
	)

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Relative markdown link to file",
			input:    `See [config.json](config.json) for details`,
			expected: `See [config.json](https://github.com/pfeilbr/test-playground/blob/master/config.json) for details`,
		},
		{
			name:     "Relative markdown link with path",
			input:    `Check [README](docs/README.md)`,
			expected: `Check [README](https://github.com/pfeilbr/test-playground/blob/master/docs/README.md)`,
		},
		{
			name:     "Relative markdown image",
			input:    `![Screenshot](images/demo.png)`,
			expected: `![Screenshot](https://raw.githubusercontent.com/pfeilbr/test-playground/master/images/demo.png)`,
		},
		{
			name:     "Relative path with leading ./",
			input:    `[File](./src/main.go)`,
			expected: `[File](https://github.com/pfeilbr/test-playground/blob/master/src/main.go)`,
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
			expected: `<img src="https://raw.githubusercontent.com/pfeilbr/test-playground/master/images/logo.png" width="100">`,
		},
		{
			name:     "Multiple relative links",
			input:    `See [file1](a.txt) and [file2](b.txt)`,
			expected: `See [file1](https://github.com/pfeilbr/test-playground/blob/master/a.txt) and [file2](https://github.com/pfeilbr/test-playground/blob/master/b.txt)`,
		},
		{
			name:     "Mixed relative and absolute",
			input:    `[Local](data.json) and [Remote](https://example.com)`,
			expected: `[Local](https://github.com/pfeilbr/test-playground/blob/master/data.json) and [Remote](https://example.com)`,
		},
		{
			name:     "Relative image link with extension gets raw URL",
			input:    `[Download](screenshot.png)`,
			expected: `[Download](https://raw.githubusercontent.com/pfeilbr/test-playground/master/screenshot.png)`,
		},
		{
			name:     "Empty alt text in image",
			input:    `![](diagram.svg)`,
			expected: `![](https://raw.githubusercontent.com/pfeilbr/test-playground/master/diagram.svg)`,
		},
		{
			name:     "Path with leading slash",
			input:    `[Root file](/README.md)`,
			expected: `[Root file](https://github.com/pfeilbr/test-playground/blob/master/README.md)`,
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
			expected: `<img src="https://raw.githubusercontent.com/pfeilbr/test-playground/master/test.png">`,
		},
		{
			name:     "Real example from test README",
			input:    "users are stored in aws secrets manager and sourced from [`users.json`](users.json)",
			expected: "users are stored in aws secrets manager and sourced from [`users.json`](https://github.com/pfeilbr/test-playground/blob/master/users.json)",
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
