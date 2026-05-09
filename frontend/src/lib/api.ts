import type { LogEntry, MaintenanceItem, Motorcycle, Settings, StatusSummary } from './types';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text().catch(() => response.statusText);
    throw new ApiError(response.status, text);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export const api = {
  motorcycle: {
    get: () => request<Motorcycle>('/api/motorcycle'),
    updateOdometer: (km: number) =>
      request<Motorcycle>('/api/motorcycle/odometer', {
        method: 'PUT',
        body: JSON.stringify({ current_odometer_km: km }),
      }),
    updatePurchaseDate: (purchase_date: string | null) =>
      request<Motorcycle>('/api/motorcycle/purchase-date', {
        method: 'PUT',
        body: JSON.stringify({ purchase_date }),
      }),
  },

  items: {
    list: () => request<MaintenanceItem[]>('/api/items'),
  },

  log: {
    list: (page = 1) => request<{ total: number; page: number; page_size: number; items: LogEntry[] }>(`/api/log?page=${page}`),
    listByItem: (itemId: number) => request<LogEntry[]>(`/api/log?item_id=${itemId}`),
    get: (id: number) => request<LogEntry>(`/api/log/${id}`),
    create: (data: { item_id: number; done_at_km: number; done_date: string; notes?: string }) =>
      request<LogEntry>('/api/log', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: number, data: Partial<{ done_at_km: number; done_date: string; notes: string }>) =>
      request<LogEntry>(`/api/log/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id: number) => request<void>(`/api/log/${id}`, { method: 'DELETE' }),
  },

  status: {
    get: () => request<StatusSummary>('/api/status'),
  },

  settings: {
    get: () => request<Settings>('/api/settings'),
    update: (data: Partial<Settings>) =>
      request<Settings>('/api/settings', { method: 'PUT', body: JSON.stringify(data) }),
    testTelegram: () => request<{ ok: boolean; message: string }>('/api/settings/test-telegram', { method: 'POST' }),
  },

  export: {
    download: () => request<unknown>('/api/export'),
  },
};
