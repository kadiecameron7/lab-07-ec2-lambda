#!/usr/bin/env python3
"""My own query on gutenberg.books."""

import json
import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Atlas settings from your environment variables, as in Lab 05
MONGODB_ATLAS_URL = os.environ["MONGODB_ATLAS_URL"]
MONGODB_ATLAS_USER = os.environ["MONGODB_ATLAS_USER"]
MONGODB_ATLAS_PWD = os.environ["MONGODB_ATLAS_PWD"]

logger = logging.getLogger(__name__)

def vocabulary_extremes(books):
    """Return 5 books with the highest vocabulary ratio and 5 with the lowest."""
    highest_vocabulary_ratio = list((books.find({}, {"title": 1, "word_count": 1, "vocabulary_ratio": 1}).sort("vocabulary_ratio", -1).limit(5)))
    lowest_vocabulary_ratio = list((books.find({}, {"title": 1, "word_count": 1, "vocabulary_ratio": 1}).sort("vocabulary_ratio", 1).limit(5)))
    return {
        "highest_vocabulary_ratio": highest_vocabulary_ratio,
        "lowest_vocabulary_ratio": lowest_vocabulary_ratio
    }

def books_by_author(books):
    """Return a list of authors with the most books."""
    authors = books.distinct("author")
    rows = []
    for author in authors:
        book_count = books.count_documents({"author": author})
        rows.append({"author": author, "books": book_count})
    rows.sort(key=lambda row: row["books"], reverse=True)
    return rows[:5]

def main():
    """Print the result of my query as JSON."""
    client = MongoClient(MONGODB_ATLAS_URL, username=MONGODB_ATLAS_USER, password=MONGODB_ATLAS_PWD)
    try:
        books = client["gutenberg"]["books"]
        result = [vocabulary_extremes(books), books_by_author(books)]  # TODO: replace [] with a call of your query function
        print(json.dumps(result, indent=2, default=str))
    except PyMongoError as e:
        logger.error("Cannot query MongoDB: %s", e)
        raise
    finally:
        client.close()  # closes the connections to Atlas, also after an error


if __name__ == "__main__":
    main()