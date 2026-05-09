const ITEMS = [
  'Fuel level — sufficient for the ride?',
  'Engine oil level — within MIN/MAX on dipstick?',
  'Coolant level — within MIN/MAX on reserve tank?',
  'Brake fluid level — within MIN/MAX on reservoir?',
  'Front brake operation — firm lever feel, no excessive play?',
  'Rear brake operation — firm lever feel, rear brake lock releases fully?',
  'Tyre condition — no cuts, cracks, or embedded objects?',
  'Tyre pressure — check and inflate if needed',
  'Lights — headlight (high/low beam), brake light, turn signals all working?',
  'Horn — works?',
  'Throttle — opens smoothly, snaps back when released?',
  'Side stand — retracts fully, cut-off switch working?',
  'Mirrors — properly adjusted?',
  'Loose parts / nuts — nothing obviously loose or rattling?',
];

function todayKey(): string {
  return `checklist_${new Date().toISOString().slice(0, 10)}`;
}

export function getChecklist(): boolean[] {
  try {
    const raw = localStorage.getItem(todayKey());
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return new Array(ITEMS.length).fill(false);
}

export function saveChecklist(state: boolean[]): void {
  localStorage.setItem(todayKey(), JSON.stringify(state));
}

export { ITEMS as CHECKLIST_ITEMS };
