# bci pain points — ranked

Items scanned: 1228 (github 712, reddit 227, discourse 289); labelled as pains: 423.
Score = count × (1 + share with paying signal) × fit. Fit and clustering are Claude judgements, not measurements.

## 1. EEG file format import/conversion with annotations intact — score 60.0
- EDF+/BDF, EGI MFF, Neuroscan, Nihon Kohden, BCI2000, OpenBCI/Muse CSV and SD-card exports fail to import, lose or shift annotations and events, garble units and scaling, or run out of memory. Moving data between EEGLAB, MNE and FieldTrip drops metadata, and JS/pandas/R readers are missing.
- Items: 56 · paying signals: 19 · engagement: 503 · who: student 19, employee 14, unknown 11
- Fit 0.8: A self-serve converter with deterministic logic, testable against sample files. Support stays flat once the format parsers are solid, and it can be sold per seat or by usage.
- Product idea: Web/CLI universal EEG converter that validates events, units and channel labels before and after conversion and flags any data that changed silently.
- Evidence:
  - [EEGLab EDF+ events misplaced and wrongly named](https://github.com/sccn/eeglab/issues/267) (github:sccn/eeglab, 2021-03-10) — "any advice would be greatly appreciated"
  - [We open-sourced our 7-channel dry-electrode EEG toolchain — not just code, but the full pipeline from hardware interface to Python analysis](https://www.reddit.com/r/BCI/comments/1u3nvxi/we_opensourced_our_7channel_dryelectrode_eeg/) (reddit:r/BCI, 2026-06-12) — "We got tired of spending two weeks on infrastructure before spending one day on the actual experiment."
  - [Is there a way to speed up loading EDF files?](https://mne.discourse.group/t/is-there-a-way-to-speed-up-loading-edf-files/8013) (discourse:mne.discourse.group, 2023-12-14) — "Loading these files using mne.io.read_raw takes about 5 minutes, or more. I just tried one that took 11 minutes to open."
  - [Issue loading EDF/EDF+ files ](https://github.com/sccn/eeglab/issues/255) (github:sccn/eeglab, 2021-02-14) — "I tried loading the ".event" files from file> "Import event info" but it didn't work out for me."
  - [Problem with create_windows_from_events working on an personal dataset](https://github.com/braindecode/braindecode/issues/135) (github:braindecode/braindecode, 2020-07-06) — "I added a copy of bnci.py script at moabb datsets an the example of trial wise decoding so I can get my datasets processed"

## 2. Multi-stream timestamp sync, jitter and drift repair — score 42.0
- In multimodal and multi-computer recordings (LSL/XDF, eye tracking, VR, video, triggers), timestamps can be irregular, jump, drift or use different clock conventions. Samples get lost and stimulus markers misalign. Researchers detect and fix this by hand offline and have no tools to measure latency or jitter.
- Items: 44 · paying signals: 12 · engagement: 425 · who: student 15, employee 14, unknown 8
- Fit 0.75: A pure software, file-in/report-out product. It is self-serve, the pain is recurring and well defined, and it needs no hardware or per-client work.
- Product idea: Upload an XDF/multi-stream recording to get a timing-integrity report (jitter, gaps, jumps, offsets) plus an auto-repaired, aligned export.
- Evidence:
  - [Not getting Trigger data using wifi shield connected to Cyton and daisy combination](https://github.com/OpenBCI/OpenBCI_GUI/issues/272) (github:OpenBCI/OpenBCI_GUI, 2017-10-24) — "Any help you can provide in this regard is much appreciated"
  - [Very specific LSL sync issues](https://github.com/sccn/labstreaminglayer/issues/13) (github:sccn/labstreaminglayer, 2019-01-27) — "I recorded 20 subjects worth of EEG data while they watched videos."
  - [Markers sent from computer with "`n" (n=1..9) create important noise on the 16 channels](https://github.com/OpenBCI/OpenBCI_GUI/issues/297) (github:OpenBCI/OpenBCI_GUI, 2017-12-13) — "sending Markers makes a huge noise on ALL electrodes at marker onset. Any solution for this?"
  - [LSL manual timestamping interferes with LSL clock_offset correction](https://github.com/OpenBCI/OpenBCI_GUI/issues/775) (github:OpenBCI/OpenBCI_GUI, 2020-05-21) — "They are unable to synchronize OpenBCI streams with those from different sources when loading xdf files saved in LabRecorder"
  - [Is Neurosity Crown streaming at wrong sampling interval? I am clocking 4.0 ms (1000 ms / 250 Hz) instead of 3.90625 ms (1000 ms / 256 Hz).](https://github.com/brainflow-dev/brainflow/issues/341) (github:brainflow-dev/brainflow, 2021-09-04) — "There is substantial va[riation]"

## 3. Automated EEG preprocessing and data-quality reports — score 36.4
- Artifact rejection, bad-channel detection and ICA classification are unreliable and need manual inspection. Best practice on pipeline step order is unclear, thresholds are guesswork, line-noise removal fails, and labs rebuild the same preprocessing for every dataset and want an automatic usability check.
- Items: 37 · paying signals: 15 · engagement: 394 · who: student 17, employee 13, unknown 5
- Fit 0.7: Hosted batch processing over open libraries (MNE, autoreject, ICLabel) with a self-serve report. Scoped to research use, it avoids clinical claims.
- Product idea: Upload raw EEG to get a standardized QC report (bad channels, artifacts, usable minutes) and a traceable, cleaned dataset with the pipeline config.
- Evidence:
  - [parallel processing with silence_periods](https://github.com/SpikeInterface/spikeinterface/issues/4038) (github:SpikeInterface/spikeinterface, 2025-07-07) — "written and applied a function to detect these periods"
  - [Thinking about making an open-source SDK for EEG/BCI analysis. Looking for thoughts from BCI/neural data scientists, researchers, or ML engineers.](https://www.reddit.com/r/BCI/comments/1sgct4x/thinking_about_making_an_opensource_sdk_for/) (reddit:r/BCI, 2026-04-09) — "3 weeks to make a b-spline interpolation for bad channels, 2 weeks to detect drowsiness from delta waves, 2 weeks for noise + artifact removal"
  - [Automatic EEG quality check & ICA for blink removal in 19-channel dry EEG](https://mne.discourse.group/t/automatic-eeg-quality-check-ica-for-blink-removal-in-19-channel-dry-eeg/11722) (discourse:mne.discourse.group, 2026-03-03) — "I am not an EEG expert, Visually inspecting every subject's data is difficult, And it is hard to apply consistent criteria across all participants."
  - [Utility for testing EEG data-cleaning pipelines?](https://github.com/NeuroTechX/moabb/issues/193) (github:NeuroTechX/moabb, 2021-06-01) — "It would be highly useful for us to have a tool that benchmarks how well a given filtering method or noisy channel detection method improves a dataset's SNR"
  - [Preprocessing with IC_Label and AutoReject: An Overeliance on Automation?](https://mne.discourse.group/t/preprocessing-with-ic-label-and-autoreject-an-overeliance-on-automation/11700) (discourse:mne.discourse.group, 2026-02-19) — "incorporating MNE's general ICA method reintroduced a manual inspection step into the pipeline"

## 4. Methods, statistics and source-localization guidance — score 36.3
- Researchers lack the expertise to set up repeated-measures and permutation designs, source reconstruction parameters, coregistration, spectral units, time-frequency parameters and connectivity metrics. They also lack ways to validate that results are physiologically plausible.
- Items: 49 · paying signals: 17 · engagement: 563 · who: student 23, employee 16, unknown 6
- Fit 0.55: An AI agent over MNE (for example an MCP server) fits the builder's skills and scales. Accuracy liability and the depth of the expertise needed limit how much users will trust it.
- Product idea: MNE-Python AI copilot (MCP server and chat) that builds, runs and explains stats and source pipelines with sanity-check plots.
- Evidence:
  - [ENH: encoding models](https://github.com/mne-tools/mne-python/issues/2796) (github:mne-tools/mne-python, 2016-01-19) — "Most of what I've been working on for my thesis has been so-called "encoding" models"
  - [Alpha/Beta ratio (PSD) for single epochs EEG for specific electrodes](https://mne.discourse.group/t/alpha-beta-ratio-psd-for-single-epochs-eeg-for-specific-electrodes/4162) (discourse:mne.discourse.group, 2021-12-17) — "I spent hours trying (and reading rutorials) and now feel stuck and desperate"
  - [Consistency in power spectra computed in STUDY by std_spec?](https://github.com/sccn/eeglab/issues/364) (github:sccn/eeglab, 2021-08-07) — "calculating psd is extremly long compared to when I compute it with pwelch directly in Matlab"
  - [statcond - bootstrap - paired](https://github.com/sccn/eeglab/issues/872) (github:sccn/eeglab, 2025-06-12) — "I spent four days examining this"
  - [using 'psd' or 'fft' in std_spec creates 60dB difference](https://github.com/sccn/eeglab/issues/172) (github:sccn/eeglab, 2020-06-14) — "A friend of mine at another university also observed this discrepancy"

## 5. Toolchain install, build and version reproducibility — score 31.5
- Building LSL and SDKs from source, missing prebuilt binaries (macOS, ARM, Android), MATLAB plugin breakage, hidden paid-toolbox dependencies, pinned ML libraries, and toolbox upgrades or machine differences that silently change results.
- Items: 46 · paying signals: 17 · engagement: 294 · who: employee 16, student 10, developer 9
- Fit 0.5: Prebuilt binaries and containers can be built by agents, but keeping up with upstream churn is a constant maintenance load. Users expect this to be free, so willingness to pay is low.
- Product idea: Versioned, prebuilt EEG/LSL environment images with a reproducibility check that diffs pipeline outputs across versions.
- Evidence:
  - [ICLabel issue when using BrainBeats ](https://github.com/sccn/eeglab/issues/707) (github:sccn/eeglab, 2023-12-06) — "I've solved a lot of previous error messages by installing plug ins, but I am new to EEGLAB and at a loss how to fix this one."
  - [A detailed tutorial of windows configuration environment is suggested](https://github.com/brainflow-dev/brainflow/issues/425) (github:brainflow-dev/brainflow, 2022-03-18) — "I tried for a long time without success"
  - [some issues using cmake with visual studio for lsl app development](https://github.com/sccn/labstreaminglayer/issues/29) (github:sccn/labstreaminglayer, 2019-07-09) — "I had to do a few things by hand because CMake got it wrong."
  - [Failed to install build.py file](https://github.com/brainflow-dev/brainflow/issues/708) (github:brainflow-dev/brainflow, 2024-03-07) — "Tried it multiple times but the same error still occurs"
  - [Support for Mac M1 and M2 processors, ARM64](https://github.com/brainflow-dev/brainflow/issues/628) (github:brainflow-dev/brainflow, 2023-05-15) — "You are my only hope"

## 6. Consumer EEG device connection & streaming reliability — score 23.8
- Getting consumer and low-cost EEG boards to connect and keep streaming over BLE, dongle or WiFi fails across operating systems. Typical problems are silent disconnects, stalled streams, dropped packets, opaque port and error codes, no way to tell whether real signal is arriving, unsupported headset revisions and single-OS vendor SDKs.
- Items: 52 · paying signals: 16 · engagement: 521 · who: hobbyist 16, employee 13, unknown 10
- Fit 0.35: A software diagnostic layer is possible, but the root causes are firmware, radio and OS driver issues. Every new device revision adds support work, and the free BrainFlow/LSL tools already compete.
- Product idea: Cross-platform 'EEG connection doctor' app that probes a headset, explains failures in plain language and confirms that real signal is arriving.
- Evidence:
  - [BUG: data streaming with wifi shield: keeps stopping after 1-2minute, have to restart](https://github.com/OpenBCI/OpenBCI_GUI/issues/263) (github:OpenBCI/OpenBCI_GUI, 2017-10-14) — "keeps stopping after 1-2minute, have to restart"
  - [testing 4.1.2 with wi-fi shield](https://github.com/OpenBCI/OpenBCI_GUI/issues/555) (github:OpenBCI/OpenBCI_GUI, 2019-07-05) — "I need to start the system 3 times, before it starts working"
  - [AAVAA board: native BLE does not connect to device on MacOS](https://github.com/brainflow-dev/brainflow/issues/667) (github:brainflow-dev/brainflow, 2023-08-17) — "fork (https://github.com/AAVAA-Inc/AAVAAflow/tree/aavaa-board-addition)"
  - [Muse S Athena on Windows 11: Failed to notify characteristic 273e0014 using MUSE_S_ATHENA_BOARD](https://github.com/brainflow-dev/brainflow/issues/835) (github:brainflow-dev/brainflow, 2026-05-19) — "Bluetooth adapter: TP-Link UB500 (Bluetooth 5.4) * Intel Bluetooth disabled"
  - [Buffer becomes empty after a while, and stays empty ](https://github.com/brainflow-dev/brainflow/issues/38) (github:brainflow-dev/brainflow, 2020-05-06) — "my program is meant to work on a real-time system, so basically the streaming continues forever"

## 7. BIDS/NWB conversion, metadata editing and validation — score 23.25
- Converting lab data into BIDS or NWB is strict and confusing. Files fail validation, metadata fields end up blank, extensions are hard to use, post-hoc metadata edits are unsupported, large files get slow or blow up memory, and de-identification is error-prone.
- Items: 21 · paying signals: 10 · engagement: 270 · who: employee 13, developer 4, student 3
- Fit 0.75: Wizard-style SaaS on top of open validators. Demand is driven by funding and journal sharing mandates, and it needs no sales calls.
- Product idea: Guided BIDS/NWB builder with metadata forms, live validation, de-identification and chunked large-file conversion.
- Evidence:
  - [[Feature]: Add `read_nwb` to simplify reading nwbfiles ](https://github.com/NeurodataWithoutBorders/pynwb/issues/1974) (github:NeurodataWithoutBorders/pynwb, 2024-10-23) — "This is a comment that I have gotten from various users: reading and nwbfile is not as easy as it could be."
  - [Error: Compensation grade of ICA (3) and Raw (0) do not match](https://mne.discourse.group/t/error-compensation-grade-of-ica-3-and-raw-0-do-not-match/11731) (discourse:mne.discourse.group, 2026-03-06) — "I proceeded searching for the best matching configuration options that could allow me to replicate (I admit, almost blindly) my reference pipeline"
  - [Need to store video](https://github.com/NeurodataWithoutBorders/pynwb/issues/1647) (github:NeurodataWithoutBorders/pynwb, 2023-02-16) — "For one recording session, we have around 300 short videos"
  - [conversion_factor per channel](https://github.com/NeurodataWithoutBorders/pynwb/issues/1064) (github:NeurodataWithoutBorders/pynwb, 2019-09-13) — "Neuropixel data is very big, so this is really not an ideal solution"
  - [[Documentation]: Streaming NWB files - recommend using remfile as the preferred method](https://github.com/NeurodataWithoutBorders/pynwb/issues/1791) (github:NeurodataWithoutBorders/pynwb, 2023-11-24) — "I created remfile about 3-4 months ago to address the slowness in lazy reading of remote NWB files"

## 8. Lightweight EEG viewing, annotation and figures — score 16.1
- EDF viewers are costly, heavy or hard to install, and large files load slowly. Sleep-label correction lacks batch editing, epoch scrolling is slow, 3D rendering fails on headless servers, and publication-quality ERP, topomap and montage figures take custom code.
- Items: 17 · paying signals: 6 · engagement: 149 · who: unknown 5, employee 4, developer 4
- Fit 0.7: A browser-based viewer and figure tool is self-serve and needs no installs. Agents can build it, and it fits freemium pricing.
- Product idea: Browser EDF/BDF viewer and annotator with fast large-file paging, batch label editing and one-click publication figures.
- Evidence:
  - [Data Logging start / stop](https://github.com/OpenBCI/OpenBCI_GUI/issues/400) (github:OpenBCI/OpenBCI_GUI, 2018-11-09) — "Files of several hours recording are not easy to handle in playback ( take very long to open etc)"
  - [`eegplot()` extremly slow when plotting later epochs](https://github.com/sccn/eeglab/issues/108) (github:sccn/eeglab, 2020-01-06) — "more than 20 seconds to plot 20 trials - which is honestly unbearable"
  - [Feature: Cyton Impedance Check Headplot](https://github.com/OpenBCI/OpenBCI_GUI/issues/648) (github:OpenBCI/OpenBCI_GUI, 2019-11-14) — "Takes too long to check impedance on all channels"
  - [STUDY visualisation is slow](https://github.com/sccn/eeglab/issues/290) (github:sccn/eeglab, 2021-05-06) — "Previously ... each time it took 1-5 minutes to plot ... With the switch to single-trial it takes forever ... daterp's from my study collectively weigh about 20.7 Gb."
  - [Is there a way to select and edit annotations in raw.plot() at the same time? If not, would that be an upcoming feature in a future update?(Holding shift and selecting multiple annotations)](https://mne.discourse.group/t/is-there-a-way-to-select-and-edit-annotations-in-raw-plot-at-the-same-time-if-not-would-that-be-an-upcoming-feature-in-a-future-update-holding-shift-and-selecting-multiple-annotations/11559) (discourse:mne.discourse.group, 2025-10-30) — "I feel that would save a tremendous amount of time"

## 9. Public EEG dataset access and BCI benchmarking — score 13.2
- Public datasets are scattered, downloads time out, metadata and preprocessing state are inconsistent, epoch timing is easy to get wrong, and there is no standard evaluation protocol or maintained leaderboard. Models are also hard to transfer to consumer hardware.
- Items: 20 · paying signals: 4 · engagement: 249 · who: developer 11, student 7, unknown 2
- Fit 0.55: A software catalog, mirror and leaderboard suits agents. Monetization is weak because users are academic and expect free data, and storage costs grow with the catalog.
- Product idea: Hosted mirror of public EEG/BCI datasets with harmonized metadata, partial-session streaming and a standardized benchmark leaderboard.
- Evidence:
  - [[No Code] Discover new datasets](https://github.com/NeuroTechX/moabb/issues/1) (github:NeuroTechX/moabb, 2017-06-03) — "We need people browsing the web to discover interesting datasets"
  - [New CrossSubjecEvaluation that supports transfer learning methods](https://github.com/NeuroTechX/moabb/issues/1077) (github:NeuroTechX/moabb, 2026-06-11) — "I myself am working on a transfer learning cross subject method and all this is motivated by real needs."
  - [problems with datasets](https://github.com/NeuroTechX/moabb/issues/523) (github:NeuroTechX/moabb, 2023-11-09) — "kindly rectify the problem or place a new dataset which is compatabile with the code kindly ASAP"
  - [Low Accuracy in EEG Emotion Recognition](https://mne.discourse.group/t/low-accuracy-in-eeg-emotion-recognition/11554) (discourse:mne.discourse.group, 2025-10-28) — "Only 24 electrodes are common to all subjects, and using them alone gives very poor results"
  - [I am building a BCI Robotic Hand Simulation](https://www.reddit.com/r/BCI/comments/1ug7j9s/i_am_building_a_bci_robotic_hand_simulation/) (reddit:r/BCI, 2026-06-26)

## 10. Browser/cloud real-time biosignal streaming and pipelines — score 9.6
- There is no browser-native way to acquire or stream biosignals, no low-latency relay to web or cloud apps, and no device emulator for development. Real-time dataflow nodes are hard to debug, and there is no lightweight processing for embedded closed-loop projects.
- Items: 13 · paying signals: 3 · engagement: 102 · who: developer 6, hobbyist 4, unknown 2
- Fit 0.6: A developer-facing SDK plus hosted relay scales well. The market is small, and device-level edge cases leak in.
- Product idea: Hosted WebSocket/WebRTC relay plus a JS SDK that forwards LSL/BrainFlow streams to web apps, with a simulated-headset mode.
- Evidence:
  - [Don't know if I should use MNE for this project](https://mne.discourse.group/t/dont-know-if-i-should-use-mne-for-this-project/11824) (discourse:mne.discourse.group, 2026-04-30) — "This project will run on a Raspberry Pi 4, but I heard MNE can be quite heavy"
  - [libLSL for WASM](https://github.com/sccn/labstreaminglayer/issues/34) (github:sccn/labstreaminglayer, 2019-08-04) — "bring LSL into our web technologies project ( www.biosignal.network )"
  - [Best practices for reusable branches](https://github.com/timeflux/timeflux/issues/56) (github:timeflux/timeflux, 2020-04-21) — "it is not easy for someone who is not expert in timeflux to know the right nodes and how best to combine them"
  - [GUI hangs when trying LSL and when played by Processing IDE, hub does not work](https://github.com/OpenBCI/OpenBCI_GUI/issues/316) (github:OpenBCI/OpenBCI_GUI, 2018-03-16)
  - [OSC data stream not working](https://github.com/OpenBCI/OpenBCI_GUI/issues/463) (github:OpenBCI/OpenBCI_GUI, 2019-03-24)

## 11. BCI education, lab discovery and career paths — score 7.6
- There are few structured BCI curricula, neuroscientists lack domain-specific Python training, nobody maintains a directory of labs, conferences or remote mentors, and literature is scattered across sources.
- Items: 13 · paying signals: 6 · engagement: 371 · who: student 11, employee 2
- Fit 0.4: A course or directory is low-support software, but students pay little and content has to be curated continuously.
- Product idea: Searchable BCI lab and program directory plus a public-dataset project curriculum for neuroscientists learning Python.
- Evidence:
  - [Neuroengineer-built BCI & neurotech research database (open-access, primary sources only)](https://www.reddit.com/r/BCI/comments/1s3j0n6/neuroengineerbuilt_bci_neurotech_research/) (reddit:r/BCI, 2026-03-25) — "I got tired of re-finding the same papers and press releases scattered across a dozen sources"
  - [Learning Python and maths for computational neuroscience as a beginner](https://www.reddit.com/r/compmathneuro/comments/1vo3myu/learning_python_and_maths_for_computational/) (reddit:r/compmathneuro, 2026-08-14) — "I have about a year to prepare before starting my PhD"
  - [How do I get into BCI](https://www.reddit.com/r/BCI/comments/1q30oe5/how_do_i_get_into_bci/) (reddit:r/BCI, 2026-01-03) — "I dont rly have money for the hardware"
  - [Is the Neuromatch Computational Neuroscience Course worth it?](https://www.reddit.com/r/compmathneuro/comments/1pccnc9/is_the_neuromatch_computational_neuroscience/) (reddit:r/compmathneuro, 2025-12-02) — "I'm not sure if the time commitment and money spent is worth it"
  - [tips for interactive teaching using google colab](https://mne.discourse.group/t/tips-for-interactive-teaching-using-google-colab/7934) (discourse:mne.discourse.group, 2023-12-01) — "that would really help me save time"

## 12. Spike sorting environments and compute — score 7.2
- GPU spike sorters need matching CUDA, MATLAB and compiler versions. Upgrades break cached results, curation exports break between versions, Apple Silicon can't run CUDA-only sorters, and large probe recordings take days of compute.
- Items: 12 · paying signals: 4 · engagement: 445 · who: employee 8, student 2, unknown 1
- Fit 0.45: Managed cloud sorting is self-serve SaaS, but GPU costs scale with usage, the datasets are huge, and debugging per-lab probe configurations drives up support.
- Product idea: Upload-and-sort cloud service running pinned SpikeInterface sorter containers with curation-ready exports.
- Evidence:
  - [Sorting takes extremely long when sorting a four shank probe by property](https://github.com/SpikeInterface/spikeinterface/issues/2625) (github:SpikeInterface/spikeinterface, 2024-03-26) — "it takes 8 hours to sort one of the four shanks and an estimated 160 hours to recompute the spike templates"
  - [Saving of ChannelSliceRecordings inefficient/basically unusable](https://github.com/SpikeInterface/spikeinterface/issues/2328) (github:SpikeInterface/spikeinterface, 2023-12-13) — "I then tried to increase the number of cores (up to 72) and the amount of RAM available (up to 1TB), but none of it helped."
  - [Navigating SpikeInterface Documentation](https://github.com/SpikeInterface/spikeinterface/issues/3656) (github:SpikeInterface/spikeinterface, 2025-01-29) — "I needed a tutorial and multiple attempts to just install anaconda, jupyter notebook, and SpikeInterface... questions that I have collected over the past weeks"
  - [Single-Unit Decoding: Relative Change or Absolute Change?](https://www.reddit.com/r/BCI/comments/1dt21sh/singleunit_decoding_relative_change_or_absolute/) (reddit:r/BCI, 2024-07-01) — "will undergo the laborious task of sorting to enrich the analysis"
  - [New version of spikeinterface](https://github.com/SpikeInterface/spikeinterface/issues/165) (github:SpikeInterface/spikeinterface, 2021-05-24)

## 13. Affordable EEG hardware and buying decisions — score 0.0
- Research-grade boards and caps are expensive, DIY builds have poor signal integrity and safety concerns, clones are unverified, and buyers can't compare headsets on usability, signal quality and cost.
- Items: 15 · paying signals: 12 · engagement: 378 · who: hobbyist 12, student 2, unknown 1
- Fit 0.1: The core need is cheaper or better physical hardware. A comparison guide alone is thin and hard to monetize. · **excluded: hardware**
- Product idea: Affordable gel-free multi-channel EEG headset with open raw-data access.
- Evidence:
  - [I designed an Open Source, 8-channel EEG board (ESP32-S3 + ADS1299). Works with LSL Brainflow and forked OpenBCI GUI](https://www.reddit.com/r/BCI/comments/1polj4b/i_designed_an_open_source_8channel_eeg_board/) (reddit:r/BCI, 2025-12-17) — "Research gear was wildly unaffordable... For those who don't want to deal with BGA soldering or sourcing components, I do have assembled units available"
  - [is there anyway for a consumer to buy a Dreem 3 headband?](https://www.reddit.com/r/BCI/comments/179tx44/is_there_anyway_for_a_consumer_to_buy_a_dreem_3/) (reddit:r/BCI, 2023-10-17) — "i would pay for it..."
  - [Is it possible to build BCI Electrode Cap from scratch?](https://www.reddit.com/r/BCI/comments/1vy8a2i/is_it_possible_to_build_bci_electrode_cap_from/) (reddit:r/BCI, 2026-08-25) — "they are too expensive so I thought that making one from scratch would help me save money"
  - [Rate my first BCI project please](https://www.reddit.com/r/BCI/comments/1tuu5hy/rate_my_first_bci_project_please/) (reddit:r/BCI, 2026-06-02) — "I am too broke for eeg headset yet."
  - [Is this video on how to make an EEG safe and accurate?](https://www.reddit.com/r/BCI/comments/1uy3pqr/is_this_video_on_how_to_make_an_eeg_safe_and/) (reddit:r/BCI, 2026-07-16) — "I wanted to make sure this would work before I actually bought everything"

## 14. Clinical EEG reading and expert interpretation — score 0.0
- Groups can't find epileptologists to read EDF recordings outside hospital systems. Caregivers want a deeper interpretation of patient EEG, and ambiguous artifact annotations need independent expert review.
- Items: 4 · paying signals: 4 · engagement: 12 · who: employee 2, developer 1, hobbyist 1
- Fit 0.1: Needs licensed human experts per case and touches medical interpretation, so it is both service work and regulated. · **excluded: regulated**
- Product idea: Marketplace connecting research groups with credentialed EEG readers for per-recording review.
- Evidence:
  - [Unknown pattern in MEG data](https://mne.discourse.group/t/unknown-pattern-in-meg-data/11803) (discourse:mne.discourse.group, 2026-04-11) — "We are observing a high-amplitude pattern in our MEG data across multiple subjects (pediatric ASD cohort)"
  - [Volunteer second opinion on three ambiguous artifact intervals in high-density EEG](https://mne.discourse.group/t/volunteer-second-opinion-on-three-ambiguous-artifact-intervals-in-high-density-eeg/11939) (discourse:mne.discourse.group, 2026-08-15) — "The review should take about 15–20 minutes"
  - [Seeking Epileptologist for Independent Review of OpenNeuro EEG Recordings](https://mne.discourse.group/t/seeking-epileptologist-for-independent-review-of-openneuro-eeg-recordings/11875) (discourse:mne.discourse.group, 2026-06-30) — "The review would be compensated."
  - [Seeking guidance on EEG analysis for SCN2A mutation clinical case (Beginner with programming)](https://mne.discourse.group/t/seeking-guidance-on-eeg-analysis-for-scn2a-mutation-clinical-case-beginner-with-programming/11882) (discourse:mne.discourse.group, 2026-07-10) — "the clinical EEG reports we receive are quite superficial and do not provide the level of detailed insights we need"
