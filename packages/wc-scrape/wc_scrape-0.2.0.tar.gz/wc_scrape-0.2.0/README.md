# Will Chen's Twitter Scraper

A simple command-line tool to fetch and process tweets.

## Features

- Fetch tweets from a specific user (most recent -- up to 3200)
- Save tweets to JSON
- Convert JSON tweets to a readable text format
- Retrieve a specific tweet by ID
- Retry on rate limit with 15-minute backoff

## Installation

Install from PyPI:

```sh
$ pip install wc-scrape
```

or

```sh
$ pip3 install wc-scrape
```

(you may need to use `sudo` or `--break-system-packages` on some systems)

## Usage

First, set up your Twitter Bearer Token:

```sh
$ wc-scrape setup
```

### Fetching Tweets

Fetch the latest tweets from a user:

```sh
$ wc-scrape fetch-tweets <username> <count>
```

This will save the tweets to a JSON file.

To generate a text file output, use the `--to-txt` flag when fetching tweets:

```sh
$ wc-scrape fetch-tweets <username> <count> --to-txt
```

To retry on rate limit with a 15-minute backoff, use the `--retry` flag:

```sh
$ wc-scrape fetch-tweets <username> <count> --retry
```
