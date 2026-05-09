export interface ChecklistItem {
  title: string;
  description: string;
}

const ITEMS: ChecklistItem[] = [
  { title: 'Fuel',               description: 'Check fuel level; refuel before riding if low.' },
  { title: 'Throttle',           description: 'Confirm throttle opens smoothly and snaps fully closed in all steering positions.' },
  { title: 'Engine oil',         description: 'Check oil level on the dipstick (right side of engine); top up with 10W-30 MB oil if below upper mark. Check for leaks.' },
  { title: 'Coolant',            description: 'Check coolant level in reserve tank; top up with Honda Pre-Mix Coolant if low.' },
  { title: 'Brake fluid',        description: 'Verify fluid is above the LWR mark. If low, check pad wear first — if pads are fine, you likely have a leak; see your dealer.' },
  { title: 'Brake pads / shoes', description: 'Front: inspect pads through the caliper port; replace if worn to the indicator. Rear: apply brake — if the arrow on the brake arm aligns with the reference mark on the panel, shoes must be replaced.' },
  { title: 'Brake system',       description: 'Check brake lever and pedal feel. Rear brake lever freeplay should be 10–20 mm; adjust if needed. Confirm brake lock lever engages and releases cleanly.' },
  { title: 'Lights & horn',      description: 'Check headlight (high/low), tail light, brake light, turn signals, and horn.' },
  { title: 'Side stand',         description: 'Confirm stand spring is intact and stand retracts fully. Test cut-off: start engine, then lower stand — the engine must stop.' },
  { title: 'Tyres',              description: 'Check for cuts, cracks, embedded objects, and unusual bulges in the sidewalls. Verify cold tyre pressure (F: 200 kPa / 29 psi · R: 225 kPa / 33 psi) and check tread wear indicators.' },
];

function todayKey(): string {
  return `checklist_${new Date().toISOString().slice(0, 10)}`;
}

export function getChecklist(): boolean[] {
  try {
    const raw = localStorage.getItem(todayKey());
    if (raw) {
      const saved: boolean[] = JSON.parse(raw);
      return Array.from({ length: ITEMS.length }, (_, i) => saved[i] ?? false);
    }
  } catch {
    /* ignore */
  }
  return new Array(ITEMS.length).fill(false);
}

export function saveChecklist(state: boolean[]): void {
  localStorage.setItem(todayKey(), JSON.stringify(state));
}

export { ITEMS as CHECKLIST_ITEMS };
