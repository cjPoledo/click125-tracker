export interface ChecklistItem {
  title: string;
  description: string;
}

const ITEMS: ChecklistItem[] = [
  { title: 'Fuel',         description: 'Check fuel level; refuel before riding if low.' },
  { title: 'Engine oil',   description: 'Check oil level via sight glass on right crankcase; top up if needed.' },
  { title: 'Coolant',      description: 'Check coolant level in reserve tank; top up with distilled water if low.' },
  { title: 'Brakes',       description: 'Check lever and pedal travel and feel; confirm rear brake lock engages and releases fully.' },
  { title: 'Tyres',        description: 'Check for cuts, cracks, or embedded objects; verify pressure (F: 200 kPa · R: 225 kPa).' },
  { title: 'Lights & horn', description: 'Check headlight (high/low), tail light, brake light, turn signals, and horn.' },
  { title: 'Throttle',     description: 'Confirm throttle opens smoothly and snaps fully closed when released.' },
  { title: 'Side stand',   description: 'Confirm stand retracts fully and the cut-off switch returns the engine to idle.' },
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
