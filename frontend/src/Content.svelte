<script lang="ts">
  // Base URL for backend API
  const BASE_URL = "http://localhost:8000";
  import { onMount, getContext, setContext } from "svelte";
  import comment from "./assets/comment.svg";
  import Comments from "./Comments.svelte";
  
  type User = { email: string; name: string };
  let user: User | null = null;
  let showSidebar = false;
  let currentTitle = "";
  let currentaid = "";
  //The array of comments
  let comments: any[] = [];
  let newComment = "";
  let textareaFocused = false;
  let commentCount = 0;

  $: {
    commentCount = comments.filter(c => !c.removed).length;
  }

  $: if (user) {
    setContext("user", user);
    console.log("Setting user context:", user);
  }

  function loadUser() {
    fetch(`${BASE_URL}/api/userinfo`, {
      credentials: 'include'
    })
    .then(res => {
      if (!res.ok) {
        throw new Error('Failed to load user');
      }
      return res.json();
    })
    .then(data => {
      console.log("User info from backend:", data);
      console.log("User name:", data.name);
      console.log("User email:", data.email);
      if (data && data.email) {
        user = data;
      }
    })
    .catch((error) => {
      console.error("Error loading user:", error);
      user = null;
    });
  }

  type LoadCommentsFunction = (article_id: string) => void;
  setContext<LoadCommentsFunction>('loadComments', loadComments);
  
  //Fetch data when component mounts
  onMount(() => {
    loadUser();
    fetch(`${BASE_URL}/api/ucdavis-news`, {credentials: 'include'})
      .then(statusCheck) // Validate HTTP status
      .then((resp) => resp.json()) // Parse JSON body
      .then(processData) // Populate the DOM with fetched articles
      .catch(handleError); // Handle any fetch errors
  });

  export function loadComments(article_id: string) {
    fetch(`${BASE_URL}/api/comments?article_id=${encodeURIComponent(article_id)}`, { credentials: 'include' })
      .then(statusCheck)
      .then((resp) => resp.json())
      .then((data) => {
        console.log('Comments loaded:', data);
        comments = data;
      })
      .catch(handleError);
  }
  //AI tool helps to give inspirations on how to nest the comments
  function nestComments(comments: any[]) {
    const map = new Map();
    const nested = [];
    for (const current of comments) {
      current.children = []; //add a children array to the current comment
      map.set(current._id, current); //add the current comment to the map
    }
    for (const current of comments) {
      if (current.parent && map.has(current.parent)) {
        map.get(current.parent).children.push(current);
      } else {
        nested.push(current);
      }
    }
    return nested;
  }

  $: nestedComments = nestComments(comments); //To ensure that everytime the comments are updated, the nestedComments are updated

  function submitComment(content: string, parent: string | null = null): Promise<any> {
    if (!content.trim()) return Promise.resolve();

    return fetch(`${BASE_URL}/api/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        article_id: currentaid,
        content,
        parent,
      })
    })
    .then(statusCheck)
    .then(() => {
      newComment = ""; // User can input new comment
      return loadComments(currentaid);
    })
    .catch(handleError);
  }

/** Fetch the # of comments for one article and update its <span> */
async function fetchCommentCount(articleId: string) {
const res = await fetch(
   `${BASE_URL}/api/comments?article_id=${encodeURIComponent(articleId)}`,
   { credentials: "include" }
);
if (!res.ok) throw new Error(`Couldn't fetch comments for ${articleId}`);
const data: any[] = await res.json();
// find the <span class="comment-count"> under the button with matching data-article-id
const span = document.querySelector(
  `button.comment[data-article-id="${articleId}"] .comment-count`
);
if (span) span.textContent = String(data.length);
}

  /**
   * This function processes the data.
   *
   * @param {any} data - The data from the fetch request.
   */
  function processData(data: any) {
    console.log(data);
    const abstracts = document.querySelectorAll(".abstract"); // find all the <p> with class abstract
    const titles = document.querySelectorAll(".title"); // find all the <h2> with class title
    const pictures = document.querySelectorAll(".picture"); // find all the <img> with class picture
    const articles = data.response.docs; // get the article list
    const readtime = document.querySelectorAll(".readtime"); // find all the <p> with class readtime
    const commentButtons = document.querySelectorAll("button.comment");

    console.log("abstracts.length: ", abstracts.length);
    for (let i = 0; i < abstracts.length; i++) {
      console.log("articles.length: ", articles.length);
      if (i < articles.length) {
        //get all the data for certain article
        const article = articles[i];
        const titleText =
          article.headline?.main ||
          article.headline?.print_headline ||
          "No Title";
        const caption = article.multimedia?.caption || "No Caption";
        const abstractText = article.abstract || "No Abstract";
        const webUrl = article.web_url;
        const imageUrl = article.multimedia?.default?.url || "";
        const readtimeText =
          Math.ceil(article.word_count / 150) + " MIN READ" || "No Readtime";
        titles[i].textContent = titleText;
        //set the title to the sidebar
        titles[i].addEventListener("click", () => {
          currentTitle = titleText;
          currentaid = article._id;  
          showSidebar = true;
          loadComments(article._id);
        });
        const btn = commentButtons[i] as HTMLButtonElement; 
        btn.setAttribute("data-article-id", article._id); 
        btn.addEventListener("click", () => {
          currentTitle = titleText;
          currentaid = article._id;
          showSidebar = true;
          loadComments(article._id);
        });
        fetchCommentCount(article._id).catch(console.error);

        if (imageUrl) {
          (pictures[i] as HTMLImageElement).src = imageUrl;
          (pictures[i] as HTMLImageElement).alt = caption;
        } else {
          (pictures[i] as HTMLElement).style.display = "none";
        }
        abstracts[i].textContent = abstractText;
        readtime[i].textContent = readtimeText;
      }
    }
  }

  /**
   * This function checks if the response is ok.
   *
   * @param {Response} res - The response from the fetch request.
   * @returns {Promise<Response>} The response from the fetch request.
   */
  async function statusCheck(res: Response) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }
  /**
   * This function handles the error.
   *
   * @param {Error} err - The error from the fetch request.
   */
  function handleError(err: Error) {
    alert("Error:" + err.message);
  }
  function toggleSidebar() {
    showSidebar = !showSidebar;
  }
  function cancelComment() {
    newComment = "";
    textareaFocused = false;
  }
</script>

<main id="content">
  <!-- Three-column layout -->
  <!-- Left column: featured articles -->
  <section class="articles">
    <div class="article">

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>
  </section>

  <!-- The line that separates the left and middle columns -->
  <div class="pline" id="lineleft"></div>

  <!-- Middle column: contain both images and text -->
  <section class="articles" id="middle">
    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

  </section>

  <div class="pline" id="lineright"></div>
  <!-- Divider -->

  <!-- Right column: mosaic + opinion -->
  <aside class="articles" id="right-column">
    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

    <div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        
        <!-- Image -->
      </figure>
      <h2 class="title">Loading...</h2>
      <p class="abstract"></p>

      <!-- Full summary -->
      <div class="readtime-comment">
        <p class="readtime"></p>
        <!-- Read time -->
        <button class="comment">
          <img src={comment} alt="comment" />
          <span class="comment-count"></span>
        </button>
      </div>
      
    </div>

    <div class="hline"></div>
    <!-- Separator -->

  </aside>
</main>

{#if showSidebar}
  <!--The area outsides the sidebar is covered by a gray layer-->
  <div class="sidebar-cover" on:click={toggleSidebar} role="button">
    <div class="sidebar" on:click|stopPropagation role="dialog">

      <div class="sidebar-header">
        <p>{currentTitle} <span class="comment-count">{commentCount}</span></p>
        <button class="close-btn" on:click={toggleSidebar}>&times;</button>
      </div>

      <div class="sidebar-content">
        <h3>Comments <span>{commentCount}</span></h3>
        <div class="comment-box">
          <!--AI tool helps to give inspirations on how to hide the submit button before click the textarea-->
          <!--When the textarea is focused, the submit button will be shown-->
          <!--When the textarea is blurred, the submit button will be hidden-->
          <textarea bind:value={newComment} 
                    placeholder="Share your thoughts..." 

                    on:focus={() => textareaFocused = true}
                    on:blur={() => {}}>
          </textarea>
          <div class="comment-buttons">
            {#if textareaFocused}
              <button id="cancel" on:click={cancelComment}>CANCEL</button>
              <button id="submit"  on:click={() => submitComment(newComment)}>SUBMIT</button>
            {/if}
          </div>
        </div>
        {#each nestComments(comments).reverse() as comment}
          <Comments {comment} {submitComment} />
        {/each}
      </div>
    </div>
  </div>
{/if}

<style>
  /* Layout for the content area: three columns with gaps */
  #content {
    margin-top: 1rem;
    gap: 1rem;
    display: flex;
    flex-direction: row;
  }

  /* Article column styling */
  .articles {
    display: flex;
    flex-direction: column;
    flex: 1;
    font-family: "Newsreader", serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
    gap: 0.8rem;
  }

  /* Headline styling */
  .articles h2 {
    font-size: 1.2rem;
    cursor: pointer;
  }

  /* Paragraph text styling */
  .articles p {
    margin-top: 0.8rem 0 0.2rem 0;
    font-size: 1rem;
    color: #beb3b3;
  }

  /* Horizontal separator between articles */
  .hline {
    height: 0.5px;
    background-color: #beb3b3;
    margin: 1rem 0;
  }

  .readtime-comment {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* Read time text styling */
  .articles .readtime {
    font-family: "Lato", sans-serif;
    margin-top: 0.5rem;
    font-weight: 350;
    font-size: 0.7rem;
    font-style: normal;
  }
  .comment {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: 0.5rem;
    height: 2rem;
    min-width: 3.5rem;
    background-color: white;
    justify-content: space-between;
    border: 1px solid #beb3b3;
    border-radius: 15px;
  }
  .comment-box button {
    align-self: flex-end;
    font-family: "Gabarito", sans-serif;
  }

  .comment img {
    width: 24px;
    height: 24px;
  }

  .comment-count {
    font-size: 16px;
  }

  /* Image column styling */
  .images {
    flex: 1.2;
    margin: 0rem 0.5rem;
  }
  .images img {
    max-width: 100%;
    height: auto;
    margin: 1rem 0rem;
  }

  /* Vertical separator between columns */
  .pline {
    width: 0.5px;
    background-color: #beb3b3;
  }

  /* Sidebar (aside) styling */
  #content aside {
    flex: 0.5;
  }
  #content aside img {
    max-width: 100%;
  }

  /* Ensure all images scale responsively */
  .picture {
    width: 100%;
    height: auto;
  }

  .sidebar-cover {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    /* Ensure the sidebar is on the top of the page */
    display: flex;
    justify-content: flex-end;
    overflow: hidden; /* prevent the sidebar from overflowing the page */
  }

  .sidebar {
    width: 400px;
    height: 100vh;
    background-color: white;
    position: relative;
    font-family: "Newsreader", serif;
    font-weight: 120;
    display: flex;
    flex-direction: column;
  }

  .sidebar-header {
    padding: 1rem;
    font-size: 1.2rem;
    font-weight: 250;
    border-bottom: 1px solid #e9e6e6;
    align-items: center;
    font-family: "Gabarito", sans-serif;
    display: flex;
    justify-content: space-between;
    flex-shrink: 0;  /* prevent the header from being compressed */
  }

  .sidebar-header p {
    font-weight: bold;
    font-size: 1rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .sidebar-header .comment-count {
    font-size: 0.9rem;
    color: gray;
  }

  .close-btn {
    font-size: 2rem;
    cursor: pointer;
    background-color: none;
    border: none;
    padding: 0.5rem;
  }

  .sidebar-content {
    padding: 1rem;
    font-family: sans-serif;
    overflow-y: auto;  /* add scrollbar */
    flex-grow: 1;  /* take up the remaining space */
    scrollbar-width: none;
  }

  .sidebar-content h3 {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  .sidebar-content h3 span {
    font-weight: lighter;
  }

  .comment-buttons {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
  }

  #submit {
    background-color: #5c7b95;
    color: white;
    border: 1px solid black;
    padding: 0.4rem 1rem;
    border-radius: 5px;
    font-size: 0.9rem;
    cursor: pointer;
    position: flex-end;
  }

  #cancel {
    background-color: #e4dfdf;
    color: black;
    border: 1px solid black;
    border: none;
    padding: 0.4rem 1rem;
    border-radius: 5px;
    font-size: 0.9rem;
    cursor: pointer;
    position: flex-end;
  }

  /* comment textbox */
  .sidebar-content textarea {
    width: 100%;
    border: 1px solid gray;
    border-radius: 12px;
    padding: 1rem;
    font-size: 0.9rem;
  }

</style>
