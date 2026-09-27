# ecommerce pain points — ranked

Items scanned: 78 (reddit 78); labelled as pains: 48.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Seller profit & margin dashboard — score 9.0
- Sellers across Amazon, Shopify, and Etsy rebuild spreadsheets by hand to work out true per-product profit, contribution margin, fees, COGS, and monthly expenses, because marketplace financial data is hard to use and suites like Helium 10 cost too much.
- Items: 6 · paying signals: 4 · engagement: 0 · who: small_business 5, hobbyist 1
- Fit 0.9: Self-serve SaaS built on marketplace APIs, with a strong fit for data pipelines and dashboards. Support stays flat once the connectors are stable.
- Product idea: Low-cost profit dashboard that pulls in Amazon, Shopify, and Etsy fees and orders and computes per-SKU net margin from user-entered COGS.
- Evidence:
  - [Is there a tool that shows real time Contribution Margin?](https://www.reddit.com/r/ecommerce/comments/1b9rf3n/is_there_a_tool_that_shows_real_time_contribution/) (reddit:r/ecommerce, ) — "I don't need a whole ERP like Netsuite, but would love to be able to see real time contribution margin"
  - [Your ideal spreadsheet for order/profit tracking? - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/497pym/your_ideal_spreadsheet_for_orderprofit_tracking/) (reddit:r/FulfillmentByAmazon, ) — "I'm building a new spreadsheet for order and profit tracking after using a different one for over a year"
  - [Excel Template for Tracking Profit Per Product : r ... - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/m47d3k/excel_template_for_tracking_profit_per_product/) (reddit:r/FulfillmentByAmazon, ) — "Basically, just an Excel doc version of the profit dashboard of programs like Hellium10"
  - [Ultimate Etsy Sales and Profit Spreadsheet - Reddit](https://www.reddit.com/r/EtsySellers/comments/vraty4/ultimate_etsy_sales_and_profit_spreadsheet/) (reddit:r/EtsySellers, ) — "I've spent the last 18 months teaching myself the ins and outs of how to use Excel and make efficient spreadsheets for my business"
  - [Are there an Amazon FBA profit and expenses Excel spreadsheet?](https://www.reddit.com/r/FulfillmentByAmazon/comments/dqampl/are_there_an_amazon_fba_profit_and_expenses_excel/) (reddit:r/FulfillmentByAmazon, )

## 2. Marketplace search visibility & ad ROI diagnostics — score 5.6
- Sellers can't tell whether marketplace ad spend pays off, don't know how to set up PPC for the first time, see unexplained drops in search visibility, and lose ground to resellers, AI-generated listings, and fake negative reviews.
- Items: 6 · paying signals: 2 · engagement: 0 · who: small_business 5, hobbyist 1
- Fit 0.7: Rank tracking, ad attribution analytics, and review anomaly detection all suit ML, but data access through Etsy and Amazon APIs is limited.
- Product idea: Etsy and Amazon rank and ad-ROI tracker that correlates visibility drops with ad spend, competitor listings, and review anomalies.
- Evidence:
  - [I'm an Amazon seller, competitor leaving me negative reviews ...](https://www.reddit.com/r/FulfillmentByAmazon/comments/ak6di0/im_an_amazon_seller_competitor_leaving_me/) (reddit:r/FulfillmentByAmazon, ) — "My star rating on my product dropped from 5 stars to 3.5 stars, and as a result my sales slowed"
  - [Etsy Ads causing a BOOM in orders : r/EtsySellers - Reddit](https://www.reddit.com/r/EtsySellers/comments/11xlssj/etsy_ads_causing_a_boom_in_orders/) (reddit:r/EtsySellers, ) — "I switched ads on my store for $2 a day"
  - [Amazon Campaign : Manual vs Automatic : r ... - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/cfhdr8/amazon_campaign_manual_vs_automatic/) (reddit:r/FulfillmentByAmazon, )
  - [Can we control in which order listings are displayed?](https://www.reddit.com/r/EtsySellers/comments/13czjs8/can_we_control_in_which_order_listings_are/) (reddit:r/EtsySellers, )
  - [The flood of POD/Ai slop on Etsy right now - Reddit](https://www.reddit.com/r/EtsySellers/comments/1cs26h5/the_flood_of_podai_slop_on_etsy_right_now/) (reddit:r/EtsySellers, )

## 3. AI catalog categorization & image-SKU matching — score 3.6
- Stores spend hours every week sorting new products into categories, matching vendor catalog items to existing inventory, and matching images to SKUs in retailer templates.
- Items: 2 · paying signals: 2 · engagement: 0 · who: small_business 2
- Fit 0.9: Classification, entity matching, and image matching are direct ML problems, and a self-serve upload-and-process product works here.
- Product idea: Upload a vendor catalog and images to get auto-categorized, deduplicated, SKU-matched rows exported in any retailer template.
- Evidence:
  - [Bulk image upload: to distributor spreadsheet : r/ecommerce](https://www.reddit.com/r/ecommerce/comments/19fd82v/bulk_image_upload_to_distributor_spreadsheet/) (reddit:r/ecommerce, ) — "We have about 100 SKU's and each SKU has about 5-6 supporting images."
  - [Automating repetitive manual tasks in my Shopify store](https://www.reddit.com/r/ecommerce/comments/11vbbia/automating_repetitive_manual_tasks_in_my_shopify/) (reddit:r/ecommerce, ) — "manually having to sort them into the categories is very time consuming (and critical to get right)"

## 4. Order & inventory tracking that outgrows Sheets — score 3.4
- Sellers track orders, inventory, and material use in homemade Google Sheets that break as volume grows and can't pull Amazon or Etsy data automatically.
- Items: 3 · paying signals: 1 · engagement: 0 · who: small_business 3
- Fit 0.85: An API-to-spreadsheet sync or light inventory app is standard multi-tenant software.
- Product idea: Auto-sync marketplace orders and inventory into a live Google Sheet or lightweight inventory app, with material-usage tracking for makers.
- Evidence:
  - [How to track orders - Google sheets, Excel, database?](https://www.reddit.com/r/FulfillmentByAmazon/comments/jpqpmn/how_to_track_orders_google_sheets_excel_database/) (reddit:r/FulfillmentByAmazon, ) — "It's getting way too large and weren't sure what to do about that"
  - [Looking for Google Sheet Templates for Amazon FBA Sellers ...](https://www.reddit.com/r/FulfillmentByAmazon/comments/167yx3w/looking_for_google_sheet_templates_for_amazon_fba/) (reddit:r/FulfillmentByAmazon, )
  - [Etsy Order and Material Tracking Spreadsheet (update)](https://www.reddit.com/r/EtsySellers/comments/lfp7y3/etsy_order_and_material_tracking_spreadsheet/) (reddit:r/EtsySellers, )

## 5. Product research & supplier comparison workspace — score 3.0
- Sellers score product ideas, compare suppliers, and track competitor features by hand in homemade spreadsheets and get flooded with supplier information.
- Items: 3 · paying signals: 1 · engagement: 0 · who: small_business 2, hobbyist 1
- Fit 0.75: LLM-based extraction and scoring of supplier quotes and competitor listings suits the builder. The market is crowded with research suites.
- Product idea: Workspace that ingests supplier quotes and competitor listings and uses LLM extraction to build a structured scoring matrix.
- Evidence:
  - [Product Research Spreadsheet : r/ecommerce - Reddit](https://www.reddit.com/r/ecommerce/comments/gho2sj/product_research_spreadsheet/) (reddit:r/ecommerce, ) — "I'm building out a giant database to make product research more effective."
  - [Spreadsheet for Amazon Market Analysis - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/7xbgfw/spreadsheet_for_amazon_market_analysis/) (reddit:r/FulfillmentByAmazon, )
  - [Product Sourcing Spreadsheet : r/FulfillmentByAmazon - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/6b7lly/product_sourcing_spreadsheet/) (reddit:r/FulfillmentByAmazon, )

## 6. Order routing to unintegrated suppliers & shipping tools — score 3.0
- Merchants re-enter orders by hand on print-on-demand supplier dashboards, cancel orders twice across the marketplace and the shipping tool, need a separate account per country, and copy tracking numbers by hand when combining shipments.
- Items: 3 · paying signals: 2 · engagement: 0 · who: small_business 3
- Fit 0.6: Automation glue can be built, but each supplier without an API may need browser automation that breaks often and adds support.
- Product idea: Order relay that forwards Shopify orders to any supplier via email, CSV, or browser automation and syncs tracking numbers back, including for merged shipments.
- Evidence:
  - [Anyone Use Shipstation? I Have a Problem With Them](https://www.reddit.com/r/ecommerce/comments/3tn84r/anyone_use_shipstation_i_have_a_problem_with_them/) (reddit:r/ecommerce, ) — "I would use shipstation again if it is not so tedious."
  - [Looking for an API to manually fulfil orders - Print on Demand](https://www.reddit.com/r/ecommerce/comments/xvi6e0/looking_for_an_api_to_manually_fulfil_orders/) (reddit:r/ecommerce, ) — "it takes a long time to manually fulfil each order. We've been trying to figure out how to automate this for a while."
  - [How do you manually enter tracking numbers for packages?](https://www.reddit.com/r/EtsySellers/comments/15i45js/how_do_you_manually_enter_tracking_numbers_for/) (reddit:r/EtsySellers, )

## 7. Cheap multichannel listing sync & bulk edit — score 2.8
- Syncing listings between Shopify and Etsy costs too much in app fees, bulk-editing listing settings is clumsy, and themes are locked to one platform.
- Items: 3 · paying signals: 1 · engagement: 0 · who: small_business 3
- Fit 0.7: Self-serve SaaS, but the market is competitive, and platform API changes plus sync edge cases raise support load.
- Product idea: Flat-price Shopify-Etsy listing sync with a spreadsheet-style bulk editor.
- Evidence:
  - [Syncing Shopify Store to Etsy : r/EtsySellers - Reddit](https://www.reddit.com/r/EtsySellers/comments/12fqz33/syncing_shopify_store_to_etsy/) (reddit:r/EtsySellers, ) — "I shouldn't get into paying for apps and integrations until I start making some sales"
  - [Template use among different ecommerce engines. - Reddit](https://www.reddit.com/r/ecommerce/comments/1trlrw/template_use_among_different_ecommerce_engines/) (reddit:r/ecommerce, )
  - [Is there a way to mass edit listings? : r/EtsySellers - Reddit](https://www.reddit.com/r/EtsySellers/comments/18vna2t/is_there_a_way_to_mass_edit_listings/) (reddit:r/EtsySellers, )

## 8. Demand forecasting & reorder planning — score 1.7
- Small merchants forecast demand by hand in spreadsheets, and bad forecasts leave them paying to carry excess inventory.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.85: Time-series forecasting is a core ML strength, and the tool is self-serve once connected.
- Product idea: Shopify and Amazon app that forecasts per-SKU demand and recommends reorder quantities and dates.
- Evidence:
  - [What do you use for demand forecasting? : r/ecommerce - Reddit](https://www.reddit.com/r/ecommerce/comments/axywcx/what_do_you_use_for_demand_forecasting/) (reddit:r/ecommerce, ) — "I find myself spending a lot of time trying to pull my sales data into a spreadsheet... Any excess inventory I buy and sit on costs me interest on the credit card"

## 9. Marketplace-to-bookkeeping sync — score 1.6
- Sellers can't automatically push order, fee, and shipping expense data into their bookkeeping tools, so they enter rows by hand.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.8: An integration connector is self-serve and repeatable. Mapping only records transactions and gives no tax advice, so it stays out of regulated territory.
- Product idea: Connector that posts categorized marketplace payouts, fees, and shipping costs to QuickBooks or Xero as journal entries.
- Evidence:
  - [Is there anything that would allow me to pull in all my Etsy ...](https://www.reddit.com/r/EtsySellers/comments/n9xv46/is_there_anything_that_would_allow_me_to_pull_in/) (reddit:r/EtsySellers, ) — "contact Janet LeBlanc, who designed the spreadsheets"

## 10. Shipping cost & FBA fee auditing — score 1.5
- Small merchants struggle with high shipping costs, and wrong dimensions and weights on listings cause FBA fulfillment overcharges that are hard to check.
- Items: 2 · paying signals: 0 · engagement: 0 · who: small_business 2
- Fit 0.75: Rule-based audits of FBA fee data against catalog dimensions are self-serve analytics, while cutting carrier rates depends on negotiated partnerships.
- Product idea: Tool that flags SKUs where Amazon's measured dimensions or fee tier don't match the seller's specs and estimates the overcharge.
- Evidence:
  - [For those who manually ship their product out, what's the ...](https://www.reddit.com/r/ecommerce/comments/x0it0g/for_those_who_manually_ship_their_product_out/) (reddit:r/ecommerce, )
  - [Fulfillment Fees : r/FulfillmentByAmazon - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/13w1dgm/fulfillment_fees/) (reddit:r/FulfillmentByAmazon, )

## 11. FBA reimbursement finder — score 1.4
- FBA sellers have trouble finding and claiming reimbursements Amazon owes for lost, damaged, or unfulfillable inventory and fees.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.7: Detection from SP-API reports can be automated and self-serve. Existing competitors mostly file the claims for sellers, which is service-like, but a DIY claim generator avoids that.
- Product idea: Self-serve scanner that reconciles FBA inventory and fee reports and generates ready-to-paste reimbursement case text.
- Evidence:
  - [Is there software that allows you to get money back from ...](https://www.reddit.com/r/FulfillmentByAmazon/comments/7d9qqk/is_there_software_that_allows_you_to_get_money/) (reddit:r/FulfillmentByAmazon, ) — "Amazon in general owes merchants a lot of backdue fees, unfulfillable items, etc for FBA. Is there a program that gathers this data"

## 12. Early review generation — score 1.0
- New sellers struggle to get their first reviews and have to request them by hand or through software.
- Items: 1 · paying signals: 1 · engagement: 0 · who: small_business 1
- Fit 0.5: Amazon's Request-a-Review automation is easy to build but already commoditized, and marketplace terms of service limit anything beyond it.
- Product idea: Automated Request-a-Review sender with timing optimized per product.
- Evidence:
  - [As a new seller I feel it's almost impossible to be ... - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/gvss6z/as_a_new_seller_i_feel_its_almost_impossible_to/) (reddit:r/FulfillmentByAmazon, ) — "manually (or via software) message each customer after their purchase and request a review"

## 13. Handmade product pricing calculator — score 0.8
- Handmade sellers struggle to set prices that cover materials, labor, and fees, and fall back on homemade spreadsheets.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.8: Simple self-serve SaaS with low support, though willingness to pay is low for hobbyist-level sellers.
- Product idea: Etsy-connected pricing calculator that tracks material costs and labor and suggests prices that hit a target margin after fees.
- Evidence:
  - [Here is the spreadsheet I created a to determine the prices ...](https://www.reddit.com/r/EtsySellers/comments/ljtxmi/here_is_the_spreadsheet_i_created_a_to_determine/) (reddit:r/EtsySellers, )

## 14. FBA inbound shipment planner — score 0.6
- FBA inbound rules such as pallet height limits and forced shipment splits make shipments hard to plan and follow.
- Items: 1 · paying signals: 0 · engagement: 0 · who: small_business 1
- Fit 0.6: A rules engine plus a packing optimizer is feasible as software, but Amazon changes the rules often and the audience is narrow.
- Product idea: Planner that validates cartons and pallets against current FBA inbound rules and previews split outcomes before creating a shipment.
- Evidence:
  - [Just a rant but getting really sick of splitting ... - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/a0lvqg/just_a_rant_but_getting_really_sick_of_splitting/) (reddit:r/FulfillmentByAmazon, )

## 15. Payment fees, holds, chargebacks & high-risk processing — score 0.0
- Merchants face high processing fees, opaque transaction holds, chargeback losses, FX losses on refunds, and refusals from processors when they sell in high-risk categories.
- Items: 8 · paying signals: 5 · engagement: 0 · who: small_business 8
- Fit 0.2: Fixing these needs acquiring relationships, underwriting, and financial compliance, and chargeback disputes are service-heavy. · **excluded: regulated**
- Product idea: Chargeback evidence-packet generator (the only self-serve piece of this cluster).
- Evidence:
  - [Payment processing fees are killing me. : r/ecommerce - Reddit](https://www.reddit.com/r/ecommerce/comments/16j0ied/payment_processing_fees_are_killing_me/) (reddit:r/ecommerce, ) — "Payment processing fees are killing me."
  - [Do Not Use Stripe!!! This is your warning. Learn from my ...](https://www.reddit.com/r/ecommerce/comments/wa20e0/do_not_use_stripe_this_is_your_warning_learn_from/) (reddit:r/ecommerce, ) — "There is a hard cap (I found out, in my case, $10k) which has to be manually increased"
  - ['high risk payment gateways' : r/shopify - Reddit](https://www.reddit.com/r/shopify/comments/nqds5n/high_risk_payment_gateways/) (reddit:r/shopify, ) — "won't onboard me due to not having proof of turnover of 20k USD a month"
  - [I refunded more than my customers paid! : r/shopify - Reddit](https://www.reddit.com/r/shopify/comments/goxn18/i_refunded_more_than_my_customers_paid/) (reddit:r/shopify, ) — "the actual USD amount I refunded is more than the USD amount I"
  - [BEWARE. Etsy Manually Charging Fees via "Square ... - Reddit](https://www.reddit.com/r/EtsySellers/comments/jm3qbn/beware_etsy_manually_charging_fees_via_square/) (reddit:r/EtsySellers, ) — "the fee is 3.5% + $0.15 per transaction"

## 16. Vendor vetting, escrow & legal/tax advice — score 0.0
- Sellers can't vet 3PLs or setup agencies, have no protection when paying overseas suppliers up front, can't get useful help from Amazon Seller Support, and lack trustworthy legal and tax advice.
- Items: 5 · paying signals: 3 · engagement: 0 · who: small_business 4, hobbyist 1
- Fit 0.15: The fixes are escrow (regulated), legal and tax advice (regulated), or review marketplaces that need moderation and a critical mass of users. · **excluded: regulated**
- Product idea: Verified-review directory of 3PLs and agencies.
- Evidence:
  - [Wealth Assistants : r/FulfillmentByAmazon - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/17lbwl5/wealth_assistants/) (reddit:r/FulfillmentByAmazon, ) — "paid their set up fee recently and they went out of business before they delivered on store setup"
  - [Almost fell for a dumb guru course. : r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/bgzz7g/almost_fell_for_a_dumb_guru_course/) (reddit:r/FulfillmentByAmazon, ) — "The only information I would pay for in the beginning is for legal & tax advice"
  - [Big Problem - Supplier threatening to sue and not release ...](https://www.reddit.com/r/FulfillmentByAmazon/comments/6q1yt0/big_problem_supplier_threatening_to_sue_and_not/) (reddit:r/FulfillmentByAmazon, ) — "not release goods that I've already paid 100% for"
  - [Man, do I hate Amazon merchant support. They are ... - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/y00yos/man_do_i_hate_amazon_merchant_support_they_are/) (reddit:r/FulfillmentByAmazon, )
  - [Did you regret going 3PL? : r/FulfillmentByAmazon - Reddit](https://www.reddit.com/r/FulfillmentByAmazon/comments/ghscaq/did_you_regret_going_3pl/) (reddit:r/FulfillmentByAmazon, )
