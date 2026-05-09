export type Status = 'ok' | 'due_soon' | 'overdue' | 'inspect';

export interface Motorcycle {
  id: number;
  name: string;
  year: number;
  current_odometer_km: number;
  last_odometer_update: string | null;
}

export interface MaintenanceItem {
  id: number;
  name: string;
  interval_km: number | null;
  interval_months: number | null;
  notes: string | null;
  status: Status;
  last_done_km: number | null;
  last_done_date: string | null;
  last_log_id: number | null;
  km_remaining: number | null;
  days_remaining: number | null;
}

export interface LogEntry {
  id: number;
  item_id: number;
  item_name: string | null;
  done_at_km: number;
  done_date: string;
  notes: string | null;
  created_at: string | null;
}

export interface LogPage {
  total: number;
  page: number;
  page_size: number;
  items: LogEntry[];
}

export interface StatusSummary {
  current_odometer_km: number;
  total_items: number;
  ok: number;
  due_soon: number;
  overdue: number;
  inspect: number;
}

export interface Settings {
  telegram_bot_token: string | null;
  telegram_chat_id: string | null;
}
