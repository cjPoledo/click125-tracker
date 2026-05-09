<script lang="ts">
  import { onMount } from 'svelte';

  let deferredPrompt: BeforeInstallPromptEvent | null = null;
  let show = false;

  interface BeforeInstallPromptEvent extends Event {
    prompt(): Promise<void>;
    userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
  }

  onMount(() => {
    const dismissed = localStorage.getItem('install_dismissed');
    if (dismissed) return;

    const handler = (e: Event) => {
      e.preventDefault();
      deferredPrompt = e as BeforeInstallPromptEvent;
      show = true;
    };

    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  });

  async function install() {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'accepted') show = false;
    deferredPrompt = null;
  }

  function dismiss() {
    show = false;
    localStorage.setItem('install_dismissed', '1');
  }
</script>

{#if show}
  <div class="banner" role="alert">
    <div class="banner-content">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <span>Add Click125 to your home screen</span>
    </div>
    <div class="banner-actions">
      <button class="btn btn-primary" style="min-height: 36px; padding: 0 16px; font-size: 14px;" onclick={install}>Install</button>
      <button class="btn btn-secondary" style="min-height: 36px; padding: 0 12px; font-size: 14px;" onclick={dismiss}>Later</button>
    </div>
  </div>
{/if}

<style>
  .banner {
    position: fixed;
    top: env(safe-area-inset-top, 0);
    left: 0;
    right: 0;
    background: var(--color-surface-raised);
    border-bottom: 1px solid var(--color-border);
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    z-index: 200;
    animation: slideDown 250ms ease;
  }

  .banner-content {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    font-weight: 500;
    color: var(--color-text);
    min-width: 0;
  }

  .banner-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }

  @keyframes slideDown {
    from { transform: translateY(-100%); }
    to   { transform: translateY(0); }
  }
</style>
