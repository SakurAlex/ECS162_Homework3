<script>
  // Import layout components for header, main content, and footer
  import Header from "./Header.svelte";
  import Content from "./Content.svelte";
  import Footer from "./Footer.svelte";
</script>

<main>
  <!-- Render the page sections in order: header, content, footer -->
  <Header />
  <Content />
  <Footer />
</main>

<style>
  /* Use a column flex layout to stack sections and fill full viewport height */
  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh; /* Ensure footer sticks to bottom if content is short */
  }
  /* Vertical line styling */
  #vline {
    width: 1px;
    height: 1.2rem;
    background-color: rgb(175, 165, 165); /*  gray  */
    margin: 1rem;
  }
</style>