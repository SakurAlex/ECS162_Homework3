<script lang="ts">
  // Base URL for backend API
  const BASE_URL = "http://127.0.0.1:8000";
  import { onMount, getContext } from "svelte";
  import comment from "./assets/comment.svg";
  const user = getContext('user');
  
  // Fetch data when component mounts
  onMount(() => {
    fetch(`${BASE_URL}/api/ucdavis-news`, {credentials: 'include'})
      .then(statusCheck) // Validate HTTP status
      .then((resp) => resp.json()) // Parse JSON body
      .then(processData) // Populate the DOM with fetched articles
      .catch(handleError); // Handle any fetch errors
  });

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

        //set the data to the html
        titles[i].innerHTML = `<a href="/article?id=${encodeURIComponent(article._id)}" class="article-link">${titleText}</a>`;

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
  <aside class="articles">
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
</style>
