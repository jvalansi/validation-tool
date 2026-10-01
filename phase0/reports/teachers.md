# teachers pain points — ranked

Items scanned: 93 (reddit 93); labelled as pains: 46.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Custom grade weighting and policy calculator — score 9.6
- Teachers build multi-tab spreadsheets for weighted categories, custom scales, drop-lowest or replace-with-final policies, and 'what do I need' calculators because LMS gradebook math is opaque or inflexible.
- Items: 7 · paying signals: 5 · engagement: 0 · who: employee 7
- Fit 0.8: Pure deterministic software, easy to build and self-serve; the main risk is low willingness to pay, since spreadsheets are free.
- Product idea: Gradebook overlay that imports LMS/CSV scores, applies arbitrary grading policies, and publishes a student-facing 'what I need' view.
- Evidence:
  - [I need A good gradebook app/website : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/4w5abg/i_need_a_good_gradebook_appwebsite/) (reddit:r/Teachers, ) — "I need A good gradebook app/website"
  - [I grade homework on a 50-100% scale, and my grade ... - Reddit](https://www.reddit.com/r/teaching/comments/726jxo/i_grade_homework_on_a_50100_scale_and_my_grade/) (reddit:r/teaching, ) — "We're gonna use a function to calculate the new point value to enter into the gradebook."
  - [Grades spreadsheet or online tool to calculate student's ...](https://www.reddit.com/r/Professors/comments/ows06g/grades_spreadsheet_or_online_tool_to_calculate/) (reddit:r/Professors, ) — "Do any of you have a simple excel spreadsheet template I can use to calculate the final grade...Or an online tool"
  - [Keeping track of grades : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/16fkewo/keeping_track_of_grades/) (reddit:r/Professors, ) — "export the raw scores and use a spreadsheet to keep track of the grades"
  - [Points or Percentage for Course Grades? : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/8knt03/points_or_percentage_for_course_grades/) (reddit:r/Professors, ) — "I include a spreadsheet for students who want to see how well they need to do on future assignments to get their goal grade."

## 2. AI-assisted grading and feedback — score 8.5
- Teachers and instructors spend hours grading essays and repetitive work, dread large piles, and would pay out of pocket or per page to offload it.
- Items: 5 · paying signals: 5 · engagement: 0 · who: employee 5
- Fit 0.85: LLM rubric-based grading and feedback drafting is core ML work, self-serve and multi-tenant; crowded market (e.g. CoGrader, EssayGrader) and accuracy/trust concerns are the main risks.
- Product idea: Upload a rubric and a stack of submissions, get draft scores and editable feedback comments in the teacher's voice.
- Evidence:
  - [AI Detection : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/1dkf0xy/ai_detection/) (reddit:r/Teachers, ) — "Teacher friendly AI that saves hours every week"
  - [What's the most tedious part of teaching that could be fixed?](https://www.reddit.com/r/Teachers/comments/slprkd/whats_the_most_tedious_part_of_teaching_that/) (reddit:r/Teachers, ) — "I've been tempted to hire someone myself"
  - [How much would you pay to have someone else grade ... - Reddit](https://www.reddit.com/r/Teachers/comments/al9z03/how_much_would_you_pay_to_have_someone_else_grade/) (reddit:r/Teachers, ) — "Perhaps .20/single sided page, .40/page for worksheets, .30/page for tests with short answers.. Would you pay this?"
  - [Anyone else get exhausted grading essays and writing ... - Reddit](https://www.reddit.com/r/Professors/comments/12e19k4/anyone_else_get_exhausted_grading_essays_and/) (reddit:r/Professors, ) — "it's so tedious and the quality is more often than not so poor (or cribbed from ChatGPT) that getting through it is a real beast"
  - [I hate grading papers. Strategies for hating it less? - Reddit](https://www.reddit.com/r/Professors/comments/ndwnxr/i_hate_grading_papers_strategies_for_hating_it/) (reddit:r/Professors, ) — "I end up putting it off and then hating it even more when I have a huge pile of papers to grade in a short amount of time."

## 3. Teacher admin paperwork and planning — score 5.4
- Duplicate parent-contact logs, spreadsheet lesson-plan templates, ADHD-friendly to-do tracking and email overload create redundant clerical work.
- Items: 5 · paying signals: 4 · engagement: 0 · who: employee 5
- Fit 0.6: Simple self-serve tools, but needs are fragmented, general productivity apps compete, and district-mandated formats limit adoption.
- Product idea: Parent-contact log that drafts the email, logs it once, and schedules follow-up reminders.
- Evidence:
  - [I think I hate teaching : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/11aihdw/i_think_i_hate_teaching/) (reddit:r/teaching, ) — "spending a lot of my money for my classroom"
  - [Admins are annoying : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/j2bcaf/admins_are_annoying/) (reddit:r/teaching, ) — "Planning is taking so much time that I've had zero time to grade."
  - [Lesson plan template? : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/s016n/lesson_plan_template/) (reddit:r/teaching, ) — "I have a template in Excel/Google Spreadsheet that I fill in and update every week. But it still feels unwieldy."
  - [Teachers with adhd : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/azlhyl/teachers_with_adhd/) (reddit:r/teaching, ) — "I have to update it and then re-sort it each day ... that takes like ten minutes at most"
  - [Emails from admin : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/s6ky1c/emails_from_admin/) (reddit:r/Teachers, )

## 4. Affordable plagiarism and peer-copying detection — score 4.5
- Turnitin dominates and only works inside LMS workflows; teachers lack cheap tools to check standalone docs or compare submissions within a class for copying.
- Items: 4 · paying signals: 2 · engagement: 0 · who: employee 4
- Fit 0.75: Intra-class similarity (embeddings plus n-gram overlap) is simple, self-serve software; web-scale source matching is costly and competes directly with Turnitin.
- Product idea: Drop in a class's submissions and get a pairwise similarity heatmap with highlighted shared passages.
- Evidence:
  - [What is the free alternative plagiarism checker to Turnitin?](https://www.reddit.com/r/Teachers/comments/w2ezde/what_is_the_free_alternative_plagiarism_checker/) (reddit:r/Teachers, ) — "now we are considering to start using another one"
  - [I Hate Teaching College Juniors and Seniors That Are Still ...](https://www.reddit.com/r/Professors/comments/10wzr2r/i_hate_teaching_college_juniors_and_seniors_that/) (reddit:r/Professors, ) — "I had to report several students for plagiarism during the last round of grading I completed."
  - [Is there a tool for checking for plagiarism (of other ...](https://www.reddit.com/r/Teachers/comments/jcffmn/is_there_a_tool_for_checking_for_plagiarism_of/) (reddit:r/Teachers, )
  - [Manually checking a paper with TurnItIn? : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/ui90jt/manually_checking_a_paper_with_turnitin/) (reddit:r/Professors, )

## 5. Quiz platform to gradebook sync — score 3.75
- Scores from Blooket, Kahoot, Scantron-style tools and external quizzes must be exported, weighted and copied into Canvas or other gradebooks by hand.
- Items: 3 · paying signals: 2 · engagement: 0 · who: employee 3
- Fit 0.75: Integration software with flat support once connectors work, though it depends on third-party export formats and LMS APIs that can change.
- Product idea: Upload any quiz platform's report and push normalized, weighted scores into Canvas, Google Classroom or Schoology in one click.
- Evidence:
  - [Opinion: Blooket is FAR superior to Kahoot. : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/1d0qfpg/opinion_blooket_is_far_superior_to_kahoot/) (reddit:r/Teachers, ) — "takes a bit of extra work"
  - [In Canvas, is there any way to grade by question ... - Reddit](https://www.reddit.com/r/Professors/comments/10z253e/in_canvas_is_there_any_way_to_grade_by_question/) (reddit:r/Professors, ) — "I find it easier to simply enter the quiz score manually in the gradesheet...make a tall, narrow window next to an open Canvas gradesheet and transfer away!"
  - [Other Scantron Alternatives Like ZipGrade? : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/7blzl0/other_scantron_alternatives_like_zipgrade/) (reddit:r/Teachers, )

## 6. Teacher career transition guidance — score 3.25
- Burned-out teachers and education-degree holders don't know which better-paying roles their skills transfer to and can't afford retraining.
- Items: 3 · paying signals: 2 · engagement: 0 · who: employee 3
- Fit 0.65: LLM skill-mapping and job matching is self-serve, but buyers are budget-constrained and competition includes free content and coaching services.
- Product idea: Paste your teaching resume, get matched transferable roles with a rewritten resume and a skills-gap plan.
- Evidence:
  - [I hate teaching and it's not because I'm underpaid - Reddit](https://www.reddit.com/r/teaching/comments/xfaid8/i_hate_teaching_and_its_not_because_im_underpaid/) (reddit:r/teaching, ) — "I can't afford to go back to school"
  - [Have masters in Teaching/education, looking to leave the ...](https://www.reddit.com/r/teaching/comments/5f0ocu/have_masters_in_teachingeducation_looking_to/) (reddit:r/teaching, ) — "I'm afraid to leave because I have no idea what I could do that would pay me more"
  - [I hate teaching and I’m not good at it : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/1aikpfc/i_hate_teaching_and_im_not_good_at_it/) (reddit:r/teaching, )

## 7. Tolerant auto-grading and bulk regrade — score 3.0
- Auto-graders mark answers wrong for misspellings, Canvas New Quizzes can't regrade by question, and open-ended or scanned paper answers need manual grading.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 2
- Fit 0.75: LLM/fuzzy matching for short answers and OCR for paper exams fit the ML profile; LMS API limits on quiz regrading are a constraint.
- Product idea: Canvas add-on that flags near-miss short answers and bulk-regrades a question across all submissions.
- Evidence:
  - [Rant: how the Canvas LMS is specifically designed to ... - Reddit](https://www.reddit.com/r/Professors/comments/11dr816/rant_how_the_canvas_lms_is_specifically_designed/) (reddit:r/Professors, ) — "the entire exam has to be reloaded student-by-student and you have to scroll through the whole exam to find the question to manually regrade"
  - [Asynchronous Online Best Practices : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/14zhv8d/asynchronous_online_best_practices/) (reddit:r/Professors, ) — "I will go back and manually correct it"

## 8. LMS admin and navigation overhead — score 3.0
- Canvas and Blackboard are hard to navigate, migrations have hidden traps, and course administration eats time, while teachers without an LMS stitch together folders and spreadsheets.
- Items: 4 · paying signals: 2 · engagement: 0 · who: employee 3, student 1
- Fit 0.5: Broad and diffuse; a migration guide or course-setup automation is feasible, but a replacement LMS is a large, sales-driven product.
- Product idea: Canvas course-maintenance assistant that bulk-edits dates, settings and modules from plain-language commands.
- Evidence:
  - [Blackboard is anti-intuitive, clunky, garbage. : r/teaching](https://www.reddit.com/r/teaching/comments/amf470/blackboard_is_antiintuitive_clunky_garbage/) (reddit:r/teaching, ) — "I have to copy paste every goddamned assignment into my submission"
  - [Bypassing Canvas : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/1crdwi4/bypassing_canvas/) (reddit:r/Professors, ) — "Please share your experiences with ways to reduce your Canvas time"
  - [Best free equivalent of "Blackboard" or "Edline"? : r/teaching](https://www.reddit.com/r/teaching/comments/1p9njc/best_free_equivalent_of_blackboard_or_edline/) (reddit:r/teaching, )
  - [My campus just adopted Canvas for the fall. What are some ...](https://www.reddit.com/r/Professors/comments/13m7q1p/my_campus_just_adopted_canvas_for_the_fall_what/) (reddit:r/Professors, )

## 9. Submission format normalization — score 2.4
- Students submit files in inconsistent formats, so instructors convert them by hand before grading or annotation, and juggle separate tools for plagiarism and markup.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 2
- Fit 0.6: Easy conversion software, but it is a narrow feature that is likely bundled into a grading tool rather than sold on its own.
- Product idea: Batch-convert a folder of mixed submissions into one annotatable PDF packet per class.
- Evidence:
  - [Is requiring Microsoft Word too much to ask? : r/Professors](https://www.reddit.com/r/Professors/comments/1bkog53/is_requiring_microsoft_word_too_much_to_ask/) (reddit:r/Professors, ) — "Or should I just get over it, and do all the file conversion myself?"
  - [How helpful is Turnitin? : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/cgcxwf/how_helpful_is_turnitin/) (reddit:r/Professors, ) — "The big downside is that it sucks for grading. I wish there was more ability to freely mark and write directly on the papers."

## 10. Teacher portfolio and evaluation text — score 2.4
- New teachers spend days writing edTPA/induction reflective portfolios, and instructors must wade through abusive course-evaluation comments to find useful feedback.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 2
- Fit 0.6: LLM drafting and comment filtering are easy to build; edTPA ghost-writing raises academic-integrity issues, and evaluation filtering is a small niche.
- Product idea: Course-evaluation filter that hides abusive comments and summarizes actionable themes.
- Evidence:
  - [I worked on the edTPA for 2 days and submitted it 12 ... - Reddit](https://www.reddit.com/r/Teachers/comments/d0vwj9/i_worked_on_the_edtpa_for_2_days_and_submitted_it/) (reddit:r/Teachers, ) — "I worked on the edTPA for 2 days"
  - [ooof... Just read my course evaluation results. - Reddit](https://www.reddit.com/r/Professors/comments/rh6d7r/ooof_just_read_my_course_evaluation_results/) (reddit:r/Professors, ) — "I wish there was some AI that would rank them on constructive value, so you could skip the useless ones."

## 11. Write-once quiz authoring and export — score 2.1
- Teachers write questions in spreadsheets and re-enter them into each quiz platform, and instructors can't turn QTI banks into scannable paper exams.
- Items: 2 · paying signals: 1 · engagement: 0 · who: employee 2
- Fit 0.7: Format conversion (QTI, CSV, platform imports) plus paper exam generation is self-serve software; some platforms lack import APIs.
- Product idea: Single question bank that exports to Kahoot, Blooket, Quizizz, Canvas QTI and printable scannable PDFs.
- Evidence:
  - [Any exisiting software that can import QTI-files ... - Reddit](https://www.reddit.com/r/Professors/comments/qdd679/any_exisiting_software_that_can_import_qtifiles/) (reddit:r/Professors, ) — "this needs some severe adaption of the software"
  - [Quiz makers : r/Teachers - Reddit](https://www.reddit.com/r/Teachers/comments/11k7c1z/quiz_makers/) (reddit:r/Teachers, )

## 12. AI-generated work detection — score 1.6
- Instructors rely on unreliable, biased AI detectors plus manual reading to catch AI-written student work.
- Items: 2 · paying signals: 2 · engagement: 0 · who: employee 2
- Fit 0.4: Squarely ML, but detection accuracy is fundamentally limited, false positives create reputational risk, and the space is saturated with free tools.
- Product idea: Process-based authorship evidence (draft history and keystroke replay in a writing editor) instead of text-only classification.
- Evidence:
  - [New Tool Can Tell If Something Is AI-Written With 99% ...](https://www.reddit.com/r/Professors/comments/1448ief/new_tool_can_tell_if_something_is_aiwritten_with/) (reddit:r/Professors, ) — "I depend on the tool"
  - [Just Failed 15 students for cheating with ChatGPT - Reddit](https://www.reddit.com/r/Professors/comments/11z7fme/just_failed_15_students_for_cheating_with_chatgpt/) (reddit:r/Professors, ) — "I really wish there was a way to catch cheating students that didn't specifically target one group."

## 13. Teacher job application tracking — score 1.3
- Teacher job seekers track openings and applications across many district websites by hand in spreadsheets.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.65: Scraping district job boards plus a tracker is buildable, but scraper maintenance across many sites grows with coverage and usage is seasonal.
- Product idea: Aggregated district job-board alerts with a built-in application tracker.
- Evidence:
  - [How did you get your teaching job? : r/teaching - Reddit](https://www.reddit.com/r/teaching/comments/14ovfm/how_did_you_get_your_teaching_job/) (reddit:r/teaching, ) — "checking each web site at least 3 times a week"

## 14. Academic research project tracking — score 1.0
- Academics manage multiple research projects across hand-built spreadsheets and separate time-tracking apps.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.5: Buildable, but it competes with generic tools (Notion, Asana, Toggl) and has a thin education-specific angle.
- Product idea: Research-project tracker combining grant deliverables, tasks and time logs per project.
- Evidence:
  - [Need help organizing multiple projects : r/Professors - Reddit](https://www.reddit.com/r/Professors/comments/ci5acr/need_help_organizing_multiple_projects/) (reddit:r/Professors, ) — "So. Many. Spreadsheets. ... I also use a billable hours app to track how much time I spend on each project"

## 15. Foundational math gap remediation — score 0.55
- High school math teachers must fill multi-year skill gaps for students while still covering the required curriculum.
- Items: 1 · paying signals: 0 · engagement: 0 · who: employee 1
- Fit 0.55: Adaptive diagnostics plus LLM-generated practice fits ML skills, but it competes with IXL/Khan and pedagogical quality needs content expertise.
- Product idea: Quick diagnostic that generates per-student targeted warm-up sets aligned to the current unit.
- Evidence:
  - [Teaching High School Math to Students Who Are Years Behind](https://www.reddit.com/r/Teachers/comments/a5abiy/teaching_high_school_math_to_students_who_are/) (reddit:r/Teachers, )

## 16. Classroom cell phone distraction — score 0.0
- Teachers lose class time to phones and rely on lockable pouches that only work with admin enforcement.
- Items: 1 · paying signals: 1 · engagement: 0 · who: employee 1
- Fit 0.15: Core solutions are physical pouches or policy enforcement; software (MDM, focus apps) requires district sales and student-device control. · **excluded: hardware**
- Product idea: Physical lockable pouch program with an admin enforcement dashboard.
- Evidence:
  - [I don’t battle with cell phones anymore. There’s a SOLUTION!!!!](https://www.reddit.com/r/Teachers/comments/1bvsiqe/i_dont_battle_with_cell_phones_anymore_theres_a/) (reddit:r/Teachers, ) — "If your admin sucks, then yeah, will be a waste of funds."

## 17. Student behavior to disorder decision aid — score 0.0
- Student teachers want a flowchart mapping observed behaviors to possible disorders or impairments.
- Items: 1 · paying signals: 0 · engagement: 0 · who: student 1
- Fit 0.2: Borders on diagnostic guidance (regulated/medical and special-ed legal territory) and is essentially static content with little software moat. · **excluded: regulated**
- Product idea: Observation-to-referral guide that points teachers to the correct school support process.
- Evidence:
  - [Is there a tool for solving psychological impairment ... - Reddit](https://www.reddit.com/r/teaching/comments/1api8g/is_there_a_tool_for_solving_psychological/) (reddit:r/teaching, )
