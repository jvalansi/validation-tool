# Opportunity sweep

22 niches, 311 clusters (28 excluded by profile).
Score = items × (1 + paying share) × fit; fit and clustering are Claude judgements.

## Top 5 — validated

### 1. Hosted, version-pinned neuro-analysis environments (MNE/EEGLAB-alt/spike sorting) that launch in one click with known-good dependency sets.  (bci, score 68.2)
- Pain: Building from source (CMake/Qt/submodules), missing prebuilt binaries, pinned-dependency conflicts, MATLAB toolbox/path/plugin-manager failures, paid-toolbox dependencies and upgrade churn (NumPy 2, matplotlib) break environments and reproducibility.
- Items 104 · paying signals 20 · fit 0.55
- Validation: **weak signal — reconsider or reframe** · competition contested · capture 0.01 · market ~$10,000,000/yr
  - risk: The core tools are free open source, and free hosted alternatives exist (for example Neurodesk, brainlife.io, Binder; these come from general knowledge, not the research data), so there is little room to charge.
  - risk: Vendors own 57% of the search results page, so paid acquisition may be the only channel, and academic buyers respond poorly to paid ads and have slow procurement tied to grant cycles.
  - risk: Price evidence is thin: one observed price, no funded competitors, and no demand signals from HN, Reddit, or Product Hunt.
  - https://github.com/brainflow-dev/brainflow/issues/425
  - https://github.com/brainflow-dev/brainflow/issues/708
  - https://github.com/brainflow-dev/brainflow/issues/628

### 2. XDF/multistream sync analyzer that detects clock jumps and drift, dejitters, aligns streams and outputs a sync-quality report plus corrected files.  (bci, score 55.9)
- Pain: Aligning EEG with eye trackers, physio sensors, video, VR and stimulus markers across machines is hard. Users hit LSL discovery failures, jittery or jumping timestamps, relative clocks, trigger delays, missing connectors, no browser/cloud relay, and no way to validate sync quality.
- Items 73 · paying signals 13 · fit 0.65
- Validation: **weak signal — reconsider or reframe** · competition unknown · capture 0.01 · market ~$1,000,000/yr
  - risk: Free open-source tools (pyxdf, MNE, the LSL ecosystem) already cover the core dejitter and clock-sync functions, which pushes willingness to pay toward zero
  - risk: Academic buyers have small budgets and slow procurement, and the total number of XDF-using labs is low
  - risk: Incumbent search failed, so the competitive landscape is unknown rather than empty
  - https://github.com/brainflow-dev/brainflow/issues/298
  - https://github.com/brainflow-dev/brainflow/issues/670
  - https://github.com/brainflow-dev/brainflow/issues/265

### 3. Domain-tuned AI analysis copilot that writes, runs and sanity-checks MNE pipelines and statistical designs on the user's data.  (bci, score 55.2)
- Pain: Users struggle with group STUDY designs, repeated-measures and cluster statistics, beamformer and forward-model setup, coordinate frames, connectivity and PAC choices, and spectral units, and they rely on forums for expert judgment.
- Items 73 · paying signals 19 · fit 0.6
- Validation: **weak signal — reconsider or reframe** · competition none_found · capture 0.01 · market ~$10,000,000/yr
  - risk: General-purpose LLM assistants (ChatGPT, Claude, Copilot) already write MNE code for free or low cost, which limits how much users will pay for a specialized tool
  - risk: Academic buyers have small, grant-bound budgets and slow procurement, and the niche caps TAM
  - risk: No demand evidence surfaced (0 HN results, no vendors), so willingness to pay is unvalidated
  - https://github.com/mne-tools/mne-python/issues/2796
  - https://github.com/sccn/labstreaminglayer/issues/47
  - https://github.com/braindecode/braindecode/issues/186

### 4. Upload-to-report EEG preprocessing service with a validated default pipeline, ML artifact/ICA classification and reproducible QC reports.  (bci, score 53.25)
- Pain: Researchers don't know the right preprocessing order (filtering, ICA, interpolation, AutoReject). Automated bad-channel and artifact detection is unreliable, ICA review is manual, events desync after cropping, and batch QC reports have to be hand-scripted.
- Items 55 · paying signals 16 · fit 0.75
- Validation: **unviable — value per customer below the acquisition floor** · competition contested · capture 0.01 · market ~$10,000,000/yr
  - risk: Free open-source tools (EEGLAB, MNE-Python, ICLabel, sEEGnal) cover the core pipeline, which limits willingness to pay
  - risk: Academic buyers have small, grant-bound budgets and slow procurement, and researchers are reluctant to hand off preprocessing choices that reviewers will scrutinize
  - risk: The measured value per customer ($6/yr) is below the $200 acquisition floor, so the unit economics are unproven
  - https://github.com/sccn/eeglab/issues/108
  - https://github.com/sccn/eeglab/issues/429
  - https://github.com/sccn/eeglab/issues/178

### 5. Web/API converter and validator for EEG formats that preserves events, units and montages, with a diff report of anything lost.  (bci, score 50.25)
- Pain: EDF+/BDF/BrainVision/MFF/CNT/Nihon Kohden and consumer CSV files fail to import or silently lose annotations, events, units and channel locations. Conversion between EEGLAB, MNE and FieldTrip is lossy, and there's no JS/browser reader.
- Items 57 · paying signals 10 · fit 0.75
- Validation: **weak signal — reconsider or reframe** · competition contested · capture 0.01 · market ~$1,000,000/yr
  - risk: Free open-source tools (EEG-BIDS/EEGLAB, and MNE-Python, which was not in the data) already handle conversion, so willingness to pay is low
  - risk: Academic labs have small, grant-bound budgets and slow procurement
  - risk: Clinical users may refuse to upload patient EEG to a hosted web service
  - https://github.com/OpenBCI/OpenBCI_GUI/issues/266
  - https://github.com/OpenBCI/OpenBCI_GUI/issues/302
  - https://github.com/sccn/eeglab/issues/267

## Next 20 by score

- 35.0 · bci · Guided NWB/BIDS converter with plain-English validation, metadata editing, de-identification and cloud-optimized output.
- 31.5 · bci · Harmonized, validated EEG dataset hub with partial downloads and a hosted leaderboard that runs submitted decoders under standard CV protocols.
- 30.6 · bci · Upload-and-verify recording QA that flags dropped samples, rate mismatches, dead aux channels and format corruption, with a repaired export.
- 22.2 · bci · Cross-platform connection doctor that walks through a device/OS diagnostic checklist and maps opaque SDK errors to fixes.
- 20.15 · bci · Web-based figure studio for EEG/MEG (topomaps, 3D sources, montage library) that works without a local graphics stack.
- 18.7 · bci · Project-based interactive BCI curriculum with hosted notebooks on public datasets and auto-graded checkpoints.
- 18.0 · bci · Browser-based low-code real-time BCI builder with a device simulator, reusable feature recipes and exports to Unity/OSC.
- 13.6 · sysadmin-devops · A GitHub App adding approval gates, scheduled releases and image promotion for non-Enterprise teams, plus a local workflow runner.
- 12.1 · bci · Cloud spike-sorting service: upload or point to data, pick a sorter, get curated-ready Phy/NWB outputs.
- 11.25 · indie-devs · Bookmark and curated-site search engine that full-text indexes saved pages and sends LLM digests.
- 10.8 · bci · Structured EEG headset comparison and feasibility checker built from SDK tests and public benchmark data.
- 10.4 · indie-devs · Cheap usage-priced automation and internal-app builder generated from a plain-English workflow description.
- 9.6 · teachers · Gradebook overlay that imports LMS/CSV scores, applies arbitrary grading policies, and publishes a student-facing 'what I need' view.
- 9.35 · creators · Web app that analyzes a video's transcript and audio for natural pauses and suggests mid-roll ad breaks at a target interval, ready to paste into YouTube Studio.
- 9.1 · sysadmin-devops · A GitHub App that spins up per-branch preview subdomains for docker-compose stacks on the customer's own cloud account.
- 9.0 · data-analytics · An affordable desktop Alteryx alternative: record or describe cleanup steps, run them locally on large files, with an optional on-device LLM.
- 9.0 · indie-devs · Agent that researches narrowly defined ICP prospects from the open web and scores fit, with built-in outreach tracking.
- 9.0 · ecommerce · Low-cost profit dashboard that pulls in Amazon, Shopify, and Etsy fees and orders and computes per-SKU net margin from user-entered COGS.
- 8.5 · teachers · Upload a rubric and a stack of submissions, get draft scores and editable feedback comments in the teacher's voice.
- 8.5 · private-practice · Cheap hour logger with per-state licensure rule packs, multi-supervisor splits and exportable signed supervisor reports.
