<script lang="ts">
  export let comment: any;
  export let submitComment: (content: string, parent?: string) => Promise<any>;
  let replyContent = "";
  let replying = false;

  async function handleReply() {   
    if (replyContent.trim() === "") return;
    await submitComment(replyContent, comment._id);
    replyContent = "";
    replying = false;
  }
</script>

<div class="comment-item">
  <p><span class="user-name">{comment.user}</span>: {comment.content}</p>

  {#if replying}
    <textarea bind:value={replyContent}></textarea>
    <button on:click={handleReply}>Reply</button>
  {:else}
    <button on:click={() => replying = true}>Reply</button>
  {/if}

  {#if comment.children}
    <div class="replies">
      {#each comment.children as child}
        <svelte:self comment={child} {submitComment} />
      {/each}
    </div>
  {/if}
</div>

<style>
  .comment-item {
    margin-left: 1rem;
    border-left: 1px solid #ccc;
    padding-left: 0.5rem;
  }
  .user-name {
    font-weight: bold;
  }
</style> 