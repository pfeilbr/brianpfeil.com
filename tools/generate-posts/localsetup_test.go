package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

var testLocal = LocalSetup{
	Profiles:      []string{"root-AWSAdministratorAccess", "hub01-admin", "admin"},
	Accounts:      []string{"529276214230"},
	HomeDirs:      []string{"/Users/pfeilbr"},
	WorkspaceDirs: []string{"projects", "dev", "tmp"},
	Replace:       map[string]string{"~/dev/emsdk": "/path/to/emsdk"},
	DropLines: []string{`(?i)^\s*[-*]\s+in vs ?code,? select .*kernel`,
		`(?i)^>?\s*Root V8 source directory is @ .* on local machine`},
}

func TestStripLocalSetup(t *testing.T) {
	tests := []struct {
		name, in, want string
	}{
		{"sso login and its comment go, the rest of the block stays",
			"```sh\npipenv install\n\n# login for boto3 credentials\naws sso login --profile root-AWSAdministratorAccess\n```\n",
			"```sh\npipenv install\n```\n"},
		{"a block left empty goes entirely",
			"intro\n\n```sh\n# login\naws sso login\n```\n\nafter\n",
			"intro\n\nafter\n"},
		{"a comment over a group stays when the group continues",
			"```sh\n# setup\naws sso login\naws s3 ls\n```",
			"```sh\n# setup\naws s3 ls\n```"},
		{"personal profile flag removed, quoted or not, mid or end of line",
			"```sh\naws --profile admin s3 ls\naws s3 ls --profile \"hub01-admin\"\nstackery deploy --aws-profile admin \\\n  -e dev\n```",
			"```sh\naws s3 ls\naws s3 ls\nstackery deploy \\\n  -e dev\n```"},
		{"demo profiles and variables are kept",
			"aws --profile partner-01 sts get-caller-identity\naws --profile \"${PROFILE}\" s3 ls\naws --profile administrator s3 ls",
			"aws --profile partner-01 sts get-caller-identity\naws --profile \"${PROFILE}\" s3 ls\naws --profile administrator s3 ls"},
		{"AWS_PROFILE export dropped with its comment",
			"```sh\n# copilot will use `AWS_PROFILE` setting\nexport AWS_PROFILE=admin\n\ncopilot init\n```",
			"```sh\ncopilot init\n```"},
		{"blank lines inside a block nobody touched are kept",
			"```sh\nls\n\n```", "```sh\nls\n\n```"},
		{"cd into a workspace folder dropped; cd into the repo itself shortened",
			"```sh\ncd ~/projects\ngit clone x\n$ cd ~/projects/demo-playground\ncd /Users/pfeilbr/tmp\n```",
			"```sh\ngit clone x\n$ cd demo-playground\n```"},
		{"other paths to the repo become /path/to/<repo>",
			"docker run -v /Users/pfeilbr/Dropbox/mac01/Users/brianpfeil/projects/demo-playground:/src img\nln -s ~/projects/demo-playground wf",
			"docker run -v /path/to/demo-playground:/src img\nln -s /path/to/demo-playground wf"},
		{"a longer repo name is not this repo",
			"cd ~/projects/demo-playground2", "cd ~/projects/demo-playground2"},
		{"home directory becomes $HOME, which still expands inside quotes",
			"VIDEO=\"/Users/pfeilbr/Downloads/a.mp4\"\n# /Users/pfeilbr/tmp (host)",
			"VIDEO=\"$HOME/Downloads/a.mp4\"\n# $HOME/tmp (host)"},
		{"image file names that merely contain the path are untouched",
			"![](https://x/__Users_pfeilbr_Dropbox_a.png)", "![](https://x/__Users_pfeilbr_Dropbox_a.png)"},
		{"B's account becomes the documented example account, in code, ARNs and hostnames",
			"docker push 529276214230.dkr.ecr.us-east-1.amazonaws.com/x\n\"Arn\": \"arn:aws:sts::529276214230:assumed-role/r\"\n<https://ap-529276214230.s3-accesspoint.us-east-1.amazonaws.com>",
			"docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/x\n\"Arn\": \"arn:aws:sts::123456789012:assumed-role/r\"\n<https://ap-123456789012.s3-accesspoint.us-east-1.amazonaws.com>"},
		{"other accounts are left alone",
			"\"AWS\": \"arn:aws:iam::802587217904:root\"", "\"AWS\": \"arn:aws:iam::802587217904:root\""},
		{"exact replacements and drop lines",
			"$ source ~/dev/emsdk_env.sh\n- in vscode select `.venv` kernel in top right\n- visit main.ipynb",
			"$ source /path/to/emsdk_env.sh\n- visit main.ipynb"},
		{"aws sso login in prose is explained, not run, so it stays (minus the profile)",
			"First login (e.g. `aws sso login --profile admin`).",
			"First login (e.g. `aws sso login`)."},
		{"untouched text keeps its blank lines, and an untouched empty block stays",
			"a\n\n\n\nb\n```\n```\n",
			"a\n\n\n\nb\n```\n```\n"},
		{"a dropped line between blanks leaves one blank",
			"a\n\n> Root V8 source directory is @ `~/dev/v8` on local machine\n\nb",
			"a\n\nb"},
		{"only the comment directly above is dropped",
			"```sh\n# copilot does not allow use of root account.\n# copilot will use `AWS_PROFILE` setting\nexport AWS_PROFILE=admin\n\ncopilot init\n```",
			"```sh\n# copilot does not allow use of root account.\n\ncopilot init\n```"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := stripLocalSetup(tt.in, "demo-playground", testLocal); got != tt.want {
				t.Errorf("got:\n%s\nwant:\n%s", got, tt.want)
			}
		})
	}
}

func TestStripLocalSetupIsIdempotent(t *testing.T) {
	in := "```sh\n# login\naws sso login --profile admin\naws --profile admin s3 ls\ncd ~/projects/demo-playground\n```\n"
	once := stripLocalSetup(in, "demo-playground", testLocal)
	if twice := stripLocalSetup(once, "demo-playground", testLocal); twice != once {
		t.Errorf("second pass changed it:\n%s\n---\n%s", once, twice)
	}
}

func TestStripExistingLeavesFrontMatterAndBanner(t *testing.T) {
	dir := t.TempDir()
	post := "+++\ntitle = \"Demo\"\nrepoFullName = \"pfeilbr/demo-playground\"\n+++\n\n" +
		"<div class=\"alert\">\n<a href=\"https://github.com/pfeilbr/demo-playground\">code</a>\n</div>\n\n" +
		"```sh\ncd ~/projects/demo-playground\naws s3 ls --profile admin\n```\n"
	f := filepath.Join(dir, "generated-demo-playground.md")
	if err := os.WriteFile(f, []byte(post), 0o644); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(dir, "hand-written.md"), []byte("cd ~/projects\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	n, err := stripExisting(dir, testLocal)
	if err != nil || n != 1 {
		t.Fatalf("stripExisting = %d, %v; want 1, nil", n, err)
	}
	b, _ := os.ReadFile(f)
	got := string(b)
	if !strings.HasPrefix(got, post[:strings.Index(post, "```")]) {
		t.Errorf("front matter or banner changed:\n%s", got)
	}
	if !strings.Contains(got, "cd demo-playground\naws s3 ls\n") {
		t.Errorf("body not stripped:\n%s", got)
	}
	if n, _ := stripExisting(dir, testLocal); n != 0 {
		t.Errorf("second run changed %d file(s); want 0", n)
	}
}

func TestLoadLocalSetupMalformedFails(t *testing.T) {
	f := filepath.Join(t.TempDir(), "bad.toml")
	os.WriteFile(f, []byte("profiles = [unclosed"), 0o644)
	if _, err := LoadLocalSetup(f); err == nil {
		t.Error("a malformed local_setup.toml must be an error, not an empty rule set")
	}
}

func TestConfigLocalSetupLoads(t *testing.T) {
	cfg, err := LoadConfig()
	if err != nil {
		t.Fatal(err)
	}
	if len(cfg.LocalSetup.Profiles) == 0 || len(cfg.LocalSetup.HomeDirs) == 0 || len(cfg.LocalSetup.Accounts) == 0 ||
		cfg.LocalSetup.Replace["brianpfeilmyfn01"] != "myfunctionapp01" || len(cfg.LocalSetup.DropLines) < 4 {
		t.Fatalf("local_setup not loaded: %+v", cfg.LocalSetup)
	}
	// Every pattern must compile, or the generator panics mid-run.
	stripLocalSetup("x", "y", cfg.LocalSetup)
}
