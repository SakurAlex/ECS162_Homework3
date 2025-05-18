<script lang="ts">
  import Comment from './Comment.svelte';
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
        <Comment comment={child} {submitComment} />
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
  