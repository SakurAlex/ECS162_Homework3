<script lang="ts">
  import { onMount } from 'svelte';
  import { setContext } from 'svelte';
  import search from './assets/search.svg';
  const baseUrl = import.meta.env.VITE_BASE_URL ?? 'http://localhost:8000';

  //User state & auth actions
  let user: { email: string; groups?: string[] } | null = null;

  async function loadUser() {
    const res = await fetch(
      `${baseUrl}/api/userinfo`,
      { credentials: 'include' }
    );
    user = res.ok ? await res.json() : null;
    setContext('user', user);  // set the user as user context
  }

  function login() {
    window.location.href = `${baseUrl}/login`;
  }
  //To ensure the user is logged out, I need to clear the session and redirect to the home page
  async function logout() {
    const response = await fetch(`${baseUrl}/logout`, {credentials: 'include'});
    if (response.ok) {
      user = null;
      setContext('user', null);
      window.location.href = '/';
    }
  }

  onMount(loadUser);
</script>

<div id="top"> <!-- Top bar -->
    <figure> 
        <img src={search} alt="search"> <!-- Search action -->
    </figure>
    <div id="languages"> 
        <!--
            The choices for languages on the top of the page
        -->
        <ul>
            <li><span id="selected">U.S.</span></li> <!-- Selected locale -->
            <li>INTERNATIONAL</li> <!-- Other options -->
            <li>CANADA</li>
            <li>ESPAÑOL</li>
            <li>中文</li>
        </ul>
    </div>
    <div class="actions">
    <!-- Static subscribe button -->
    <button class="subscribe">SUBSCRIBE FOR $1/WEEK</button>
    <!-- Dynamic login/logout button -->
    {#if user}
      <button class="auth" on:click={logout}>
        LOG OUT ({user.email})
      </button>
    {:else}
      <button class="auth" on:click={login}>
        LOG IN
      </button>
    {/if}
  </div>
</div>

<style>
/* Layout for top bar: space between search, languages, and buttons */
#top {
    display: flex;
    width: 100%;
    font-size: 0.7rem;
    justify-content: space-between;
    align-items: center;
    max-height: 2rem;
}

/* Allocate space for the search icon */
#top figure {
    flex: 0.4;
}

/* Language list styling */
#top ul{
    flex: 1;
    list-style: none; /* Remove bullets */
    align-items: baseline;
    color: grey; /* Muted text color for inactive locales */
    display: flex;
    gap: 1rem; /* Spacing between items */
}

/* Highlight the currently selected locale */
#selected {
    color: black;
}

/* Make the search icon and list items clickable */
#top img, li{
    cursor: pointer;
}

/* Right-hand container for subscribe + auth buttons */
.actions {
  display: flex;
  gap: 0.4rem;
}

/* Style for action buttons */
button {
    background-color: #5c7b95;
    color: white;
    padding: 0.4rem 0.8rem;
    margin: auto 0.4rem;
    border: none;
    border-radius: 5px;
    font-family: "Gabarito", sans-serif;
    font-optical-sizing: auto;
    font-weight: 775;
    font-style: normal;
    cursor: pointer; /* Interactive cursor */
}

/* Subscribe button variation */
.subscribe {
  background-color: #5c7b95;
}

/* Auth button variation */
.auth {
  background-color: #5c7b95;
}
</style>