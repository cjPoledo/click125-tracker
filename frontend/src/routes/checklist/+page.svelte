<script lang="ts">
  import { onMount } from 'svelte';
  import { CHECKLIST_ITEMS, getChecklist, saveChecklist } from '$lib/checklist';

  let checks = $state<boolean[]>(new Array(CHECKLIST_ITEMS.length).fill(false));

  onMount(() => {
    checks = getChecklist();
  });

  function toggle(index: number) {
    checks[index] = !checks[index];
    saveChecklist(checks);
  }

  function reset() {
    checks = new Array(CHECKLIST_ITEMS.length).fill(false);
    saveChecklist(checks);
  }

  let checkedCount = $derived(checks.filter(Boolean).length);
  let allDone = $derived(checkedCount === CHECKLIST_ITEMS.length);
  let today = new Date().toLocaleDateString('en-PH', { weekday: 'long', month: 'long', day: 'numeric' });
</script>

<svelte:head><title>Pre-Ride Check — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header">
    <h1 class="page-title">Pre-Ride Check</h1>
    <p style="font-size: 13px; color: var(--color-text-muted); margin-top: 2px;">{today}</p>
  </div>

  <div class="content">
    <!-- Tyre pressure reference card -->
    <div class="tyre-card card" style="margin-bottom: var(--space-md);">
      <div class="tyre-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>
        Tyre Pressure Reference
      </div>
      <table class="pressure-table">
        <thead>
          <tr>
            <th>Load</th>
            <th>Pos.</th>
            <th>kPa</th>
            <th>kgf/cm²</th>
            <th>PSI</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="2">Solo</td>
            <td>Front</td>
            <td>200</td>
            <td>2.00</td>
            <td class="psi">29</td>
          </tr>
          <tr>
            <td>Rear</td>
            <td>225</td>
            <td>2.25</td>
            <td class="psi">33</td>
          </tr>
          <tr>
            <td rowspan="2">Pillion</td>
            <td>Front</td>
            <td>200</td>
            <td>2.00</td>
            <td class="psi">29</td>
          </tr>
          <tr>
            <td>Rear</td>
            <td>225</td>
            <td>2.25</td>
            <td class="psi">33</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Progress bar -->
    <div class="progress-row">
      <span class="progress-label">{checkedCount} / {CHECKLIST_ITEMS.length} checked</span>
      <button class="reset-btn" onclick={reset} aria-label="Reset checklist">Reset</button>
    </div>
    <div class="progress-bar" role="progressbar" aria-valuenow={checkedCount} aria-valuemin={0} aria-valuemax={CHECKLIST_ITEMS.length}>
      <div class="progress-fill" style="width: {(checkedCount / CHECKLIST_ITEMS.length) * 100}%;"></div>
    </div>

    {#if allDone}
      <div class="all-done" role="status">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
        Good to go!
      </div>
    {/if}

    <!-- Checklist items -->
    <ul class="checklist" aria-label="Pre-ride checklist">
      {#each CHECKLIST_ITEMS as item, i}
        <li>
          <button
            class="check-item"
            class:check-item--done={checks[i]}
            onclick={() => toggle(i)}
            aria-pressed={checks[i]}
            role="checkbox"
            aria-checked={checks[i]}
          >
            <span class="check-box" aria-hidden="true">
              {#if checks[i]}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>
              {/if}
            </span>
            <span class="check-text" class:check-text--done={checks[i]}>{i + 1}. {item}</span>
          </button>
        </li>
      {/each}
    </ul>
  </div>
</div>

<style>
  .tyre-card { padding: var(--space-sm) var(--space-md); }
  .tyre-title {
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--color-text-muted);
    margin-bottom: var(--space-sm);
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .pressure-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-xs);
  }
  .pressure-table th {
    text-align: left;
    color: var(--color-text-muted);
    font-weight: 500;
    padding: 4px 6px 4px 0;
    border-bottom: 1px solid var(--color-border);
  }
  .pressure-table td {
    padding: 5px 6px 5px 0;
    color: var(--color-text);
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .pressure-table .psi {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: var(--color-primary);
  }

  .progress-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .progress-label { font-size: var(--text-sm); color: var(--color-text-muted); font-weight: 500; }
  .reset-btn {
    font-size: var(--text-sm);
    color: var(--color-text-muted);
    padding: 4px 8px;
    border-radius: var(--radius-sm);
    transition: color 150ms ease;
    cursor: pointer;
    min-height: 32px;
  }
  .reset-btn:hover { color: var(--color-text); }

  .progress-bar {
    height: 4px;
    background: var(--color-border);
    border-radius: 2px;
    margin-bottom: var(--space-md);
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: var(--color-primary);
    border-radius: 2px;
    transition: width 200ms ease;
  }

  .all-done {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.12);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: var(--color-ok);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    font-weight: 600;
    font-size: var(--text-base);
    margin-bottom: var(--space-md);
  }

  .checklist { list-style: none; display: flex; flex-direction: column; gap: 2px; }

  .check-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    width: 100%;
    text-align: left;
    padding: 14px var(--space-sm);
    border-radius: var(--radius-md);
    min-height: 52px;
    transition: background 100ms ease;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  .check-item:hover { background: var(--color-surface); }
  .check-item--done { background: rgba(34, 197, 94, 0.05); }

  .check-box {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 2px solid var(--color-border);
    flex-shrink: 0;
    margin-top: 1px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 150ms ease, border-color 150ms ease;
    color: white;
  }
  .check-item--done .check-box {
    background: var(--color-ok);
    border-color: var(--color-ok);
  }

  .check-text {
    font-size: var(--text-base);
    line-height: 1.4;
    color: var(--color-text);
    transition: color 150ms ease;
  }
  .check-text--done {
    color: var(--color-text-muted);
    text-decoration: line-through;
  }
</style>
