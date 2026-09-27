# private-practice pain points — ranked

Items scanned: 51 (reddit 51); labelled as pains: 24.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Licensure hour tracking for pre-licensed clinicians — score 8.5
- Pre-licensure counselors and therapists log supervised direct, indirect and supervision hours in spreadsheets or pricey apps (Time2Track, TrackMyHours) that often miscount under state-specific rules, especially with multiple supervisors.
- Items: 6 · paying signals: 4 · engagement: 0 · who: employee 6
- Fit 0.85: Pure self-serve CRUD plus a state rules engine; no PHI needed, multi-tenant, low support once rules are encoded; main cost is keeping 50-state rule tables current.
- Product idea: Cheap hour logger with per-state licensure rule packs, multi-supervisor splits and exportable signed supervisor reports.
- Evidence:
  - [How do you guys keep track of your clinical hours? - Reddit](https://www.reddit.com/r/therapists/comments/1dsg6zv/how_do_you_guys_keep_track_of_your_clinical_hours/) (reddit:r/therapists, ) — "I bought a LMHC hours tracker but it doesn't appear to have accurate hours counting"
  - [I created LCSW BBS Hours Tracking Log : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/15a7maf/i_created_lcsw_bbs_hours_tracking_log/) (reddit:r/therapists, ) — "TrackMyHours charge you $200 to track your hours for 3 years"
  - [hour tracking for licensure : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/xkmwzr/hour_tracking_for_licensure/) (reddit:r/therapists, ) — "I have two supervisors and just keep two excel files"
  - [Hi everyone! Is time2track and trackmyhours actually better ...](https://www.reddit.com/r/therapists/comments/13m17wl/hi_everyone_is_time2track_and_trackmyhours/) (reddit:r/therapists, ) — "Is time2track and trackmyhours actually better than just an excel spreadsheet?"
  - [How do you keep track of your clinical hours? : r/therapists](https://www.reddit.com/r/therapists/comments/uq4m90/how_do_you_keep_track_of_your_clinical_hours/) (reddit:r/therapists, )

## 2. Client payments, FSA/HSA autopay and collections — score 3.6
- Solo practitioners stitch together payment tools, charge cards by hand, can't autopay with FSA/HSA cards, and have no structured process for collecting balances after denials.
- Items: 3 · paying signals: 3 · engagement: 0 · who: freelancer 3
- Fit 0.6: Buildable on Stripe with automated reminders and payment plans; FSA/HSA card handling and collections compliance (FDCPA-style rules) add some complexity.
- Product idea: Stripe-based card-on-file autopay with FSA/HSA support, automated balance reminders and self-serve payment plans.
- Evidence:
  - [Anyone NOT using an EHR? : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/1bwn1kv/anyone_not_using_an_ehr/) (reddit:r/therapists, ) — "I manually enter credit card charges on the phone... It's a pain but it's simple and relatively cheap"
  - [Using helloalma and a client has not paid her copay](https://www.reddit.com/r/therapists/comments/10wbkoe/using_helloalma_and_a_client_has_not_paid_her/) (reddit:r/therapists, ) — "I reminded her again in the morning of our session... they have yet to be paid"
  - [Clients that refuse to pay : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/17b51h6/clients_that_refuse_to_pay/) (reddit:r/therapists, ) — "She paid $500 off her balance of $1000"

## 3. Insurance claim status and payment reconciliation — score 2.7
- Solo therapists file claims by hand on payer portals, post payments manually when ERAs don't sync to the EHR, and can't see what opaque billing intermediaries owe them.
- Items: 3 · paying signals: 3 · engagement: 0 · who: freelancer 3
- Fit 0.45: Software-solvable via clearinghouse/ERA (835) parsing, but needs PHI handling, payer integrations and billing-edge-case support that grows with customers.
- Product idea: ERA/EOB parser that reconciles payer payments against sessions and flags unpaid or underpaid claims.
- Evidence:
  - [Billing & Claims in SimplePractice : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/115ntp3/billing_claims_in_simplepractice/) (reddit:r/therapists, ) — "This method requires good bookkeeping prior to sending the claim, and afterwards"
  - [simple practice not showing optum payments : r/therapists](https://www.reddit.com/r/therapists/comments/1dfp4rl/simple_practice_not_showing_optum_payments/) (reddit:r/therapists, ) — "I need to enter them manually, which is incredibly time-consuming"
  - [Headway Mishap : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/1asa6ni/headway_mishap/) (reddit:r/therapists, ) — "they have a much better rate with that insurer ($20 more)"

## 4. Out-of-network benefits checks and superbills — score 1.65
- Self-pay practitioners manually check each client's OON benefits and coverage for specific services, and don't understand superbills well enough to guide clients through reimbursement.
- Items: 3 · paying signals: 0 · engagement: 0 · who: small_business 2, freelancer 1
- Fit 0.55: Eligibility APIs (270/271) and superbill generation are automatable, but per-check API costs and payer variability add support load; existing players (Thrizer, Reimbursify) compete.
- Product idea: Client-facing OON benefits estimator plus auto-generated superbills with step-by-step reimbursement submission guidance.
- Evidence:
  - [Need a reality check - private practice self pay only rates ...](https://www.reddit.com/r/therapists/comments/100a6cz/need_a_reality_check_private_practice_self_pay/) (reddit:r/therapists, )
  - [Help me understand super bills : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/15fbs5e/help_me_understand_super_bills/) (reddit:r/therapists, )
  - [Prehab : r/physicaltherapy - Reddit](https://www.reddit.com/r/physicaltherapy/comments/ew7jzb/prehab/) (reddit:r/physicaltherapy, )

## 5. Practice income and reimbursement tracking — score 1.5
- Private-practice therapists track session income, insurance reimbursement rates and expected vs received payments in hand-built spreadsheets.
- Items: 1 · paying signals: 1 · engagement: 0 · who: freelancer 1
- Fit 0.75: Straightforward bookkeeping-lite SaaS with CSV/bank imports; competes with spreadsheets and general tools.
- Product idea: Therapist-specific income ledger tracking expected vs received payment per session and payer, with rate and aging reports.
- Evidence:
  - [Spreadsheet for Income Tracking? : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/138xy1a/spreadsheet_for_income_tracking/) (reddit:r/therapists, ) — "a little more manual input if you don't use those"

## 6. Multi-agency visit and earnings tracking for home-health clinicians — score 1.5
- Home-health clinicians working for several agencies at different per-visit rates piece together visits and earnings from calendars and Excel.
- Items: 1 · paying signals: 1 · engagement: 0 · who: freelancer 1
- Fit 0.75: Mobile-friendly logger with per-agency rates, no clinical data needed; niche but self-serve.
- Product idea: Visit logger with per-agency rate cards, mileage, and per-agency earnings and invoice reports.
- Evidence:
  - [Tracking the number of visits as a home health care provider](https://www.reddit.com/r/physicaltherapy/comments/144vfqv/tracking_the_number_of_visits_as_a_home_health/) (reddit:r/physicaltherapy, ) — "Is there any good (and easy) way to track using an app or Excel? I suck at Excel"

## 7. Physician referral pipeline tracking — score 1.4
- Clinics track incoming physician referrals in Google Docs or Excel with no dedicated pipeline tool.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.7: Lightweight CRM for referrals is simple self-serve SaaS; minimal PHI if limited to referral metadata.
- Product idea: Referral-intake kanban tracking each referral from receipt to first visit, with referral-source analytics.
- Evidence:
  - [Referral management : r/physicaltherapy - Reddit](https://www.reddit.com/r/physicaltherapy/comments/15t92g2/referral_management/) (reddit:r/physicaltherapy, ) — "is there software to make it easier to manage the referral pipeline?"

## 8. AI-assisted clinical note writing — score 1.0
- Therapists with high caseloads spend large amounts of time writing progress notes even with EMR templates.
- Items: 1 · paying signals: 1 · engagement: 0 · who: freelancer 1
- Fit 0.5: Strong ML fit, but handles PHI (HIPAA, BAAs, security reviews) and the space is crowded with funded AI-scribe competitors.
- Product idea: HIPAA-compliant tool that drafts SOAP/DAP notes from brief session bullets or audio, pasted into any EHR.
- Evidence:
  - [Private practice notes : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/11bsipr/private_practice_notes/) (reddit:r/therapists, ) — "it's just so tedious when I see 27 people a week"

## 9. Genogram / family diagram software — score 0.8
- Therapists lack a good dedicated tool for building client family genograms.
- Items: 1 · paying signals: 0 · engagement: 0 · who: freelancer 1
- Fit 0.8: Self-contained diagramming web app with standard McGoldrick symbols; can run client-side to avoid storing PHI.
- Product idea: Browser-based genogram editor with standard notation, relationship lines and PDF export, storing data locally.
- Evidence:
  - [Genogram software? : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/17hxm64/genogram_software/) (reddit:r/therapists, )

## 10. Pre-PT observation hour logging and verification — score 0.75
- Pre-PT (and similar pre-health) applicants have no standard tool to log clinical observation hours and get them verified by supervising clinicians for program applications.
- Items: 1 · paying signals: 0 · engagement: 0 · who: student 1
- Fit 0.75: Simple multi-tenant app with emailed verification links; small, price-sensitive student market limits revenue.
- Product idea: Observation-hour log where supervisors verify entries via one-click email links, exporting a PTCAS-ready summary.
- Evidence:
  - [[Question] How does logging in observation hours work if I am ...](https://www.reddit.com/r/physicaltherapy/comments/2zvkxq/question_how_does_logging_in_observation_hours/) (reddit:r/physicaltherapy, )

## 11. Counselor compensation and fee benchmarks — score 0.7
- Counselors lack reliable benchmark data on pay and session fees to set rates or negotiate compensation.
- Items: 1 · paying signals: 0 · engagement: 0 · who: employee 1
- Fit 0.7: Crowdsourced data product plus scraping of public sources; fully self-serve, but needs a cold-start data collection push.
- Product idea: Anonymous crowdsourced database of therapist pay, session rates and payer reimbursement by region and license type.
- Evidence:
  - [salary/fee transperancy : r/therapists - Reddit](https://www.reddit.com/r/therapists/comments/umndu1/salaryfee_transperancy/) (reddit:r/therapists, )

## 12. Cash-based practice financial modeling — score 0.7
- Clinicians starting cash-based practices build their own spreadsheets to model overhead, pricing and patient volume.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.7: Simple calculator/template product, no PHI; low support but also one-off usage limits recurring revenue.
- Product idea: Interactive break-even and pricing model for opening a cash-pay practice, with scenario comparisons.
- Evidence:
  - [Cash-based Physical Therapy, Your Experience and Thoughts](https://www.reddit.com/r/physicaltherapy/comments/89ub3a/cashbased_physical_therapy_your_experience_and/) (reddit:r/physicaltherapy, )

## 13. Guidance on insurance fee, reimbursement and balance-billing rules — score 0.0
- Therapists struggle to understand payer rules on fees, reimbursement, and what they may legally balance-bill.
- Items: 1 · paying signals: 0 · engagement: 0 · who: freelancer 1
- Fit 0.3: Mostly an education/interpretation need; authoritative answers on balance billing and contract terms verge on legal advice and vary by payer and state. · **excluded: regulated**
- Product idea: Plain-language reference library of payer and state billing rules with citations.
- Evidence:
  - [Does the insurance company determine what I can charge for ...](https://www.reddit.com/r/therapists/comments/13qi14k/does_the_insurance_company_determine_what_i_can/) (reddit:r/therapists, )
