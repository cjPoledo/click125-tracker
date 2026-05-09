<script lang="ts">
  import { goto } from '$app/navigation';
  import { items, motorcycle, showToast } from '$lib/stores';
  import { api } from '$lib/api';

  let itemId = $state('');
  let doneAtKm = $state($motorcycle ? String($motorcycle.current_odometer_km) : '');
  let doneDate = $state(new Date().toISOString().slice(0, 10));
  let notes = $state('');
  let saving = $state(false);

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
</style>
