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