<script>
  import arrow from './assets/arrow.svg';
</script>

<nav>
    <!--
        The navigation bar
    -->
    <ul>
        <!--
            Image source: veryicon
            https://www.veryicon.com/icons/system/zoomlion-linear-icon/drop-down-43.html
        -->
        <li>
            <a href="https://www.nytimes.com/section/us" target="_blank" rel="noopener">
                U.S. <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/section/world" target="_blank" rel="noopener">
                World <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/section/business" target="_blank" rel="noopener">
                Business <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/section/arts" target="_blank" rel="noopener">
                Arts <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/spotlight/lifestyle" target="_blank" rel="noopener">
                Lifestyle <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/section/opinion" target="_blank" rel="noopener">
                Opinion <img src={arrow} alt="arrow" />
            </a>
        </li>
    </ul>

    <!-- Vertical separator -->
    <div id="vline"></div> 

    <ul> <!-- Right links -->
        <li>
            <a href="https://www.nytimes.com/spotlight/podcasts" target="_blank" rel="noopener">
                Audio <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/crosswords" target="_blank" rel="noopener">
                Games <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://cooking.nytimes.com/" target="_blank" rel="noopener">
                Cooking <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/wirecutter/" target="_blank" rel="noopener">
                Wirecutter <img src={arrow} alt="arrow" />
            </a>
        </li>
        <li>
            <a href="https://www.nytimes.com/athletic/" target="_blank" rel="noopener">
                The Athletic <img src={arrow} alt="arrow" />
            </a>
        </li>
    </ul>
</nav>

<style>
/* Flex layout for navigation: centered items with wrapping */
nav {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    padding: 0.75rem 1rem;
    border-bottom: 2px double grey; /* Double-lined bottom border */
}

/* Layout for each group of links */
nav ul {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem; /* Spacing between list items */
    list-style: none; /* Remove default bullets */
}

/* Style for each navigation item */
nav li {
    position: relative; /* For potential dropdown positioning */
    cursor: pointer; /* Pointer cursor on hover */
}

/* Size the dropdown arrow icon */
nav li img {
    width: 0.5rem;
}

/* Vertical line separator styling */
#vline {
    width: 1px;
    height: 1.2rem;
    background-color: rgb(175, 165, 165);
    margin: 1rem;
}
</style>