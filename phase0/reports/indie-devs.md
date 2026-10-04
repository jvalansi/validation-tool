# indie-devs pain points — ranked

Items scanned: 813 (reddit 663, hackernews 150); labelled as pains: 358.
Score = count × (1 + share with paying signal) × fit. Fit and clustering are Claude judgements, not measurements.

## 1. Social buying-intent lead finder — score 53.55
- Founders spend hours scanning Reddit, X, and LinkedIn for high-intent threads, competitor complaints, and buying signals. Keyword alerts and social listening tools are noisy, capped, or expensive, and posting replies risks spam flags. This cluster also covers the general 'can't get first users or distribution after launch' complaint.
- Items: 37 · paying signals: 26 · engagement: 12913 · who: developer 21, small_business 13, freelancer 2
- Fit 0.85: Self-serve, multi-tenant SaaS that runs on scraping plus LLM relevance scoring and needs almost no support. The market is crowded, and Reddit API terms are a risk.
- Product idea: Monitors subreddits, X, and HN for posts that match a product's pain points, scores buying intent with an LLM, and sends a daily digest with draft replies to approve.
- Evidence:
  - [AI made everyone a builder. It forgot to make more buyers.](https://www.reddit.com/r/SaaS/comments/1wk4rbe/ai_made_everyone_a_builder_it_forgot_to_make_more/) (reddit:r/SaaS, 2026-09-18) — "Anyone else spending more time finding users than building?"
  - [Launched my first SaaS yesterday. Woke up to 3 paying users and broo I’m actually shaking 😭 😭 😭 😭](https://www.reddit.com/r/SaaS/comments/1qx8bzd/launched_my_first_saas_yesterday_woke_up_to_3/) (reddit:r/SaaS, 2026-02-06) — "I'm a dev, not a marketer."
  - [Just hit $2K MRR after 8 months of grinding](https://www.reddit.com/r/SaaS/comments/1sl3mrh/just_hit_2k_mrr_after_8_months_of_grinding/) (reddit:r/SaaS, 2026-04-14) — "we are still struggling to get a reach and clients, can someone help us with that??"
  - [My SaaS just made $0.000 revenue in 60days after launch and I am so grateful, this feels so real 🎉🎉🎉](https://www.reddit.com/r/SaaS/comments/1wlg91y/my_saas_just_made_0000_revenue_in_60days_after/) (reddit:r/SaaS, 2026-09-20) — "We have tons of features but sadly no users"
  - [Vibe coding is about to kill 95% of you and it's not why you think.](https://www.reddit.com/r/SaaS/comments/1uklw96/vibe_coding_is_about_to_kill_95_of_you_and_its/) (reddit:r/SaaS, 2026-07-01) — "solo founders maxing out credit cards"

## 2. Pain-point mining and idea validation — score 51.2
- Builders can't find validated, unsaturated problems people will pay to solve. They read threads by hand, find competitors only after building, get flattering AI feedback, and lack honest peer critique and accountability.
- Items: 41 · paying signals: 23 · engagement: 5093 · who: developer 30, unknown 3, small_business 3
- Fit 0.8: Pure software that aggregates complaints by industry, finds competitors, and gives critical LLM scoring, which matches the builder's ML skills. Buyers are low-budget and churn quickly.
- Product idea: A searchable database of recurring pain points from communities, grouped by industry, with a competitor check and a blunt viability score for each idea.
- Evidence:
  - [How I used Claude to validate my idea in 10 minutes (Now at $2.3k MRR)](https://www.reddit.com/r/SaaS/comments/1lwlk57/how_i_used_claude_to_validate_my_idea_in_10/) (reddit:r/SaaS, 2025-07-10) — "Built two different projects. First one got exactly 3 signups. Second one never even made it past my localhost"
  - [I built 4 apps on ideas that AI told me were great. All 4 failed. The signals were fake](https://www.reddit.com/r/SaaS/comments/1tt29e6/i_built_4_apps_on_ideas_that_ai_told_me_were/) (reddit:r/SaaS, 2026-05-31) — "I wasted about a year of nights and weekends on it"
  - [How I validate ideas in 48 hours now](https://www.reddit.com/r/indiehackers/comments/1pxq7uz/how_i_validate_ideas_in_48_hours_now/) (reddit:r/indiehackers, 2025-12-28) — "Build MVP (2-3 weeks)... Usually silence"
  - [How do you come up with SaaS ideas that aren’t already saturated?](https://www.reddit.com/r/SaaS/comments/1nibh53/how_do_you_come_up_with_saas_ideas_that_arent/) (reddit:r/SaaS, 2025-09-16) — "I've tried idea lists, market research, and just building for myself"
  - [I uploaded 70 books to Amazon KDP in 5 years. Result: 0 sales.](https://www.reddit.com/r/microsaas/comments/1rayu8m/i_uploaded_70_books_to_amazon_kdp_in_5_years/) (reddit:r/microsaas, 2026-02-21) — "In total, I uploaded nearly 70 books/notebooks."

## 3. Developer and LLM-ops utilities — score 30.6
- Developers want a unified LLM gateway, prompt comparison and evals, agent cost control, JSON-API anomaly alerts, managed backups, .env versioning, UI component extraction, CRUD boilerplate, and syntax-aware diffs.
- Items: 33 · paying signals: 18 · engagement: 951 · who: developer 25, small_business 4, employee 3
- Fit 0.6: These match the builder's skills and are self-serve. The needs are fragmented, and open-source alternatives keep willingness to pay low.
- Product idea: A hosted prompt and eval workbench that runs prompt banks across providers, grades the results, and tracks cost for each prompt version.
- Evidence:
  - [Solo SaaS reached $25K MRR, 100% inbound, and mostly runs itself](https://www.reddit.com/r/microsaas/comments/1s4lpbi/solo_saas_reached_25k_mrr_100_inbound_and_mostly/) (reddit:r/microsaas, 2026-03-26) — "$25K MRR, 100% from inbound customers... we even got Ramp (a $32B company) as a customer... people avoid building this in-house"
  - [Finnnally!!! Hit 1,000 users after 4 months with 0 COST!!  process > hype， AMA](https://www.reddit.com/r/microsaas/comments/1qdmesr/finnnally_hit_1000_users_after_4_months_with_0/) (reddit:r/microsaas, 2026-01-15) — "tweaking prompts took forever"
  - [Ask HN: Would you pay $5 for a CRUD app?](https://news.ycombinator.com/item?id=21722317) (hackernews, 2019-12-06) — "I would pay about $5, to save a couple of days worth of work"
  - [Ask HN: Would you pay for instant devops help?](https://news.ycombinator.com/item?id=19329603) (hackernews, 2019-03-07) — "if I could just 'talk to a guy', who already knows it, for an hour or two, it would save multiples of those hours for me"
  - [All in one tool?](https://www.reddit.com/r/SaaS/comments/1e52lm6/all_in_one_tool/) (reddit:r/SaaS, 2024-07-16) — "after countless videos on YouTube I'm turning to Reddit"

## 4. Targeted prospect lists and personalized outreach — score 23.1
- Lead databases return poor-fit contacts, so founders build lists by hand, stitch together scrapers, LLMs, and CRMs through CSVs, warm up email domains, and get low reply rates. LinkedIn automation risks getting the account banned.
- Items: 23 · paying signals: 19 · engagement: 3154 · who: small_business 21, employee 1, freelancer 1
- Fit 0.55: Signal-based list building and personalization are buildable. Deliverability, LinkedIn terms-of-service risk, and a saturated market add support load and fragility.
- Product idea: Builds a prospect list from fine-grained criteria such as map listings, site quality, and job changes, then writes personalized first lines and exports to the user's sender.
- Evidence:
  - [I got 30 clients paying 2600$ on average thanks to this playbook](https://www.reddit.com/r/microsaas/comments/1j0w1ys/i_got_30_clients_paying_2600_on_average_thanks_to/) (reddit:r/microsaas, 2025-03-01) — "I got 30 clients paying 2600$ on average"
  - [The best tool to generate a list of highly targeted leads for B2B cold outreach](https://www.reddit.com/r/SaaS/comments/1c4jvhy/the_best_tool_to_generate_a_list_of_highly/) (reddit:r/SaaS, 2024-04-15) — "I tried Apollo, Zoominfo, and Cognisim, but 90% of what I find aren't the right fit... finding all my leads manually, but it is very tiring"
  - [How we're personalising cold emails at scale in 2026](https://www.reddit.com/r/SaaS/comments/1q80r0l/how_were_personalising_cold_emails_at_scale_in/) (reddit:r/SaaS, 2026-01-09) — "our team spent a lot of time & money refining this process"
  - [Built a simple tool that makes $3k/month doing one boring thing](https://www.reddit.com/r/microsaas/comments/1mx0dnf/built_a_simple_tool_that_makes_3kmonth_doing_one/) (reddit:r/microsaas, 2025-08-22) — "I charge $29/month for it... 127 paying customers"
  - [I vibe coded a LinkedIn outreach automation tool, and made $2k in the first month](https://www.reddit.com/r/microsaas/comments/1t34d5y/i_vibe_coded_a_linkedin_outreach_automation_tool/) (reddit:r/microsaas, 2026-05-04) — "made $2k in the first month"

## 5. Consumer info overload and job search — score 22.8
- Individuals struggle with long videos, bookmarks, news overload, note apps, personal finance tracking, and repetitive job applications and résumé tailoring.
- Items: 37 · paying signals: 20 · engagement: 3188 · who: unknown 13, employee 11, hobbyist 8
- Fit 0.4: Building it is easy, but consumer acquisition is expensive and churn is high. The pains are scattered and willingness to pay is low.
- Product idea: Tailors a résumé and cover letter to each matched remote role and tracks applications automatically.
- Evidence:
  - [We did itt ! 😭😭 4 paying users in one day](https://www.reddit.com/r/SaaS/comments/1t7szer/we_did_itt_4_paying_users_in_one_day/) (reddit:r/SaaS, 2026-05-09) — "4 paying users in one day"
  - [Ask HN: I would pay X for Y](https://news.ycombinator.com/item?id=15602081) (hackernews, 2017-11-01) — "I would pay $10 every 3 months for a highlevel review/changelog of the top Javascript frameworks"
  - [I'm building the opposite of Notion. It's a notes app where you can't customize anything.](https://www.reddit.com/r/indiehackers/comments/1r9zjq7/im_building_the_opposite_of_notion_its_a_notes/) (reddit:r/indiehackers, 2026-02-20) — "I'd be signing myself up for an hour of tinkering to build the "perfect" medicine tracker"
  - [I got into a bad habit with YouTube… so I built something to fix it (I can't code either!)](https://www.reddit.com/r/indiehackers/comments/1sweumr/i_got_into_a_bad_habit_with_youtube_so_i_built/) (reddit:r/indiehackers, 2026-04-26) — "30–40 minutes really adds up and began messing with my sleep"
  - [I built the opposite of Notion. It's a notes/second brain tool where you can't customize anything. It launches today!](https://www.reddit.com/r/indiehackers/comments/1rx5pfr/i_built_the_opposite_of_notion_its_a_notessecond/) (reddit:r/indiehackers, 2026-03-18) — "I'd be signing myself up for an hour of tinkering to build the "perfect" medicine tracker"

## 6. Faceless marketing video and ad creatives — score 19.8
- Founders who don't want to be on camera or lack design skills struggle to produce short-form videos, product demos, screen recordings, ad creatives, carousels, social posts, and app store screenshots.
- Items: 20 · paying signals: 13 · engagement: 5324 · who: developer 7, small_business 6, freelancer 3
- Fit 0.6: Generative media SaaS is self-serve, but compute costs are high, competition is heavy, and output quality is hard to make consistent.
- Product idea: Turns a product URL plus a screen recording into polished demo clips, short-form ads, and resized social variants in one step.
- Evidence:
  - [Finally! My First SaaS got acquired...🚀🚀🚀](https://www.reddit.com/r/microsaas/comments/1qlglwd/finally_my_first_saas_got_acquired/) (reddit:r/microsaas, 2026-01-24) — "more than 75+ people started signing up quickly in just a week. founders indie hackers marketers all saying they had the same pain"
  - [Drop your startup in the comments and i'll generate 3 ad creatives for free](https://www.reddit.com/r/indiehackers/comments/1od5tl5/drop_your_startup_in_the_comments_and_ill/) (reddit:r/indiehackers, 2025-10-22) — "With over 120 links shared"
  - [i hate managing twitter, linkedin, and a blog while coding. so i built an over-engineered voice memo app to do it for me.](https://www.reddit.com/r/indiehackers/comments/1sm23ml/i_hate_managing_twitter_linkedin_and_a_blog_while/) (reddit:r/indiehackers, 2026-04-15) — "context-switching between writing code and writing linkedin posts was killing my momentum"
  - [I was tired of manually creating App Store screenshots for 10+ languages, so I built an agent to do that!](https://www.reddit.com/r/indiehackers/comments/1tdwrfs/i_was_tired_of_manually_creating_app_store/) (reddit:r/indiehackers, 2026-05-15) — "updating screenshots every release was becoming insanely annoying once I started localizing apps"
  - [I'm a one person business and distribution was eating 3-4 hours a day. Here’s the simple way I fixed it and got my first sale.](https://www.reddit.com/r/indiehackers/comments/1u1skdy/im_a_one_person_business_and_distribution_was/) (reddit:r/indiehackers, 2026-06-10) — "distribution was eating 3-4 hours a day ... gave the videos that did ok to really small UGC creators for $20/video"

## 7. Security and production-readiness checks for AI-built apps — score 16.8
- Fast-shipped and AI-built apps leak secrets, break tenant isolation, have weak auth and webhook handling, attract .env probing, and fail silently on edge cases. Non-expert founders can't audit them.
- Items: 13 · paying signals: 8 · engagement: 5282 · who: developer 8, small_business 5
- Fit 0.8: An automated scanner run against a URL or repo is self-serve, scales well, and has growing demand. It must report findings and avoid becoming consulting work.
- Product idea: Point it at a deployed app or repo to get automated checks for exposed secrets, auth, tenant-isolation, and webhook issues, with copy-paste fixes.
- Evidence:
  - [Vibe coding is making us 10x faster but 100x dumber.](https://www.reddit.com/r/SaaS/comments/1rwa2ox/vibe_coding_is_making_us_10x_faster_but_100x/) (reddit:r/SaaS, 2026-03-17) — "I spent 4 hours "prompting" the AI to fix it"
  - [When attempting to scale their products 90% of Upwork SaaS Builds Fa](https://www.reddit.com/r/SaaS/comments/1kgng1a/when_attempting_to_scale_their_products_90_of/) (reddit:r/SaaS, 2025-05-07) — "The founder hired an individual freelancer at a low cost who delivered a functioning product before disappearing"
  - [Vulnerability exploiters](https://www.reddit.com/r/microsaas/comments/1s9c7bw/vulnerability_exploiters/) (reddit:r/microsaas, 2026-04-01) — "I have to rebuild lot of my data from scratch now"
  - [I’ve been doing pentests on a bunch of AI-built SaaS this year (probably ~50 by now), and I keep seeing the same stuff over and over.](https://www.reddit.com/r/microsaas/comments/1t3hy7q/ive_been_doing_pentests_on_a_bunch_of_aibuilt/) (reddit:r/microsaas, 2026-05-04) — "I run a small pentest firm... doing pentests on a bunch of AI-built SaaS this year (probably ~50 by now)"
  - [AI made code cheap to write, not cheap to verify!!!](https://www.reddit.com/r/indiehackers/comments/1vrbe6m/ai_made_code_cheap_to_write_not_cheap_to_verify/) (reddit:r/indiehackers, 2026-08-18) — "it's now "took me 3 days to verify it actually works in prod.""

## 8. SaaS, infra, and AI-API spend tracking — score 15.75
- Founders and small teams lose track of subscriptions, renewals, price increases, and infrastructure and AI API costs across vendors and projects. They can't tie AI spend to features or split costs between projects.
- Items: 11 · paying signals: 10 · engagement: 1410 · who: small_business 6, developer 2, employee 1
- Fit 0.75: Integrations with billing APIs plus alerting give low-touch self-serve SaaS, though there are many incumbents. Per-feature AI cost attribution is a sharper wedge.
- Product idea: An SDK and dashboard that tags LLM and infra spend by feature and project, with spike alerts and renewal reminders.
- Evidence:
  - [The CEO keeps asking me why our IT costs are so high and I don't know how to explain that software costs money](https://www.reddit.com/r/SaaS/comments/1pav2cx/the_ceo_keeps_asking_me_why_our_it_costs_are_so/) (reddit:r/SaaS, 2025-11-30) — "he'll approve a $30k purchase for new office furniture without blinking but then grill me about why we're spending $2k"
  - [I made $1000 from a "useless" app in a saturated market. Here's my journey](https://www.reddit.com/r/microsaas/comments/1pbwslo/i_made_1000_from_a_useless_app_in_a_saturated/) (reddit:r/microsaas, 2025-12-02) — "Today, I have 90+ paying customers."
  - [Why are so many people moving away from Supabase/Railway for production?](https://www.reddit.com/r/indiehackers/comments/1uq4bjv/why_are_so_many_people_moving_away_from/) (reddit:r/indiehackers, 2026-07-07) — "it gets harder to predict what next month's bill is going to look like, especially with usage-b[ased pricing]"
  - [Spent 30 mins on a free tool and it made me over 6k visitors and $500 in revenue](https://www.reddit.com/r/microsaas/comments/1pyg9zk/spent_30_mins_on_a_free_tool_and_it_made_me_over/) (reddit:r/microsaas, 2025-12-29) — "made about $500 in conversions for my main app"
  - [Who’s actually feeling the pain of AI API costs?](https://www.reddit.com/r/SaaS/comments/1srfdyk/whos_actually_feeling_the_pain_of_ai_api_costs/) (reddit:r/SaaS, 2026-04-21) — "our AI API bills have been creeping up every month"

## 9. Lightweight feedback, onboarding, and activation suite — score 14.95
- Small SaaS teams juggle five or six tools for feedback, feature requests, onboarding, popups, and churn analysis. They lose requests, can't tell why trials don't convert, and fight free-tier and trial abuse.
- Items: 16 · paying signals: 7 · engagement: 5403 · who: small_business 12, developer 3, employee 1
- Fit 0.65: One embeddable widget is self-serve and multi-tenant. The category is crowded, so it needs a sharp wedge such as close-the-loop notifications or trial-abuse detection.
- Product idea: One script tag that collects feature requests from all channels, tracks activation drop-off, and emails users automatically when their request ships.
- Evidence:
  - [Bootstrapped a tiny SaaS and finally sold (feels unreal)](https://www.reddit.com/r/SaaS/comments/1mn0eo9/bootstrapped_a_tiny_saas_and_finally_sold_feels/) (reddit:r/SaaS, 2025-08-11) — "charged $29/mo from day one... 283 paying"
  - [Shutting down our free tier tomorrow](https://www.reddit.com/r/SaaS/comments/1rxfb0n/shutting_down_our_free_tier_tomorrow/) (reddit:r/SaaS, 2026-03-18) — "Free users generate 60% of support tickets... Converting at 0.95%"
  - [Discovered my biggest customer has been sharing their login with 14 people at their company. Do I say something?](https://www.reddit.com/r/SaaS/comments/1pbiht1/discovered_my_biggest_customer_has_been_sharing/) (reddit:r/SaaS, 2025-12-01) — "That's $319/month I'm losing. $3,828/year from a single customer."
  - [Ask HN: Is there a tool / product that enables commenting on HTML elements?](https://news.ycombinator.com/item?id=32315035) (hackernews, 2022-08-02) — "I'm searching for a commercial product that enables commenting on HTML elements"
  - [Spent an hour trying to explain "Workspaces" to a founder who built the whole product](https://www.reddit.com/r/indiehackers/comments/1ond6in/spent_an_hour_trying_to_explain_workspaces_to_a/) (reddit:r/indiehackers, 2025-11-03) — "his support team gets asked "what's a Workspace" about 10 times a day"

## 10. Launch directory submission and tracking — score 14.0
- Founders submit to hundreds of startup and backlink directories by hand. They can't tell which directories are live or which bring traffic or SEO value, and automated submission gets flagged as spam.
- Items: 12 · paying signals: 8 · engagement: 2988 · who: developer 6, small_business 6
- Fit 0.7: A curated, scored directory database plus a form-filling assistant is easy to build and self-serve. Spam detection and a crowded, low-price market limit it.
- Product idea: A ranked, regularly verified directory list with domain-rating and traffic data, plus a browser extension that pre-fills submissions from one product profile.
- Evidence:
  - [I launched my first tool in April. Now I have over 1,000 users and $5K+ in revenue.](https://www.reddit.com/r/indiehackers/comments/1w12wnz/i_launched_my_first_tool_in_april_now_i_have_over/) (reddit:r/indiehackers, 2026-08-28) — "over 1,000 users and $5K+ in revenue"
  - [How to get your first 100 users (even if you suck at marketing)](https://www.reddit.com/r/SaaS/comments/1kc6wo7/how_to_get_your_first_100_users_even_if_you_suck/) (reddit:r/SaaS, 2025-05-01) — "Submit your product there. Manually. Or use a tool."
  - [I've manually submitted startups to 220+ directories. Only about 15 mattered.](https://www.reddit.com/r/indiehackers/comments/1vdlnb1/ive_manually_submitted_startups_to_220/) (reddit:r/indiehackers, 2026-08-02) — "we always do submission in curated and high authority relevant directories for our client Startup"
  - [It's Friday. Drop your link. 🚀](https://www.reddit.com/r/microsaas/comments/1pkqw6e/its_friday_drop_your_link/) (reddit:r/microsaas, 2025-12-12) — "hand-typing submissions for 300+ sites like G2 and BetaList took me 40+ hours"
  - [Its Wednesday - what are you building? Lets promote each other](https://www.reddit.com/r/microsaas/comments/1pj2xtf/its_wednesday_what_are_you_building_lets_promote/) (reddit:r/microsaas, 2025-12-10) — "Submitting to directories takes forever."

## 11. Table and data extraction from PDFs and images — score 13.5
- People retype bank statements, PDF and screenshot tables, lab biomarkers, and event flyers into spreadsheets or calendars, and clean broken CSVs by hand.
- Items: 12 · paying signals: 6 · engagement: 1902 · who: small_business 4, unknown 3, employee 2
- Fit 0.75: Vision-LLM extraction is a natural ML fit and self-serve with flat support. It is horizontal and price-competitive, so pricing power is weak.
- Product idea: Drop in a PDF, screenshot, or CSV and get clean, validated spreadsheet or calendar output, with presets for bank statements and lab reports.
- Evidence:
  - [Software devs don’t realize the magic they wield.](https://www.reddit.com/r/SaaS/comments/17hxbgq/software_devs_dont_realize_the_magic_they_wield/) (reddit:r/SaaS, 2023-10-27) — "they thought they'd spend a month manually entering data. They thought they'd have to dedicate half the team to it."
  - [🥗 $16K/Month With a Simple Web Tool](https://www.reddit.com/r/SaaS/comments/1jb81an/16kmonth_with_a_simple_web_tool/) (reddit:r/SaaS, 2025-03-14) — "Revenue: $16,000/month (MRR)... accountants were drowning in manual data entry"
  - [I built an app to solve my own problem. Here's what happened after a YouTuber picked it up.](https://www.reddit.com/r/indiehackers/comments/1szqzkc/i_built_an_app_to_solve_my_own_problem_heres_what/) (reddit:r/indiehackers, 2026-04-30) — "I got tired of manually adding everything to my calendar"
  - [Made my first dollar with an app vibe-coded in 2 days](https://www.reddit.com/r/indiehackers/comments/1mkrho3/made_my_first_dollar_with_an_app_vibecoded_in_2/) (reddit:r/indiehackers, 2025-08-08) — "Fifteen minutes here, twenty there, it adds up."
  - [CHATGPT REFERRED SOMEONE TO MY TINY SAAS AND THEY ACTUALLY OPENED IT 😭🥹](https://www.reddit.com/r/microsaas/comments/1wwr32m/chatgpt_referred_someone_to_my_tiny_saas_and_they/) (reddit:r/microsaas, 2026-10-03) — "I currently have 2 paying customers."

## 12. Automated SEO content and upkeep — score 9.1
- Small teams don't have time for keyword research, blog posts, 'X vs Y' comparison pages, internal linking, technical SEO setup, or content refreshes. SEO tools are too expensive for occasional use.
- Items: 9 · paying signals: 4 · engagement: 605 · who: small_business 7, developer 2
- Fit 0.7: LLM-driven content pipelines are self-serve and automatable. The space is crowded, and new low-authority domains get weak results.
- Product idea: Connects to Search Console and the site, then auto-generates and refreshes comparison pages and posts, fixes technical SEO issues, and reports rankings.
- Evidence:
  - [Everything I did differently to go from $0 in 3 years to $200 in 2 weeks](https://www.reddit.com/r/SaaS/comments/1gvkk1n/everything_i_did_differently_to_go_from_0_in_3/) (reddit:r/SaaS, 2024-11-20) — "$200 in 2 weeks"
  - [Built autonomous agents that do full marketing tasks end to end.](https://www.reddit.com/r/indiehackers/comments/1mwdvlf/built_autonomous_agents_that_do_full_marketing/) (reddit:r/indiehackers, 2025-08-21) — "Onboarded 15 paying businesses into the closed beta"
  - [I created a SEO AI agent, web views has increased by 7593%](https://www.reddit.com/r/SaaS/comments/1re9a8c/i_created_a_seo_ai_agent_web_views_has_increased/) (reddit:r/SaaS, 2026-02-25) — "spent a few weeks setting up an AI agent to basically act as an "SEO operator.""
  - [Ask HN: Is there a tool to track search rankings in Google Play?](https://news.ycombinator.com/item?id=4288065) (hackernews, 2012-07-24) — "this is getting tedious and I'd gladly pay a small amount for an app to do it for me"
  - [what I actually did in the first 10 days to make Google notice my product](https://www.reddit.com/r/indiehackers/comments/1rjtja0/what_i_actually_did_in_the_first_10_days_to_make/) (reddit:r/indiehackers, 2026-03-03)

## 13. AI assistant visibility (GEO) — score 6.8
- Brands can't see whether or how ChatGPT, Perplexity, and AI agents mention or recommend them compared with competitors, and don't know how to improve it. The cluster also covers exposing products to agents through APIs or MCP.
- Items: 5 · paying signals: 3 · engagement: 2998 · who: small_business 5
- Fit 0.85: A multi-tenant tracker that runs scheduled prompts across LLM APIs fits an ML engineer well and needs little support. It is a new category with growing demand.
- Product idea: Runs buyer-style prompts daily across major LLMs, tracks mention share against competitors, and suggests content fixes.
- Evidence:
  - [I accidentally discovered that ChatGPT was sending me users. Then I figured out why.](https://www.reddit.com/r/SaaS/comments/1tsam1y/i_accidentally_discovered_that_chatgpt_was/) (reddit:r/SaaS, 2026-05-30) — "ChatGPT is responsible for roughly half of all my signups"
  - [The single biggest shift coming to SaaS](https://www.reddit.com/r/SaaS/comments/1w5qg2s/the_single_biggest_shift_coming_to_saas/) (reddit:r/SaaS, 2026-09-02) — "they'll pick a competitor"
  - [Suggestions on how to do Chatgpt seo](https://www.reddit.com/r/SaaS/comments/1kmqq6o/suggestions_on_how_to_do_chatgpt_seo/) (reddit:r/SaaS, 2025-05-14) — "is there a tool that can give me more actionable insights on how to improve this?"
  - [I copied an existing startup idea, launched my own SaaS 2 days ago, and now I’m 😭](https://www.reddit.com/r/microsaas/comments/1pmxw34/i_copied_an_existing_startup_idea_launched_my_own/) (reddit:r/microsaas, 2025-12-15)
  - [I am a solo entrepreneur , learnt one new thing . What I found changed how I look at websites . Want to share with all indiehackers.](https://www.reddit.com/r/indiehackers/comments/1sl7xpt/i_am_a_solo_entrepreneur_learnt_one_new_thing/) (reddit:r/indiehackers, 2026-04-14)

## 14. Vertical small-business operations software — score 0.0
- Field service, trades, hotels, gyms, manufacturers, event planners, and local shops run scheduling, dispatch, inventory, reordering, WhatsApp lead replies, and invoicing on whiteboards and spreadsheets.
- Items: 18 · paying signals: 14 · engagement: 3472 · who: small_business 17, employee 1
- Fit 0.35: These buyers are non-technical, usually need onboarding and sales calls, and need different software for each vertical. That conflicts with flat support hours and 15 hours a week. · **excluded: service_heavy**
- Product idea: A WhatsApp AI receptionist that answers FAQs, qualifies leads, and books appointments for local service businesses.
- Evidence:
  - [After 8 failed side projects, I finally get why most indie hackers stay broke](https://www.reddit.com/r/indiehackers/comments/1o50cai/after_8_failed_side_projects_i_finally_get_why/) (reddit:r/indiehackers, 2025-10-12) — "They have problems worth *actual* money"
  - [Just crossed ₹5L revenue, 5 months after launching my Saas product.](https://www.reddit.com/r/SaaS/comments/1vn9njc/just_crossed_5l_revenue_5_months_after_launching/) (reddit:r/SaaS, 2026-08-13) — "Just crossed ₹5L revenue, 5 months after launching"
  - [talked to 12 micro saas founders making $5k to $30k/month. none of them found their idea by brainstorming. here's what they actually did](https://www.reddit.com/r/microsaas/comments/1ri2rsz/talked_to_12_micro_saas_founders_making_5k_to/) (reddit:r/microsaas, 2026-03-01) — "scheduling tool for trade contractors, $14k/month"
  - [I built software to solve a problem in my contracting business. It works. How do I turn it into a SaaS company?](https://www.reddit.com/r/SaaS/comments/1w8efcy/i_built_software_to_solve_a_problem_in_my/) (reddit:r/SaaS, 2026-09-05) — "For years I used a combination of Jobber, Pruvan Direct, QuickBooks and other processes to handle different pieces of this. None of them really connected the entire workflow"
  - [I turned my gym membership into a mini call center business](https://www.reddit.com/r/indiehackers/comments/1p6z4w2/i_turned_my_gym_membership_into_a_mini_call/) (reddit:r/indiehackers, 2025-11-26) — "if my receptionist starts calling this list, he'll quit"

## 15. Payments, payroll, legal, and compliance — score 0.0
- This cluster covers international contractor payroll, Stripe freezes and unsupported countries, chargebacks, founder vesting agreements, IP protection, HIPAA, IT compliance evidence, and investor risk tools.
- Items: 13 · paying signals: 13 · engagement: 7060 · who: small_business 7, freelancer 2, developer 2
- Fit 0.15: Most of these items are regulated financial, legal, or medical work or need licensed expertise and high-touch support. · **excluded: regulated**
- Product idea: Automatically collects evidence for IT compliance audits from cloud and SaaS APIs.
- Evidence:
  - [New accountant literally laughed when he saw our payroll costs](https://www.reddit.com/r/SaaS/comments/1pisnbk/new_accountant_literally_laughed_when_he_saw_our/) (reddit:r/SaaS, 2025-12-10) — "paying around $6,600/month... you're paying 3x market rate... cost the company like $30k"
  - [Co-founder left after 14 months. No vesting agreement. He walked with 40% equity and zero obligation.](https://www.reddit.com/r/SaaS/comments/1s5gsxj/cofounder_left_after_14_months_no_vesting/) (reddit:r/SaaS, 2026-03-27) — "he wants $80K"
  - [Company copied my code after refusing to pay for a license. I know because their site is sending data to MY Hotjar account. What would you do?](https://www.reddit.com/r/SaaS/comments/1vltxz0/company_copied_my_code_after_refusing_to_pay_for/) (reddit:r/SaaS, 2026-08-11) — "I rebuilt it from scratch in my own time... never got paid"
  - [Here's how to waste 250K in building an healthcare app](https://www.reddit.com/r/SaaS/comments/1oifxh3/heres_how_to_waste_250k_in_building_an_healthcare/) (reddit:r/SaaS, 2025-10-28) — "Here's how to waste 250K in building an healthcare app"
  - [First real money ever made from my SaaS!!](https://www.reddit.com/r/SaaS/comments/1v950sz/first_real_money_ever_made_from_my_saas/) (reddit:r/SaaS, 2026-07-28) — "Since Stripe isn't supported in my country, and I'm not a full business yet, I just went with Paddle"
