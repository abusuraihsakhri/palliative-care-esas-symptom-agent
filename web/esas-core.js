// Deterministic ESAS-r scoring; no backend, storage or network required.
export const SYMPTOMS = Object.freeze([
  { key: "pain", label: "Pain", hint: "0 = no pain" },
  { key: "tiredness", label: "Tiredness", hint: "Lack of energy" },
  { key: "drowsiness", label: "Drowsiness", hint: "Feeling sleepy" },
  { key: "nausea", label: "Nausea", hint: "0 = no nausea" },
  { key: "lack_of_appetite", label: "Lack of appetite", hint: "0 = no lack of appetite" },
  { key: "shortness_of_breath", label: "Shortness of breath", hint: "0 = no shortness of breath" },
  { key: "depression", label: "Depression", hint: "Feeling sad" },
  { key: "anxiety", label: "Anxiety", hint: "Feeling nervous" },
  { key: "wellbeing", label: "Wellbeing", hint: "0 = best wellbeing; 10 = worst" },
]);

export function summarizeScores(values) {
  if (values === null || typeof values !== "object" || Array.isArray(values)) {
    throw new TypeError("scores must be an object");
  }
  const allowed = new Set(SYMPTOMS.map((item) => item.key));
  const unknown = Object.keys(values).filter((key) => !allowed.has(key));
  if (unknown.length) throw new RangeError(`Unknown symptom(s): ${unknown.join(", ")}`);

  const scores = {};
  const missing = [];
  let sum = 0;
  for (const { key } of SYMPTOMS) {
    const value = values[key] ?? null;
    if (value !== null && (!Number.isInteger(value) || value < 0 || value > 10)) {
      throw new RangeError(`${key} must be an integer from 0 to 10 or null`);
    }
    scores[key] = value;
    if (value === null) missing.push(key);
    else sum += value;
  }
  return {
    instrument: "ESAS-r",
    scores,
    answered: SYMPTOMS.length - missing.length,
    complete: missing.length === 0,
    missing,
    total: missing.length === 0 ? sum : null,
    maximum_total: 90,
    interpretation: "Descriptive symptom profile only; no validated total-score triage cutoff is applied.",
  };
}
