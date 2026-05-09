<script lang="ts">
  import { onMount } from 'svelte';
  import { motorcycle, items, showToast } from '$lib/stores';
  import { api } from '$lib/api';

  let odometerInput = $state('');
  let savingOdo = $state(false);

  let botToken = $state('');
  let chatId = $state('');
  let savingTelegram = $state(false);
  let testingTelegram = $state(false);

  let exporting = $state(false);

  onMount(async () => {
    odometerInput = $motorcycle ? String($motorcycle.current_odometer_km) : '0';
    try {
      const settings = await api.settings.get();
      botToken = settings.telegram_bot_token ?? '';
      chatId = settings.telegram_chat_id ?? '';
    } catch {
      /* ignore */
    }
  });

  async function saveOdometer() {
    const km = parseInt(odometerInput, 10);
    if (isNaN(km) || km < 0) return;
    savingOdo = true;
    try {
      const updated = await api.motorcycle.updateOdometer(km);
      motorcycle.set(updated);
      const refreshed = await api.items.list();
      items.set(refreshed);
      showToast('Odometer updated');
    } catch {
      showToast('Failed to update odometer', 'error');
    } finally {
      savingOdo = false;
    }
  }

  async function saveTelegram() {
    savingTelegram = true;
    try {
      await api.settings.update({
        telegram_bot_token: botToken || null,
        telegram_chat_id: chatId || null,
      });
      showToast('Telegram settings saved');
    } catch {
      showToast('Failed to save settings', 'error');
    } finally {
      savingTelegram = false;
    }
  }

  async function testTelegram() {
    testingTelegram = true;
    try {
      const result = await api.settings.testTelegram();
      showToast(result.ok ? 'Telegram check triggered — check your chat!' : 'Test failed', result.ok ? 'success' : 'error');
    } catch {
      showToast('Test failed — check your bot token and chat ID', 'error');
    } finally {
      testingTelegram = false;
    }
  }

  async function exportData() {
    exporting = true;
    try {
      const data = await api.export.download();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `click125-export-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      showToast('Data exported');
    } catch {
      showToast('Export failed', 'error');
    } finally {
      exporting = false;
    }
  }
</script>

<svelte:head><title>Settings — Click125 Tracker</title></svelte:head>

<div class="page">
  <div class="page-header">
    <h1 class="page-title">Settings</h1>
  </div>

  <div class="content">
    <!-- Odometer section -->
    <div class="section">
      <div class="section-title">Odometer</div>
      <div class="form-group">
        <label class="label" for="odo-setting">Current odometer (km)</label>
        <input id="odo-setting" type="number" inputmode="numeric" class="input odometer" bind:value={odometerInput} min="0" style="font-size: 20px;" />
      </div>
      <button class="btn btn-primary btn-full" onclick={saveOdometer} disabled={savingOdo}>
        {#if savingOdo}<span class="spinner"></span>{:else}Update Odometer{/if}
      </button>
    </div>

    <div class="divider"></div>

    <!-- Telegram section -->
    <div class="section">
      <div class="section-title">Telegram Reminders</div>
      <p class="section-desc">
        Create a bot via <strong>@BotFather</strong> on Telegram. Get your Chat ID by messaging <strong>@userinfobot</strong>.
      </p>
      <div class="form-group">
        <label class="label" for="bot-token">Bot Token</label>
        <input id="bot-token" type="text" class="input" bind:value={botToken} placeholder="123456:ABCDEFabcdef…" autocomplete="off" />
      </div>
      <div class="form-group">
        <label class="label" for="chat-id">Chat ID</label>
        <input id="chat-id" type="text" inputmode="numeric" class="input" bind:value={chatId} placeholder="e.g. 123456789" autocomplete="off" />
      </div>
      <div style="display: flex; flex-direction: column; gap: var(--space-sm);">
        <button class="btn btn-primary btn-full" onclick={saveTelegram} disabled={savingTelegram}>
          {#if savingTelegram}<span class="spinner"></span>{:else}Save Telegram Settings{/if}
        </button>
        <button class="btn btn-secondary btn-full" onclick={testTelegram} disabled={testingTelegram || !botToken || !chatId}>
          {#if testingTelegram}<span class="spinner"></span>{:else}Test Reminders Now{/if}
        </button>
      </div>
    </div>

    <div class="divider"></div>

    <!-- Export section -->
    <div class="section">
      <div class="section-title">Data</div>
      <p class="section-desc">Export all your maintenance records as JSON.</p>
      <button class="btn btn-secondary btn-full" onclick={exportData} disabled={exporting}>
        {#if exporting}<span class="spinner"></span>{:else}Export Data as JSON{/if}
      </button>
    </div>

    <div class="divider"></div>

    <div class="section" style="padding-bottom: 0;">
      <p style="font-size: var(--text-xs); color: var(--color-text-muted); text-align: center;">
        Click125 Tracker v1.0 · Honda Click 125i 2024 PH
      </p>
    </div>
  </div>
</div>

<style>
  .section { padding: var(--space-sm) 0; }
  .section-title { font-size: var(--text-sm); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: var(--color-text-muted); margin-bottom: var(--space-md); }
  .section-desc { font-size: var(--text-sm); color: var(--color-text-muted); margin-bottom: var(--space-md); line-height: 1.5; }
</style>
