<svelte:head><title>Maintenance Schedule — Click125 Tracker</title></svelte:head>

<script lang="ts">
  import { items, selectedItem } from '$lib/stores';

  const COLS = ['Pre-ride', '1k km', '6k km', '12k km', '18k km', '24k km', '30k km', '36k km', 'Annual', 'Replace'];

  type Level = 'Standard' | 'Intermediate' | 'Technical';

  // Row name → DB item name mapping (only rows that have a matching DB item)
  const NAME_MAP: Record<string, string> = {
    'Fuel Line':                  'Fuel Line',
    'Throttle Operation':         'Throttle Operation',
    'Air Cleaner':                'Air Cleaner Element',
    'Crankcase Breather':         'Crankcase Breather',
    'Spark Plug':                 'Spark Plug',
    'Valve Clearance':            'Valve Clearance',
    'Engine Oil':                 'Engine Oil Change',
    'Engine Oil Strainer Screen': 'Engine Oil Strainer Screen',
    'Engine Idle Speed':          'Engine Idle Speed',
    'Radiator Coolant':           'Radiator Coolant',
    'Cooling System':             'Cooling System',
    'Drive Belt':                 'Drive Belt',
    'Final Drive Oil':            'Final Drive Oil',
    'Brake Fluid':                'Brake Fluid',
    'Brake System':               'Brake System',
    'Brake Lock Operation':       'Brake Lock Operation',
    'Headlight Aim':              'Headlight Aim',
    'Clutch Shoes Wear':          'Clutch Shoes Wear',
    'Side Stand':                 'Side Stand',
    'Suspension':                 'Suspension',
    'Nuts, Bolts & Fasteners':    'Nuts & Bolts',
    'Wheels/Tyres':               'Wheels & Tyres',
    'Steering Head Bearings':     'Steering Head Bearings',
  };

  function openDrawer(rowName: string) {
    const dbName = NAME_MAP[rowName];
    if (!dbName) return;
    const found = $items.find(i => i.name === dbName);
    if (found) selectedItem.set(found);
  }

  // ● = Inspect   ■ = Replace   C = Clean   '' = N/A
  // Columns: [pre, 1k, 6k, 12k, 18k, 24k, 30k, 36k, annual, replace]
  const ROWS: { name: string; level: Level; cells: string[] }[] = [
    { name: 'Fuel Line',                  level: 'Intermediate', cells: ['',  '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Fuel Level',                 level: 'Standard',     cells: ['●', '',  '',  '',  '',  '',  '',  '',  '',  ''] },
    { name: 'Throttle Operation',         level: 'Intermediate', cells: ['●', '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Air Cleaner',                level: 'Intermediate', cells: ['',  '',  '',  '',  '■', '',  '■', '',  '',  ''] },
    { name: 'Crankcase Breather',         level: 'Standard',     cells: ['',  '',  'C', 'C', 'C', 'C', 'C', 'C', '',  ''] },
    { name: 'Spark Plug',                 level: 'Standard',     cells: ['',  '',  '●', '■', '●', '■', '●', '■', '',  ''] },
    { name: 'Valve Clearance',            level: 'Intermediate', cells: ['',  '',  '●', '●', '●', '●', '●', '●', '',  ''] },
    { name: 'Engine Oil',                 level: 'Standard',     cells: ['●', '■', '■', '■', '■', '■', '■', '■', '■', ''] },
    { name: 'Engine Oil Strainer Screen', level: 'Standard',     cells: ['',  '',  '',  'C', '',  'C', '',  'C', '',  ''] },
    { name: 'Engine Idle Speed',          level: 'Intermediate', cells: ['',  '●', '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Radiator Coolant',           level: 'Standard',     cells: ['●', '',  '',  '●', '',  '●', '',  '●', '●', '3 yr'] },
    { name: 'Cooling System',             level: 'Intermediate', cells: ['',  '',  '',  '●', '',  '●', '',  '●', '●', ''] },
    { name: 'Drive Belt',                 level: 'Intermediate', cells: ['',  '',  '',  '●', '',  '■', '',  '●', '',  ''] },
    { name: 'Final Drive Oil',            level: 'Intermediate', cells: ['',  '',  '',  '',  '',  '',  '',  '',  '',  '2 yr'] },
    { name: 'Brake Fluid',                level: 'Standard',     cells: ['●', '',  '●', '●', '●', '●', '●', '●', '●', '2 yr'] },
    { name: 'Brake Shoes/Pads Wear',      level: 'Standard',     cells: ['●', '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Brake System',               level: 'Standard',     cells: ['●', '●', '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Brake Lock Operation',       level: 'Intermediate', cells: ['',  '',  '●', '●', '●', '●', '●', '●', '',  ''] },
    { name: 'Headlight Aim',              level: 'Standard',     cells: ['',  '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Lights & Horn',              level: 'Standard',     cells: ['●', '',  '',  '',  '',  '',  '',  '',  '',  ''] },
    { name: 'Clutch Shoes Wear',          level: 'Technical',    cells: ['',  '',  '',  '●', '',  '●', '',  '●', '',  ''] },
    { name: 'Side Stand',                 level: 'Standard',     cells: ['●', '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Suspension',                 level: 'Intermediate', cells: ['',  '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Nuts, Bolts & Fasteners',    level: 'Intermediate', cells: ['',  '●', '',  '●', '',  '●', '',  '●', '●', ''] },
    { name: 'Wheels/Tyres',              level: 'Technical',    cells: ['●', '',  '●', '●', '●', '●', '●', '●', '●', ''] },
    { name: 'Steering Head Bearings',     level: 'Technical',    cells: ['',  '',  '',  '●', '',  '●', '',  '●', '●', ''] },
  ];

  const LEVEL_LABEL: Record<Level, string> = {
    Standard:     'STD',
    Intermediate: 'INT',
    Technical:    'TECH',
  };
</script>

<div class="page">
  <div class="page-header">
    <h1 class="page-title">Maintenance Schedule</h1>
    <p class="subtitle">Honda Click 125i 2024 — Owner's Manual pp. 55–57</p>
  </div>

  <div class="content">

    <!-- ── Section 1: Schedule Table ── -->
    <section class="section">
      <h2 class="section-title">Scheduled Maintenance</h2>
      <div class="table-wrap">
        <table class="sched-table">
          <thead>
            <tr>
              <th class="col-item sticky-col">Item</th>
              <th class="col-level">Level</th>
              {#each COLS as col}
                <th class="col-data">{col}</th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each ROWS as row}
              <tr class:row-tappable={NAME_MAP[row.name]} onclick={() => openDrawer(row.name)}>
                <td class="col-item sticky-col">{row.name}</td>
                <td class="col-level">
                  <span
                    class="level-badge level-{row.level.toLowerCase()}"
                    title="{row.level}"
                  >{LEVEL_LABEL[row.level]}</span>
                </td>
                {#each row.cells as cell}
                  <td class="col-data" class:cell-filled={cell !== ''} class:cell-replace={cell !== '●' && cell !== '■' && cell !== 'C' && cell !== ''} class:cell-clean={cell === 'C'}>
                    {cell}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>

      <!-- Legend -->
      <div class="legend">
        <span class="legend-item"><span class="sym">●</span> Inspect</span>
        <span class="legend-item"><span class="sym">■</span> Replace</span>
        <span class="legend-item"><span class="sym sym-clean">C</span> Clean</span>
        <span class="legend-divider"></span>
        <span class="legend-item"><span class="level-badge level-standard">STD</span> Owner serviceable</span>
        <span class="legend-item"><span class="level-badge level-intermediate">INT</span> Dealer recommended</span>
        <span class="legend-item"><span class="level-badge level-technical">TECH</span> Dealer required</span>
      </div>
    </section>

    <!-- ── Section 2: Maintenance Notes ── -->
    <section class="section">
      <h2 class="section-title">Maintenance Notes</h2>
      <div class="card notes-card">
        <p class="notes-heading">Interval notes</p>
        <ul class="notes-list">
          <li>Repeat all scheduled maintenance at the same frequency once the odometer exceeds 36,000 km.</li>
          <li><em>Air Cleaner:</em> Service more frequently when riding in unusually wet or dusty conditions.</li>
          <li><em>Crankcase Breather:</em> Service more frequently when riding in rain, at full throttle, or after washing or overturning the vehicle.</li>
          <li><em>Radiator Coolant:</em> First replacement at 3 years; every 2 years thereafter.</li>
          <li><em>Final Drive Oil:</em> Replacement every 2 years — dealer recommended.</li>
          <li><em>Brake Fluid:</em> Replacement every 2 years — dealer recommended.</li>
        </ul>

        <p class="notes-heading" style="margin-top: var(--space-md);">Maintenance level</p>
        <ul class="notes-list">
          <li><span class="level-badge level-standard">STD</span> <strong>Standard</strong> — Owner can perform at home with proper tools and mechanical skill.</li>
          <li><span class="level-badge level-intermediate">INT</span> <strong>Intermediate</strong> — Possible with Honda Shop Manual, but dealer service is recommended.</li>
          <li><span class="level-badge level-technical">TECH</span> <strong>Technical</strong> — Dealer service required for safety — do not attempt at home.</li>
        </ul>

        <p class="notes-heading" style="margin-top: var(--space-md);">Technical items (dealer required)</p>
        <p class="dealer-list">Clutch Shoes Wear · Wheels/Tyres · Steering Head Bearings</p>
      </div>
    </section>

    <!-- ── Section 3: Tyre & Fluid Quick Reference ── -->
    <section class="section">
      <h2 class="section-title">Tyre &amp; Fluid Quick Reference</h2>
      <div class="card ref-card">

        <p class="notes-heading">Tyre pressure (cold)</p>
        <table class="ref-table">
          <thead>
            <tr><th>Load</th><th>Front</th><th>Rear</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>Driver only</td>
              <td>200 kPa · 2.00 kgf/cm² · 29 psi</td>
              <td>225 kPa · 2.25 kgf/cm² · 33 psi</td>
            </tr>
            <tr>
              <td>Driver + passenger</td>
              <td>200 kPa · 2.00 kgf/cm² · 29 psi</td>
              <td>225 kPa · 2.25 kgf/cm² · 33 psi</td>
            </tr>
          </tbody>
        </table>

        <p class="notes-heading" style="margin-top: var(--space-md);">Fluids</p>
        <ul class="notes-list">
          <li><strong>Engine oil:</strong> JASO T903 MB · SAE 10W-30 · API SJ or higher</li>
          <li><strong>Brake fluid:</strong> Honda DOT 3 or DOT 4 (or equivalent)</li>
          <li><strong>Coolant:</strong> Honda Pre-Mix Coolant only — do not dilute with water</li>
          <li><strong>Fuel:</strong> Unleaded petrol, RON 91 or higher · Tank capacity: 5.5 L</li>
        </ul>

        <p class="notes-heading" style="margin-top: var(--space-md);">Battery</p>
        <p class="dealer-list">Maintenance-free type — no electrolyte check required, no distilled water top-up.</p>
      </div>
    </section>

    <p class="source-footer">Source: Honda Click 125i 2024 Owner's Manual (Philippines spec)</p>
  </div>
</div>

<style>
  .subtitle {
    font-size: 12px;
    color: var(--color-text-muted);
    margin-top: 2px;
  }

  .section { margin-bottom: var(--space-lg); }

  .section-title {
    font-size: var(--text-sm);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--color-text-muted);
    margin-bottom: var(--space-sm);
  }

  /* ── Schedule Table ── */
  .table-wrap {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }

  .sched-table {
    border-collapse: separate;
    border-spacing: 0;
    font-size: 11px;
    width: max-content;
    min-width: 100%;
  }

  .sched-table th,
  .sched-table td {
    padding: 7px 8px;
    border-bottom: 1px solid var(--color-border);
    white-space: nowrap;
  }

  .sched-table th {
    background: var(--color-surface);
    color: var(--color-text-muted);
    font-weight: 600;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .sched-table tbody tr:last-child td { border-bottom: none; }

  .sched-table tbody tr:hover { background: rgba(255,255,255,0.03); }
  .row-tappable { cursor: pointer; }
  .row-tappable:active { background: rgba(255,255,255,0.06); }

  .col-item {
    text-align: left;
    min-width: 160px;
    max-width: 180px;
    white-space: normal;
    font-weight: 500;
    color: var(--color-text);
  }

  .col-data {
    text-align: center;
    min-width: 48px;
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    color: var(--color-text-muted);
    font-size: 10px;
  }

  .sticky-col {
    position: sticky;
    left: 0;
    z-index: 2;
    background: var(--color-background);
    border-right: 1px solid var(--color-border);
  }

  .sched-table th.sticky-col {
    background: var(--color-surface);
    z-index: 3;
  }

  .cell-filled {
    color: var(--color-text);
    font-weight: 700;
    font-size: 13px;
  }

  .cell-replace {
    font-size: 10px;
    font-family: inherit;
    font-weight: 500;
    color: var(--color-primary);
  }

  .cell-clean { color: #38bdf8; }

  .sym-clean { color: #38bdf8; }

  /* Level column */
  .col-level {
    text-align: center;
    min-width: 52px;
    padding: 7px 6px;
    border-right: 1px solid var(--color-border);
  }

  /* Level badges */
  .level-badge {
    display: inline-block;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
    font-family: 'JetBrains Mono', ui-monospace, monospace;
  }

  .level-standard     { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
  .level-intermediate { background: rgba(245, 158, 11, 0.15);  color: #fbbf24; }
  .level-technical    { background: rgba(239, 68, 68, 0.15);   color: #f87171; }

  /* Legend */
  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 14px;
    margin-top: var(--space-sm);
    font-size: 11px;
    color: var(--color-text-muted);
    align-items: center;
  }

  .legend-item { display: flex; align-items: center; gap: 6px; }

  .legend-divider {
    width: 1px;
    height: 14px;
    background: var(--color-border);
    margin: 0 2px;
  }

  .sym {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text);
    min-width: 14px;
    text-align: center;
  }

  .sym.empty { font-size: 11px; font-weight: 400; color: var(--color-text-muted); }

  /* Notes & Ref Cards */
  .notes-card,
  .ref-card {
    padding: var(--space-md);
  }

  .notes-heading {
    font-size: var(--text-xs);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    margin-bottom: 8px;
  }

  .notes-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: var(--text-sm);
    color: var(--color-text);
    line-height: 1.5;
  }

  .notes-list li:not(:has(.level-badge))::before {
    content: '– ';
    color: var(--color-text-muted);
  }

  .notes-list li:has(.level-badge) {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .dealer-list {
    font-size: var(--text-sm);
    color: var(--color-text);
    line-height: 1.6;
  }

  .ref-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-xs);
    margin-bottom: 4px;
  }

  .ref-table th {
    text-align: left;
    color: var(--color-text-muted);
    font-weight: 600;
    padding: 4px 0 6px;
    border-bottom: 1px solid var(--color-border);
  }

  .ref-table td {
    padding: 6px 0;
    color: var(--color-text);
    border-bottom: 1px solid rgba(255,255,255,0.04);
    vertical-align: top;
    line-height: 1.5;
  }

  .ref-table td:not(:first-child) {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 11px;
  }

  .source-footer {
    font-size: 11px;
    color: var(--color-text-muted);
    text-align: center;
    margin-top: var(--space-md);
    font-style: italic;
    padding-bottom: var(--space-sm);
  }
</style>
