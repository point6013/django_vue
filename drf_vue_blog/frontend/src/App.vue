<!--   frontend/src/App.vue   -->

<template>
    <BlogHeader/>
    <ArticleList/>
    <BlogFooter/>
</template>

<script>
    import BlogHeader from "./components/BlogHeader.vue"
    import BlogFooter from "./components/BlogFooter";
    import ArticleList from "./components/ArticleList";

    export default {
        name: 'App',
        components: {BlogFooter, BlogHeader, ArticleList}
    }
</script>

<style>

    #app {
        font-family: Georgia, Arial, sans-serif;
        margin-left: 40px;
        margin-right: 40px;
    }


</style>
