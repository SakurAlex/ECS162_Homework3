<script lang="ts">
  import { onMount, setContext } from "svelte";
  import search from './assets/search.svg';
  const BASE_URL = "http://localhost:8000";
  type User = { email: string; name: string };
  let user: User | null = null;
  let showSidebar = false;

  /**
   * Set the user context for the app
   */
  $: if (user) {
    setContext("user", user);
  }

  /**
   * Load the user info from the backend
   */
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
      if (data && data.email) {
        user = data;
      }
    })
    .catch((error) => {
      console.error("Error loading user:", error);
      user = null;
    });
  }

  /**
   * Toggle the sidebar
   */
  function toggleSidebar() {
    showSidebar = !showSidebar;
  }

  /**
   * Login the user
   */
  function login() {
    window.location.href = `${BASE_URL}/login`;
  }
  //To ensure the user is logged out, I need to clear the session and redirect to the home page
  async function logout() {
    toggleSidebar();
    const response = await fetch(`${BASE_URL}/logout`, {credentials: 'include'});
    if (response.ok) {
      user = null;
      setContext('user', null);
      window.location.href = '/';
    }
  }

  onMount(() => {
    loadUser();
  });
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
    <!-- Dynamic login/logout button -->
    {#if user}
      <p id="account" on:click={toggleSidebar}>
        Account
      </p>
    {:else}
      <button on:click={login}>
        LOG IN
      </button>
    {/if}
  </div>
</div>

{#if showSidebar}
  <!--The area outsides the sidebar is covered by a gray layer-->
  <div class="sidebar-cover" on:click={toggleSidebar} role="button">
    <div class="sidebar" on:click|stopPropagation role="dialog">

      <div class="sidebar-header">
        <p>{user?.email}</p>
        <span class="close-btn" on:click={toggleSidebar}>&times;</span>
        <!--The close button for sidebar-->
      </div>

      <div class="sidebar-content">
        <p>Good afternoon.</p>
        <p id="logout" on:click={logout}>Log out</p>
      </div>
    </div>
  </div>
{/if}

<style>
/* Layout for top bar: space between search, languages, and buttons */
#top {
    display: flex;
    width: 100%;
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

/* Right-hand container for auth buttons */
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
/* Style for the account button */
#account {  
  color: black;
  font-size: 1rem;
  font-family: "Gabarito", sans-serif;
  cursor: pointer;
  padding-left: 8rem;
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

/* Style for the sidebar */
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

/* Style for the sidebar header */
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
  font-size: 2rem;
  cursor: pointer;
  color: #363434;
  padding: 0.5rem;
}

/* Style for the sidebar content */
.sidebar-content {
  font-size: 2.5rem;
  padding: 2rem;
  padding-top: 10rem;
  flex-grow: 1;
}

/* Style for the logout button */
#logout {
  color: #333;
  font-size: 1.7rem;
  font-weight: 775;
  font-family: "Gabarito", sans-serif;
  cursor: pointer;
  position: absolute;
  padding: 1rem;
  bottom: 1.5rem;
  left: 1.5rem;
  text-decoration: underline;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
</style>