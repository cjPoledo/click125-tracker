<script lang="ts">
  import type { Status } from '$lib/types';

  let { status }: { status: Status } = $props();

  const labels: Record<Status, string> = {
    ok: 'OK',
    due_soon: 'Due Soon',
    overdue: 'Overdue',
    inspect: 'Inspect',
  };
</script>

<span class="badge badge--{status}">{labels[status]}</span>
