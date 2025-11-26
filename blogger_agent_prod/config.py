"""Configuration constants and defaults for blogger_agent"""
import os

DEFAULT_OUTPUT_DIR = os.environ.get('BLOGGER_OUT', './out')
DEFAULT_MIN_WORDS = int(os.environ.get('BLOGGER_MIN_WORDS', '400'))
DEFAULT_RSS_FEEDS = os.environ.get('BLOGGER_RSS_FEEDS', '').split(',') if os.environ.get('BLOGGER_RSS_FEEDS') else []
