# Daily Better

Smart bookmarks manager with content recomendation.

# What?

The main idea of the project is to give you easy daily quests like "read this article today" or "watch that video". By doing this consistently, you will (probably) become better.

# Why?

To handle thousands of unread bookmarks with articles, lectures, books, etc.

---

# For development

`.env` file example:

```bash
#!/usr/bin/env bash

# For testing
export DB_URL='sqlite:///temp.db'

# For production
export DB_URL='postgresql+psycopg2://postgres:changeme@localhost:5432/postgres'
```


bookmarklet:

```javascript
javascript:(function() {
    const title = encodeURIComponent(document.title);
    const bookmark_url = encodeURIComponent(window.location.href);

    const api_params = `?title=${title}&url=${bookmark_url}`;
    const api_url = 'http://localhost:7777/bookmarklet' + api_params;

    const context = '_blank';
    const window_params = 'width=700, height=400, titlebar=no, toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no';

    const new_window = window.open(api_url, context, window_params);
})()
```
