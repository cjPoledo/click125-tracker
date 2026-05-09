export interface ChecklistItem {
  title: string;
  description: string;
}

const ITEMS: ChecklistItem[] = [
  { title: 'Fuel',               description: 'Check fuel level; refuel before riding if low.' },
  { title: 'Throttle',           description: 'Confirm throttle opens smoothly and snaps fully closed in all steering positions.' },
  { title: 'Engine oil',         description: 'Check oil level via sight glass on right crankcase; top up if needed.' },
  { title: 'Coolant',            description: 'Check coolant level in reserve tank; top up with Honda Pre-Mix Coolant if low.' },
  { title: 'Brake fluid',        description: 'Check brake fluid level in reservoir; top up with DOT 3 or DOT 4 if low.' },
  { title: 'Brake pads / shoes', description: 'Check brake pad and shoe wear; replace if at or near the wear indicator.' },
  { title: 'Brake system',       description: 'Check lever and pedal travel and feel; confirm rear brake lock engages and releases fully.' },
  { title: 'Lights & horn',      description: 'Check headlight (high/low), tail light, brake light, turn signals, and horn.' },
  { title: 'Side stand',         description: 'Confirm stand retracts fully and the engine cut-off switch works.' },
  { title: 'Tyres',              description: 'Check for cuts, cracks, or embedded objects; verify cold pressure (F: 200 kPa / 29 psi · R: 225 kPa / 33 psi).' },
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
