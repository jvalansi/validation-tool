# architecture-interiors pain points — ranked

Items scanned: 914 (reddit 914); labelled as pains: 350.
Score = count × (1 + share with paying signal) × fit. Fit and clustering are Claude judgements, not measurements.

## 1. Consumer room and furniture layout planner — score 37.05
- Homeowners and renters can't make a to-scale plan from photos or listing floorplans, test and compare furniture/TV layouts against clearances, or preview finishes and renovations reliably, so they rely on Canva, AI images and crowd feedback.
- Items: 36 · paying signals: 21 · engagement: 10805 · who: hobbyist 28, unknown 7, student 1
- Fit 0.65: Self-serve consumer software that suits ML (floorplan scale calibration, layout optimization, rendering); consumer willingness to pay and marketing cost are the risk.
- Product idea: Upload a floorplan image or room photo, calibrate scale, then get AI-generated to-scale furniture layout options checked against clearance rules and rendered.
- Evidence:
  - [Small/narrow bathroom redesign – foresty green tiles: good idea or mistake?](https://www.reddit.com/r/InteriorDesign/comments/1qmr2ek/smallnarrow_bathroom_redesign_foresty_green_tiles/) (reddit:r/InteriorDesign, 2026-01-25) — "The AI generated image using tiles we're considering makes it look fine, but suspect they could be darker in real life"
  - [Where would you put a TV?](https://www.reddit.com/r/InteriorDesign/comments/1ttve5s/where_would_you_put_a_tv/) (reddit:r/InteriorDesign, 2026-06-01) — "I'd consider making the framing of the fireplace smaller to accommodate"
  - [Would it be insane to use a backwards bookcase as a headboard?](https://www.reddit.com/r/InteriorDesign/comments/1uqr5jd/would_it_be_insane_to_use_a_backwards_bookcase_as/) (reddit:r/InteriorDesign, 2026-07-08) — "everyone is wasting their time suggesting things that won't work because the image doesn't contain all the details"
  - [Thinking about expanding a 3x3 window to 5x5 or 6x6, worth it?](https://www.reddit.com/r/InteriorDesign/comments/1v2iqcq/thinking_about_expanding_a_3x3_window_to_5x5_or/) (reddit:r/InteriorDesign, 2026-07-21) — "Thinking about expanding a 3x3 window to 5x5 or 6x6... before committing"
  - [Are these sofas too large for my space?](https://www.reddit.com/r/InteriorDesign/comments/1qxut63/are_these_sofas_too_large_for_my_space/) (reddit:r/InteriorDesign, 2026-02-06) — "I'm open to returning a couch"

## 2. Batch CAD file processing and LISP routine library — score 31.2
- Drafters apply standards, purge layers, sanitize proprietary blocks, convert thousands of DWGs to PDF and sync layer/block libraries file by file, and depend on fragile, disappearing LISP routines.
- Items: 28 · paying signals: 20 · engagement: 846 · who: employee 21, small_business 5, enterprise 1
- Fit 0.65: Batch processing can run headless (e.g. ODA/LibreDWG) as a self-serve web or desktop tool; the user base is fragmented and lower-paying.
- Product idea: Cloud batch DWG processor with recipes for purge/sanitize, apply layer standards, bulk title block edits and DWG-to-PDF conversion, plus a hosted searchable LISP routine library.
- Evidence:
  - [Purge unused . Purge unused . Purge unused](https://www.reddit.com/r/Revit/comments/1c5sfmq/purge_unused_purge_unused_purge_unused/) (reddit:r/Revit, 2024-04-16) — "The file is 600MB"
  - [Do you use lisp, and are there tools you are missing?](https://www.reddit.com/r/AutoCAD/comments/1tif46x/do_you_use_lisp_and_are_there_tools_you_are/) (reddit:r/AutoCAD, 2026-05-20) — "i use a lot of lisp routines for the most basic tasks and made another one (with AI) just last week"
  - [Trying to find someone that wants to make a little cash on the side for some autocad work](https://www.reddit.com/r/AutoCAD/comments/1uyn47y/trying_to_find_someone_that_wants_to_make_a/) (reddit:r/AutoCAD, 2026-07-17) — "Trying to find someone that wants to make a little cash on the side for some autocad work"
  - [Huge file](https://www.reddit.com/r/AutoCAD/comments/1qhkiry/huge_file/) (reddit:r/AutoCAD, 2026-01-19) — "It takes forever to remove layers because I have to open each one"
  - [Sharing MEP Revit model with Contractors outside of Arch Agreement?](https://www.reddit.com/r/Revit/comments/1ol2qp0/sharing_mep_revit_model_with_contractors_outside/) (reddit:r/Revit, 2025-10-31) — "we would have the contractor sign a CAD release form then we would export the work to CAD then purge almost everything out"

## 3. Small A/E firm project, fee and time management — score 27.3
- Small architecture and design firms run projects, timesheets, fees, scope creep, staffing and invoicing across scattered spreadsheets because Deltek and ArchiOffice are costly and clunky, and generic tools like Asana need too much setup.
- Items: 22 · paying signals: 17 · engagement: 650 · who: small_business 14, employee 6, freelancer 2
- Fit 0.7: Self-serve multi-tenant SaaS with no hardware; the market has incumbents but fixed-fee and scope-creep tracking for 1-20 person firms is underserved and can be sold without sales calls.
- Product idea: Lightweight project tracker for small architecture firms that ties fixed-fee budgets, timesheets and scope-change logs together and shows burn and overrun alerts to the firm and its client.
- Evidence:
  - [Just did a post-mortem on a recent job and I’m pretty sure I paid the client to work for them. How do you guys stop this?](https://www.reddit.com/r/Architects/comments/1qu6ydq/just_did_a_postmortem_on_a_recent_job_and_im/) (reddit:r/Architects, 2026-02-02) — "my hourly rate probably dropped below minimum wage... I'm genuinely desperate for a better workflow"
  - [My architecture degree broke me, and now I'm stuck in a soul-crushing project management job. Can anyone relate?](https://www.reddit.com/r/architecture/comments/1nfqye3/my_architecture_degree_broke_me_and_now_im_stuck/) (reddit:r/architecture, 2025-09-13) — "It's just endless spreadsheets, emails, and checking invoices that have already been c"
  - [I hate trying to determine fair fees.](https://www.reddit.com/r/architecture/comments/1eutnd0/i_hate_trying_to_determine_fair_fees/) (reddit:r/architecture, 2024-08-17) — "There were easier ways to make minimum wage!"
  - [Deltek vs. everybody](https://www.reddit.com/r/Architects/comments/1dhm0qe/deltek_vs_everybody/) (reddit:r/Architects, 2024-06-17) — "Deltek Vision Cloud... and 25 year old spreadsheets... the lack of integration of our tools is a problem"
  - [My architecture firm is working hours on projects beyond budget, but not charging for them, because they don't want to lose the bid for clients who are asking for too many changes???](https://www.reddit.com/r/Architects/comments/14antg1/my_architecture_firm_is_working_hours_on_projects/) (reddit:r/Architects, 2023-06-16) — "working overtime hours without charging... so that we don't lose the bid"

## 4. Revit/AutoCAD data round-trip with spreadsheets — score 25.9
- Users can't easily push and pull parameters, schedules, title block fields, block attributes, BOMs, keynotes and shared parameters between Revit/AutoCAD and Excel or Google Sheets, so they pay for aggressive add-ins or write LISP/VBA.
- Items: 23 · paying signals: 14 · engagement: 462 · who: employee 15, small_business 3, developer 3
- Fit 0.7: A narrow, well-defined plugin plus web app that AI agents can build against documented APIs; it needs Windows/Revit testing but support stays flat.
- Product idea: Low-cost Revit and AutoCAD add-in that syncs element parameters, title blocks and block attributes two ways with Google Sheets/Excel.
- Evidence:
  - [Request from a Consultant](https://www.reddit.com/r/Revit/comments/1qjfl2m/request_from_a_consultant/) (reddit:r/Revit, 2026-01-22) — "Don't make us download and open your model and dig through to find it"
  - [Whatever you do, do not call about Axiom Revit add-ins](https://www.reddit.com/r/Architects/comments/1txmrtk/whatever_you_do_do_not_call_about_axiom_revit/) (reddit:r/Architects, 2026-06-05) — "I needed a simple & fairly cheap script or add-in to link a spreadsheet into Revit"
  - [I'm trying to find the area of multiple rooms](https://www.reddit.com/r/AutoCAD/comments/hx5lzl/im_trying_to_find_the_area_of_multiple_rooms/) (reddit:r/AutoCAD, 2020-07-24) — "I would rather not manually go through each room and add them up via a spreadsheet"
  - [Revit Titleblocks & Parameters](https://www.reddit.com/r/Revit/comments/1r3ycs6/revit_titleblocks_parameters/) (reddit:r/Revit, 2026-02-13) — "If I were to load in their titleblocks every time, I would have to adjust our parameters every time."
  - [DiRoots. Previous versions](https://www.reddit.com/r/Revit/comments/1pb5s2s/diroots_previous_versions/) (reddit:r/Revit, 2025-12-01) — "Does anyone have a copy ... of DiRoots *pre* having to pay for it?"

## 5. Scan/PDF/image to clean CAD vectors — score 21.75
- Scanned plans, PDF floor plans, images and fragmented consultant linework have to be traced or cleaned by hand into closed polylines, rooms and areas because existing converters give poor output; GIS and site data to CAD has the same problem.
- Items: 18 · paying signals: 11 · engagement: 458 · who: unknown 6, employee 4, small_business 4
- Fit 0.75: An ML-heavy vision problem that matches the builder's skills and sells as self-serve pay-per-conversion; the technical bar for accuracy is high.
- Product idea: Web tool that converts scanned or PDF floor plans into layered DWG/DXF with closed room polylines, snapped dimensions and an area schedule.
- Evidence:
  - [Best way to convert scanned PDF plans to AutoCAD efficiently?](https://www.reddit.com/r/AutoCAD/comments/1gbxzbs/best_way_to_convert_scanned_pdf_plans_to_autocad/) (reddit:r/AutoCAD, 2024-10-25) — "I tried using tools like Scan2CAD... fixing the result would take almost as much time as drawing everything from scratch."
  - [large TIFF building plan to DWG](https://www.reddit.com/r/AutoCAD/comments/1q2smpp/large_tiff_building_plan_to_dwg/) (reddit:r/AutoCAD, 2026-01-03) — "I am currently trying Print2CAD program with different settings, no luck yet"
  - [Newbie Question: Converting PDF to AutoCad](https://www.reddit.com/r/AutoCAD/comments/1qkyo5z/newbie_question_converting_pdf_to_autocad/) (reddit:r/AutoCAD, 2026-01-23) — "I have a contractor asking the I convert my survey ... how can I get this done?"
  - [Post keeps being removed?](https://www.reddit.com/r/AutoCAD/comments/1tt24cb/post_keeps_being_removed/) (reddit:r/AutoCAD, 2026-05-31) — "He's been trying to redraw"
  - [How would you all recommend converting raster plans to dwg (or any other vectoral format)? other than having to do it manually?](https://www.reddit.com/r/Architects/comments/1u4x9m7/how_would_you_all_recommend_converting_raster/) (reddit:r/Architects, 2026-06-13) — "I would accept any workflow even if it is 70% accurate"

## 6. BIM model auditing, standards and content library — score 21.0
- Firms can't audit or enforce Revit modeling standards, templates, family naming, client deliverable checks or rule-based coordination checks, and they lack a maintained, searchable source of quality families and living standards docs.
- Items: 22 · paying signals: 13 · engagement: 4164 · who: employee 11, small_business 6, freelancer 2
- Fit 0.6: Rule-based model checking is software-only and multi-tenant, but it needs deep Revit API knowledge and firm-specific rules may pull in onboarding support.
- Product idea: Revit add-in plus dashboard that runs configurable standards and coordination rules (naming, hidden elements, proximity rules) and reports violations per model.
- Evidence:
  - [AI in architecture is frighteningly inaccurate](https://www.reddit.com/r/architecture/comments/1pdmv1u/ai_in_architecture_is_frighteningly_inaccurate/) (reddit:r/architecture, 2025-12-04) — "this particular person is advertising themselves as a full service render, BIM and documentation service"
  - [Babysitting MEP](https://www.reddit.com/r/Architects/comments/1sunes5/babysitting_mep/) (reddit:r/Architects, 2026-04-24) — "Constant follow-ups, pinging them over and over just to get a simple update pushed."
  - [What’s everyone’s thoughts: wall sweeps or model in place for interior baseboard and crowns?](https://www.reddit.com/r/Revit/comments/1r8nxh4/whats_everyones_thoughts_wall_sweeps_or_model_in/) (reddit:r/Revit, 2026-02-19) — "This is a constant debate and source of tension in the office"
  - [Trying to become a Revit God. Any advanced good / best practice / tutorials or courses ?](https://www.reddit.com/r/Revit/comments/q26a2l/trying_to_become_a_revit_god_any_advanced_good/) (reddit:r/Revit, 2021-10-05) — "Any advanced good / best practice / tutorials or courses ?"
  - [General Architectural Notes](https://www.reddit.com/r/Architects/comments/1eanjnp/general_architectural_notes/) (reddit:r/Architects, 2024-07-24) — "We have a bad habit of copying notes from project to project and editing (if even) to suite the project."

## 7. Spreadsheet-driven parametric drawing generation — score 14.5
- Fabricators, electrical/solar designers, installers and framers redraw custom parts, panel schematics, single-line diagrams, cable schedules, framing plans and cut lists by hand instead of generating them from a component list or parameters.
- Items: 17 · paying signals: 12 · engagement: 537 · who: employee 9, small_business 5, hobbyist 1
- Fit 0.5: Generating DXF/PDF from structured input is pure software, but each vertical (solar, panels, sheet metal, framing) has its own conventions, which fragments the market.
- Product idea: Web app that generates DXF/PDF drawings and schedules from a spreadsheet of components or dimensions using reusable parametric templates, starting with one vertical (e.g. solar single-line diagrams).
- Evidence:
  - [Is Revit Right for Me](https://www.reddit.com/r/Revit/comments/1uy3dwl/is_revit_right_for_me/) (reddit:r/Revit, 2026-07-16) — "Sometimes it will take us longer to draw something in AutoCAD then it does to lay it out in the shop!"
  - [Circuit diagrams in ACAD (not acad electrical)](https://www.reddit.com/r/AutoCAD/comments/1pkw0a7/circuit_diagrams_in_acad_not_acad_electrical/) (reddit:r/AutoCAD, 2025-12-12) — "I spend too much time on drawing"
  - [Contractor Question](https://www.reddit.com/r/AutoCAD/comments/1ret7ei/contractor_question/) (reddit:r/AutoCAD, 2026-02-25) — "I cant afford to hire someone to do a rendering and drawing for a deck, but it looks so professional to show up with a rendering and a plan"
  - [Looking for an AutoCAD/Excel Consultant](https://www.reddit.com/r/AutoCAD/comments/1jp4xrv/looking_for_an_autocadexcel_consultant/) (reddit:r/AutoCAD, 2025-04-01) — "Does anyone have any recommendations on where to find someone that would be able to streamline this process?"
  - [Drawing lines within a block based on an attribute value](https://www.reddit.com/r/AutoCAD/comments/sn4221/drawing_lines_within_a_block_based_on_an/) (reddit:r/AutoCAD, 2022-02-07) — "I have hundreds of these to create and dont want to do it manually"

## 8. ARE and NCIDQ exam prep — score 13.8
- ARE and NCIDQ candidates pay for expensive, fragmented prep materials that don't match the real exam, lose access after vendor policy changes, and lack reliable reviews or practice questions.
- Items: 13 · paying signals: 10 · engagement: 438 · who: employee 11, student 2
- Fit 0.6: Self-serve content and quiz software scales without support, but question accuracy needs domain expertise and the exam's content rights are restricted.
- Product idea: Low-cost adaptive practice-question bank for ARE/NCIDQ divisions with explanations citing public code references and one-time lifetime access.
- Evidence:
  - [Avoid YoungArchitectsAcademy, they took my $300 and essentially blocked me from contacting them](https://www.reddit.com/r/Architects/comments/1waa0us/avoid_youngarchitectsacademy_they_took_my_300_and/) (reddit:r/Architects, 2026-09-08) — "I bought their package, which cost me over $300."
  - [1 for 3 for ARE exams. Want to vent.](https://www.reddit.com/r/Architects/comments/1mxjsvg/1_for_3_for_are_exams_want_to_vent/) (reddit:r/Architects, 2025-08-22) — "after looking at these AIA contacts for 4-5 months in a row"
  - [ARE study guides to avoid](https://www.reddit.com/r/Architects/comments/1fn7jby/are_study_guides_to_avoid/) (reddit:r/Architects, 2024-09-23) — "before spending several hundred dollars (or potentially more)"
  - [ARE exam prep.](https://www.reddit.com/r/architecture/comments/vnuwu8/are_exam_prep/) (reddit:r/architecture, 2022-06-30) — "If I'm going to dish out several hundred dollars I would like the best quality."
  - [Question about the NCIDQ IDFX Test](https://www.reddit.com/r/InteriorDesign/comments/19d42yi/question_about_the_ncidq_idfx_test/) (reddit:r/InteriorDesign, 2024-01-22) — "going through QPractice and have been reading out of Ballast's interior design reference manual and guide to interior/construction details, as well as Harmon's guide to the codebooks"

## 9. Drawing set revision diff, register and transmittals — score 11.9
- Architects compare revised PDF sets page by page by eye, track drawing registers and sheet indexes in copied Excel tables, and contractors bid off the wrong set because permit/bid version control is weak.
- Items: 8 · paying signals: 6 · engagement: 631 · who: employee 7, small_business 1
- Fit 0.85: Pure software on PDFs that suits an ML engineer (sheet matching, visual diff, title block OCR); self-serve per-project pricing with little support load.
- Product idea: Upload two PDF drawing sets to get auto-matched sheets, visual diffs with revision clouds, an extracted sheet register and a generated transmittal.
- Evidence:
  - [Built a free offline PDF diff tool for architects over the weekends](https://www.reddit.com/r/Architects/comments/1ructt8/built_a_free_offline_pdf_diff_tool_for_architects/) (reddit:r/Architects, 2026-03-15) — "Kept spending hours manually checking what changed between revised drawing sets, page by page."
  - [Contractor used wrong set to bid the project and is now casting blame for change orders](https://www.reddit.com/r/architecture/comments/1cdzknh/contractor_used_wrong_set_to_bid_the_project_and/) (reddit:r/architecture, 2024-04-26) — "change orders are at 11% of the original cost"
  - [Update: I finished the free, offline PDF diff tool I shared here recently. The Beta is now live (and it auto-draws revision clouds)](https://www.reddit.com/r/Architects/comments/1ry4tpx/update_i_finished_the_free_offline_pdf_diff_tool/) (reddit:r/Architects, 2026-03-19) — "It turns out we all share this exact same bottleneck"
  - [Using Excel file to fill out Sheet Index](https://www.reddit.com/r/Revit/comments/1pnmq0u/using_excel_file_to_fill_out_sheet_index/) (reddit:r/Revit, 2025-12-15) — "I know there are many add-ons out there we can use but most of them require pa[yment]"
  - [Scheduling schedules?](https://www.reddit.com/r/Revit/comments/41wc51/scheduling_schedules/) (reddit:r/Revit, 2016-01-20) — "it's becoming overwhelming to try and keep track"

## 10. Stylized architectural visualization and presentation graphics — score 10.8
- Designers fiddle by hand to turn 3D models or CAD into isometric line-work, hand-sketch styles and presentation graphics, can't find diverse cutout people, and struggle with portfolio formatting and compression.
- Items: 11 · paying signals: 7 · engagement: 1405 · who: student 4, employee 3, freelancer 2
- Fit 0.6: AI image pipelines and asset libraries are self-serve and low-support, but the market is crowded with general AI render tools and has to compete on style quality.
- Product idea: Upload a SketchUp/Rhino export or CAD plan and get stylized line-work, sketch or post-digital collage renders with a diverse generated entourage library.
- Evidence:
  - [Bringing a flat CAD section to life |  Spent the weekend drawing custom vector entourage and fixing lineweights for my project. What do you think?](https://www.reddit.com/r/Architects/comments/1va9t72/bringing_a_flat_cad_section_to_life_spent_the/) (reddit:r/Architects, 2026-07-29) — "Spent the weekend drawing custom vector entourage and fixing lineweights for my project."
  - [Is there an inexpensive online course aimed at making these kind of illustrations? (Very detailed, kinda like a Bartlett drawing that actually makes sense)](https://www.reddit.com/r/Architects/comments/1rezm87/is_there_an_inexpensive_online_course_aimed_at/) (reddit:r/Architects, 2026-02-26) — "I'm not willing to pay thousands of dollars for an actual course. Is there an online alternative that teaches this for less?"
  - [I made a collection of cutout people from Africa for Architecture Visualization](https://www.reddit.com/r/architecture/comments/1ahtvz9/i_made_a_collection_of_cutout_people_from_africa/) (reddit:r/architecture, 2024-02-03) — "Finding pictures of African people for architecture visualization is a real struggle."
  - [Isometric rendering help?!](https://www.reddit.com/r/architecture/comments/1tohhu/isometric_rendering_help/) (reddit:r/architecture, 2013-12-25) — "is there a tool out there to model and render like this without lots of fiddling around?"
  - [I'm sick and tired of Google Slides and PowerPoint, so I'm making an app for Design Proposals that's not so tedious and boring, but focuses on conveying my ideas better. What bugs you guys the most about those apps and which modern features do you really want?](https://www.reddit.com/r/Architects/comments/1ntn4tr/im_sick_and_tired_of_google_slides_and_powerpoint/) (reddit:r/Architects, 2025-09-29) — "I hate formatting pictures and text, it takes forever"

## 11. Interior designer sourcing, selections and billing — score 10.5
- Interior designers source products across vendor sites, track SKUs, prices, client selections, sign-offs and budgets in spreadsheets, and make billing errors on long multi-order projects because Studio Designer is too expensive for solos.
- Items: 9 · paying signals: 6 · engagement: 128 · who: small_business 3, freelancer 2, unknown 2
- Fit 0.7: Self-serve SaaS for solo designers with an AI product-clipper is buildable; competition exists (Programa, Houzz Pro) but they are priced and built for firms.
- Product idea: Browser clipper plus room-by-room spec board that captures product data from any vendor page, collects client approvals and rolls up budget and invoices.
- Evidence:
  - [Messy accounting with Interior Designer](https://www.reddit.com/r/InteriorDesign/comments/a8xp7z/messy_accounting_with_interior_designer/) (reddit:r/InteriorDesign, 2018-12-23) — "I put in a large order over many months for a full house... I've found errors in billing from my interior designer."
  - [Going crazy trying to manage client decisions (for material & products selections). Suggestions for great apps or best practices? [Currently using email, PDFs, and spreadsheets..kill me]](https://www.reddit.com/r/InteriorDesign/comments/5rjaet/going_crazy_trying_to_manage_client_decisions_for/) (reddit:r/InteriorDesign, 2017-02-02) — "Currently using email, PDFs, and spreadsheets..kill me ... Any help appreciated. You'll make my year."
  - [Do architecture firms also spend huge amounts of time on product sourcing/specs?](https://www.reddit.com/r/architecture/comments/1rqfzov/do_architecture_firms_also_spend_huge_amounts_of/) (reddit:r/architecture, 2026-03-11) — "I had ~25 tabs open just trying to track down specs, pricing, and availability for a single sectional... dozens, sometimes hundreds of products."
  - [What is easy to learn interior design software?](https://www.reddit.com/r/InteriorDesign/comments/5wl36l/what_is_easy_to_learn_interior_design_software/) (reddit:r/InteriorDesign, 2017-02-28) — "My mom wants to transition into helping clients design the interior of their homes on the side"
  - [Advice: Designer over budget](https://www.reddit.com/r/InteriorDesign/comments/1h6iysj/advice_designer_over_budget/) (reddit:r/InteriorDesign, 2024-12-04) — "Her fee ended up at $14, over 3x her original estimate"

## 12. Construction administration RFI, submittal and markup tracking — score 6.6
- RFIs, shop drawing reviews, Bluebeam comments, change orders and consultant markups are tracked by hand across PDFs and email, which wipes out profit during CA.
- Items: 6 · paying signals: 5 · engagement: 538 · who: employee 5, small_business 1
- Fit 0.6: Self-serve SaaS with AI extraction of PDF comments is feasible; Procore-style incumbents serve contractors more than small architects, so a niche exists.
- Product idea: Architect-side CA log that extracts PDF markup comments from submittals, threads them like pull requests and drafts RFI responses from the drawing set.
- Evidence:
  - [My boss just asked me to find an AI tool that can track submittal comments…](https://www.reddit.com/r/Architects/comments/1gksbc7/my_boss_just_asked_me_to_find_an_ai_tool_that_can/) (reddit:r/Architects, 2024-11-06) — "My boss just asked me to find an AI tool that can track submittal comments (340k commercial project)"
  - [I hate being a PM / construction admin](https://www.reddit.com/r/Architects/comments/10ev80w/i_hate_being_a_pm_construction_admin/) (reddit:r/Architects, 2023-01-18) — "I can't stand pushing paper all day. Answering RFIs all day and reviewing shop drawings."
  - [Stress stress stress / Do I stay in Arch??](https://www.reddit.com/r/Architects/comments/1vmv3oa/stress_stress_stress_do_i_stay_in_arch/) (reddit:r/Architects, 2026-08-13) — "random CA fires that show up and blow up my day/week"
  - [What tools do you use for tracking markups/changes that need to be implemented from designers/engineers/clients etc](https://www.reddit.com/r/Revit/comments/1u659ta/what_tools_do_you_use_for_tracking_markupschanges/) (reddit:r/Revit, 2026-06-15) — "We just end up with a mess of emails with partial replies... Wishing we had a well-agreed on system like developers have with Github"
  - [Recommendations for how to Manage Construction Administration “CA” on a Project](https://www.reddit.com/r/Architects/comments/pdb47q/recommendations_for_how_to_manage_construction/) (reddit:r/Architects, 2021-08-28) — "Our principals never budget the correct amount of time and money it takes... shooting way past our numbers"

## 13. Revit/CAD training and onboarding — score 6.3
- Career changers, SketchUp/AutoCAD switchers and small offices lack affordable, current, hands-on Revit/MEP and niche Civil 3D training and want live guidance beyond YouTube.
- Items: 11 · paying signals: 7 · engagement: 396 · who: employee 4, student 3, small_business 2
- Fit 0.35: Course content could be self-serve, but the demand is for live hands-on guidance, which is service work, and free content competes heavily.
- Product idea: Interactive project-based Revit course with automated checking of submitted models against step goals.
- Evidence:
  - [Revit might have its problems but after using Archicad im never complaining again](https://www.reddit.com/r/Revit/comments/1u5yvpi/revit_might_have_its_problems_but_after_using/) (reddit:r/Revit, 2026-06-14) — "its been some painfull months"
  - [AutoCAD to BIM software](https://www.reddit.com/r/Revit/comments/it5f1v/autocad_to_bim_software/) (reddit:r/Revit, 2020-09-15) — "automated take offs (or quicker than my manual workings)"
  - [Am I totally screwed? ](https://www.reddit.com/r/Architects/comments/1dhlgba/am_i_totally_screwed/) (reddit:r/Architects, 2024-06-17) — "I hate vectorworks it is the worst program I have ever had to use!"
  - [Beginner Looking For Instruction](https://www.reddit.com/r/Revit/comments/1r3ad3l/beginner_looking_for_instruction/) (reddit:r/Revit, 2026-02-13) — "I've spent the week watching videos on YouTube and on LinkedIn Learning... But I am still having trouble creating anything on my own."
  - [Structured revit course](https://www.reddit.com/r/Revit/comments/1q2v6wb/structured_revit_course/) (reddit:r/Revit, 2026-01-03) — "I wanted to get him a course to learn... something structured with support would work best"

## 14. Building code analysis and permit drawing assistance — score 3.2
- Architects, contractors and owner-builders do egress, occupancy load and fire separation analyses by hand, type life-safety tags manually, and lack tools to turn designs into permit-ready drawings with code checks.
- Items: 5 · paying signals: 3 · engagement: 112 · who: small_business 2, employee 2, hobbyist 1
- Fit 0.4: Software can automate calculations, but code interpretation varies by jurisdiction and carries liability close to regulated professional advice, which raises accuracy and support burden.
- Product idea: Code analysis calculator that computes occupancy loads, egress widths and travel distances from a plan and outputs a cited code-analysis sheet for architect review.
- Evidence:
  - [NFPA 101/IBC = EVIL ... I . HATE . CODE](https://www.reddit.com/r/Architects/comments/17qthlq/nfpa_101ibc_evil_i_hate_code/) (reddit:r/Architects, 2023-11-08) — "takes me FOREVER, and inevitably something (or many) is wrong... why I've hit a wall in my career"
  - [Code Analysis](https://www.reddit.com/r/architecture/comments/4edudk/code_analysis/) (reddit:r/architecture, 2016-04-12) — "Its more work for me that I would rather an Architect do 99% of the time"
  - [Software options?](https://www.reddit.com/r/architecture/comments/11tyw2d/software_options/) (reddit:r/architecture, 2023-03-17) — "I've bought land with all the cash I have and now I'm trying to skip hiring an architect"
  - [Revit Room Tags in Life Safety Plans?](https://www.reddit.com/r/Architects/comments/1feh1f9/revit_room_tags_in_life_safety_plans/) (reddit:r/Architects, 2024-09-11)
  - [Need help with a formula](https://www.reddit.com/r/Revit/comments/1qy8r2x/need_help_with_a_formula/) (reddit:r/Revit, 2026-02-07)

## 15. Autodesk licensing, cloud outages and core tool limits — score 0.0
- Users resent subscription cost, licensing errors, cloud outages with no offline fallback, missing Mac support, version deprecations and core Revit/AutoCAD UX gaps, and some want on-demand expert drafting help.
- Items: 80 · paying signals: 42 · engagement: 4430 · who: employee 50, unknown 8, small_business 7
- Fit 0.15: The root causes sit inside Autodesk's products and licensing, so a competing CAD/BIM platform is far beyond 15 hours/week, and on-demand drafting help is per-client service work. · **excluded: no_software_solution**
- Product idea: None viable; at most a cloud status/offline-fallback monitor for ACC-hosted models.
- Evidence:
  - [How would you model an organic facade like this in Revit](https://www.reddit.com/r/Architects/comments/1pnyh6f/how_would_you_model_an_organic_facade_like_this/) (reddit:r/Architects, 2025-12-16) — "I've experimented with Massing, in place component, but I keep hitting Revit's geometric limits."
  - [Revit is killing my love of architecture & design](https://www.reddit.com/r/Revit/comments/t55xm8/revit_is_killing_my_love_of_architecture_design/) (reddit:r/Revit, 2022-03-02) — "After 15 years of using Revit"
  - [Having an existential crisis because of revit](https://www.reddit.com/r/architecture/comments/15ms63c/having_an_existential_crisis_because_of_revit/) (reddit:r/architecture, 2023-08-09) — "When in revit it was always frustrating like cut my wrist frustrating."
  - [I would not wish hatching a drawing in AutoCAD on my worst enemy](https://www.reddit.com/r/Architects/comments/1w7b0p5/i_would_not_wish_hatching_a_drawing_in_autocad_on/) (reddit:r/Architects, 2026-09-04) — "people seem far to accepting of this performance for such an expensive software"
  - [Sorry, but I need to rant](https://www.reddit.com/r/Revit/comments/1r4ztth/sorry_but_i_need_to_rant/) (reddit:r/Revit, 2026-02-14) — "For every one cool/interesting thing I learn Revit CAN do, I feel like I've found ten other things it CAN'T do"
