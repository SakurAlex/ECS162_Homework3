<script>
  import { getContext } from 'svelte';
  const user = getContext('user');
  export let comment;         // { _id, user, content, created, removed }
  export let onRemove;        // function to call when "Remove" is clicked
</script>

<div class="comment">
  <header>
    <strong>{comment.user}</strong>
    <small>— {new Date(comment.created).toLocaleString()}</small>
    {#if comment.removed}
      <em>(removed)</em>
    {/if}
  </header>
  <p>{comment.content}</p>
  {#if $user?.groups?.includes("admin") && !comment.removed}
    <button on:click={() => onRemove(comment._id)}>
      Remove
    </button>
  {/if}
</div>

<style>
  .comment {
    border-top: 1px solid #ddd;
    padding: 0.5rem 0;
  }
  header {
    display: flex;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: #555;
  }
  button {
    margin-left: auto;
    font-size: 0.8rem;
  }
</style>
