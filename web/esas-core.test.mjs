import assert from "node:assert/strict";
import { test } from "node:test";
import { summarizeScores, SYMPTOMS } from "./esas-core.js";

const full = (value) => Object.fromEntries(SYMPTOMS.map(({ key }) => [key, value]));

test("complete zero and maximum profiles", () => {
  assert.equal(summarizeScores(full(0)).total, 0);
  assert.equal(summarizeScores(full(10)).total, 90);
  assert.equal(summarizeScores(full(10)).answered, 9);
});
test("unanswered is missing rather than a zero", () => {
  const profile = summarizeScores({ pain: 7 });
  assert.equal(profile.total, null);
  assert.equal(profile.answered, 1);
  assert.equal(profile.missing.length, 8);
  assert.equal(profile.scores.wellbeing, null);
});
test("wellbeing has no inverted coding", () => {
  assert.equal(summarizeScores({ ...full(0), wellbeing: 10 }).total, 10);
});
test("reject invalid and unknown ratings", () => {
  for (const value of [-1, 11, 2.5, "4", true, NaN, Infinity]) {
    assert.throws(() => summarizeScores({ pain: value }));
  }
  assert.throws(() => summarizeScores({ foo: 1 }));
  assert.throws(() => summarizeScores(null));
});
