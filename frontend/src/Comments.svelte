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

  //Both requires textarea, so similar way to handle
  let replyContent = "";
  let replying = false;
  let redactContent = comment.content;
  let redacting = false;
  
  console.log("Current user in Comments:", user);

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

  function redactComment(original: string, edited: string): string {
    let redacted = '';
    
    if (edited.length > original.length) {
      alert("You can only redact the content, not add more!");
      return original;
    }
    //iteratively check each character with the original content
    let i = 0, j = 0; //using greedy algorithm to check each character
    while (i < original.length) {
      if (j < edited.length && original[i] === edited[j]) {
        //If the character is the same, add it to the redacted content
        redacted += original[i];
        i++;
        j++;
      } else {
        //If the character is different, add a full block to the redacted content
        redacted += "█"; // full block U+2588
        i++;
      }
    }
    //If the edited content is not the same length as the original, return the original content
    if (j < edited.length) {
      alert("Invalid redaction!");
      return original;
    }

    return redacted;
  }

  async function handleRedact() {
    const redacted = redactComment(comment.content, redactContent);
    await fetch(`http://localhost:8000/api/comments/${comment._id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" }, //specify the content type as json
      credentials: "include",
      body: JSON.stringify({ content: redacted }) //send the redacted content to the backend
    });

    redacting = false;
    await loadComments(currentaid);
  }

</script>

<!-- Comment display and interaction UI -->
<div class="comment-item">
  <!-- User name and comment content -->
  <p class="user-name">{comment.user}</p>
  <p class="content" class:removed={comment.removed}>{comment.content}</p>

  <div class="comment-buttons">
    {#if replying}
      <!-- Reply input form -->
      <div class="submit-and-cancel">
        <textarea bind:value={replyContent}></textarea>
        <button class="submit-button" on:click={handleReply}>Submit</button>
        <button class="cancel-button" on:click={() => replying = false}>Cancel</button>
      </div>  
    {:else if redacting}
      <!-- Redact input form -->
      <div class="submit-and-cancel">
        <textarea bind:value={redactContent}></textarea>
        <button on:click={handleRedact}>Confirm</button>
        <button on:click={() => redacting = false}>Cancel</button>
      </div>
    {:else}
      <!--if NOT replying or redacting, only reply redact and delete buttons are comment-actions-->
      <div id="reply-and-redact">
        <button class="reply-button" on:click={() => replying = true}>Reply</button>
        {#if user && (user.email === 'moderator@hw3.com' || user.email === 'admin@hw3.com')}
          <button class="redact-button" on:click={() => redacting = true}>Redact</button>
        {/if}
      </div>
    {/if}
  
    <!-- Delete button (only visible to moderators and admins) -->
    {#if user && (user.email === 'moderator@hw3.com' || user.email === 'admin@hw3.com')}
      <button class="delete-button" on:click={() => deleteComment(comment._id)}>Delete</button>
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
  .comment-buttons, .submit-and-cancel {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
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
  .delete-button, .cancel-button, .redact-button {
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
    color: #999; /*gray color is removed by the moderator*/
    font-style: italic;
  }
</style>
  