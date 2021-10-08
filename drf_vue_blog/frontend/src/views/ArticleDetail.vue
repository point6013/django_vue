<template>

    <BlogHeader/>
    <div v-if="article!==null" class="grid-container">
        <div>
            <h1 id="title">{{article.title}}</h1>
            <p id="subtitle">本文由{{article.author.username}}发布于{{formatted_time(article.created)}}</p>
            <div class="article-body" v-html="article.body_html"  />
        </div>
        <div>
            <h3>目录</h3>
            <div v-html='article.toc_html' class="toc" >
            </div>
        </div>
    </div>
    <BlogFooter/>
</template>

<script>
    import BlogHeader from "../components/BlogHeader";
    import BlogFooter from "../components/BlogFooter";
    import axios from 'axios'
    // import 'highlight.js/styles/github-dark-dimmed.css';
    // import markdownItTocDoneRight  from "markdown-it-toc-done-right"
    // import marked from 'marked'
    // import 'highlight.js/styles/monokai-sublime.css'
    // import hljs from "highlight.js";
    // import hljs from 'highlight.js/lib/common';
    // import hljsVuePlugin from "@highlightjs/vue-plugin";
    // import VueMarkdownIt from 'vue3-markdown-it'
    import 'highlight.js/styles/monokai.css'
    import '../assets/pygments.css'
    // 导入pygments.css


    export default {
        name: "ArticleDetail.vue",
        components: {BlogFooter, BlogHeader},
        data: function () {
            return {
                article: null

            }
        },
        mounted() {
            axios.get('/api/article/' + this.$route.params.id).then(
                response => (this.article = response.data)
            )
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            }

        }
    }
</script>


<style>
    .article-body p img {
        max-width: 100%;
        border-radius: 5px;
        box-shadow: gray 0 0 20px;
        margin-left: 50px;
    }

    .article-body pre {
        /*max-width: 100%;*/
        /*border-radius: 5px;*/
        /*box-shadow: gray 0 0 20px;*/
        margin-left: 50px;
    }

    .toc ul {
        list-style-type: none;
    }

    .toc a {
        color: gray;
    }
</style>


<style scoped>
    .grid-container {
        display: grid;
        grid-template-columns: 3fr 1fr;
    }


    #title {
        text-align: center;
        font-size: x-large;
    }

    #subtitle {
        text-align: center;
        color: gray;
        font-size: small;
    }

</style>