<script lang="ts">
  // Base URL for backend API
  const BASE_URL = "http://127.0.0.1:8000";
  import { onMount } from "svelte";

  // Fetch data when component mounts
  onMount(() => {
    fetch(`${BASE_URL}/api/ucdavis-news`)
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
        titles[i].innerHTML =
          `<a href="${webUrl}" target="_blank">${titleText}</a>`;

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
    <article>
      <div>
        <h2 class="title">Loading...</h2>
        <p class="abstract"></p>
        <!-- Full summary -->
        <p class="readtime"></p>
        <!-- Read time -->
        <figure class="images">
          <img class="picture" alt="Loading..." />
          <!-- Image -->
        </figure>
      </div>

      <div class="hline"></div>
      <!-- Separator -->

      <div>
        <h2 class="title">Loading...</h2>
        <p class="abstract"></p>
        <!-- Full summary -->
        <p class="readtime"></p>
      </div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        <!-- Image -->
      </figure>

      <div class="hline"></div>
      <!-- Separator -->

      <div>
        <h2 class="title">Loading...</h2>
        <p class="abstract"></p>
        <!-- Full summary -->
        <p class="readtime"></p>
      </div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        <!-- Image -->
      </figure>

      <div class="hline"></div>
      <!-- Separator -->

      <div>
        <h2 class="title">Loading...</h2>
        <p class="abstract"></p>
        <!-- Full summary -->
        <p class="readtime"></p>
      </div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        <!-- Image -->
      </figure>

      <div class="hline"></div>
      <!-- Separator -->

      <div>
        <h2 class="title">Loading...</h2>
        <p class="abstract"></p>
        <!-- Full summary -->
        <p class="readtime"></p>
      </div>

      <figure class="images">
        <img class="picture" alt="Loading..." />
        <!-- Image -->
      </figure>
    </article>
  </section>

  <!-- The line that separates the left and middle columns -->
  <div class="pline" id="lineleft"></div>

  <!-- Middle column: contain both images and text -->
  <section class="images" id="middle">
    <figure>
      <img class="picture" alt="Loading..." />
      <!-- Image -->
    </figure>

    <section class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </section>
    <div class="hline"></div>

    <figure>
      <img class="picture" alt="Loading..." />
      <!-- Image -->
    </figure>

    <section class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </section>
    <div class="hline"></div>

    <figure>
      <img class="picture" alt="Loading..." />
      <!-- Image -->
    </figure>

    <section class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </section>
    <div class="hline"></div>

    <figure>
      <img class="picture" alt="Loading..." />
      <!-- Image -->
    </figure>

    <section class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </section>
    <div class="hline"></div>

    <figure>
      <img class="picture" alt="Loading..." />
      <!-- Image -->
    </figure>

    <section class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </section>
  </section>

  <div class="pline" id="lineright"></div>
  <!-- Divider -->

  <!-- Right column: mosaic + opinion -->
  <aside>
    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
    <div class="hline"></div>

    <img class="picture" alt="Loading..." />

    <div class="articles">
      <article>
        <div>
          <h2 class="title">Loading...</h2>
          <p class="abstract"></p>
          <!-- Full summary -->
          <p class="readtime"></p>
        </div>
      </article>
    </div>
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
    display: column;
    flex: 1;
    font-family: "Newsreader", serif;
    font-optical-sizing: auto;
    font-weight: 400;
    font-style: normal;
    gap: 1rem;
  }

  /* Headline styling */
  .articles article h2 {
    font-size: 1.2rem;
    cursor: pointer;
  }

  /* Paragraph text styling */
  .articles p {
    margin: 0.8rem 0 0.2rem 0;
    font-size: 1rem;
    color: rgb(114, 110, 110);
  }

  /* Horizontal separator between articles */
  .hline {
    height: 0.5px;
    background-color: rgb(175, 165, 165);
    margin: 1rem 0;
  }

  /* Read time text styling */
  .articles .readtime {
    font-family: "Lato", sans-serif;
    margin: 0.5rem 0 0.2rem 0;
    font-weight: 350;
    font-size: 0.7rem;
    font-style: normal;
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
    background-color: rgb(196, 190, 190);
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
