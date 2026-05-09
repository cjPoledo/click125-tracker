<script lang="ts">
  import { goto } from '$app/navigation';
  import StatusBadge from '$lib/components/StatusBadge.svelte';
  import { motorcycle, items, showToast } from '$lib/stores';
  import { api } from '$lib/api';
  import type { Status } from '$lib/types';

  let showOdometerModal = $state(false);
  let newOdometer = $state('');
  let savingOdometer = $state(false);

  const statusOrder: Status[] = ['overdue', 'due_soon', 'ok', 'inspect'];

  let sortedItems = $derived(
    [...$items].sort(
      (a, b) => statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status)
    )
  );

  let counts = $derived({
    ok: $items.filter((i) => i.status === 'ok').length,
    due_soon: $items.filter((i) => i.status === 'due_soon').length,
    overdue: $items.filter((i) => i.status === 'overdue').length,
    inspect: $items.filter((i) => i.status === 'inspect').length,
  });

  let lastUpdate = $derived(() => {
    if (!$motorcycle?.last_odometer_update) return null;
    return new Date($motorcycle.last_odometer_update).toLocaleDateString('en-PH', {
      month: 'short', day: 'numeric', year: 'numeric',
    });
  });

  async function saveOdometer() {
    const km = parseInt(newOdometer, 10);
    if (isNaN(km) || km < 0) return;
    savingOdometer = true;
    try {
      const updated = await api.motorcycle.updateOdometer(km);
      motorcycle.set(updated);
      const refreshed = await api.items.list();
      items.set(refreshed);
      showToast('Odometer updated');
      showOdometerModal = false;
      newOdometer = '';
    } catch {
      showToast('Failed to update odometer', 'error');
    } finally {
      savingOdometer = false;
    }
  }

  function openOdometerModal() {
    newOdometer = $motorcycle ? String($motorcycle.current_odometer_km) : '';
    showOdometerModal = true;
  }
</script>

<svelte:head><title>Dashboard — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
      <h1 class="page-title">Click125 Tracker</h1>
    </div>
    <p style="font-size: 13px; color: var(--color-text-muted);">Honda Click 125i · {$motorcycle?.year ?? 2024}</p>
  </div>

  <div class="content">
    <!-- Odometer card -->
    <button class="odometer-card" onclick={openOdometerModal} aria-label="Update odometer reading">
      <div>
        <span class="odo-label">Current Odometer</span>
        <div class="odo-value odometer">
          {($motorcycle?.current_odometer_km ?? 0).toLocaleString()} <span class="odo-unit">km</span>
        </div>
        {#if lastUpdate()}
          <span class="odo-updated">Updated {lastUpdate()}</span>
        {:else}
          <span class="odo-updated">Tap to set odometer</span>
        {/if}
      </div>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-muted)" stroke-width="2" aria-hidden="true">
        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
      </svg>
    </button>

    <!-- Status summary -->
    {#if $items.length > 0}
      <div class="status-summary">
        <div class="summary-chip" style="color: var(--color-overdue);">
          <strong>{counts.overdue}</strong> overdue
        </div>
        <div class="summary-chip" style="color: var(--color-due-soon);">
          <strong>{counts.due_soon}</strong> due soon
        </div>
        <div class="summary-chip" style="color: var(--color-ok);">
          <strong>{counts.ok}</strong> OK
        </div>
        {#if counts.inspect > 0}
          <div class="summary-chip" style="color: #94a3b8;">
            <strong>{counts.inspect}</strong> inspect
          </div>
        {/if}
      </div>
    {/if}

    <!-- Items list -->
    <div class="items-list">
      {#each sortedItems as item (item.id)}
        <div class="item-card card card--{item.status}">
          <div class="item-top">
            <span class="item-name">{item.name}</span>
            <StatusBadge status={item.status} />
          </div>
          <div class="item-meta">
            {#if item.last_done_date}
              <span>Last: <span class="odometer">{item.last_done_km?.toLocaleString()} km</span> · {item.last_done_date}</span>
            {:else}
              <span style="color: var(--color-text-muted);">Never serviced</span>
            {/if}
          </div>
          {#if item.km_remaining !== null}
            <div class="item-remaining" style="color: {item.status === 'ok' ? 'var(--color-text-muted)' : item.status === 'due_soon' ? 'var(--color-due-soon)' : 'var(--color-overdue)'};">
              {item.km_remaining >= 0 ? `${item.km_remaining.toLocaleString()} km remaining` : `${Math.abs(item.km_remaining).toLocaleString()} km overdue`}
            </div>
          {:else if item.days_remaining !== null}
            <div class="item-remaining" style="color: {item.status === 'ok' ? 'var(--color-text-muted)' : item.status === 'due_soon' ? 'var(--color-due-soon)' : 'var(--color-overdue)'};">
              {item.days_remaining >= 0 ? `${item.days_remaining} days remaining` : `${Math.abs(item.days_remaining)} days overdue`}
            </div>
          {/if}
          {#if item.notes}
            <div class="item-notes">{item.notes}</div>
          {/if}
        </div>
      {/each}

      {#if $items.length === 0}
        <div class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p>Loading maintenance items…</p>
        </div>
      {/if}
    </div>
  </div>
</div>

<!-- FAB -->
<a href="/log/new" class="fab" aria-label="Log new maintenance entry">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
    <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
  </svg>
</a>

<!-- Odometer modal -->
{#if showOdometerModal}
  <div class="modal-overlay" role="dialog" aria-modal="true" aria-label="Update odometer">
    <div class="modal">
      <h2 class="modal-title">Update Odometer</h2>
      <div class="form-group">
        <label class="label" for="odo-input">Current odometer (km)</label>
        <input
          id="odo-input"
          type="number"
          inputmode="numeric"
          class="input odometer"
          bind:value={newOdometer}
          placeholder="e.g. 5280"
          min="0"
          style="font-size: 20px;"
          onkeydown={(e) => e.key === 'Enter' && saveOdometer()}
        />
      </div>
      <div style="display: flex; gap: 12px; margin-top: 8px;">
        <button class="btn btn-secondary btn-full" onclick={() => (showOdometerModal = false)}>Cancel</button>
        <button class="btn btn-primary btn-full" onclick={saveOdometer} disabled={savingOdometer}>
          {#if savingOdometer}<span class="spinner"></span>{:else}Save{/if}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .odometer-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-md);
    margin-bottom: var(--space-md);
    text-align: left;
    cursor: pointer;
    transition: border-color 150ms ease;
    -webkit-tap-highlight-color: transparent;
  }
  .odometer-card:hover { border-color: var(--color-primary); }

  .odo-label { font-size: var(--text-xs); color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.06em; display: block; margin-bottom: 4px; }
  .odo-value { font-size: var(--text-3xl); font-weight: 700; color: var(--color-text); }
  .odo-unit  { font-size: var(--text-lg); font-weight: 400; color: var(--color-text-muted); }
  .odo-updated { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 4px; display: block; }

  .status-summary {
    display: flex;
    gap: var(--space-md);
    margin-bottom: var(--space-md);
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-md);
  }

  .summary-chip { flex: 1; text-align: center; font-size: var(--text-sm); }
  .summary-chip strong { display: block; font-size: var(--text-2xl); font-weight: 700; }

  .items-list { display: flex; flex-direction: column; gap: var(--space-sm); }

  .item-card { cursor: default; }
  .item-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; margin-bottom: 6px; }
  .item-name { font-size: var(--text-base); font-weight: 600; flex: 1; }
  .item-meta { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: 4px; }
  .item-remaining { font-size: var(--text-sm); font-weight: 500; }
  .item-notes { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 6px; font-style: italic; }

  .fab {
    position: fixed;
    bottom: calc(var(--nav-height) + var(--safe-bottom) + 16px);
    right: 16px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--color-primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 16px rgba(204, 0, 0, 0.4);
    transition: transform 150ms ease, box-shadow 150ms ease;
    -webkit-tap-highlight-color: transparent;
    z-index: 50;
  }
  .fab:active { transform: scale(0.93); box-shadow: 0 2px 8px rgba(204, 0, 0, 0.3); }

  .modal-overlay {
    position: fixed; inset: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex; align-items: flex-end;
    z-index: 300;
    animation: fadeIn 150ms ease;
  }
  .modal {
    background: var(--color-surface);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    padding: var(--space-lg);
    width: 100%;
    padding-bottom: calc(var(--space-lg) + var(--safe-bottom));
    animation: slideUp 200ms ease;
  }
  .modal-title { font-size: var(--text-xl); font-weight: 700; margin-bottom: var(--space-md); }

  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
</style>
