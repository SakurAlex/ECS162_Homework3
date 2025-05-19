<script lang="ts">
  import Comments from './Comments.svelte';
  import { getContext } from 'svelte';
  const BASE_URL = 'http://localhost:8000';

  // Required by TypeScript
  type LoadCommentsFunction = (article_id: string) => void;
  type User = { email: string; name: string };

  // Get context values from parent components
  const user = getContext<User>('user');
  const loadComments = getContext<LoadCommentsFunction>('loadComments');
  const currentaid = getContext<string>('currentaid');

  // Component props
  export let comment: any;  // The current comment object to display
  export let comments: any[];  // Array of all comments
  export let submitComment: (content: string, parent?: string) => Promise<any>;  // Function to submit new comments

  // Local state for reply functionality
  let replyContent = "";
  let replying = false;

  console.log("Current user in Comments (from context):", user);

  // Handle reply submission
  async function handleReply() {   
    if (replyContent.trim() === "") return;
    await submitComment(replyContent, comment._id);  // Submit reply with parent comment ID
    replyContent = "";  // Clear input after submission
    replying = false;   // Hide reply form
  }

  // Handle comment deletion (moderator/admin only)
  async function deleteComment(commentId: string) {
    try {
      // Send DELETE request to backend
      const response = await fetch(`http://localhost:8000/api/comments/${commentId}`, {
        method: "DELETE",
        credentials: "include"
      });

      if (!response.ok) {
        throw new Error(`Failed to delete comment: ${response.status}`);
      }

      // Update the comment's content to show it was removed
      comment.content = "COMMENT REMOVED BY MODERATOR!";
      comment.removed = true;
      comment = comment; // Trigger Svelte reactivity

      // Fetch updated comments list
      const updatedComments = await fetch(`${BASE_URL}/api/comments?article_id=${currentaid}`, { 
        credentials: 'include' 
      }).then(res => res.json());
      
      comments = updatedComments;

    } catch (error) {
      console.error("Error deleting comment:", error);
    }
  }
</script>

<!-- Comment display and interaction UI -->
<div class="comment-item">
  <!-- User name and comment content -->
  <p class="user-name">{comment.user}</p>
  <p class="content" class:removed={comment.removed}>{comment.content}</p>

  <div class="comment-actions">
    <!-- Reply functionality -->
    <div class="left-actions">
      {#if replying}
        <!-- Reply input form -->
        <textarea bind:value={replyContent}></textarea>
        <button class="submit-button" on:click={handleReply}>Submit</button>
        <button class="cancel-button" on:click={() => replying = false}>Cancel</button>
      {:else}
        <button class="reply-button" on:click={() => replying = true}>Reply</button>
      {/if}
    </div>
  
    <!-- Delete button (only visible to moderators and admins) -->
    {#if user && (user.email === 'moderator@hw3.com' || user.email === 'admin@hw3.com')}
      <div class="right-actions">
        <button class="delete-button" on:click={() => deleteComment(comment._id)}>Delete</button>
      </div>
    {/if}
  </div>

  <!-- Recursive rendering of child comments -->
  {#if comment.children}
    <div class="replies">
      {#each comment.children as child}
        <svelte:self comment={child} {submitComment} {user}/>
      {/each}
    </div>
  {/if}
</div>

<style>
  /* Comment container styling */
  .comment-item {
    border-left: 2px solid #ddd;
    margin-bottom: 1rem;
    padding-left: 1rem;
  }

  /* Username styling */
  .comment-item .user-name {
    font-weight: bold;
    font-size: 0.95rem;
    display: inline-block;
    margin-bottom: 0.2rem;
  }
 
  /* Layout for action buttons */
  .comment-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
  }

  /* Reply form and buttons container */
  .left-actions {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    width: 100%;
  }

  /* Reply textarea styling */
  .left-actions textarea {
    width: 100%;
    border: 1px solid gray;
    border-radius: 12px;
    padding: 1rem;
    font-size: 0.9rem;
  }

  /* Container for delete button */
  .right-actions {
    display: flex;
  }

  /* Base button styling */
  .comment-item button {
    background: none;
    font-size: 0.85rem;
    font-weight: bold;
    border: none;
    cursor: pointer;
    padding: 0;
  }

  /* Reply and submit button styling */
  .reply-button, .submit-button {
    color: #3b5998;
  }

  /* Delete and cancel button styling */
  .delete-button, .cancel-button {
    padding: 4px 8px !important;
    border: none;
    border-radius: 4px;
    margin-left: 8px;
    color: #686868 !important;
  }

  /* Comment text styling */
  .comment-item p {
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
  }

  /* Nested replies container */
  .replies {
    margin-top: 0.5rem;
  }

  /* Styling for removed comments */
  .removed {
    color: #999;
    font-style: italic;
  }
</style>
  