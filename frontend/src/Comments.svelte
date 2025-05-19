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

 /*
  * This function handles the reply submission by the users.
  */
  async function handleReply() {   
    if (replyContent.trim() === "") return;
    await submitComment(replyContent, comment._id);  // Submit reply with parent comment ID
    replyContent = "";  // Clear input after submission
    replying = false;   // Hide reply form
  }

  /*
   * This function handles the comment deletion after the moderator or admin confirm deletion.
   */
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
      // AI tool helps to give inspirations on how to update the comments immediately
      comment.content = "COMMENT REMOVED BY MODERATOR!";
      comment.removed = true;
      comment = comment;

      // Fetch updated comments list
      const updatedComments = await fetch(`${BASE_URL}/api/comments?article_id=${currentaid}`, { 
        credentials: 'include' 
      }).then(res => res.json());
      
      comments = updatedComments;

    } catch (error) {
      console.error("Error deleting comment:", error);
    }
  }

  /*
   * This function redacts the comment by the moderator or admin after they confirm the redaction.
   */
  function redactComment(original: string, edited: string): string {
    try {
      console.log("Original content:", original);
      console.log("Edited content:", edited);
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
          console.log("Redacting", redacted);
          i++;
        }
      }
      console.log("Redacted result:", redacted);
      //If the edited content is not the same length as the original, return the original content
      if (j < edited.length) {
        alert("Invalid redaction!");
        return original;
      }

      return redacted;
    } catch (error) {
      console.error("Error redacting comment:", error);
      return original;
    }
  }

  /*
   * This function handles the redaction of the comment by the moderator or admin after they confirm the redaction.
   */
  async function handleRedact() {
    //check if the comment has already been removed
    if (comment.removed) {
      alert("This comment has already been removed by moderator!");
      redacting = false;
      return;
    }

    console.log("Before redaction - comment content:", comment.content);
    console.log("Redact content:", redactContent);
    const redacted = redactComment(comment.content, redactContent);
    console.log("After redaction - redacted content:", redacted);

    const response = await fetch(`http://localhost:8000/api/comments/${comment._id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" }, //specify the content type as json
      credentials: "include",
      body: JSON.stringify({ content: redacted }) //send the redacted content to the backend
    });

    if (!response.ok) {
        throw new Error(`Failed to redact comment: ${response.status}`);
    }
    //update the comment content
    comment.content = redacted;
    comment = comment; 

    redacting = false;
  }

</script>

<!-- Comment display and interaction UI -->
<div class="comment-item" class:has-parent={comment.parent}>
  <!-- User name and comment content -->
  <p class="user-name">{comment.user}</p>
  <p class="content" class:removed={comment.removed}>{comment.content}</p>

  <div class="comment-buttons">
    {#if replying}
      <!-- Reply input form -->
      <textarea bind:value={replyContent}></textarea>
      <div class="submit-and-cancel">
        <button class="submit-button" on:click={handleReply}>Submit</button>
        <button class="cancel-button" on:click={() => replying = false}>Cancel</button>
      </div>  
    {:else if redacting}
      <!-- Redact input form -->
      <textarea bind:value={redactContent}></textarea>
      <div class="submit-and-cancel">
        <button class="submit-button" on:click={handleRedact}>Submit</button>
        <button class="cancel-button" on:click={() => redacting = false}>Cancel</button>
      </div>
    {:else}
      <div class="reply-redact-delete">
        <!--if NOT replying or redacting, only reply redact and delete buttons are comment-buttons-->
        <div id="reply-and-redact">
          <button class="reply-button" on:click={() => replying = true}>Reply</button>
          {#if user && (user.email === 'moderator@hw3.com' || user.email === 'admin@hw3.com')}
            <button class="redact-button" on:click={() => redacting = true}>Redact</button>
          {/if}
        </div>
        <div id="delete-button">
          <!-- Delete button (only visible to moderators and admins) -->
          {#if user && (user.email === 'moderator@hw3.com' || user.email === 'admin@hw3.com')}
            <button class="delete-button" on:click={() => deleteComment(comment._id)}>Delete</button>
          {/if}
        </div>
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
    margin: 1rem;
  }
  /* Comment with parent has a border on the left */
  .has-parent {
    border-left: 1.5px solid #ddd;
    padding-left: 1rem;
    margin-left: 0.5rem;
  }

  /* Username styling */
  .comment-item .user-name {
    font-weight: bold;
    font-size: 0.95rem;
    display: inline-block;
    margin-bottom: 0.5rem;
  }
 
  /* Layout for action buttons */
  .comment-buttons {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    border: none;
    width: 100%;
    margin-top: 0.5rem;
  }

  /* textarea */
  .comment-buttons textarea {
    width: 100%;
    min-height: 30px;
    margin-top: 4px;
    font-size: 14px;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 6px;
    box-sizing: border-box;
  }

  .submit-and-cancel {
    margin-top: 5px;
    display: flex;
    gap: 20px;
    justify-content: flex-end;
  }
  #reply-and-redact {
    display: flex;
    justify-content: flex-start;
    gap: 20px;
  }

  .reply-redact-delete {
    display: flex;
    justify-content: space-between;
    gap: 20px;
  }

  .reply-button, .submit-button {
    background-color: white;
    font-weight: bold;
    border: none;
    color: #547994;
  }

  .redact-button, .delete-button, .cancel-button {  
    background-color: white;
    font-weight: bold;
    border: none;
    color: grey;
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
  