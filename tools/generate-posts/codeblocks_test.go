package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func block(fence, indent string, n int) string {
	var b strings.Builder
	b.WriteString(indent + fence + "json\n")
	for i := 1; i <= n; i++ {
		fmt.Fprintf(&b, "%sline %d\n", indent, i)
	}
	b.WriteString(indent + fence)
	return b.String()
}

func TestTruncateLongCodeBlocksKeepsShortBlocks(t *testing.T) {
	in := "intro\n\n" + block("```", "", maxCodeBlockLines) + "\n\nafter"
	if got := truncateLongCodeBlocks(in, "https://github.com/u/r"); got != in {
		t.Errorf("short block changed:\n%s", got)
	}
}

func TestTruncateLongCodeBlocksCutsLongBlocks(t *testing.T) {
	in := "intro\n\n" + block("```", "", 540) + "\n\nafter"
	got := truncateLongCodeBlocks(in, "https://github.com/u/r")
	if !strings.Contains(got, "line 40\n```\n") {
		t.Errorf("expected the block closed after line 40:\n%s", got)
	}
	if strings.Contains(got, "line 41") {
		t.Error("line 41 should be cut")
	}
	if !strings.Contains(got, "*… 500 more lines — see the [full README](https://github.com/u/r#readme).*") {
		t.Errorf("missing note:\n%s", got)
	}
	if !strings.HasSuffix(got, "\n\nafter") {
		t.Error("text after the block lost")
	}
}

func TestTruncateLongCodeBlocksIndentedAndTilde(t *testing.T) {
	in := "* item\n\n" + block("~~~", "    ", 600) + "\n"
	got := truncateLongCodeBlocks(in, "https://github.com/u/r")
	if !strings.Contains(got, "    line 40\n    ~~~\n\n    *… 560 more lines") {
		t.Errorf("indentation not kept:\n%s", got)
	}
}

func TestTruncateLongCodeBlocksUnclosedFence(t *testing.T) {
	in := "```\n" + strings.Repeat("x\n", 700)
	if got := truncateLongCodeBlocks(in, "u"); got != in {
		t.Error("unclosed fence should be left alone")
	}
}

func TestTruncateLongCodeBlocksIsIdempotent(t *testing.T) {
	once := truncateLongCodeBlocks(block("```", "", 900), "u")
	if twice := truncateLongCodeBlocks(once, "u"); twice != once {
		t.Error("second pass changed the output")
	}
}

func TestTrimExisting(t *testing.T) {
	dir := t.TempDir()
	long := "+++\nrepoHTMLURL = \"https://github.com/u/r\"\n+++\n\n" + block("```", "", 900) + "\n"
	short := "+++\nrepoHTMLURL = \"https://github.com/u/s\"\n+++\n\nhi\n"
	write := func(name, s string) {
		if err := os.WriteFile(filepath.Join(dir, name), []byte(s), 0o644); err != nil {
			t.Fatal(err)
		}
	}
	write("generated-long.md", long)
	write("generated-short.md", short)
	write("handwritten.md", long)
	n, err := trimExisting(dir)
	if err != nil || n != 1 {
		t.Fatalf("trimExisting = %d, %v; want 1, nil", n, err)
	}
	b, _ := os.ReadFile(filepath.Join(dir, "handwritten.md"))
	if string(b) != long {
		t.Error("non-generated post was touched")
	}
	b, _ = os.ReadFile(filepath.Join(dir, "generated-long.md"))
	if !strings.Contains(string(b), "https://github.com/u/r#readme") {
		t.Error("generated post not trimmed")
	}
}
