<script lang="ts">
  // Base URL for backend API
  const BASE_URL = "http://127.0.0.1:8000";
  import { onMount, getContext } from "svelte";
  import comment from "./assets/comment.svg";
  import Comment from "./Comment.svelte";
  const user = getContext('user');
  let showSidebar = false;
  let currentTitle = "";
  let currentaid = "";
  //The array of comments
  let comments: any[] = [];
  let newComment = "";

  
  //Fetch data when component mounts
  onMount(() => {
    fetch(`${BASE_URL}/api/ucdavis-news`, {credentials: 'include'})
      .then(statusCheck) // Validate HTTP status
      .then((resp) => resp.json()) // Parse JSON body
      .then(processData) // Populate the DOM with fetched articles
      .catch(handleError); // Handle any fetch errors
  });

  function loadComments(article_id: string) {
    fetch(`${BASE_URL}/api/comments?article_id=${encodeURIComponent(article_id)}`, { credentials: 'include' })
      .then(statusCheck)
      .then((resp) => resp.json())
      .then((data) => {comments = data;})
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

  async function submitComment(parent = null) {
    const content = newComment;
    if (!content) return;

    const res = await fetch("/api/comments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        article_id: currentaid,
        content,
        parent,
      })
    });

    if (res.ok) {
      newComment = ""; // User can input new comment
      await loadComments(currentaid); 
    } else {
      alert("fail to comment");
    }
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
    const comment = document.querySelectorAll(".comment"); // find all the <button> with class comment

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
        comment[i].addEventListener("click", () => {
          currentTitle = titleText;
          currentaid = article._id;
          showSidebar = true;
          loadComments(article._id);
        });

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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count"> 0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
          <span class="comment-count">0</span>
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
        <p>{currentTitle} <span>{comments.length}</span></p>
        <span class="close-btn" on:click={toggleSidebar}>&times;</span>
        <!--The close button for sidebar-->
      </div>

      <div class="sidebar-content">
        <h3>Comments</h3>
        {#each nestComments(comments) as comment} <!-- repeatedly load the comments -->
          <CommentItem {comment} {submitComment} />
        {/each}
      
        <textarea bind:value={newComment} placeholder="Share your thoughts..."></textarea>
        <button on:click={() => submitComment()}>Post</button>
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
}

  .sidebar {
    width: 400px;
    height: 100%;
    background-color: white;
    position: relative;
    font-family: "Newsreader", serif;
    font-weight: 120;
    justify-content: space-between;
    position: flex;
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
  }

  .close-btn {
    font-size: 1.5rem;
    cursor: pointer;
    color: #363434;
    padding: 0.5rem;
  }

  .sidebar-content {
    font-size: 2.5rem;
    padding: 2rem;
    flex-grow: 1;
  }
</style>
