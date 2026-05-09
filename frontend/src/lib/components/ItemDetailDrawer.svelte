<script lang="ts">
  import { goto } from '$app/navigation';
  import { selectedItem } from '$lib/stores';
  import { api } from '$lib/api';
  import StatusBadge from './StatusBadge.svelte';
  import type { LogEntry, MaintenanceItem, MaintenanceLevel } from '$lib/types';

  let item = $derived($selectedItem);
  let open = $derived(item !== null);

  let history = $state<LogEntry[]>([]);
  let loadingHistory = $state(false);

  $effect(() => {
    if (!item) { history = []; return; }
    loadingHistory = true;
    api.log.listByItem(item.id)
      .then(h => { history = h; })
      .catch(() => { history = []; })
      .finally(() => { loadingHistory = false; });
  });

  function close() {
    selectedItem.set(null);
  }

  function logService() {
    if (!item) return;
    const id = item.id;
    close();
    goto(`/log/new?item_id=${id}`);
  }

  function intervalLabel(item: MaintenanceItem): string {
    const { interval_km, interval_months } = item;
    if (interval_km && interval_months) {
      return `Every ${interval_km.toLocaleString()} km or ${monthsLabel(interval_months)} — whichever comes first`;
    }
    if (interval_km) return `Every ${interval_km.toLocaleString()} km`;
    if (interval_months) return monthsLabel(interval_months, true);
    return 'Inspect as needed — no fixed interval';
  }

  function monthsLabel(months: number, capitalize = false): string {
    if (months === 12) return capitalize ? 'Annual (every 12 months)' : 'annual (every 12 months)';
    if (months === 24) return capitalize ? 'Every 2 years' : 'every 2 years';
    if (months === 36) return capitalize ? 'Every 3 years' : 'every 3 years';
    return capitalize ? `Every ${months} months` : `every ${months} months`;
  }

  function intervalExtra(name: string): string | null {
    if (name === 'Engine Oil Change') return 'First change at 1,000 km.';
    if (name === 'Spark Plug') return 'Inspect at 6,000 km; replace at 12,000 km — alternating every 6,000 km.';
    if (name === 'Drive Belt') return 'Inspect at 12,000 km; replace at 24,000 km — alternating every 12,000 km.';
    if (name === 'Engine Idle Speed') return 'Also check at 1,000 km.';
    if (name === 'Brake System') return 'Also check at 1,000 km.';
    if (name === 'Nuts & Bolts') return 'Also check at 1,000 km.';
    return null;
  }

  function replaceDueLabel(days: number): string {
    if (days < 0) return `${Math.abs(days)} days overdue`;
    if (days === 0) return 'Due today';
    return `${days} days remaining`;
  }

  const LEVEL_EMOJI: Record<NonNullable<MaintenanceLevel>, string> = {
    Standard:     '🔵',
    Intermediate: '🟡',
    Technical:    '🔴',
  };

  const LEVEL_DESC: Record<NonNullable<MaintenanceLevel>, string> = {
    Standard:     'Owner serviceable',
    Intermediate: 'Dealer recommended',
    Technical:    'Dealer required',
  };

  function nextDueLabel(item: MaintenanceItem): string {
    if (!item.last_done_date) return '—';
    const parts: string[] = [];
    if (item.km_remaining !== null) {
      const km = item.km_remaining;
      parts.push(km >= 0 ? `${km.toLocaleString()} km remaining` : `${Math.abs(km).toLocaleString()} km overdue`);
    }
    if (item.days_remaining !== null) {
      const d = item.days_remaining;
      parts.push(d >= 0 ? `${d} days remaining` : `${Math.abs(d)} days overdue`);
    }
    return parts.length ? parts.join(' · ') : '—';
  }
</script>

{#if open && item}
  <!-- Backdrop -->
  <div
    class="backdrop"
    role="presentation"
    onclick={close}
    aria-hidden="true"
  ></div>

  <!-- Drawer -->
  <div class="drawer" role="dialog" aria-modal="true" aria-label={item.name}>
    <!-- Drag handle -->
    <div class="drag-handle"></div>

    <!-- Scrollable content -->
    <div class="drawer-scroll">

      <!-- Header -->
      <div class="drawer-header">
        <div class="header-main">
          <h2 class="item-title">{item.name}</h2>
          {#if item.maintenance_level}
            <div class="level-row">
              <span class="level-badge level-{item.maintenance_level.toLowerCase()}">
                {LEVEL_EMOJI[item.maintenance_level]} {item.maintenance_level}
              </span>
              <span class="level-desc">{LEVEL_DESC[item.maintenance_level]}</span>
            </div>
          {/if}
        </div>
        <button class="close-btn" onclick={close} aria-label="Close">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Service Interval -->
      <section class="drawer-section">
        <h3 class="section-label">Service Interval</h3>
        <p class="interval-text">{intervalLabel(item)}</p>
        {#if intervalExtra(item.name)}
          <p class="interval-extra">{intervalExtra(item.name)}</p>
        {/if}
      </section>

      <!-- Current Status -->
      <section class="drawer-section">
        <h3 class="section-label">Current Status</h3>
        <div class="status-row">
          <StatusBadge status={item.status} />
        </div>
        <div class="status-grid">
          <div class="status-cell">
            <span class="cell-label">Last serviced</span>
            {#if item.last_done_date}
              <span class="cell-value">{item.last_done_date} · <span class="odometer">{item.last_done_km?.toLocaleString()} km</span></span>
            {:else}
              <span class="cell-value muted">Never logged</span>
            {/if}
          </div>
          <div class="status-cell">
            <span class="cell-label">Next due</span>
            <span class="cell-value">{nextDueLabel(item)}</span>
          </div>
          {#if item.replace_days_remaining !== null}
            <div class="status-cell" style="margin-top: 8px;">
              <span class="cell-label">Mandatory replace due</span>
              <span class="cell-value" class:overdue-text={item.replace_days_remaining < 0}>
                {replaceDueLabel(item.replace_days_remaining)}
              </span>
            </div>
          {/if}
          {#if item.replace_months !== null && item.last_replace_date}
            <div class="status-cell">
              <span class="cell-label">Last replaced</span>
              <span class="cell-value">
                {item.last_replace_date}
                {#if item.last_replace_km !== null}
                  · <span class="odometer">{item.last_replace_km.toLocaleString()} km</span>
                {/if}
              </span>
            </div>
          {/if}
        </div>
      </section>

      <!-- What to Do -->
      {#if item.notes}
        <section class="drawer-section">
          <h3 class="section-label">What to Do</h3>
          <p class="notes-text">{item.notes}</p>
        </section>
      {/if}

      <!-- Service History -->
      <section class="drawer-section">
        <h3 class="section-label">Service History</h3>
        {#if loadingHistory}
          <p class="muted">Loading…</p>
        {:else if history.length === 0}
          <p class="muted">No history yet.</p>
        {:else}
          <ul class="history-list">
            {#each history as entry (entry.id)}
              <li class="history-entry">
                <div class="history-top">
                  <span class="history-date">{entry.done_date}</span>
                  <div class="history-right">
                    <span class="log-type-pill" class:log-type-replace={entry.log_type === 'replace'}>
                      {entry.log_type === 'replace' ? 'Replaced' : 'Inspected'}
                    </span>
                    <span class="history-km odometer">{entry.done_at_km.toLocaleString()} km</span>
                  </div>
                </div>
                {#if entry.notes}
                  <p class="history-notes">{entry.notes}</p>
                {/if}
              </li>
            {/each}
          </ul>
        {/if}
      </section>

      <!-- Footer -->
      <div class="drawer-footer">
        <button class="btn btn-primary btn-full" onclick={logService}>+ Log Service</button>
        <p class="source-line">Source: Honda Click 125i 2024 Owner's Manual</p>
      </div>

    </div>
  </div>
{/if}

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    z-index: 200;
    animation: fadeIn 150ms ease;
  }

  .drawer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 201;
    background: var(--color-surface);
    border-radius: 16px 16px 0 0;
    max-height: 90dvh;
    display: flex;
    flex-direction: column;
    animation: slideUp 220ms cubic-bezier(0.32, 0.72, 0, 1);
  }

  .drag-handle {
    width: 36px;
    height: 4px;
    background: var(--color-border);
    border-radius: 2px;
    margin: 10px auto 0;
    flex-shrink: 0;
  }

  .drawer-scroll {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    padding: var(--space-md) var(--space-md) calc(var(--space-lg) + env(safe-area-inset-bottom));
  }

  /* Header */
  .drawer-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: var(--space-md);
  }

  .header-main { flex: 1; }

  .item-title {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: 6px;
    line-height: 1.2;
  }

  .level-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .level-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 8px;
    border-radius: var(--radius-full);
    font-size: var(--text-xs);
    font-weight: 600;
  }

  .level-standard     { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
  .level-intermediate { background: rgba(245, 158, 11, 0.15);  color: #fbbf24; }
  .level-technical    { background: rgba(239, 68, 68, 0.15);   color: #f87171; }

  .level-desc { font-size: var(--text-xs); color: var(--color-text-muted); }

  .close-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    color: var(--color-text-muted);
    flex-shrink: 0;
    cursor: pointer;
    transition: color 150ms ease;
  }
  .close-btn:hover { color: var(--color-text); }

  /* Sections */
  .drawer-section {
    border-top: 1px solid var(--color-border);
    padding-top: var(--space-md);
    margin-top: var(--space-md);
  }

  .section-label {
    font-size: var(--text-xs);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--color-text-muted);
    margin-bottom: 8px;
  }

  /* Interval */
  .interval-text {
    font-size: var(--text-base);
    color: var(--color-text);
    font-weight: 500;
    line-height: 1.4;
  }

  .interval-extra {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    margin-top: 4px;
    font-style: italic;
  }

  /* Status */
  .status-row { margin-bottom: 10px; }

  .status-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .status-cell { display: flex; flex-direction: column; gap: 2px; }
  .cell-label  { font-size: var(--text-xs); color: var(--color-text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }
  .cell-value  { font-size: var(--text-sm); color: var(--color-text); }
  .muted       { color: var(--color-text-muted); }
  .overdue-text { color: var(--color-overdue); }

  /* Notes */
  .notes-text {
    font-size: var(--text-sm);
    color: var(--color-text);
    line-height: 1.6;
  }

  /* History */
  .history-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .history-entry {
    padding: var(--space-sm);
    background: var(--color-surface-raised);
    border-radius: var(--radius-md);
  }

  .history-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
  }

  .history-date  { font-size: var(--text-sm); color: var(--color-text); font-weight: 500; }
  .history-right { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
  .history-km    { font-size: var(--text-sm); color: var(--color-text-muted); }
  .history-notes { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 4px; }

  .log-type-pill {
    font-size: 10px; font-weight: 600;
    padding: 2px 7px;
    border-radius: var(--radius-full);
    background: rgba(100, 116, 139, 0.15); color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.03em;
    white-space: nowrap;
  }
  .log-type-pill.log-type-replace {
    background: rgba(204, 0, 0, 0.15); color: var(--color-primary);
  }

  /* Footer */
  .drawer-footer {
    border-top: 1px solid var(--color-border);
    padding-top: var(--space-md);
    margin-top: var(--space-md);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
  }

  .source-line {
    font-size: 11px;
    color: var(--color-text-muted);
    text-align: center;
    font-style: italic;
  }

  @keyframes fadeIn  { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
</style>
