## 11. Domain-aware AI agent for M/EEG analysis
- **Free:** CogEEGAgent, built on MNE with verification [arXiv](https://arxiv.org/abs/2607.25045); EEGAgent [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/38867); EEG-AI for artifact removal [PubMed](https://pubmed.ncbi.nlm.nih.gov/41932504/); NS-Copilot [arXiv](https://arxiv.org/pdf/2609.01971).
- **Paid general tools:** Cursor Pro $20/mo [NxCode](https://www.nxcode.io/resources/news/cursor-ai-pricing-plans-guide-2026); Elicit Plus $10–12/mo [Fastio](https://fast.io/resources/elicit-ai-review-2026/); Julius AI Pro $45/mo [Coefficient](https://coefficient.io/julius-ai-pricing); SciSpace $20–200/mo [costbench](https://costbench.com/software/ai-research-tools/scispace/). High end: BrainVision Analyzer 2 first license $11,960 [FAU quote](https://techfee.fau.edu/approvedproposals/Download.cfm?sid=53&pid=25).
- **Reachable base:** mne 306,766 PyPI downloads last month, inflated by CI and mirrors (pypistats, 2026-09-25). MNE forum: 2,428 registered users, 82 active in 30 days, 22 posting (mne.discourse.group/about.json, 2026-09-25). EEGLAB ~400k downloads over 10 years, 140k sessions/month [SCCN 2021](https://sccn.ucsd.edu/githubwiki/files/EEGLAB_overview2021.pdf).
- **Pays?** Paid workshops exist (3-day BrainVision Analyzer, 4-day OPM-FLUX; report.md evidence). No paid EEG-specific AI assistant found.
- **Price:** $20/mo, matching Cursor Pro and Julius entry (ASSUMPTION).
- **Customers @24mo:** 10 / 40 / 150, ~1–5% of engaged MNE forum users plus outside users (ASSUMPTION). **ARR:** $2.4k / $9.6k / $36k.
- **Hours:** MVP 200h + 6 h/wk for LLM, MNE-version and eval churn (ASSUMPTION) ≈ 746h. **Infra:** $100–300/mo LLM tokens, ~$0 if users bring their own key (ASSUMPTION).
- **ROI:** $9.6k ÷ 746h ≈ **$13/h**.
- **Risk:** Claude Code/Cursor plus free academic agents cover most of this; the only moat is the eval set and reference outputs.

## 12. BCI learning path / hosted course
- **Free/subsidized:** Neuromatch Academy, regionally adjusted fees, 3,000+ students in one run [NSF PAR](https://par.nsf.gov/servlets/purl/10298867), [FAQ](https://academy.neuromatch.io/faq); g.tec Spring School, free, listed as worth €980 [g.tec](https://www.gtec.at/spring-school-2021/); NeuroTechEDU 40h course [bciguys](https://www.bciguys.com/course); Alison BCI course [Alison](https://alison.com/course/an-introduction-to-brain-computer-interfaces).
- **Paid:** Mike X Cohen's neural signal processing course on Udemy, $119.99 list (~$13 with coupon), ~10k students, 1,763 reviews [CoursesPeak](https://coursespeak.com/complete-neural-signal-processing-and-analysis-zero-to-hero/); 350k+ students across his courses [Udemy](https://www.udemy.com/user/mike-x-cohen/). Queen's/NeuroTechX capstone CAD $1,699 [Queen's Gazette](https://www.queensu.ca/gazette/media/news-release-queen-s-micro-credentials-address-knowledge-gaps-burgeoning-neurotech-industry).
- **Reachable base:** NeuroTechX Slack 6,000+ members [NeuroTechX](https://neurotechx.com/community/). No reliable count of BCI students.
- **Pays?** Yes (Cohen, Queen's), but mostly through marketplaces or institutions, not solo self-hosted courses.
- **Price:** $79 one-time (ASSUMPTION).
- **Sales in year 2:** 40 / 120 / 400, self-hosted with no marketplace traffic (ASSUMPTION). **Revenue:** $3.2k / $9.5k / $32k per year.
- **Hours:** MVP 250h, mostly content + 4 h/wk (ASSUMPTION) ≈ 598h. **Infra:** $20–100/mo (ASSUMPTION).
- **ROI:** $9.5k ÷ 598h ≈ **$16/h**.
- **Risk:** discovery; free, well-branded options take the audience, and Udemy's price floor is ~$13.

## 13. Public EEG dataset catalog & loaders
- **Free:** EEGDash catalogs 700+ BIDS datasets (791 recordings, 39,778 participants) with PyTorch loaders, NSF-funded (1935749, 2423943) and hosted on AWS Open Data [arXiv](https://arxiv.org/abs/2606.16041), [GitHub](https://github.com/eegdash/EEGDash), [AWS](https://registry.opendata.aws/eegdash/); NEMAR/OpenNeuro, NIH-funded [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9650770/); MOABB, 36 datasets [arXiv](https://arxiv.org/abs/2404.15319); Meta NeuralBench, 94 datasets behind one interface [arXiv](https://arxiv.org/abs/2605.08495).
- **Reachable base:** last-month PyPI downloads (pypistats, 2026-09-25): moabb 13,347, braindecode 21,796, eegdash 4,706.
- **Pays?** No; 0 paying signals in the report, and funding comes from grants.
- **Price:** ≤$15/mo pro tier (ASSUMPTION); realistically only a grant or sub-award pays.
- **Customers @24mo:** 0 / 5 / 30 (ASSUMPTION). **ARR:** $0 / $0.9k / $5.4k.
- **Hours:** MVP 150h + 5 h/wk (ASSUMPTION) ≈ 620h. **Infra:** $100–400/mo for a mirror (ASSUMPTION; S3 ~$23/TB-month and ~$0.09/GB egress are standard AWS list prices, not checked here).
- **ROI:** $0.9k ÷ 620h ≈ **$1.5/h**; negative net of infra.
- **Risk:** EEGDash already does this for free with NSF money and AWS hosting.

## 14. Hosted BCI decoding benchmark
- **Free:** MOABB benchmark [arXiv](https://arxiv.org/abs/2404.15319); Meta NeuralBench-EEG, 36 tasks, 94 datasets [Meta AI](https://ai.meta.com/research/publications/neuralbench-a-unifying-framework-to-benchmark-neuroai-models/); FALCON on EvalAI [FALCON](https://snel-repo.github.io/falcon/); Codabench, free hosting with organizer compute workers [Codabench](https://www.codabench.org/); NeurIPS EEG Foundation Challenge [2025](https://eeg2025.github.io/eeg2025.github.io/), [2026](https://neural-interfaces26.github.io/).
- **Reachable base:** moabb 13,347 PyPI downloads/month (pypistats). Report evidence: 11 of 12 items from academic labs. No count of BCI decoding groups.
- **Pays?** Meta sponsored $2,500 cash prizes plus travel for the top 3 teams in the NeurIPS 2025 EEG challenge [eeglablist](https://sccn.ucsd.edu/pipermail/eeglablist/2025/018512.html). Money comes from sponsors and grants; no one charges benchmark users.
- **Revenue model:** sponsorship or grants (ASSUMPTION): $0 / $5k / $25k per year from 0 / 1 / 3 sponsors.
- **Hours:** MVP 200h, small for this builder given NLB/FALCON experience, + 4 h/wk (ASSUMPTION) ≈ 564h. **Infra:** $200–500/mo GPU scoring, ~$0 on Codabench with donated workers (ASSUMPTION).
- **ROI:** $5k ÷ 564h ≈ **$9/h**, roughly break-even after infra.
- **Risk:** Meta NeuralBench and MOABB fill the space; the value is reputation and citations, not cash.

## 15. Consumer EEG BLE connection doctor
- **Paid:** Petal Metrics $14.99 / $39.99 / $79.99 per month [petal.tech](https://petal.tech/); Mind Monitor $14.99 one-time [App Store](https://apps.apple.com/us/app/mind-monitor/id988527143), [FAQ](https://mind-monitor.com/FAQ.php). **Free:** BlueMuse [GitHub](https://github.com/kowalej/BlueMuse), BrainFlow, OpenBCI GUI.
- **Reachable base:** Muse "hundreds of thousands" of users in 2018, mostly meditators [CNBC](https://www.cnbc.com/2018/10/29/muse-2-meditation-assistant-headband-review.html). Developers: brainflow 8,328 and muselsl 1,027 PyPI downloads last month (pypistats, 2026-09-25). OpenBCI in 60+ countries, no unit sales published [Wikipedia](https://en.wikipedia.org/wiki/OpenBCI).
- **Pays?** Hobbyists pay for Muse streaming and connection tools (Petal, Mind Monitor). No paid diagnostic-only tool found.
- **Price:** $19 one-time (ASSUMPTION).
- **Sales in year 2:** 30 / 150 / 500, ~1–2% of monthly brainflow/muselsl downloaders (ASSUMPTION). **Revenue:** $0.6k / $2.9k / $9.5k per year.
- **Hours:** MVP 150h + ~$1–2k device/dongle test matrix + 4 h/wk for OS, firmware and BLE churn (ASSUMPTION) ≈ 526h. **Infra:** <$20/mo (ASSUMPTION).
- **ROI:** $2.9k ÷ 526h ≈ **$5.5/h**, before hardware cost.
- **Risk:** it needs hardware across every OS/radio combination, which the builder lacks (0.3 ML fit), while free BrainFlow and BlueMuse fixes keep improving.

## Summary (11–15)
- **Base-case ROI:** course ~$16/h > agent ~$13/h > benchmark ~$9/h > BLE doctor ~$5.5/h > catalog ~$1.5/h.
- All low, consistent with open-source academic tooling monetizing poorly; #14 fits the builder's reputation best but pays least in cash.
- **Not found:** Neuromatch fee amounts (interactive calculator), Queen's BCI module price ("registration coming soon"), and reliable counts of EEG labs or BCI students worldwide.
