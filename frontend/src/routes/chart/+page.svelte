<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { api } from '$lib/api';
  import type { LogEntry } from '$lib/types';

  let canvas: HTMLCanvasElement;
  let chart: import('chart.js').Chart | null = null;
  let loading = $state(true);
  let hasData = $state(false);

  onMount(async () => {
    try {
      const result = await api.log.list(1);
      // Get all entries for the chart
      const allResult = await api.log.list(1);

      // Collect all entries with odometer data, sorted by date ascending
      const entries: LogEntry[] = allResult.items
        .slice()
        .sort((a, b) => a.done_date.localeCompare(b.done_date));

      if (entries.length === 0) {
        loading = false;
        return;
      }

      hasData = true;

      // Deduplicate by date — keep max km per date for the chart
      const byDate = new Map<string, number>();
      for (const e of entries) {
        byDate.set(e.done_date, Math.max(byDate.get(e.done_date) ?? 0, e.done_at_km));
      }

      const labels = [...byDate.keys()];
      const data = [...byDate.values()];

      const { Chart } = await import('chart.js/auto');

      chart = new Chart(canvas, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Odometer (km)',
            data,
            borderColor: '#CC0000',
            backgroundColor: 'rgba(204, 0, 0, 0.08)',
            borderWidth: 2,
            pointBackgroundColor: '#CC0000',
            pointBorderColor: '#CC0000',
            pointRadius: 4,
            pointHoverRadius: 6,
            fill: true,
            tension: 0.3,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#1a1a1a',
              borderColor: '#2e2e2e',
              borderWidth: 1,
              titleColor: '#f0f0f0',
              bodyColor: '#a0a0a0',
              callbacks: {
                label: (ctx) => ` ${ctx.parsed.y.toLocaleString()} km`,
              },
            },
          },
          scales: {
            x: {
              ticks: { color: '#a0a0a0', font: { size: 11 } },
              grid: { color: 'rgba(255,255,255,0.05)' },
            },
            y: {
              ticks: {
                color: '#a0a0a0',
                font: { size: 11 },
                callback: (v) => `${Number(v).toLocaleString()} km`,
              },
              grid: { color: 'rgba(255,255,255,0.05)' },
            },
          },
        },
      });
    } finally {
      loading = false;
    }
  });

  onDestroy(() => {
    chart?.destroy();
  });
</script>

<svelte:head><title>Odometer History — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header">
    <h1 class="page-title">Odometer History</h1>
  </div>

  <div class="content">
    {#if loading}
      <div class="empty-state"><div class="spinner" style="margin: 0 auto;"></div></div>
    {:else if !hasData}
      <div class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        <p style="margin-top: 12px;">No data yet.</p>
        <p style="font-size: var(--text-sm); margin-top: 4px;">Log your first service entry to see the chart.</p>
        <a href="/log/new" class="btn btn-primary" style="margin-top: 16px;">Log first service</a>
      </div>
    {:else}
      <div class="chart-card card">
        <canvas bind:this={canvas}></canvas>
      </div>
      <p style="font-size: var(--text-xs); color: var(--color-text-muted); margin-top: 12px; text-align: center;">
        Tap data points for exact values. Showing max odometer per service date.
      </p>
    {/if}
  </div>
</div>

<style>
  .chart-card { padding: var(--space-md); }
</style>
