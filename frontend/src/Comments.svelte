<script lang="ts">
  import Comments from './Comments.svelte';
  import { getContext } from 'svelte';
  type LoadCommentsFunction = (article_id: string) => void;
  type User = { email: string; name: string };
  const user = getContext<User>('user');
  const loadComments = getContext<LoadCommentsFunction>('loadComments');
  let replyContent = "";
  let replying = false;
  const currentaid = getContext<string>('currentaid');
  export let comment: any;
  export let submitComment: (content: string, parent?: string) => Promise<any>;

  console.log("Current user in Comments (from context):", user);

  async function handleReply() {   
    if (replyContent.trim() === "") return;
    await submitComment(replyContent, comment._id);  // submit using the function
    replyContent = "";
    replying = false;
  }
  async function deleteComment(commentId: string) {
    if (!confirm("Are you sure you want to delete this comment?")) return;

    await fetch(`http://localhost:8000/api/comments/${commentId}`, {
      method: "DELETE",
      credentials: "include"
    });

    await loadComments(currentaid);
  }
</script>

<div class="comment-item">
  <p><span class="user-name">{comment.user}</span>: {comment.content}</p>

  <div class="comment-actions">
    <div class="left-actions">
      {#if replying}
        <textarea bind:value={replyContent}></textarea>
        <button class="submit-button" on:click={handleReply}>Submit</button>
        <button class="cancel-button" on:click={() => replying = false}>Cancel</button>
      {:else}
        <button class="reply-button" on:click={() => replying = true}>Reply</button>
      {/if}
    </div>
  
    {#if user && user.email === 'moderator@hw3.com'}
      <div class="right-actions">
        <button class="delete-button" on:click={() => deleteComment(comment._id)}>Delete</button>
      </div>
    {/if}
  </div>

  {#if comment.children} <!-- if the comment has children -->
    <div class="replies">
      {#each comment.children as child} <!-- for each child -->
        <svelte:self comment={child} {submitComment} {user}/>
      {/each}
    </div>
  {/if}
</div>

<style>
  .comment-item {
    border-left: 2px solid #ddd;
    margin-bottom: 1rem;
    padding-left: 1rem;
  }

  /* user name */
  .comment-item .user-name {
    font-weight: bold;
    font-size: 0.95rem;
    display: inline-block;
    margin-bottom: 0.2rem;
  }
 
  .comment-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
  }

  .left-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .right-actions {
    display: flex;
  }

  /* basic button */
  .comment-item button {
    background: none;
    font-size: 0.85rem;
    font-weight: bold;
    border: none;
    cursor: pointer;
    padding: 0;
  }

  /* reply button */
  .reply-button, .submit-button {
    color: #3b5998;
  }

  /* delete and cancel button */
  .delete-button, .cancel-button {
    padding: 4px 8px !important;
    border: none;
    border-radius: 4px;
    margin-left: 8px;
    color: #686868 !important;
  }


  /* comment content */
  .comment-item p {
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
  }

  /* child comment container */
  .replies {
    margin-top: 0.5rem;
  }
</style>
  