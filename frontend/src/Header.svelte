<script>
    // Import sub-components for each part of the site header
    import Top from "./Top.svelte";
    import Logo from "./Logo.svelte"; 
    import Categories from "./Categories.svelte";
</script>

<header class="header">
    
</header>

<header> <!-- Site header -->
    <!--
        The header is divided into 3 rows in total:
            - top
            - logo
            - navigation
    -->
    <Top />
    <Logo />
    <Categories />
</header>

<style>
/* Base header typography and spacing */
header {
    font-family: "Lato", sans-serif;
    font-weight: 450;
    font-style: normal;
}
</style>