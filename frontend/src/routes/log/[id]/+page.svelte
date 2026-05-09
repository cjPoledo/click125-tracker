<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { items, showToast } from '$lib/stores';
  import { api } from '$lib/api';
  import type { LogEntry, LogType } from '$lib/types';

  let entry = $state<LogEntry | null>(null);
  let loading = $state(true);
  let editing = $state(false);
  let deleting = $state(false);
  let saving = $state(false);
  let showDeleteConfirm = $state(false);

  let editKm = $state('');
  let editDate = $state('');
  let editNotes = $state('');
  let editLogType = $state<LogType>('inspect');

  const logId = $derived(parseInt($page.params.id, 10));

  onMount(async () => {
    try {
      entry = await api.log.get(logId);
      if (entry) {
        editKm = String(entry.done_at_km);
        editDate = entry.done_date;
        editNotes = entry.notes ?? '';
        editLogType = entry.log_type ?? 'inspect';
      }
    } catch {
      showToast('Entry not found', 'error');
      goto('/log');
    } finally {
      loading = false;
    }
  });

  async function save() {
    if (!entry) return;
    saving = true;
    try {
      const updated = await api.log.update(logId, {
        done_at_km: parseInt(editKm, 10),
        done_date: editDate,
        notes: editNotes.trim() || undefined,
        log_type: editLogType,
      });
      entry = updated;
      const refreshed = await api.items.list();
      items.set(refreshed);
      showToast('Entry updated');
      editing = false;
    } catch {
      showToast('Failed to update entry', 'error');
    } finally {
      saving = false;
    }
  }

  async function deleteEntry() {
    deleting = true;
    try {
      await api.log.delete(logId);
      const refreshed = await api.items.list();
      items.set(refreshed);
      showToast('Entry deleted');
      goto('/log');
    } catch {
      showToast('Failed to delete entry', 'error');
      deleting = false;
    }
  }

  function formatDate(d: string) {
    return new Date(d + 'T00:00:00').toLocaleDateString('en-PH', {
      weekday: 'long', month: 'long', day: 'numeric', year: 'numeric',
    });
  }
</script>

<svelte:head><title>{entry?.item_name ?? 'Log Entry'} — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header" style="display: flex; align-items: center; gap: 12px;">
    <a href="/log" class="back-btn" aria-label="Go back">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
    </a>
    <h1 class="page-title" style="font-size: var(--text-xl);">Log Entry</h1>
  </div>

  <div class="content">
    {#if loading}
      <div class="empty-state"><div class="spinner" style="margin: 0 auto;"></div></div>
    {:else if entry}
      {#if !editing}
        <div class="card" style="margin-bottom: var(--space-md);">
          <div style="font-size: var(--text-xs); color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;">Maintenance Type</div>
          <div style="font-size: var(--text-lg); font-weight: 700;">{entry.item_name}</div>
        </div>

        <div class="detail-row">
          <span class="detail-label">Action</span>
          <span class="log-type-badge" class:badge-replace={entry.log_type === 'replace'}>
            {entry.log_type === 'replace' ? 'Replaced' : 'Inspected'}
          </span>
        </div>
        <div class="divider"></div>
        <div class="detail-row">
          <span class="detail-label">Odometer</span>
          <span class="detail-value odometer">{entry.done_at_km.toLocaleString()} km</span>
        </div>
        <div class="divider"></div>
        <div class="detail-row">
          <span class="detail-label">Date</span>
          <span class="detail-value">{formatDate(entry.done_date)}</span>
        </div>
        {#if entry.notes}
          <div class="divider"></div>
          <div class="detail-row" style="flex-direction: column; align-items: flex-start; gap: 4px;">
            <span class="detail-label">Notes</span>
            <span class="detail-value" style="font-style: italic; color: var(--color-text-muted);">{entry.notes}</span>
          </div>
        {/if}

        <div style="margin-top: var(--space-xl); display: flex; flex-direction: column; gap: var(--space-sm);">
          <button class="btn btn-secondary btn-full" onclick={() => (editing = true)}>
            Edit Entry
          </button>
          <button class="btn btn-danger btn-full" onclick={() => (showDeleteConfirm = true)}>
            Delete Entry
          </button>
        </div>
      {:else}
        <h2 style="font-size: var(--text-lg); font-weight: 600; margin-bottom: var(--space-md); color: var(--color-text-muted);">
          {entry.item_name}
        </h2>

        <div class="form-group">
          <span class="label">Action</span>
          <div class="type-toggle">
            <button
              type="button"
              class="toggle-btn"
              class:active={editLogType === 'inspect'}
              onclick={() => (editLogType = 'inspect')}
            >Inspected</button>
            <button
              type="button"
              class="toggle-btn toggle-replace"
              class:active={editLogType === 'replace'}
              onclick={() => (editLogType = 'replace')}
            >Replaced</button>
          </div>
        </div>

        <div class="form-group">
          <label class="label" for="edit-km">Odometer at service (km)</label>
          <input id="edit-km" type="number" inputmode="numeric" class="input odometer" bind:value={editKm} required min="0" style="font-size: 18px;" />
        </div>
        <div class="form-group">
          <label class="label" for="edit-date">Date</label>
          <input id="edit-date" type="date" class="input" bind:value={editDate} required />
        </div>
        <div class="form-group">
          <label class="label" for="edit-notes">Notes (optional)</label>
          <textarea id="edit-notes" class="input" bind:value={editNotes} rows="3" style="resize: none;"></textarea>
        </div>

        <div style="display: flex; gap: var(--space-sm); margin-top: var(--space-md);">
          <button class="btn btn-secondary btn-full" onclick={() => (editing = false)}>Cancel</button>
          <button class="btn btn-primary btn-full" onclick={save} disabled={saving}>
            {#if saving}<span class="spinner"></span>{:else}Save{/if}
          </button>
        </div>
      {/if}
    {/if}
  </div>
</div>

<!-- Delete confirm modal -->
{#if showDeleteConfirm}
  <div class="modal-overlay" role="dialog" aria-modal="true">
    <div class="modal">
      <h2 class="modal-title">Delete Entry?</h2>
      <p style="color: var(--color-text-muted); margin-bottom: var(--space-lg);">This action cannot be undone.</p>
      <div style="display: flex; gap: var(--space-sm);">
        <button class="btn btn-secondary btn-full" onclick={() => (showDeleteConfirm = false)}>Cancel</button>
        <button class="btn btn-danger btn-full" onclick={deleteEntry} disabled={deleting}>
          {#if deleting}<span class="spinner"></span>{:else}Delete{/if}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .back-btn {
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    color: var(--color-text-muted);
    flex-shrink: 0;
  }

  .detail-row { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; padding: var(--space-sm) 0; }
  .detail-label { font-size: var(--text-sm); color: var(--color-text-muted); }
  .detail-value { font-size: var(--text-base); font-weight: 500; text-align: right; }

  .log-type-badge {
    font-size: var(--text-xs); font-weight: 600;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    background: rgba(100, 116, 139, 0.15); color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.03em;
  }
  .log-type-badge.badge-replace {
    background: rgba(204, 0, 0, 0.15); color: var(--color-primary);
  }

  .type-toggle {
    display: grid; grid-template-columns: 1fr 1fr;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 3px; gap: 3px;
  }
  .toggle-btn {
    min-height: 42px;
    border-radius: calc(var(--radius-md) - 3px);
    font-size: var(--text-sm); font-weight: 600;
    color: var(--color-text-muted);
    transition: background 150ms ease, color 150ms ease;
    cursor: pointer;
  }
  .toggle-btn.active { background: var(--color-surface-raised); color: var(--color-text); }
  .toggle-replace.active { background: rgba(204, 0, 0, 0.15); color: var(--color-primary); }

  .modal-overlay {
    position: fixed; inset: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex; align-items: flex-end;
    z-index: 300;
  }
  .modal {
    background: var(--color-surface);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    padding: var(--space-lg);
    width: 100%;
    padding-bottom: calc(var(--space-lg) + var(--safe-bottom));
  }
  .modal-title { font-size: var(--text-xl); font-weight: 700; margin-bottom: var(--space-sm); }
</style>
