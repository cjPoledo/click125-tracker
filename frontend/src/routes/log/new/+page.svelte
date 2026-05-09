<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { items, motorcycle, showToast } from '$lib/stores';
  import { api } from '$lib/api';
  import type { LogType } from '$lib/types';

  let itemId = $state('');
  let doneAtKm = $state($motorcycle ? String($motorcycle.current_odometer_km) : '');
  let doneDate = $state(new Date().toISOString().slice(0, 10));
  let notes = $state('');
  let saving = $state(false);
  let logType = $state<LogType>('inspect');

  const selectedItem = $derived($items.find(i => i.id === parseInt(itemId, 10)) ?? null);

  $effect(() => {
    if (selectedItem) {
      logType = (selectedItem.interval_km === null && selectedItem.interval_months === null)
        ? 'replace'
        : 'inspect';
    }
  });

  // Pre-select item from ?item_id= URL param
  $effect(() => {
    const paramId = $page.url.searchParams.get('item_id');
    if (paramId && !itemId) itemId = paramId;
  });

  // Keep km in sync with motorcycle store on first load
  $effect(() => {
    if ($motorcycle && !doneAtKm) {
      doneAtKm = String($motorcycle.current_odometer_km);
    }
  });

  async function submit(e: Event) {
    e.preventDefault();
    if (!itemId || !doneAtKm || !doneDate) return;
    saving = true;
    try {
      await api.log.create({
        item_id: parseInt(itemId, 10),
        done_at_km: parseInt(doneAtKm, 10),
        done_date: doneDate,
        notes: notes.trim() || undefined,
        log_type: logType,
      });
      const refreshed = await api.items.list();
      items.set(refreshed);
      showToast('Log entry saved');
      goto('/log');
    } catch {
      showToast('Failed to save entry', 'error');
    } finally {
      saving = false;
    }
  }
</script>

<svelte:head><title>New Entry — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header" style="display: flex; align-items: center; gap: 12px;">
    <a href="/log" class="back-btn" aria-label="Go back">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
    </a>
    <h1 class="page-title">New Entry</h1>
  </div>

  <div class="content">
    <form onsubmit={submit}>
      <div class="form-group">
        <label class="label" for="item-select">Maintenance type *</label>
        <select id="item-select" class="input" bind:value={itemId} required>
          <option value="" disabled>Select an item…</option>
          {#each $items as item (item.id)}
            <option value={String(item.id)}>{item.name}</option>
          {/each}
        </select>
      </div>

      <div class="form-group">
        <span class="label">Action *</span>
        <div class="type-toggle">
          <button
            type="button"
            class="toggle-btn"
            class:active={logType === 'inspect'}
            onclick={() => (logType = 'inspect')}
          >Inspected</button>
          <button
            type="button"
            class="toggle-btn toggle-replace"
            class:active={logType === 'replace'}
            onclick={() => (logType = 'replace')}
          >Replaced</button>
        </div>
      </div>

      <div class="form-group">
        <label class="label" for="km-input">Odometer at service (km) *</label>
        <input id="km-input" type="number" inputmode="numeric" class="input odometer" bind:value={doneAtKm} required min="0" placeholder="e.g. 5280" style="font-size: 18px;" />
      </div>

      <div class="form-group">
        <label class="label" for="date-input">Date *</label>
        <input id="date-input" type="date" class="input" bind:value={doneDate} required />
      </div>

      <div class="form-group">
        <label class="label" for="notes-input">Notes (optional)</label>
        <textarea id="notes-input" class="input" bind:value={notes} rows="3" placeholder="Parts used, shop name, cost…" style="resize: none; height: auto;"></textarea>
      </div>

      <div style="margin-top: var(--space-md); display: flex; flex-direction: column; gap: var(--space-sm);">
        <button type="submit" class="btn btn-primary btn-full" disabled={saving || !itemId || !doneAtKm || !doneDate}>
          {#if saving}<span class="spinner"></span> Saving…{:else}Save Entry{/if}
        </button>
        <a href="/log" class="btn btn-secondary btn-full">Cancel</a>
      </div>
    </form>
  </div>
</div>

<style>
  .back-btn {
    display: flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    color: var(--color-text-muted);
    transition: color 150ms ease;
    flex-shrink: 0;
  }
  .back-btn:hover { color: var(--color-text); }

  .type-toggle {
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 3px;
    gap: 3px;
  }

  .toggle-btn {
    min-height: 42px;
    border-radius: calc(var(--radius-md) - 3px);
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--color-text-muted);
    transition: background 150ms ease, color 150ms ease;
    cursor: pointer;
  }

  .toggle-btn.active {
    background: var(--color-surface-raised);
    color: var(--color-text);
  }

  .toggle-replace.active {
    background: rgba(204, 0, 0, 0.15);
    color: var(--color-primary);
  }
</style>
