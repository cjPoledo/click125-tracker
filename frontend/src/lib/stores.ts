import { writable } from 'svelte/store';
import type { MaintenanceItem, Motorcycle } from './types';

export const motorcycle = writable<Motorcycle | null>(null);
export const items = writable<MaintenanceItem[]>([]);
export const selectedItem = writable<MaintenanceItem | null>(null);
export const toastMessage = writable<{ text: string; type: 'success' | 'error' } | null>(null);

let toastTimer: ReturnType<typeof setTimeout>;

export function showToast(text: string, type: 'success' | 'error' = 'success') {
  clearTimeout(toastTimer);
  toastMessage.set({ text, type });
  toastTimer = setTimeout(() => toastMessage.set(null), 4000);
}
