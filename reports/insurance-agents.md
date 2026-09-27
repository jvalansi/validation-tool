# insurance-agents pain points — ranked

Items scanned: 26 (reddit 26); labelled as pains: 13.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Contents claim itemization & ACV calculator — score 3.2
- Contents claims and total-loss lists require building itemized spreadsheets by hand, with replacement-cost lookups and depreciation/ACV worked out per item.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 1, unknown 1
- Fit 0.8: ML-heavy self-serve tool (item recognition, price lookup, depreciation tables) with high per-use value for policyholders and adjusters.
- Product idea: Describe or photograph lost items to get a carrier-format contents schedule with sourced replacement costs and computed ACV.
- Evidence:
  - [How do I determine the value of water-damaged items? - Reddit](https://www.reddit.com/r/Insurance/comments/3z6a8k/how_do_i_determine_the_value_of_waterdamaged_items/) (reddit:r/Insurance, ) — "We got the replacement cost prices from websites like target.com or wallmart.com or sears.com and copied the hyperlink"
  - [Any tips for personal property inventory after a house fire?](https://www.reddit.com/r/Insurance/comments/ejiz8i/any_tips_for_personal_property_inventory_after_a/) (reddit:r/Insurance, ) — "it took us 20 hours between us to create the contents spreadsheet for a 1,300 sq ft ranch house"

## 2. Prospect declarations-page collection — score 1.5
- Agents struggle to get dec pages and current policy details from prospects, which stalls quoting.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.75: Self-serve upload link plus document extraction is a strong ML fit and needs little support.
- Product idea: Shareable intake link where prospects upload or photograph dec pages, with AI extraction into structured quote-ready data.
- Evidence:
  - [Getting peoples dec pages : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/ctlfra/getting_peoples_dec_pages/) (reddit:r/InsuranceAgent, ) — "our biggest challenge is getting peoples dec page information"

## 3. Automated client premium reminders — score 1.4
- Agents send recurring premium-payment reminders to each client by hand, without a simple scheduling tool.
- Items: 1 · paying signals: 1 · engagement: 0 · who: freelancer 1
- Fit 0.7: Simple self-serve scheduling and messaging SaaS with flat support, though the feature is easy to copy.
- Product idea: Import a client/policy list and get automated SMS/email premium and renewal reminders on a schedule.
- Evidence:
  - [Question : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/1bjdo78/question/) (reddit:r/InsuranceAgent, ) — "I'm looking for a system in which I can set up every client... for the program to send this messages to every client every month"

## 4. Home contents inventory for policyholders — score 1.3
- Renters and homeowners have no simple standard tool to document belongings, values and receipts, and their spreadsheets get abandoned.
- Items: 2 · paying signals: 0 · engagement: 0 · who: unknown 2
- Fit 0.65: Consumer self-serve app with photo/receipt AI tagging fits well, but retention and willingness to pay are weak and free alternatives exist.
- Product idea: Photo/video walkthrough app that auto-itemizes belongings with estimated values and stores receipts for claims.
- Evidence:
  - [Personal Property Inventory spreadsheet : r/Insurance - Reddit](https://www.reddit.com/r/Insurance/comments/12xjkfh/personal_property_inventory_spreadsheet/) (reddit:r/Insurance, )
  - [I'm making a spreadsheet to document belongings. Any ... - Reddit](https://www.reddit.com/r/Insurance/comments/11ozgdy/im_making_a_spreadsheet_to_document_belongings/) (reddit:r/Insurance, )

## 5. Multi-carrier quoting without re-entry — score 1.2
- Agents distrust comparative raters, so they re-enter applicant data on each carrier portal and compare quotes by hand.
- Items: 2 · paying signals: 1 · engagement: 0 · who: unknown 1, small_business 1
- Fit 0.4: Browser automation plus ML fits, but brittle carrier portals, carrier appointment and ToS limits drive up maintenance.
- Product idea: Browser extension that autofills a stored applicant profile across carrier portals and collects the returned quotes into a comparison sheet.
- Evidence:
  - [Comparative rater tools : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/1dbbfec/comparative_rater_tools/) (reddit:r/InsuranceAgent, ) — "some people prefer to go to carrier sites, pull data from there, and compare it manually"
  - [Software for generating quotes from multiple carriers](https://www.reddit.com/r/InsuranceAgent/comments/1b7qnff/software_for_generating_quotes_from_multiple/) (reddit:r/InsuranceAgent, )

## 6. Agency business-plan projection templates — score 1.1
- Prospective agency owners build multi-year financial projections for carrier proposals from scratch, with no standard template.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.55: Easy to build as a template/wizard product, but the audience is small and mostly one-time buyers.
- Product idea: Guided wizard that produces a carrier-ready 3-5 year agency pro forma from a few inputs.
- Evidence:
  - [STATE FARM AGENCY OWNER : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/169z2yk/state_farm_agency_owner/) (reddit:r/InsuranceAgent, ) — "I don't want to reinvent the will so somebody is willing to share their spreadsheet with all the cells coded"

## 7. Affordable AMS for paper-based small agencies — score 1.0
- Small agencies run their workflow on paper, post-it notes and manual follow-ups, and need an affordable integrated agency management system.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.5: Self-serve multi-tenant SaaS fits, but a full AMS is broad, integration-heavy and competes with entrenched vendors.
- Product idea: Minimal CRM/AMS for 1-5 person agencies covering clients, policies, renewals and follow-up tasks.
- Evidence:
  - [Agency Workflow : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/1af6uia/agency_workflow/) (reddit:r/InsuranceAgent, ) — "We are looking into EPIC or Vertafore for our AMS... free up time and space for growth"

## 8. Automated policy entry into enterprise AMS — score 0.9
- Applied TAM/EPIC need manual updates for non-downloadable policies, which adds data-entry steps.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.45: Document extraction is a good fit, but pushing data into closed enterprise AMS platforms needs integrations and enterprise sales.
- Product idea: Turns policy PDFs into structured records and pushes them into Applied Epic/TAM through their APIs or RPA.
- Evidence:
  - [Applied TAM v. Applied EPIC : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/157em72/applied_tam_v_applied_epic/) (reddit:r/InsuranceAgent, ) — "I already struggle to remember to update TAM manually on non-downloadable files"

## 9. Commission & expense tracking for independent agents — score 0.6
- Independent agents track commission income and business expenses for taxes in manual monthly spreadsheets.
- Items: 1 · paying signals: 0 · engagement: 0 · who: freelancer 1
- Fit 0.6: Self-serve SaaS with statement parsing and categorization; crowded by generic bookkeeping tools and must avoid tax advice.
- Product idea: Upload carrier commission statements and bank feeds to get auto-reconciled commission and expense ledgers with tax-ready exports.
- Evidence:
  - [Income/expenses question : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/1d477h2/incomeexpenses_question/) (reddit:r/InsuranceAgent, )

## 10. Commercial lines underwriting throughput — score 0.25
- Most commercial lines quotes are underwritten manually by several people, so firm numbers are slow to arrive.
- Items: 1 · paying signals: 0 · engagement: 0 · who: employee 1
- Fit 0.25: The buyers are carriers and MGAs, so this means enterprise sales, underwriting-authority rules and heavy customization.
- Product idea: AI submission triage that extracts ACORD/loss-run data and pre-fills underwriter worksheets.
- Evidence:
  - [Commercial Lines Quote : r/InsuranceAgent - Reddit](https://www.reddit.com/r/InsuranceAgent/comments/mcwb1n/commercial_lines_quote/) (reddit:r/InsuranceAgent, )
