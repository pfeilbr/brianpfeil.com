// Tests for assets/js/gh-search.js, the query language behind /github/.
//   node --test tools/github-repos/search.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const G = createRequire(import.meta.url)("../../assets/js/gh-search.js");

const AREA = { serverless: "Serverless & IaC", cloud: "Cloud", data: "Données", other: "Other" };
const S0 = { kind: "all", area: [], lang: [], forks: false, art: false, demo: false, rm: true,
  cf: 0, ct: 0, pf: 0, pt: 0, stars: 0 };

function repo(o) {
  return G.prep(Object.assign({ name: "x", desc: "", lang: "", langs: [], areas: ["other"], tags: [],
    kind: "playground", stars: 0, created: "2019-05-01", pushed: "2021-01-01", readme: "" }, o), AREA, o.post);
}
const R = [
  repo({ name: "aws-lambda-go-playground", lang: "Go", areas: ["serverless", "cloud"], tags: ["lambda"], post: "/post/a/" }),
  repo({ name: "aws-step-functions-playground", lang: "JavaScript", areas: ["serverless"], tags: ["step-functions"],
    desc: "Learn Step Functions", created: "2021-02-02", pushed: "2024-03-03", stars: 3 }),
  repo({ name: "dynamo-thing", lang: "Python", areas: ["data"], kind: "project", homepage: "https://x.dev",
    readme: "uses a secret sauce", created: "2015-01-01" }),
  repo({ name: "someone-fork", lang: "Go", kind: "fork", created: "2020-01-01" }),
  repo({ name: "old-archive", lang: "", kind: "project", archived: true, created: "2010-01-01" }),
];
const find = (q, s = {}) => {
  const P = G.parse(q), S = Object.assign({}, S0, s);
  return R.filter((r) => G.match(r, P, S) >= 0).map((r) => r.name);
};

test("range", () => {
  assert.deepEqual(G.range("2019"), [2019, 2019]);
  assert.deepEqual(G.range("2018..2020"), [2018, 2020]);
  assert.deepEqual(G.range(">2020"), [2021, 9999]);
  assert.deepEqual(G.range(">=2020"), [2020, 9999]);
  assert.deepEqual(G.range("<2015"), [0, 2014]);
  assert.deepEqual(G.range("<=2015"), [0, 2015]);
  assert.equal(G.range("soon"), null);
});

test("parse splits words, phrases, exclusions and qualifiers", () => {
  const P = G.parse('lambda "step functions" -azure lang:Go -is:fork language:python stars:>2 year:2019 foo:bar');
  assert.deepEqual(P.words, ["lambda", "foo:bar"]);
  assert.deepEqual(P.phrases, ["step functions"]);
  assert.deepEqual(P.nots, ["azure"]);
  assert.deepEqual(P.lang, ["go", "python"]);
  assert.deepEqual(P.not.is, ["fork"]);
  assert.equal(P.stars, 3);
  assert.deepEqual(P.created, [2019, 2019]);
});

test("free words must all match; forks hidden by default", () => {
  assert.deepEqual(find("lambda"), ["aws-lambda-go-playground"]);
  assert.deepEqual(find("aws playground"), ["aws-lambda-go-playground", "aws-step-functions-playground"]);
  assert.deepEqual(find("lang:go"), ["aws-lambda-go-playground"]);
  assert.deepEqual(find("lang:go", { forks: true }), ["aws-lambda-go-playground", "someone-fork"]);
  assert.deepEqual(find("is:fork"), ["someone-fork"]);
});

test("negated qualifiers exclude", () => {
  assert.deepEqual(find("aws -lang:go"), ["aws-step-functions-playground"]);
  assert.deepEqual(find("-is:playground"), ["dynamo-thing", "old-archive"]);
  assert.deepEqual(find("-is:archived is:project"), ["dynamo-thing"]);
  assert.deepEqual(find("aws -tag:lambda"), ["aws-step-functions-playground"]);
  assert.deepEqual(find("-has:article aws"), ["aws-step-functions-playground"]);
  assert.deepEqual(find("-area:serverless -is:archived"), ["dynamo-thing"]);
});

test("has, dates, stars", () => {
  assert.deepEqual(find("has:article"), ["aws-lambda-go-playground"]);
  assert.deepEqual(find("has:demo"), ["dynamo-thing"]);
  assert.deepEqual(find("created:2018..2020"), ["aws-lambda-go-playground"]);
  assert.deepEqual(find("pushed:>2023"), ["aws-step-functions-playground"]);
  assert.deepEqual(find("stars:>2"), ["aws-step-functions-playground"]);
  assert.deepEqual(find("", { cf: 2015, ct: 2015 }), ["dynamo-thing"]);
});

test("README text only when asked, and accents fold", () => {
  assert.deepEqual(find("sauce"), ["dynamo-thing"]);
  assert.deepEqual(find("sauce", { rm: false }), []);
  assert.deepEqual(find("donnees"), ["dynamo-thing"]);
  assert.deepEqual(find("area:donnees"), ["dynamo-thing"]);
  assert.deepEqual(find('"step functions"'), ["aws-step-functions-playground"]);
});

test("facet skip ignores that facet only", () => {
  const P = G.parse(""), S = Object.assign({}, S0, { lang: ["Python"] });
  const all = R.filter((r) => G.match(r, P, S, "lang") >= 0).length;
  const narrowed = R.filter((r) => G.match(r, P, S) >= 0).length;
  assert.equal(narrowed, 1);
  assert.equal(all, 4);
});

test("scores rank exact names first; sorts", () => {
  const P = G.parse("aws-lambda-go-playground");
  assert.ok(G.match(R[0], P, S0) > 100);
  const byName = R.slice().sort(G.SORTS.name).map((r) => r.name);
  assert.equal(byName[0], "aws-lambda-go-playground");
  const oldest = R.slice().sort(G.SORTS.oldest).map((r) => r.name);
  assert.equal(oldest[0], "old-archive");
  assert.equal(R.slice().sort(G.SORTS.stars)[0].name, "aws-step-functions-playground");
});

test("safeHref", () => {
  assert.equal(G.safeHref("https://x.dev"), "https://x.dev");
  assert.equal(G.safeHref("javascript:alert(1)"), "");
  assert.equal(G.safeHref(undefined), "");
});

test("prep tolerates missing fields", () => {
  const r = G.prep({ name: "bare" }, AREA);
  assert.deepEqual(r.areas, ["other"]);
  assert.ok(G.match(r, G.parse("bare"), S0) >= 0);
});
