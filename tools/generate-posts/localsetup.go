package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"

	"github.com/BurntSushi/toml"
)

// LocalSetupFile is shared with tools/github-repos/refresh.py.
const LocalSetupFile = "local_setup.toml"

// LoadLocalSetup reads local_setup.toml (relative to the working directory,
// like config.yaml). A missing file means no rules (a test's scratch
// directory); a malformed one is an error. TestConfigLocalSetupLoads holds
// the real file to having rules.
func LoadLocalSetup(path string) (LocalSetup, error) {
	var ls LocalSetup
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return ls, nil
	}
	if _, err := toml.DecodeFile(path, &ls); err != nil {
		return ls, fmt.Errorf("read %s: %w", path, err)
	}
	return ls, nil
}

// LocalSetup lists what in a README only works on B's own laptop: his AWS
// CLI profiles, his home directory, the folders he keeps checkouts in, and a
// few lines that say where he installed something. stripLocalSetup removes
// or generalises these so a lab note's steps work for whoever reads them.
type LocalSetup struct {
	// AWS CLI profiles that exist only in B's ~/.aws/config. Profiles a
	// README defines or depends on as part of its demo (a partner account,
	// an assumed lambda role) are deliberately not listed.
	Profiles []string `toml:"profiles"`
	// B's own AWS account numbers, rewritten to AWS's documented example
	// account, 123456789012. AWS-owned accounts in a README (Ground Truth
	// lambdas, Serverless Inc's trust account) must not be listed here.
	Accounts []string `toml:"accounts"`
	// Absolute home directories, rewritten to $HOME/.
	HomeDirs []string `toml:"home_dirs"`
	// Folders under ~ that B works in; a bare `cd` into one is dropped.
	WorkspaceDirs []string `toml:"workspace_dirs"`
	// Exact strings to rewrite, longest first.
	Replace map[string]string `toml:"replace"`
	// Lines (regexes) that only describe B's machine; dropped.
	DropLines []string `toml:"drop_lines"`
}

// ExampleAccount is the account number AWS's own documentation uses.
const ExampleAccount = "123456789012"

var (
	fenceLine   = regexp.MustCompile("^\\s*(```|~~~)")
	shellCmt    = regexp.MustCompile(`^\s*#`)
	ssoLogin    = regexp.MustCompile(`^\s*(\$\s*)?aws\s+sso\s+login(\s.*)?$`)
	shellPrompt = regexp.MustCompile(`^(\s*(?:\$\s*)?)cd\s+`)
)

// stripLocalSetup rewrites a README body (Markdown) for a reader who is not
// B. repoName is the repo the README belongs to, so a path to B's own
// checkout of it ("~/projects/<repo>") can become "cd <repo>" or
// "/path/to/<repo>".
func stripLocalSetup(body, repoName string, ls LocalSetup) string {
	keys := make([]string, 0, len(ls.Replace))
	for k := range ls.Replace {
		keys = append(keys, k)
	}
	sort.Slice(keys, func(i, j int) bool {
		if len(keys[i]) != len(keys[j]) {
			return len(keys[i]) > len(keys[j])
		}
		return keys[i] < keys[j]
	})

	homes := make([]string, 0, len(ls.HomeDirs))
	for _, h := range ls.HomeDirs {
		homes = append(homes, regexp.QuoteMeta(strings.TrimSuffix(h, "/")))
	}
	homeAlt := "~"
	if len(homes) > 0 {
		homeAlt = "(?:~|" + strings.Join(homes, "|") + ")"
	}

	var ownRepo, cdOwnRepo *regexp.Regexp
	if repoName != "" {
		p := homeAlt + "(?:/[^\\s:'\"`]*?)?/projects/" + regexp.QuoteMeta(repoName) + `\b`
		ownRepo = regexp.MustCompile(p)
		cdOwnRepo = regexp.MustCompile(`^(\s*(?:\$\s*)?)cd\s+` + p + `/?\s*$`)
	}
	var workspaceCd *regexp.Regexp
	if len(ls.WorkspaceDirs) > 0 {
		ws := make([]string, 0, len(ls.WorkspaceDirs))
		for _, w := range ls.WorkspaceDirs {
			ws = append(ws, regexp.QuoteMeta(strings.Trim(w, "/")))
		}
		workspaceCd = regexp.MustCompile(`^\s*(\$\s*)?cd\s+` + homeAlt + `/(?:` + strings.Join(ws, "|") + `)/?\s*$`)
	}
	var profileFlag, profileEnv []*regexp.Regexp
	for _, p := range ls.Profiles {
		q := regexp.QuoteMeta(p)
		val := `(?:"` + q + `"|'` + q + `'|` + q + `)`
		profileFlag = append(profileFlag, regexp.MustCompile(`[ \t]+--(?:aws-)?profile[= ]`+val+"([\\s`)\\\\]|$)"))
		profileEnv = append(profileEnv, regexp.MustCompile(`^\s*(?:export\s+)?AWS_PROFILE=`+val+`\s*$`))
	}
	var drops []*regexp.Regexp
	for _, d := range ls.DropLines {
		drops = append(drops, regexp.MustCompile(d))
	}
	var homeDir []*regexp.Regexp
	for _, h := range homes {
		homeDir = append(homeDir, regexp.MustCompile(h+`(/|\b)`))
	}

	lines := strings.Split(body, "\n")
	out := make([]string, 0, len(lines))
	inFence := false
	fenceStart := -1 // index in out of the open fence line
	droppedInFence := false

	skipBlank := false
	dropped := func(i int) {
		next := ""
		if i+1 < len(lines) {
			next = lines[i+1]
		}
		nextBlank := strings.TrimSpace(next) == ""
		// A shell comment directly above a dropped command explains only
		// that command when nothing follows it in the same group, so it
		// goes too ("# login for boto3 credentials" over "aws sso login").
		// Only the one line directly above: a comment further up usually
		// says something more general ("copilot does not allow use of
		// root account") that is still true.
		if inFence && (nextBlank || fenceLine.MatchString(next)) &&
			len(out) > fenceStart+1 && shellCmt.MatchString(out[len(out)-1]) {
			out = out[:len(out)-1]
		}
		// Don't leave two blank lines (or a blank first line in a block)
		// where the dropped line sat.
		atStart := len(out) == 0 || (inFence && len(out) == fenceStart+1)
		if nextBlank && (atStart || strings.TrimSpace(out[len(out)-1]) == "") {
			skipBlank = true
		}
	}

	for i, line := range lines {
		if skipBlank {
			skipBlank = false
			if strings.TrimSpace(line) == "" {
				continue
			}
		}
		if fenceLine.MatchString(line) {
			if !inFence {
				inFence, fenceStart, droppedInFence = true, len(out), false
			} else {
				inFence = false
				// A block left with nothing but blank lines goes entirely.
				empty := true
				for _, l := range out[fenceStart+1:] {
					if strings.TrimSpace(l) != "" {
						empty = false
						break
					}
				}
				if empty && droppedInFence {
					out = out[:fenceStart]
					// and the blank line that separated it from what follows
					skipBlank = len(out) > 0 && strings.TrimSpace(out[len(out)-1]) == ""
					continue
				}
				// Nor does a block end on blank lines a dropped line left.
				if droppedInFence {
					for len(out) > fenceStart+1 && strings.TrimSpace(out[len(out)-1]) == "" {
						out = out[:len(out)-1]
					}
				}
			}
			out = append(out, line)
			continue
		}

		for _, k := range keys {
			line = strings.ReplaceAll(line, k, ls.Replace[k])
		}
		for _, a := range ls.Accounts {
			line = strings.ReplaceAll(line, a, ExampleAccount)
		}
		drop := false
		for _, d := range drops {
			if d.MatchString(line) {
				drop = true
			}
		}
		if inFence && ssoLogin.MatchString(line) {
			drop = true
		}
		for _, re := range profileEnv {
			if re.MatchString(line) {
				drop = true
			}
		}
		if workspaceCd != nil && workspaceCd.MatchString(line) {
			drop = true
		}
		if drop {
			dropped(i)
			if inFence {
				droppedInFence = true
			}
			continue
		}

		if cdOwnRepo != nil && cdOwnRepo.MatchString(line) {
			prefix := shellPrompt.FindStringSubmatch(line)[1]
			line = prefix + "cd " + repoName
		} else if ownRepo != nil {
			line = ownRepo.ReplaceAllString(line, "/path/to/"+repoName)
		}
		for _, re := range profileFlag {
			line = re.ReplaceAllString(line, "$1")
		}
		for _, re := range homeDir {
			// $HOME, not ~: a tilde inside double quotes is not expanded.
			line = re.ReplaceAllString(line, "$$HOME$1")
		}
		out = append(out, line)
	}

	return strings.Join(out, "\n")
}

var repoNameLine = regexp.MustCompile(`(?m)^repoFullName = "[^"/]+/([^"]+)"`)

// stripExisting applies stripLocalSetup to the generated posts already in
// dir, body only (front matter and the repo banner are left alone), without
// calling GitHub. Returns how many files changed.
func stripExisting(dir string, ls LocalSetup) (int, error) {
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
		m := repoNameLine.FindStringSubmatch(s)
		if m == nil {
			continue
		}
		// The body starts after the front matter's closing +++ and the
		// banner's closing </div>.
		cut := strings.Index(s, "\n+++\n")
		if cut < 0 {
			continue
		}
		cut += len("\n+++\n")
		if d := strings.Index(s[cut:], "</div>\n"); d >= 0 {
			cut += d + len("</div>\n")
		}
		out := s[:cut] + stripLocalSetup(s[cut:], m[1], ls)
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
