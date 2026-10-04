# data-analytics pain points — ranked

Items scanned: 898 (reddit 814, hackernews 84); labelled as pains: 410.
Score = count × (1 + share with paying signal) × fit. Fit and clustering are Claude judgements, not measurements.

## 1. Recurring report and deck generation from many sources — score 59.2
- Finance and ops staff pull from QBO, HubSpot, ERP exports and spreadsheets into Excel and PowerPoint every month, fixing broken links and formatting, and writing board narratives by hand.
- Items: 41 · paying signals: 33 · engagement: 5959 · who: employee 28, small_business 7, enterprise 4
- Fit 0.8: Templated, repeatable self-serve product with clear time savings; SMB finance buyers sign up without demos; AI agents can build connectors and slide rendering.
- Product idea: Connect QuickBooks/HubSpot/Sheets once, and get the monthly KPI deck and Excel pack auto-refreshed into your own PowerPoint template with an AI-drafted commentary.
- Evidence:
  - [What’s the Excel macro you’ve written that saved you hours?](https://www.reddit.com/r/excel/comments/1m9p7ph/whats_the_excel_macro_youve_written_that_saved/) (reddit:r/excel, 2025-07-26) — "it saves me a ton of time every week"
  - [Rejoice with me because no one in my life understands!](https://www.reddit.com/r/excel/comments/tkg0m0/rejoice_with_me_because_no_one_in_my_life/) (reddit:r/excel, 2022-03-22) — "I don't have to enter my invoices twice"
  - [Please read this if you are thinking of becoming data analyst...](https://www.reddit.com/r/analytics/comments/1oj4j9r/please_read_this_if_you_are_thinking_of_becoming/) (reddit:r/analytics, 2025-10-29) — "So much of my workload is QAing spread[sheets]"
  - [Stop stealing my teams work..](https://www.reddit.com/r/dataengineering/comments/1gugtv6/stop_stealing_my_teams_work/) (reddit:r/dataengineering, 2024-11-18) — "extremely time intensive... the reason they have a huge backlog"
  - [I've used excel at minimum capacity for many years and I'm just now learning what all it can do](https://www.reddit.com/r/excel/comments/1cuylwl/ive_used_excel_at_minimum_capacity_for_many_years/) (reddit:r/excel, 2024-05-18) — "my work may need a couple rounds of drafts before it's more than a kludged tog"

## 2. Messy CSV/Excel file ingestion into a fixed schema — score 45.9
- Client and partner spreadsheets arrive with inconsistent columns, header rows, merged cells, dates and formats; teams hand-map, merge and clean recurring files before loading to a database.
- Items: 32 · paying signals: 22 · engagement: 7164 · who: employee 19, small_business 7, developer 2
- Fit 0.85: Well-bounded self-serve workflow, LLM column mapping is a strong lever, recurring usage, no sales calls needed for SMB buyers.
- Product idea: Upload-or-email inbox that AI-maps any messy spreadsheet to your saved schema, remembers the mapping, validates, dedupes and loads to Postgres/Sheets/warehouse.
- Evidence:
  - [I legitimately feel like I’ve wasted years of my life not knowing about Power Query.](https://www.reddit.com/r/excel/comments/1pgkdwm/i_legitimately_feel_like_ive_wasted_years_of_my/) (reddit:r/excel, 2025-12-07) — "It took me about 2 hours every time."
  - [What’s the most underrated Excel feature you’ve only recently started using?](https://www.reddit.com/r/excel/comments/1o7czni/whats_the_most_underrated_excel_feature_youve/) (reddit:r/excel, 2025-10-15) — "I used to manually clean and merge data every week until I realized I could automate 90% of it"
  - [That 5-minute task in Excel](https://www.reddit.com/r/excel/comments/1tioz6s/that_5minute_task_in_excel/) (reddit:r/excel, 2026-05-20) — "This will be a quick 5-minute Excel task... 2 hours later"
  - [I've been playing with Power Query for a week and I can't figure out how I survived prior to this.](https://www.reddit.com/r/excel/comments/jd7yct/ive_been_playing_with_power_query_for_a_week_and/) (reddit:r/excel, 2020-10-18) — "There's a lot of room for error on their side while populating"
  - [Is automation in excel possible?](https://www.reddit.com/r/excel/comments/1iz453f/is_automation_in_excel_possible/) (reddit:r/excel, 2025-02-27) — "she wants this process to be automate so we can spent time on other thing"

## 3. Repetitive spreadsheet reshaping, cleaning and enrichment — score 32.0
- Users hand-reshape wide/long data, split reports per location, standardize vendor names, categorize products or job titles, look up row data on the web, and extract PDF/image tables.
- Items: 21 · paying signals: 19 · engagement: 1542 · who: employee 14, unknown 4, small_business 3
- Fit 0.8: LLM-powered row-level transforms are easy to productize as a self-serve add-in or web app with usage pricing and minimal support.
- Product idea: Sheets/Excel add-in where you describe a transform or categorization in plain English and it applies it to every row and saves it as a reusable recipe.
- Evidence:
  - [My first python code 1500 lines to automate my daily boring task.](https://www.reddit.com/r/analytics/comments/1jdck8e/my_first_python_code_1500_lines_to_automate_my/) (reddit:r/analytics, 2025-03-17) — "1500 lines to automate my daily boring task"
  - [12 year analyst feeling like a dinosaur. Need advice on moving away from massive flat files without forcing Power BI on my team.](https://www.reddit.com/r/excel/comments/1r6vv5x/12_year_analyst_feeling_like_a_dinosaur_need/) (reddit:r/excel, 2026-02-17) — "I've basically been surviving on VLOOKUPs and brute force ever since."
  - [Senior Data Analyst](https://www.reddit.com/r/analytics/comments/1wi8a3u/senior_data_analyst/) (reddit:r/analytics, 2026-09-16) — "I was told that all analysis work is done within Excel."
  - [All the noteable BI bs I dealt with this week](https://www.reddit.com/r/BusinessIntelligence/comments/1o9e8kv/all_the_noteable_bi_bs_i_dealt_with_this_week/) (reddit:r/BusinessIntelligence, 2025-10-17) — "We have 18,000 food items but no categorization... Categorizing them has been on backburner"
  - [Is there anything that's ONLY possible with pivot tables and not with formulas?](https://www.reddit.com/r/excel/comments/6p8c5p/is_there_anything_thats_only_possible_with_pivot/) (reddit:r/excel, 2017-07-24) — "I'd rather take the extra 10 minutes to setup the helper columns"

## 4. Ad-hoc data requests, unused dashboards and untrusted AI answers — score 29.15
- Analysts drown in quick-number requests and pivot asks; dashboards go unused; NL-to-SQL/AI chatbots fabricate numbers or fail on real schemas; SMB owners want answers pushed in plain English.
- Items: 32 · paying signals: 21 · engagement: 5510 · who: employee 15, enterprise 8, small_business 5
- Fit 0.55: Software-only and in demand, but accuracy/trust is the core hard problem and the space is very crowded with funded competitors.
- Product idea: Slack bot that answers data questions only from verified saved queries/metrics, shows the SQL, and logs which dashboards and answers actually get used.
- Evidence:
  - [can someone explain why users ask for dashboards they literally never open?](https://www.reddit.com/r/BusinessIntelligence/comments/1p9od0u/can_someone_explain_why_users_ask_for_dashboards/) (reddit:r/BusinessIntelligence, 2025-11-29) — "this one manager begged me for months to make him this super important dashboard... guess how many times he opened it? two. two times. In four months."
  - [If I build one more "urgent" dashboard that gets zero views, I’m going to lose my mind.](https://www.reddit.com/r/analytics/comments/1ra18vt/if_i_build_one_more_urgent_dashboard_that_gets/) (reddit:r/analytics, 2026-02-20) — "I drop everything, pivot, clean the messy data, build the visualizations... Two weeks later... ASKING FOR THE SAME THING"
  - [Everyone is an analyst now](https://www.reddit.com/r/analytics/comments/1qqd9kr/everyone_is_an_analyst_now/) (reddit:r/analytics, 2026-01-29) — "spending so many hours thinking about how it can give all 4000 employees Power BI access"
  - [DON’T BE ME !!!!!!!](https://www.reddit.com/r/dataengineering/comments/1ou0igf/dont_be_me/) (reddit:r/dataengineering, 2025-11-11) — "spent weeks perfecting data models, custom DAX, and a BI dashboard ... the client didn't use half of it"
  - [Anyone else seeing fewer dashboard requests this year?](https://www.reddit.com/r/BusinessIntelligence/comments/1qulihh/anyone_else_seeing_fewer_dashboard_requests_this/) (reddit:r/BusinessIntelligence, 2026-02-03) — "They don't want to log into a portal, find the right tab, filter five times just to see if sales are up."

## 5. Pipeline breakage, schema drift and data quality alerts — score 28.0
- Pipelines fail silently or break on upstream schema/business-logic changes; testing is manual row-count eyeballing; engineers act as firefighting/retry operators with no contracts, lineage or anomaly alerting.
- Items: 24 · paying signals: 16 · engagement: 5383 · who: employee 17, enterprise 5, small_business 1
- Fit 0.7: Pure multi-tenant SaaS connecting to warehouses read-only; self-serve setup possible, though crowded (Monte Carlo, Elementary, dbt tests) and some adoption resistance noted.
- Product idea: Zero-config warehouse monitor that auto-learns volume/null/schema baselines per table and alerts on Slack with the upstream change that likely caused it.
- Evidence:
  - [Vibe coded dashboard failing on a Friday](https://www.reddit.com/r/dataengineering/comments/1uhidmb/vibe_coded_dashboard_failing_on_a_friday/) (reddit:r/dataengineering, 2026-06-28) — "got pinged at the end of the day Friday ... now im taking over the dashboard and setting up a proper pipeline"
  - [My “small data” pipeline checklist that saved me from building a fake-big-data mess](https://www.reddit.com/r/dataengineering/comments/1ppuky6/my_small_data_pipeline_checklist_that_saved_me/) (reddit:r/dataengineering, 2025-12-18) — "spend my life debugging glue"
  - [Most data engineers would be unemployed if pipelines stopped breaking](https://www.reddit.com/r/dataengineering/comments/1pty9p3/most_data_engineers_would_be_unemployed_if/) (reddit:r/dataengineering, 2025-12-23) — "A scary amount of our job is being the human retry button"
  - [Data engineers who are not building LLM to SQL. What cool projects are you actually working on?](https://www.reddit.com/r/dataengineering/comments/1p1y34k/data_engineers_who_are_not_building_llm_to_sql/) (reddit:r/dataengineering, 2025-11-20) — "duct taping pipelines, fixing bad schemas, and begging product teams to stop shipping breaking changes on Fridays"
  - [Unpopular Opinion: Data Quality is a product management problem, not an engineering one.](https://www.reddit.com/r/dataengineering/comments/1opz0ve/unpopular_opinion_data_quality_is_a_product/) (reddit:r/dataengineering, 2025-11-06) — "We spend countless hours building data quality frameworks, setting up Great Expectations, and writing custom DBT tests"

## 6. Spreadsheet error auditing, documentation and diffing — score 28.0
- Business-critical workbooks hide broken lookups, auto-conversion corruption, slow volatile formulas and unreadable logic only one person understands; no diffing, versioning or PII checks.
- Items: 21 · paying signals: 14 · engagement: 6921 · who: employee 10, enterprise 6, unknown 2
- Fit 0.8: File-in/report-out analysis is self-serve, scalable and well suited to LLM explanation; buyers are individual analysts with low support needs.
- Product idea: Upload a workbook to get an error/risk audit, plain-English documentation of every sheet and formula, slowdown hotspots, and cell-level diff against prior versions.
- Evidence:
  - [Excel saved my job](https://www.reddit.com/r/excel/comments/1v83bcl/excel_saved_my_job/) (reddit:r/excel, 2026-07-27) — "my workbooks were too engrained into our operations and I was the only one who knew how to maintain them"
  - [I hate how Excel removes leading zeroes](https://www.reddit.com/r/excel/comments/1wthj0w/i_hate_how_excel_removes_leading_zeroes/) (reddit:r/excel, 2026-09-29) — "it's impossible to ever to VLOOKUPS with data where you had to manually formulate leading zeroes"
  - [What's the "Excel Incident" at your job that people still talk about?](https://www.reddit.com/r/excel/comments/1mznt68/whats_the_excel_incident_at_your_job_that_people/) (reddit:r/excel, 2025-08-25) — "I had to spend the next 4 hours manually reconstructing data from emailed spreadsheets and PDF reports"
  - [I taught my supervisor 2 simple things in excel that are important for everyone to know](https://www.reddit.com/r/excel/comments/gti4gh/i_taught_my_supervisor_2_simple_things_in_excel/) (reddit:r/excel, 2020-05-30) — "only one person actually understands and everybody else assumes someone else is correct"
  - [The $6 Billion Typo: What’s the most critical spreadsheet error you’ve encountered?](https://www.reddit.com/r/excel/comments/1ps86yh/the_6_billion_typo_whats_the_most_critical/) (reddit:r/excel, 2025-12-21) — "The $6 Billion Typo"

## 7. Conflicting metrics and undocumented data stacks — score 24.6
- Same metric differs across dashboards; no data dictionary, lineage or semantic layer; new hires reverse-engineer thousands of lines of SQL and inherited BI reports from tribal knowledge.
- Items: 26 · paying signals: 15 · engagement: 7422 · who: enterprise 14, employee 12
- Fit 0.6: LLMs can auto-generate docs and metric catalogs from warehouse/dbt/BI metadata, but org-level adoption and integration breadth make it harder solo.
- Product idea: AI that crawls your warehouse, dbt and BI tools to auto-build a searchable data dictionary and flags metrics defined differently across dashboards.
- Evidence:
  - [Semantic layer](https://www.reddit.com/r/dataengineering/comments/1trnima/semantic_layer/) (reddit:r/dataengineering, 2026-05-30) — "Documenting field and metric definitions which also evolve will take a long time, how is this being done at scale ?"
  - [The biggest data problem I keep running into isn't dirty data. It's teams defining the same metric differently.](https://www.reddit.com/r/BusinessIntelligence/comments/1s077q9/the_biggest_data_problem_i_keep_running_into_isnt/) (reddit:r/BusinessIntelligence, 2026-03-22) — "Recently got brought in to fix a client's data model... This wasn't some edge case. I've seen this play out over and over with different clients"
  - [How do you handle increasing stress?](https://www.reddit.com/r/dataengineering/comments/10rudcp/how_do_you_handle_increasing_stress/) (reddit:r/dataengineering, 2023-02-02) — "set back in some instances nearly two years and I'm working 14-16 hour days trying to rebuild things"
  - [8 months into analytics at a FAANG-level company and I feel like I’m drowning ,Is this normal?](https://www.reddit.com/r/analytics/comments/1rs25j3/8_months_into_analytics_at_a_faanglevel_company/) (reddit:r/analytics, 2026-03-12) — "Tight deadlines + pressure meant I kept relying on internal AI tools just to survive"
  - [Anthropic says agentic analytics accuracy drifts 95% → 65% in a month without maintenance. How is your team keeping context fresh?](https://www.reddit.com/r/BusinessIntelligence/comments/1txaamo/anthropic_says_agentic_analytics_accuracy_drifts/) (reddit:r/BusinessIntelligence, 2026-06-05) — "Without active maintenance, it drifts back to 65% in a single month."

## 8. Lightweight scheduled API-to-table ingestion — score 24.0
- Analysts and small teams need to poll bespoke REST APIs, flatten nested JSON and schedule scripts/notebooks daily, but managed connectors skip long-tail APIs and Airflow/managed orchestration is too complex or expensive.
- Items: 23 · paying signals: 9 · engagement: 1633 · who: employee 11, developer 6, small_business 3
- Fit 0.75: Serverless multi-tenant runner with AI-generated connectors fits the profile; competition from Fivetran/Airbyte/cron but long-tail and pricing gaps are real.
- Product idea: Paste an API URL or notebook, get an AI-built connector that flattens nested JSON into relational tables and runs on a cheap hosted schedule with upserts.
- Evidence:
  - [dagster price increase 10x insane , don't ever use them](https://www.reddit.com/r/dataengineering/comments/1tv5evp/dagster_price_increase_10x_insane_dont_ever_use/) (reddit:r/dataengineering, 2026-06-02) — "went from $10, $20, $50, now $500+ ... now i'm back to 30 bucks a month"
  - [Best way to automatically pull data from an API everyday](https://www.reddit.com/r/dataengineering/comments/1df4z7n/best_way_to_automatically_pull_data_from_an_api/) (reddit:r/dataengineering, 2024-06-13) — "I don't want to run this code manually everyday."
  - [How much would you charge monthly to own a basic ETL in maintenance mode as a consultant?](https://www.reddit.com/r/dataengineering/comments/1gvirwf/how_much_would_you_charge_monthly_to_own_a_basic/) (reddit:r/dataengineering, 2024-11-20) — "Airflow deployment costs me like 50 bucks per month"
  - [Learning APIs as BI Analyst](https://www.reddit.com/r/BusinessIntelligence/comments/evcn00/learning_apis_as_bi_analyst/) (reddit:r/BusinessIntelligence, 2020-01-28) — "without the need to get assistance from programmers"
  - [Would you be interested in a detailed post on building Automated analytics for Salesforce.com?](https://www.reddit.com/r/BusinessIntelligence/comments/6rbio6/would_you_be_interested_in_a_detailed_post_on/) (reddit:r/BusinessIntelligence, 2017-08-03) — "some are downloading it manually"

## 9. Affordable lightweight BI, sharing and embedding — score 21.6
- Small businesses and SaaS builders can't easily share a sheet-based dashboard online/mobile or embed secure multi-tenant dashboards; incumbents have per-seat pricing, sales-gated pricing and weak chart types.
- Items: 24 · paying signals: 12 · engagement: 2462 · who: employee 9, small_business 5, enterprise 4
- Fit 0.6: Self-serve multi-tenant SaaS with transparent pricing is a stated buyer wish, but BI is crowded (Metabase, Looker Studio, Preset).
- Product idea: Turn a Google Sheet or Postgres query into a login-protected, mobile-friendly, embeddable dashboard with row-level tenant filtering and public pricing.
- Evidence:
  - [Tableau is horrible.](https://www.reddit.com/r/analytics/comments/1u41h8i/tableau_is_horrible/) (reddit:r/analytics, 2026-06-12) — "Tableau is charging about $700-$500 per creator license"
  - [Looking for Tableau alternatives](https://www.reddit.com/r/BusinessIntelligence/comments/1ut1kqp/looking_for_tableau_alternatives/) (reddit:r/BusinessIntelligence, 2026-07-10) — "license per user, not so cheap"
  - [I refuse to book a demo before signing up for analytics services.](https://www.reddit.com/r/BusinessIntelligence/comments/1ss3z98/i_refuse_to_book_a_demo_before_signing_up_for/) (reddit:r/BusinessIntelligence, 2026-04-21) — "I have purchasing authority. A corporate credit card. A goal... You want our money."
  - [Is there a online class that teaches pivot tables?](https://www.reddit.com/r/excel/comments/7tfq9c/is_there_a_online_class_that_teaches_pivot_tables/) (reddit:r/excel, 2018-01-27) — "To build this report took me 15 minutes total. I tried to have a percentage column in a pivot table for 3 hours"
  - [Which tool can I use to embed a dashboard to our website while keeping the underlying data secure and not accessible?](https://www.reddit.com/r/BusinessIntelligence/comments/gdz5ii/which_tool_can_i_use_to_embed_a_dashboard_to_our/) (reddit:r/BusinessIntelligence, 2020-05-05) — "it doesn't seem to be able to do that (at a reasonable cost)"

## 10. Outgrown spreadsheets used as databases and data-entry apps — score 13.5
- Teams run inventory, fleet, loyalty, time tracking, records and write-back workflows in sprawling Excel tabs and need a validated no-code data-entry front end on a real database.
- Items: 20 · paying signals: 10 · engagement: 2446 · who: employee 7, small_business 7, developer 2
- Fit 0.45: Software-only, but Airtable/Smartsheet/Glide dominate and vertical variants fragment demand, so differentiation and distribution are hard.
- Product idea: Import a messy workbook and get an AI-generated validated database plus mobile entry forms that still export back to Excel.
- Evidence:
  - [I helped my girlfriend improve her invoices in Excel and it blew her mind](https://www.reddit.com/r/analytics/comments/1qyr7qc/i_helped_my_girlfriend_improve_her_invoices_in/) (reddit:r/analytics, 2026-02-07) — "it was taking her hours to create each invoice"
  - [Excel file with hundreds of tabs](https://www.reddit.com/r/excel/comments/1onh11l/excel_file_with_hundreds_of_tabs/) (reddit:r/excel, 2025-11-03) — "there are hundreds and hundreds of tabs on an excel file for each of my 3 coworkers"
  - [I can write code to fix this. I should not have to write code to fix this.](https://www.reddit.com/r/dataengineering/comments/1wdxacc/i_can_write_code_to_fix_this_i_should_not_have_to/) (reddit:r/dataengineering, 2026-09-12) — "So clunky ass VBA it is."
  - [Google sheets “Database”](https://www.reddit.com/r/dataengineering/comments/1paby5v/google_sheets_database/) (reddit:r/dataengineering, 2025-11-30) — "reduce a lot of manual work"
  - [What do you think about Excel as a UI ?](https://www.reddit.com/r/excel/comments/1fkijdl/what_do_you_think_about_excel_as_a_ui/) (reddit:r/excel, 2024-09-19) — "if a client asks to interact with data ... then my first choice is always Excel"

## 11. Marketing attribution and multi-site web analytics — score 12.6
- GA4 is confusing and laggy, multi-site comparisons and UTM hygiene are manual, last-click attribution misallocates budget, and AI/LLM referral traffic can't be attributed.
- Items: 13 · paying signals: 8 · engagement: 1043 · who: small_business 6, employee 4, developer 1
- Fit 0.6: Self-serve SaaS on top of GA4/ad APIs fits, but attribution accuracy claims and API dependency limit defensibility.
- Product idea: One dashboard over all your GA4 properties with UTM cleanup, AI-referral traffic tracking and plain-English weekly change explanations.
- Evidence:
  - [My department was blown away I know excel](https://www.reddit.com/r/excel/comments/1qelc6z/my_department_was_blown_away_i_know_excel/) (reddit:r/excel, 2026-01-16) — "We have a lot of useful data but no one ever looks at it the right way"
  - [Last-click attribution is marketing's flat earth theory. Change my mind.](https://www.reddit.com/r/analytics/comments/1oetqwx/lastclick_attribution_is_marketings_flat_earth/) (reddit:r/analytics, 2025-10-24) — "Their Google Search conversions dropped 30% over the next quarter"
  - [Opinion: GA4 is worse product than UA.](https://www.reddit.com/r/analytics/comments/wxmlyk/opinion_ga4_is_worse_product_than_ua/) (reddit:r/analytics, 2022-08-25) — "clients ask to migrate back to UA properties"
  - [Only data analyst at a digital marketing agency, being asked to build new data ecosystem while being a newbie. Does my proposed plan make sense?](https://www.reddit.com/r/BusinessIntelligence/comments/o8b63e/only_data_analyst_at_a_digital_marketing_agency/) (reddit:r/BusinessIntelligence, 2021-06-26) — "My company is currently using an external tool which has its own API connections, data warehouse and dashboard visualization. They're thinking of switching"
  - [Anyone else tired of GA4 but forced to use it?](https://www.reddit.com/r/analytics/comments/1s0r7zx/anyone_else_tired_of_ga4_but_forced_to_use_it/) (reddit:r/analytics, 2026-03-22) — "it takes me 5 days to actually dig up the answer. By the time I find it the opportunity is gone."

## 12. Data skills practice and candidate screening — score 12.5
- Aspiring data engineers and Excel users lack hands-on sandboxes and practice; employers struggle to screen data engineers for real software skills amid AI-assisted interview cheating.
- Items: 15 · paying signals: 10 · engagement: 4857 · who: employee 11, student 2, small_business 1
- Fit 0.5: Hosted practice platforms are self-serve software, but hosted Airflow/Kafka sandboxes add infra cost and hiring tools face proctoring/anti-cheat challenges.
- Product idea: Browser-based data engineering challenge platform with graded pipeline tasks on realistic broken data, usable for practice and take-home screening.
- Evidence:
  - [If you are still manually highlighting duplicates in your data, please stop](https://www.reddit.com/r/excel/comments/1p6gn4b/if_you_are_still_manually_highlighting_duplicates/) (reddit:r/excel, 2025-11-25) — "I watched a colleague spend 20 minutes manually coloring rows"
  - [I think most people learn Excel backwards. What actually made you faster?](https://www.reddit.com/r/excel/comments/1vignwt/i_think_most_people_learn_excel_backwards_what/) (reddit:r/excel, 2026-08-07) — "the other takes 3x as long"
  - [We were struggling to find Data Engineers](https://www.reddit.com/r/dataengineering/comments/1wu7drd/we_were_struggling_to_find_data_engineers/) (reddit:r/dataengineering, 2026-09-30) — "We interviewed 22 candidates and no one is fitting the Role."
  - [Caught the candidate using AI for screening](https://www.reddit.com/r/dataengineering/comments/1qaoqlz/caught_the_candidate_using_ai_for_screening/) (reddit:r/dataengineering, 2026-01-12) — "these kind of people mess up the project pretty badly"
  - [What exactly does a Data Engineering Manager at a FAANG company or in a $250k+ role do day-to-day](https://www.reddit.com/r/dataengineering/comments/1oj9q76/what_exactly_does_a_data_engineering_manager_at_a/) (reddit:r/dataengineering, 2025-10-29) — "Any tools which can do ATS,AutoApply,rewrite"

## 13. Warehouse spend and slow query optimization — score 11.05
- Snowflake/Databricks/BigQuery costs exceed estimates and are only noticed after the bill; engineers lack tools that turn query plans into concrete optimization advice.
- Items: 10 · paying signals: 7 · engagement: 2662 · who: enterprise 4, employee 4, freelancer 1
- Fit 0.65: Read-only metadata access enables self-serve SaaS with clear ROI; competitive space and enterprise buyers may want security reviews.
- Product idea: Connect read-only to your warehouse and get weekly ranked fixes (query rewrites, clustering, idle compute) with dollar savings per fix.
- Evidence:
  - [In 6 years, I've never seen a data lake used properly](https://www.reddit.com/r/dataengineering/comments/1r73l52/in_6_years_ive_never_seen_a_data_lake_used/) (reddit:r/dataengineering, 2026-02-17) — "Massive amounts of engineering time ... exclusively skyrocketed infra costs"
  - [Is anyone migrating away from Databricks?](https://www.reddit.com/r/dataengineering/comments/1t6ch3j/is_anyone_migrating_away_from_databricks/) (reddit:r/dataengineering, 2026-05-07) — "Our bill is already around 2x higher than our original estimate, and that estimate included a 50% buffer"
  - [I can’t* understand the hype on Snowflake](https://www.reddit.com/r/dataengineering/comments/1o03g0b/i_cant_understand_the_hype_on_snowflake/) (reddit:r/dataengineering, 2025-10-07) — "don't have too much options on performance/cost optimization (can get pricey fast)"
  - [Why pay for DBT cloud when Fivetran has built in DBT Core?](https://www.reddit.com/r/dataengineering/comments/1318f7s/why_pay_for_dbt_cloud_when_fivetran_has_built_in/) (reddit:r/dataengineering, 2023-04-27) — "an ever growing number of data tools, each with their own expensive price tag"
  - [What is the BI tool for large Star Schema Data](https://www.reddit.com/r/BusinessIntelligence/comments/1okxxpk/what_is_the_bi_tool_for_large_star_schema_data/) (reddit:r/BusinessIntelligence, 2025-10-31) — "If I use a live connection our warehouse is cloud and it will cost us."

## 14. Developer data tooling for dev environments and debugging — score 9.1
- Engineers lack easy tools for anonymized referentially-consistent prod subsets, realistic mock data, Parquet inspection, dbt CTE step-through, and impact analysis on large dbt projects.
- Items: 10 · paying signals: 3 · engagement: 939 · who: employee 7, developer 3
- Fit 0.7: Developer tools fit an engineer builder and can be sold self-serve or open-core; willingness to pay per point tool is modest.
- Product idea: CLI plus hosted service that clones a referentially consistent, PII-masked subset of production Postgres into dev with one command.
- Evidence:
  - [How big are your DBT projects and how do you build/manage them?](https://www.reddit.com/r/dataengineering/comments/1av9i90/how_big_are_your_dbt_projects_and_how_do_you/) (reddit:r/dataengineering, 2024-02-20) — "the required thought/impact analysis that is put into changes has multiplied by 10x"
  - [Creating a Star Schema from a flat table.](https://www.reddit.com/r/BusinessIntelligence/comments/2hcjij/creating_a_star_schema_from_a_flat_table/) (reddit:r/BusinessIntelligence, 2014-09-24) — "I just really want to avoid having to do this totally manually with SSIS"
  - [Ask HN: Tips for software engineering sanity with Databricks notebooks?](https://news.ycombinator.com/item?id=34003064) (hackernews, 2022-12-15) — "It is driving me nuts to use auto-saved versions instead of clearly defined explicitly defined commits"
  - [holy s*** PowerQuery is amazing; how do you guys maintain it?](https://www.reddit.com/r/excel/comments/1pib8ox/holy_s_powerquery_is_amazing_how_do_you_guys/) (reddit:r/excel, 2025-12-09)
  - [A tool to visualize any Parquet file’s internals](https://www.reddit.com/r/dataengineering/comments/1vsl2s0/a_tool_to_visualize_any_parquet_files_internals/) (reddit:r/dataengineering, 2026-08-19)

## 15. Enterprise platform migrations, mentorship and data cleanup projects — score 0.0
- Legacy SAS/ERP/BI migrations, governance design, architecture mentorship, acquisition data stitching and leadership-mandated cleanups require bespoke expert work per organization.
- Items: 22 · paying signals: 13 · engagement: 4087 · who: employee 10, enterprise 8, small_business 3
- Fit 0.15: Value is delivered through per-client consulting, sales-led enterprise deals and custom integration, which scales support hours with customers. · **excluded: service_heavy**
- Product idea: Migration and architecture advisory engagements for enterprises moving off legacy data platforms.
- Evidence:
  - [My experience working with Palantir as a Client](https://www.reddit.com/r/dataengineering/comments/1v3u40k/my_experience_working_with_palantir_as_a_client/) (reddit:r/dataengineering, 2026-07-22) — "multimillion dollar price tag ... 2 of those were directly employed by Palantir as part of an additional contract (read: more $$)"
  - ["Excel Databases:" I am That Guy](https://www.reddit.com/r/excel/comments/wbjsek/excel_databases_i_am_that_guy/) (reddit:r/excel, 2022-07-30) — "tonight, for a client, I am absolutely building an Excel Database"
  - [Client pulling the plug, moving it all to Claude](https://www.reddit.com/r/analytics/comments/1s9vluq/client_pulling_the_plug_moving_it_all_to_claude/) (reddit:r/analytics, 2026-04-01) — ""How can you support us transitioning in this direction""
  - [i messed up :(](https://www.reddit.com/r/dataengineering/comments/1p9k43o/i_messed_up/) (reddit:r/dataengineering, 2025-11-29) — "biggest customer of my small company which pays like 60% of our salaries"
  - [VP told me to 'just use Cowork' to fix years of data chaos in a month. I am losing my mind.](https://www.reddit.com/r/dataengineering/comments/1tifbvq/vp_told_me_to_just_use_cowork_to_fix_years_of/) (reddit:r/dataengineering, 2026-05-20) — "company-wide mandate came down requiring each sector to generate a defined amount of AI-driven revenue per year through cost savings"
