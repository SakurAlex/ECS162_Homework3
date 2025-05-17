<script>
    // Import the New York Times logo
    import logo from './assets/NewYorkTimes.svg';
    
    //Keep current date on the top left corner
    const date = new Date();
    const currentDate = date.toLocaleString("en-US", {
        weekday: "long", // Full weekday name, e.g., "Monday"
        year: "numeric", // Four-digit year
        month: "long", // Full month name, e.g., "January"
        day: "numeric", // Day of the month
        hour: "2-digit", // Hour (00–23)
        minute: "2-digit" // Minute (00–59)
    });

    //Trend data on the top right corner
    const data = [
        {
            name: "Sleep",
            value: "-0.19%↓",
            color: "red"
        },
        {
            name: "Study",
            value: "+0.31%↑",
            color: "green"
        },
        {
            name: "Social",
            value: "-0.45%↓",
            color: "red"
        }
    ];

    // Index to track current trend item
    let index = 0;
    // Initialize displayed trend to the first element
    let currentTrend = data[0];

    /**
     * This function updates the current trend.
     */
    function updateMarket() {
        index = (index + 1) % 3;
        currentTrend = data[index];
    }

    // Rotate trend every 1.5 seconds
    setInterval(updateMarket, 1500);
</script>

<div id="logo">
    <!--
        The row in the header which includes the logo "New York Times"
    -->
    <div id="date"> 
        <!--
            The time of the current day
        -->
        <p>{currentDate}</p>
        <p>Today's Paper</p> <!-- Static label -->
    </div>
    <figure>
        <!--
            The logo "New York Time" in the center of the page
            Image source: wikipedia
            https://en.m.wikipedia.org/wiki/File:NewYorkTimes.svg
        -->
        <a href="https://www.nytimes.com/"><img src={logo} alt="NewYorkTimes"></a> <!-- Link to homepage -->
    </figure>
    <div id="trend"> 
        <!--
            The current trend (stock market)
        -->
        <p>{currentTrend.name} <span style="color: {currentTrend.color};">{currentTrend.value}</span></p>
    </div>
</div>

<style>
/* Flex layout to space out date, logo, and trend evenly */
#logo {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}

/* Styling for the date block */
#date {
    display:flex;
    flex-direction: column;
    max-width: 20%;
    gap: 0.5rem;
    font-size: 0.85rem;
}

/* Logo image sizing */
#logo img {
    height: 4rem;
    max-width: 100%;
}

/* Container for the rotating trend display */
#trend {
    width: 8rem;
    max-width: 12%;
}
</style>