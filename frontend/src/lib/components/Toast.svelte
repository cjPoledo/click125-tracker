<script lang="ts">
  import { toastMessage } from '$lib/stores';
</script>

{#if $toastMessage}
  <div class="toast toast--{$toastMessage.type}" role="alert" aria-live="polite">
    {#if $toastMessage.type === 'success'}
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
    {:else}
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
    {/if}
    {$toastMessage.text}
  </div>
{/if}

<style>
  .toast {
    position: fixed;
    top: calc(env(safe-area-inset-top, 0px) + 12px);
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    animation: slideDown 200ms ease;
  }

  .toast--success { background: #22c55e; color: #000; }
  .toast--error   { background: #ef4444; color: #fff; }

  @keyframes slideDown {
    from { opacity: 0; transform: translateX(-50%) translateY(-8px); }
    to   { opacity: 1; transform: translateX(-50%) translateY(0); }
  }
</style>
