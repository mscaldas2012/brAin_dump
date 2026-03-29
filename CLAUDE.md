# Overview

This project holds a static website for my personal blog deployed via github repo.

## Structure

Root folder contains the index.html page.
This page is basically a Table of Contents page to access previous blog posts.
This page will have to be modified every time I "post" a new blog.

Each blog is an HTML page. it needs to be saved under folders for year (yyyy) and month (MM)


The index.html page should have:
- a carroussel with the last 4 publshed blogs
- older blogs listed in most recent to oldest, indented by year


## Publishing

To publish a new post, place the HTML file in `/inbox` and run `/post-blog`.
