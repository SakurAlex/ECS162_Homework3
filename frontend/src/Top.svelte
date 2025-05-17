<script>
  import search from './assets/search.svg';
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
    <div>
        <!--
            Two buttons on the top-right corner for subscription & logging in
        -->
        <button>SUBSCRIBE FOR $1/WEEK</button> <!-- Subscribe button -->
        <button>LOG IN</button> <!-- Login button -->
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
</style>