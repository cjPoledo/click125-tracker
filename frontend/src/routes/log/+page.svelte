<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api';
  import type { LogEntry } from '$lib/types';

  let logEntries = $state<LogEntry[]>([]);
  let total = $state(0);
  let loading = $state(true);
  let page = $state(1);

  async function loadLog() {
    loading = true;
    try {
      const result = await api.log.list(page);
      logEntries = result.items;
      total = result.total;
    } finally {
      loading = false;
    }
  }

  onMount(loadLog);

  function formatDate(d: string) {
    return new Date(d + 'T00:00:00').toLocaleDateString('en-PH', {
      month: 'short', day: 'numeric', year: 'numeric',
    });
  }
</script>

<svelte:head><title>Maintenance Log — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header" style="display: flex; align-items: center; justify-content: space-between;">
    <h1 class="page-title">Log</h1>
    <a href="/log/new" class="btn btn-primary" style="min-height: 40px; padding: 0 16px; font-size: 14px;">+ New</a>
  </div>

  <div class="content">
    {#if loading}
      <div class="empty-state"><div class="spinner" style="margin: 0 auto;"></div></div>
    {:else if logEntries.length === 0}
      <div class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <p style="margin-top: 12px;">No log entries yet.</p>
        <a href="/log/new" class="btn btn-primary" style="margin-top: 16px;">Log first service</a>
      </div>
    {:else}
      <div style="font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-md);">
        {total} entries total
      </div>
      <div style="display: flex; flex-direction: column; gap: var(--space-sm);">
        {#each logEntries as entry (entry.id)}
          <a href="/log/{entry.id}" class="log-card card">
            <div class="log-top">
              <span class="log-item-name">{entry.item_name ?? 'Unknown'}</span>
              <span class="log-km odometer">{entry.done_at_km.toLocaleString()} km</span>
            </div>
            <div class="log-date">{formatDate(entry.done_date)}</div>
            {#if entry.notes}
              <div class="log-notes">{entry.notes}</div>
            {/if}
          </a>
        {/each}
      </div>

      {#if total > logEntries.length}
        <button class="btn btn-secondary btn-full" style="margin-top: 16px;" onclick={() => { page++; loadLog(); }}>
          Load more
        </button>
      {/if}
    {/if}
  </div>
</div>

<style>
  .log-card {
    display: block;
    transition: border-color 150ms ease;
    -webkit-tap-highlight-color: transparent;
  }
  .log-card:hover { border-color: var(--color-primary); }

  .log-top { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; margin-bottom: 4px; }
  .log-item-name { font-size: var(--text-base); font-weight: 600; flex: 1; }
  .log-km { font-size: var(--text-sm); color: var(--color-text-muted); flex-shrink: 0; }
  .log-date { font-size: var(--text-sm); color: var(--color-text-muted); }
  .log-notes { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 6px; font-style: italic; }
</style>
