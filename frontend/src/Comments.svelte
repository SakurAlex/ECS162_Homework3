<script lang="ts">
  import Comments from './Comments.svelte';
  export let comment: any;
  export let submitComment: (content: string, parent?: string) => Promise<any>;
  let replyContent = "";
  let replying = false;

  async function handleReply() {   
    if (replyContent.trim() === "") return;
    await submitComment(replyContent, comment._id);  // submit using the function
    replyContent = "";
    replying = false;
  }
</script>

<div class="comment-item">
  <p><span class="user-name">{comment.user}</span>: {comment.content}</p>

  {#if replying}
    <textarea bind:value={replyContent}></textarea> <!-- bind the replyContent to the textarea -->
    <button on:click={handleReply}>Reply</button> <!-- button to submit the reply -->
  {:else}
    <button on:click={() => replying = true}>Reply</button> <!-- button to reply -->
  {/if}

  {#if comment.children} <!-- if the comment has children -->
    <div class="replies">
      {#each comment.children as child} <!-- for each child -->
        <svelte:self comment={child} {submitComment} />
      {/each}
    </div>
  {/if}
</div>

<style>
  .comment-item {
    border-left: 2px solid #ddd;
    margin-left: 1rem;
    padding-left: 1rem;
    margin-bottom: 1rem;
  }

  /* user name */
  .comment-item .user-name {
    font-weight: bold;
    font-size: 0.95rem;
    display: inline-block;
    margin-bottom: 0.2rem;
  }

  /* comment content */
  .comment-item p {
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
  }

  /* Reply button */
  .comment-item button {
    background: none;
    color: #3b5998;
    font-size: 0.85rem;
    border: none;
    cursor: pointer;
    padding: 0;
  }
  /* child comment container */
  .replies {
    margin-top: 0.5rem;
  }
</style>
  