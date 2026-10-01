# trades pain points — ranked

Items scanned: 93 (reddit 93); labelled as pains: 27.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Estimating & bid/proposal builder for small contractors — score 7.2
- Residential and trade contractors, electricians especially, price jobs with homemade Excel/Word/VBA sheets, keep their own historical labor and material data, and often underbid because the process is error-prone.
- Items: 5 · paying signals: 4 · engagement: 0 · who: small_business 5
- Fit 0.8: This is self-serve SaaS built on templates, calculations and document generation. ML can suggest line items and flag underpriced bids using a contractor's own history.
- Product idea: Trade-specific estimating app that learns from past jobs, catches missing or underpriced items, and exports a branded proposal.
- Evidence:
  - [Residential Estimating spreadsheet : r/Construction - Reddit](https://www.reddit.com/r/Construction/comments/9dpuw0/residential_estimating_spreadsheet/) (reddit:r/Construction, ) — "I’m finding out new ways to streamline my company to be more profitable and efficient every day."
  - [Electrical estimating : r/electricians - Reddit](https://www.reddit.com/r/electricians/comments/yprfnm/electrical_estimating/) (reddit:r/electricians, ) — "start building up data until you can accurately come up with your own"
  - [How do you estimate/bid on jobs? : r/electricians - Reddit](https://www.reddit.com/r/electricians/comments/2cpo3y/how_do_you_estimatebid_on_jobs/) (reddit:r/electricians, ) — "You can have you excel spreadsheet import data into your word proposal"
  - [I underbid a job. What can I do? : r/Contractor - Reddit](https://www.reddit.com/r/Contractor/comments/13q1dc6/i_underbid_a_job_what_can_i_do/) (reddit:r/Contractor, ) — "I underbid a job"
  - [Bidding spreadsheet? : r/Construction - Reddit](https://www.reddit.com/r/Construction/comments/slnome/bidding_spreadsheet/) (reddit:r/Construction, )

## 2. Scope, change-order & work-authorization sign-off — score 3.75
- Contractors don't document scope, approvals or labor-vs-materials terms and skip signed authorizations, which leads to disputes, micromanaging clients and bills they can't collect.
- Items: 3 · paying signals: 2 · engagement: 0 · who: small_business 3
- Fit 0.75: E-sign workflow SaaS with AI-drafted scope summaries is self-serve. The product must stay template-based to avoid giving legal advice.
- Product idea: Mobile app that turns a job description into a clear scope/price agreement and change orders the client e-signs before work starts.
- Evidence:
  - [Advice? We performed $1800 of work on a property ... - Reddit](https://www.reddit.com/r/Plumbing/comments/tbcnma/advice_we_performed_1800_of_work_on_a_property/) (reddit:r/Plumbing, ) — "We performed $1800 of work at a property... The customer is saying that he doesn't want to pay"
  - [Subcontractor providing labor only but paying for material..](https://www.reddit.com/r/Contractor/comments/1cq3ept/subcontractor_providing_labor_only_but_paying_for/) (reddit:r/Contractor, ) — "this is something that my boss has done for years with no issue bc the contractor would pay the materials back"
  - [Hate working with rude and micromanaging homeowners](https://www.reddit.com/r/Construction/comments/xthq9i/hate_working_with_rude_and_micromanaging/) (reddit:r/Construction, )

## 3. Back-office admin automation & business onboarding for new contractors — score 3.3
- Owners lose hours to computer admin, and tradespeople turned contractors lack business knowledge on bidding, admin, sales and choosing FSM software with opaque pricing.
- Items: 3 · paying signals: 3 · engagement: 0 · who: small_business 3
- Fit 0.55: An AI agent for email, invoicing and follow-ups plus an FSM pricing comparison is software. The scope is broad and it risks becoming a service.
- Product idea: AI back-office assistant that handles quotes follow-ups, invoicing reminders and paperwork, plus a transparent FSM pricing comparison tool.
- Evidence:
  - [Dislike being an electrician but don’t know what else to do ...](https://www.reddit.com/r/electricians/comments/vz6g98/dislike_being_an_electrician_but_dont_know_what/) (reddit:r/electricians, ) — "I don’t know where to go learn it better nor do I know what questing to ask."
  - [Best Software & prices for new HVAC company & 6 techs](https://www.reddit.com/r/HVAC/comments/10l9qm0/best_software_prices_for_new_hvac_company_6_techs/) (reddit:r/HVAC, ) — "launching my own business with 6 techs. How much does Service Titan, Field Edge, Housecall Pro or other cost?"
  - [Going out on my own? : r/Contractor - Reddit](https://www.reddit.com/r/Contractor/comments/1b3y2st/going_out_on_my_own/) (reddit:r/Contractor, ) — "I hate sitting behind a computer all day. I dread coming into work almost every day."

## 4. Trade engineering calculators (load calc, Manual D, HVAC savings) — score 2.6
- Electricians and HVAC techs use locked or poorly documented spreadsheets for load calculations, Manual D duct design and equipment-replacement energy savings estimates.
- Items: 3 · paying signals: 1 · engagement: 0 · who: small_business 1, unknown 1, employee 1
- Fit 0.65: Deterministic calculation software is easy to build and self-serve. Results must be correct to code standards, which adds liability, and each calculator serves a small niche.
- Product idea: Web suite of editable NEC load calc, Manual D and HVAC savings calculators with worked examples and printable reports.
- Evidence:
  - [Calculating air conditioning annual run hours : r/HVAC - Reddit](https://www.reddit.com/r/HVAC/comments/8ea83z/calculating_air_conditioning_annual_run_hours/) (reddit:r/HVAC, ) — "a general calculation sheet that can be used at any of our properties"
  - [Load Calculation worksheets : r/electricians - Reddit](https://www.reddit.com/r/electricians/comments/za4r3j/load_calculation_worksheets/) (reddit:r/electricians, )
  - [Standalone Manual D software : r/HVAC - Reddit](https://www.reddit.com/r/HVAC/comments/3hfyf6/standalone_manual_d_software/) (reddit:r/HVAC, )

## 5. Simple construction scheduling & PM templates — score 2.4
- P6 is hard to use and data entry wastes hours, and contractors without spreadsheet skills lack ready-made project management templates.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 1, small_business 1
- Fit 0.6: SaaS with AI-generated schedules from a job description is feasible. The market is crowded (Buildertrend, Procore, Monday), and P6 users are enterprise.
- Product idea: Describe a job and get an editable Gantt schedule with trade templates, exportable to P6/XER.
- Evidence:
  - [Ive spent like 6 hours today going through the program trying ...](https://www.reddit.com/r/Construction/comments/1dk5zdz/ive_spent_like_6_hours_today_going_through_the/) (reddit:r/Construction, ) — "Ive spent like 6 hours today going through the program trying to get the planner to enter stuff correctly."
  - [Anyone found/made a nice excel template for project ... - Reddit](https://www.reddit.com/r/Construction/comments/3edqos/anyone_foundmade_a_nice_excel_template_for/) (reddit:r/Construction, ) — "I suck at excel and a nice template would really help"

## 6. Job costing & cost-code tracking — score 2.1
- Contractors track job costs in fragile multi-tab Excel files, can't find CSI MasterFormat codes in usable form, and aren't sure whether to use bookkeeping software or spreadsheets.
- Items: 3 · paying signals: 0 · engagement: 0 · who: small_business 2, employee 1
- Fit 0.7: Multi-tenant SaaS with cost-code templates and receipt/invoice categorization. It is bookkeeping tooling, not financial advice, but it competes with QuickBooks add-ons.
- Product idea: Lightweight job-costing app with preloaded CSI cost codes that auto-categorizes receipts and bills to jobs and syncs with QuickBooks.
- Evidence:
  - [CSI Code Spreadsheet : r/Construction - Reddit](https://www.reddit.com/r/Construction/comments/15p7oo2/csi_code_spreadsheet/) (reddit:r/Construction, )
  - [Construction Costs Tracking With Excel/Other Options?](https://www.reddit.com/r/Construction/comments/rfnsbb/construction_costs_tracking_with_excelother/) (reddit:r/Construction, )
  - [Should I use a bookkeeping software or my own excel ... - Reddit](https://www.reddit.com/r/Construction/comments/18ugv9m/should_i_use_a_bookkeeping_software_or_my_own/) (reddit:r/Construction, )

## 7. Quantity takeoff from plans — score 1.4
- Estimators take quantities off civil and construction PDF plans by hand or with generic PDF readers.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.7: Vision and ML on PDF drawings suits an ML engineer. Accuracy on messy plan sets is hard, and incumbents like Bluebeam and PlanSwift are well established.
- Product idea: Browser-based takeoff tool that auto-detects lengths, areas and counts on civil PDFs and pushes them into an estimate.
- Evidence:
  - [Civil Estimating Software? : r/Construction - Reddit](https://www.reddit.com/r/Construction/comments/8hrnmw/civil_estimating_software/) (reddit:r/Construction, ) — "So many plans show where they want concrete and the scale of the drawing... It's so tedious."

## 8. Flat-rate pricing book — score 1.2
- Trade contractors lack a current flat-rate price book with labor times and up-to-date material costs.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.6: SaaS with material-price scraping and labor-time data is doable. Building and keeping an accurate labor-time dataset is the main difficulty.
- Product idea: Subscription price book with regional material prices updated automatically and customizable labor times and markups.
- Evidence:
  - [Here's a copy of a flat rate book if any of you are ... - Reddit](https://www.reddit.com/r/electricians/comments/edsm9n/heres_a_copy_of_a_flat_rate_book_if_any_of_you/) (reddit:r/electricians, ) — "I spent days typing this into Excel... the material costs are from 2008 so I'm sure they could use adjustment."

## 9. Subcontractor payment protection & lien deadlines — score 0.9
- Subs have no visibility or protection when GCs don't pay and no easy way to secure payment or file liens.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.45: Deadline tracking and notice generation are software. Lien law varies by state and edges into legal advice, and Levelset already serves this market.
- Product idea: Tracker that computes state-specific preliminary notice and lien deadlines per job and generates notice forms.
- Evidence:
  - [My contractor hasn't paid a subcontractor and has gone MIA](https://www.reddit.com/r/Contractor/comments/1dkog1n/my_contractor_hasnt_paid_a_subcontractor_and_has/) (reddit:r/Contractor, ) — "it's hard for him not to be paid"

## 10. AIA G702/G703 progress billing — score 0.85
- Subs and GCs rebuild AIA pay applications from their schedule of values by hand every month.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.85: A narrow, recurring, well-specified document workflow. It is easy to build and self-serve, and support load stays low.
- Product idea: Upload a schedule of values once, enter percent complete monthly, and get G702/G703 PDFs with retainage and change orders tracked.
- Evidence:
  - [How do you guys handle your G702/703’s? - Reddit](https://www.reddit.com/r/Construction/comments/9j8t4s/how_do_you_guys_handle_your_g702703s/) (reddit:r/Construction, )

## 11. Card payments & fee pass-through — score 0.8
- Clients refuse card processing fees, so contractors fall back on checks and ACH or awkward surcharge workarounds.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.4: Can be built on Stripe for invoicing plus compliant surcharging or ACH incentives. Payment-rule compliance and thin differentiation limit it.
- Product idea: Contractor invoicing link that offers low-fee ACH by default and handles state-compliant card surcharges automatically.
- Evidence:
  - [How do you get paid? : r/Contractor - Reddit](https://www.reddit.com/r/Contractor/comments/1ay2clk/how_do_you_get_paid/) (reddit:r/Contractor, ) — "Credit card is a shit show and clients never want to pay the fees"

## 12. Shared client vetting / bad-payer registry — score 0.6
- Contractors have no shared way to vet property owners or warn each other about dishonest or non-paying clients.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.3: The software is simple, but the product depends on network effects, carries high defamation and moderation load, and has FCRA-like concerns.
- Product idea: Contractor-only review registry of property owners, with payment history pulled from public lien and court records.
- Evidence:
  - [Who are these people… : r/Contractor - Reddit](https://www.reddit.com/r/Contractor/comments/1da5f7n/who_are_these_people/) (reddit:r/Contractor, ) — "we often wish there was a way to warn colleagues off dishonest or unreasonable owners"

## 13. Subcontractor finding & vetting — score 0.35
- New contractors struggle to find and vet reliable subcontractors in trades they want to expand into.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.35: This is a two-sided marketplace with a cold-start problem. License and insurance checks can be automated, but gaining traction takes sales and community effort.
- Product idea: Sub directory that auto-verifies license, insurance and reviews from public data, filtered by trade and area.
- Evidence:
  - [Finding Subcontractors : Contractor](https://en.reddit.com/r/Contractor/comments/1gf92jb/finding_subcontractors/) (reddit:r/Contractor, )

## 14. Transparent tool financing for new techs — score 0.0
- New trade techs face high upfront tool costs and opaque employer tool-debt arrangements.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.15: Consumer lending or financing is a regulated financial product that needs capital and compliance. · **excluded: regulated**
- Product idea: Transparent tool-financing marketplace for apprentices.
- Evidence:
  - [Tool account over $5000 : r/HVAC - Reddit](https://www.reddit.com/r/HVAC/comments/1br0ft0/tool_account_over_5000/) (reddit:r/HVAC, ) — "Tool account over $5000"
