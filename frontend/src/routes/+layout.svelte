<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import Toast from '$lib/components/Toast.svelte';
  import InstallBanner from '$lib/components/InstallBanner.svelte';
  import ItemDetailDrawer from '$lib/components/ItemDetailDrawer.svelte';
  import { motorcycle, items } from '$lib/stores';
  import { api } from '$lib/api';

  let { children } = $props();

  onMount(async () => {
    try {
      const [moto, itemList] = await Promise.all([api.motorcycle.get(), api.items.list()]);
      motorcycle.set(moto);
      items.set(itemList);
    } catch {
      /* offline or first load — stores stay null */
    }
  });
</script>

<InstallBanner />
<Toast />
<main>
  {@render children()}
</main>
<BottomNav />
<ItemDetailDrawer />
