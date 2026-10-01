# bookkeeping pain points — ranked

Items scanned: 49 (reddit 49); labelled as pains: 15.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. PDF bank/credit card statement to categorized CSV — score 3.6
- Bookkeepers and small businesses key in transactions from PDF statements by hand and lack a reliable tool that converts them to CSV and auto-categorizes them with rules for QBO/Xero import.
- Items: 3 · paying signals: 1 · engagement: 0 · who: freelancer 2, small_business 1
- Fit 0.9: Document extraction plus rule/ML categorization is core ML work, fully self-serve, multi-tenant, and support stays flat.
- Product idea: Upload PDF statements, get clean QBO/Xero-ready CSV with rule-based and learned auto-categorization.
- Evidence:
  - [Looking for software to read PDF bank statements, and auto ...](https://www.reddit.com/r/Bookkeeping/comments/11dg7pz/looking_for_software_to_read_pdf_bank_statements/) (reddit:r/Bookkeeping, ) — "Trying to avoid majority of data entry or manually going through bank statements"
  - [simple categorizing expenses software? : r/Bookkeeping - Reddit](https://www.reddit.com/r/Bookkeeping/comments/18w04m8/simple_categorizing_expenses_software/) (reddit:r/Bookkeeping, )
  - [Converting pdf bank statements to csv : r/Bookkeeping - Reddit](https://www.reddit.com/r/Bookkeeping/comments/17k718p/converting_pdf_bank_statements_to_csv/) (reddit:r/Bookkeeping, )

## 2. Automated QBO bookkeeping quality check — score 1.6
- Small business owners can't tell whether cheap outsourced bookkeepers are keeping their QBO books correctly.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.8: Anomaly detection and rule checks over the QBO API are ML-friendly, recurring and fully automated.
- Product idea: Connect QBO and get a monthly automated health report flagging miscategorizations, unreconciled accounts and suspicious entries.
- Evidence:
  - [Should I fire this guy : r/Bookkeeping - Reddit](https://www.reddit.com/r/Bookkeeping/comments/1bv6b8q/should_i_fire_this_guy/) (reddit:r/Bookkeeping, ) — "paying this virtual employee $20/mo to do my books in QBO is not even worth it"

## 3. Multi-tax-rate receipt splitting — score 1.5
- Purchases that mix tax rates need tedious line-by-line splitting and tax coding in accounting software.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.75: Receipt OCR plus line-item tax classification and an accounting API push is well-scoped, self-serve software.
- Product idea: Receipt scanner that splits line items by tax rate and posts correctly coded split transactions to QBO/Xero.
- Evidence:
  - [Setting taxes for purchases including more than one tax rate ...](https://www.reddit.com/r/Bookkeeping/comments/al14xy/setting_taxes_for_purchases_including_more_than/) (reddit:r/Bookkeeping, ) — "It's just so tedious to split purchases and line by line code the tax to each item"

## 4. Automated supplementary schedules and workpapers — score 1.2
- Business returns now need extensive supplementary worksheets and documentation for expanding schedules, which makes preparation 2-3x slower and drives burnout.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.6: LLM-driven document assembly from trial balances fits, but schedules change often and have to integrate with incumbent tax software.
- Product idea: Generate draft supplementary schedules and supporting workpapers from a client's trial balance and source documents.
- Evidence:
  - [A1 PA taxes are SO TEDIOUS and I’m losing my mind - Reddit](https://www.reddit.com/r/Accounting/comments/1bsf0eg/a1_pa_taxes_are_so_tedious_and_im_losing_my_mind/) (reddit:r/Accounting, ) — "It takes 2-3 times longer to do a business tax return than five years ago"

## 5. Combined secure document exchange and e-signature for preparers — score 1.1
- Tax preparers stitch together separate tools for secure client document exchange and e-signatures, and have few trustworthy reviews to help them choose.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.55: Multi-tenant SaaS fits the profile, but the market is crowded (TaxDome, SmartVault) and security expectations raise the support burden.
- Product idea: Simple, flat-priced client portal bundling secure uploads, document requests and e-signature for solo tax preparers.
- Evidence:
  - [Anyone here have experience with Verifyle? : r/taxpros - Reddit](https://www.reddit.com/r/taxpros/comments/ihtnzy/anyone_here_have_experience_with_verifyle/) (reddit:r/taxpros, ) — "I decided on the secure portal through my website for document exchange and docusign for collecting signed 8879's"

## 6. Brokerage tax document summary extraction — score 0.85
- Brokerage 1099 composite PDFs bury summary totals deep in long documents, so preparers page through them by hand to pull out the figures.
- Items: 1 · paying signals: 0 · engagement: 0 · who: employee 1
- Fit 0.85: Narrow PDF extraction task with clear ground truth that suits an ML engineer, sold self-serve to preparers.
- Product idea: Drop in a consolidated 1099 PDF and get a one-page summary of all totals, mapped to tax-software input fields.
- Evidence:
  - [I hate vanguard with a passion : r/taxpros - Reddit](https://www.reddit.com/r/taxpros/comments/127t923/i_hate_vanguard_with_a_passion/) (reddit:r/taxpros, )

## 7. Low-cost T2 filing for small Canadian corporations — score 0.8
- Small Canadian corporations with simple or nil activity need affordable web software to file T2 returns, now that free options have become paid.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.4: Self-serve web software fits, but it needs CRA NETFILE certification, yearly form updates and tax-rule accuracy, so the compliance load is high for 15 hrs/week.
- Product idea: Web app that walks a nil or simple Canadian corporation through its T2 return and files it via CRA-certified e-file.
- Evidence:
  - [Nil Tax return T2 Canada - Free software? : r/Accounting - Reddit](https://www.reddit.com/r/Accounting/comments/wr5bvb/nil_tax_return_t2_canada_free_software/) (reddit:r/Accounting, ) — "TaxTron used to be free but now charge $79.99 for a nil return"

## 8. AP automation that keeps vendor relationships intact — score 0.7
- AP automation vendors that take over vendor payments, for example by forcing card payments to earn rebates, can damage key supplier relationships.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.35: An invoice-capture and approval layer is feasible, but a crowded market and payment-rail and money-movement compliance make it a weak fit.
- Product idea: Invoice capture and approval workflow that leaves payment method and vendor communication fully under the business's control.
- Evidence:
  - [AP automation almost got CFO fired : r/Bookkeeping - Reddit](https://www.reddit.com/r/Bookkeeping/comments/1dddpxy/ap_automation_almost_got_cfo_fired/) (reddit:r/Bookkeeping, ) — "One of our clients signed up for AP automation"

## 9. P2P rent collection bookkeeping for small landlords — score 0.65
- Small landlords struggle to accept Zelle, Venmo and Cash App rent while keeping business records clean and separate from personal funds.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.65: Transaction matching and categorization via bank feeds is feasible and self-serve, but P2P apps have limited APIs.
- Product idea: Bank-feed tool that detects P2P rent payments, matches them to tenants and units, and exports clean rental books.
- Evidence:
  - [Tenants want to use Zelle, Venmo, Apple Pay, Cash App etc](https://www.reddit.com/r/Bookkeeping/comments/r8v19k/tenants_want_to_use_zelle_venmo_apple_pay_cash/) (reddit:r/Bookkeeping, )

## 10. Alternative general ledger to Intuit/NetSuite — score 0.6
- Accountants resent Intuit's dominance and find expensive platforms like NetSuite missing basics such as cash-basis balance sheets and simple reconciliation.
- Items: 2 · paying signals: 1 · engagement: 0 · who: employee 2
- Fit 0.2: A full accounting platform is a huge build with heavy migration and support load and entrenched competitors, so it does not fit 15 hrs/week.
- Product idea: Lightweight cloud general ledger with cash/accrual toggles and simple reconciliation, aimed at firms leaving QuickBooks Desktop.
- Evidence:
  - [Alternatives to QuickBooks Desktop : r/taxpros - Reddit](https://www.reddit.com/r/taxpros/comments/1bvw3tp/alternatives_to_quickbooks_desktop/) (reddit:r/taxpros, ) — "For being such an expensive and "robust" program its limitations are ridiculous"
  - [Hated Intuit before but now that they've acquired Mailchimp I ...](https://www.reddit.com/r/taxpros/comments/pq1fm4/hated_intuit_before_but_now_that_theyve_acquired/) (reddit:r/taxpros, )

## 11. Guided client walkthroughs for state tax elections — score 0.3
- State elections such as NY PTET can only be made through the client's own portal, so preparers walk small-business clients through the filings by hand.
- Items: 1 · paying signals: 0 · engagement: 0 · who: employee 1
- Fit 0.3: The filing happens in government portals software can't access, so a product is limited to guided checklists, and the per-client hand-holding stays.
- Product idea: Shareable step-by-step portal walkthroughs per state election that preparers send to clients, with completion tracking.
- Evidence:
  - [NY PTET: A rant in which I hate NYS : r/taxpros - Reddit](https://www.reddit.com/r/taxpros/comments/tetmwk/ny_ptet_a_rant_in_which_i_hate_nys/) (reddit:r/taxpros, )

## 12. Alternative to QBO Payroll — score 0.0
- Bookkeepers see QuickBooks Online Payroll as hassle-prone and contractually exclude it in favor of alternatives.
- Items: 1 · paying signals: 1 · engagement: 0 · who: freelancer 1
- Fit 0.1: Payroll involves tax filing liability, money movement and multi-jurisdiction compliance, which makes it regulated and support-heavy. · **excluded: regulated**
- Product idea: Payroll service for small businesses that integrates with bookkeepers' workflows.
- Evidence:
  - [QuickBooks Online - Payroll Emails : r/Bookkeeping - Reddit](https://www.reddit.com/r/Bookkeeping/comments/1182czr/quickbooks_online_payroll_emails/) (reddit:r/Bookkeeping, ) — "It's in my contracts that I'm not using QB for payroll, it's a nightmare"
