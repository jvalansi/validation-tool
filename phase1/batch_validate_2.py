#!/usr/bin/env python3
"""Batch validate Notion projects 11-20 and update pages."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from batch_validate import process_project

PROJECTS = [
    {
        "id": "58f189e2-b094-4242-b1cf-bc45c1177dc2",
        "name": "Unsupervised learning (Hebbian)",
        "desc": "Unsupervised neural learning using Hebbian 'fire together wire together' co-activation rules",
        "query": "unsupervised learning Hebbian neural network",
        "subreddits": "r/MachineLearning,r/artificial,r/deeplearning",
        "prob": 0.40,
    },
    {
        "id": "b653b3c3-459c-496c-9c28-ebb4b1cc22d9",
        "name": "Startup investment",
        "desc": "Evaluating and investing in startups",
        "query": "startup investment evaluation AI tool",
        "subreddits": "r/startups,r/investing,r/venturecapital",
        "prob": 0.08,
    },
    {
        "id": "c981a894-abd1-4dfb-aacc-9089497c2c85",
        "name": "לבדוק אם חברות (financial ratios similarity)",
        "desc": "Test whether companies with similar financial ratios behave similarly in the market",
        "query": "stock financial ratios similarity clustering analysis",
        "subreddits": "r/algotrading,r/stocks,r/investing",
        "prob": 0.10,
    },
    {
        "id": "b0cf29ee-92c2-4a7d-b37c-e057ce326068",
        "name": "Gamification",
        "desc": "Turn tasks into a game with points and rewards to boost personal productivity",
        "query": "gamification productivity tasks app",
        "subreddits": "r/productivity,r/selfimprovement,r/gamedesign",
        "prob": 0.20,
    },
    {
        "id": "78492d63-ec06-4db8-bde0-88a811159fba",
        "name": "השקעה לפי PE (PEAD trading)",
        "desc": "A systematic trading bot that exploits Post-Earnings Announcement Drift (PEAD)",
        "query": "PEAD post earnings announcement drift trading strategy",
        "subreddits": "r/algotrading,r/stocks,r/investing",
        "prob": 0.06,
    },
    {
        "id": "d4c91fb8-2171-47c5-b1c5-1f5021641c63",
        "name": "Connect music to heartbeat",
        "desc": "Music frequency that matches heartbeat for wellness/meditation",
        "query": "music binaural heartbeat brainwave entrainment app",
        "subreddits": "r/binaural,r/meditation,r/musicproduction",
        "prob": 0.10,
    },
    {
        "id": "cc74ca9a-43ae-43fc-8d68-9e7ce0cdcf64",
        "name": "Simulate parents",
        "desc": "Interactive AI avatars of real people — talk to a deceased parent using their recordings, or chat with Einstein/celebrities using Wikipedia as context",
        "query": "AI avatar deceased loved ones voice clone chatbot",
        "subreddits": "r/artificial,r/MachineLearning,r/Futurology",
        "prob": 0.10,
    },
    {
        "id": "32505a1b-5e01-810f-a451-cfbcecddd31d",
        "name": "slack-claude-bot",
        "desc": "A Slack bot that lets users chat with Claude directly in Slack, with per-thread conversation continuity",
        "query": "Slack AI chatbot Claude integration",
        "subreddits": "r/Slack,r/artificial,r/devtools",
        "prob": 0.40,
    },
    {
        "id": "6968eb11-bcc6-4c5d-b4de-6254a15532ed",
        "name": "Homework",
        "desc": "Homework help and tutoring tool",
        "query": "AI homework help tutoring tool students",
        "subreddits": "r/edtech,r/education,r/artificial",
        "prob": 0.08,
    },
    {
        "id": "b602c8e9-9e4e-4334-9938-d65baea51573",
        "name": "Construction Q&A",
        "desc": "Q&A tool for construction and building regulation questions",
        "query": "AI construction building regulations Q&A tool",
        "subreddits": "r/construction,r/architecture,r/artificial",
        "prob": 0.10,
    },
]

if __name__ == "__main__":
    for p in PROJECTS:
        try:
            process_project(p)
        except Exception as e:
            print(f"ERROR on {p['name']}: {e}")
    print("\n✅ Done")
