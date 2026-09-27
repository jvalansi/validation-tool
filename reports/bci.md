# BCI pain points — ranked

Items scanned: 1356 (github 713, reddit 354, discourse 289); labelled as pains: 701.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Automated, validated EEG preprocessing and artifact QC — score 48.0
- There's no trusted order for preprocessing steps. ICA and bad-channel labeling still need manual review, automated rejection is unreliable or slow at cohort scale, and nonstandard data (dry electrodes, TMS, CI users, fNIRS) falls outside the defaults.
- Items: 46 · paying signals: 14 · engagement: 490 · who: academic_lab 30, student 9, clinician 5
- ML fit 0.8: Learned artifact and bad-channel classifiers and pipeline scoring are ML tasks the builder can train on public data.
- Product idea: ML-based auto-preprocessing API that cleans EEG, explains every rejection, and outputs a QC report scored against downstream decoding.
- Evidence:
  - [parallel processing with silence_periods](https://github.com/SpikeInterface/spikeinterface/issues/4038) (github:SpikeInterface/spikeinterface, 2025-07-07) — "written and applied a function to detect these periods"
  - [Thinking about making an open-source SDK for EEG/BCI analysis. Looking for thoughts from BCI/neural data scientists, researchers, or ML engineers.](https://www.reddit.com/r/BCI/comments/1sgct4x/thinking_about_making_an_opensource_sdk_for/) (reddit:r/BCI, 2026-04-09) — "3 weeks to make a b-spline interpolation for bad channels, 2 weeks to detect drowsiness from delta waves, 2 weeks for noise + artifact removal"
  - [Automatic EEG quality check & ICA for blink removal in 19-channel dry EEG](https://mne.discourse.group/t/automatic-eeg-quality-check-ica-for-blink-removal-in-19-channel-dry-eeg/11722) (discourse:mne, 2026-03-03) — "I am not an EEG expert, Visually inspecting every subject's data is difficult"
  - [annotating bad segments, then cropping signal, annotations don't get shifted?](https://mne.discourse.group/t/annotating-bad-segments-then-cropping-signal-annotations-dont-get-shifted/11221) (discourse:mne, 2025-05-23) — "Luckily, my colleague compared the pre/post cropping annotations and noted that they didn`t get shifted."
  - [`eegplot()` extremly slow when plotting later epochs](https://github.com/sccn/eeglab/issues/108) (github:sccn/eeglab, 2020-01-06) — "more than 20 seconds to plot 20 trials - which is honestly unbearable"

## 2. EEG file-format import/export and cross-tool conversion — score 43.2
- EDF+, BDF, MFF, Neuroscan, BrainVision, Nihon Kohden and legacy files fail to import or lose annotations and events. Units, channel locations and sample rates get garbled when moving data between EEGLAB, MNE and FieldTrip.
- Items: 60 · paying signals: 12 · engagement: 605 · who: academic_lab 32, student 18, developer 3
- ML fit 0.6: This is pure software parsing work the builder can test against public files, but covering every vendor quirk takes a long time.
- Product idea: Web and CLI converter that round-trips any EEG format with event, unit and montage verification and a diff report.
- Evidence:
  - [We open-sourced our 7-channel dry-electrode EEG toolchain — not just code, but the full pipeline from hardware interface to Python analysis](https://www.reddit.com/r/BCI/comments/1u3nvxi/we_opensourced_our_7channel_dryelectrode_eeg/) (reddit:r/BCI, 2026-06-12) — "We got tired of spending two weeks on infrastructure before spending one day on the actual experiment."
  - [Is there a way to speed up loading EDF files?](https://mne.discourse.group/t/is-there-a-way-to-speed-up-loading-edf-files/8013) (discourse:mne, 2023-12-14) — "Loading these files using mne.io.read_raw takes about 5 minutes, or more. I just tried one that took 11 minutes to open."
  - [Data stream freezes when saving in the BDF+ file type](https://github.com/OpenBCI/OpenBCI_GUI/issues/266) (github:OpenBCI/OpenBCI_GUI, 2017-10-16) — "I want to use the BDF+ file type so I do not have to convert the data in EDFbrowser to BDF for import into EEGLAB"
  - [MFF files imports not working](https://github.com/sccn/eeglab/issues/797) (github:sccn/eeglab, 2024-08-15) — "I have tried different version of Matlab, EEGlab, mffimport plugin. I have also increased the JAVA memory allowance."
  - ["mexsload not found in path" Issue](https://github.com/sccn/eeglab/issues/657) (github:sccn/eeglab, 2023-07-17) — "I removed then loaded the latest version of Biosig, try lots of things but I keep having this problem"

## 3. LSL connectors, bridges and web/cloud relay — score 26.5
- Many devices have no LSL connector. There are no browser, mobile, VR, LabVIEW or Simulink bridges, and multi-machine discovery fails silently behind firewalls or multicast limits.
- Items: 43 · paying signals: 10 · engagement: 261 · who: academic_lab 21, developer 10, hobbyist 4
- ML fit 0.5: Protocol bridges and relay servers fit someone who can run servers, but the device-specific connectors need the hardware.
- Product idea: Hosted, low-latency relay that bridges LSL, UDP and OSC streams to browsers, the cloud and mobile via WebSocket/WebRTC.
- Evidence:
  - [Muse S Athena Support (MS-03)](https://github.com/brainflow-dev/brainflow/issues/776) (github:brainflow-dev/brainflow, 2025-07-02) — "we have been using the muse 2 for research until the athena dropped, and it has no support yet"
  - [Add Support to Polar H10](https://github.com/brainflow-dev/brainflow/issues/670) (github:brainflow-dev/brainflow, 2023-08-30) — "My team is currently working on a project with Muse, EmotiBit, and Polar H10"
  - [Add support for EGIAmpServerPro](https://github.com/brainflow-dev/brainflow/issues/643) (github:brainflow-dev/brainflow, 2023-06-29) — "If not, how would we be able to connect the device ourselves?"
  - [How to use Brainflow with custom hardware](https://github.com/brainflow-dev/brainflow/issues/300) (github:brainflow-dev/brainflow, 2021-06-27) — "I've working on a custom signal acquisition board"
  - [Brainflow with ThinkPulse sensors on OpenBCI helmets](https://github.com/brainflow-dev/brainflow/issues/553) (github:brainflow-dev/brainflow, 2022-09-20) — "I will appreciate it if you could help me to run my code and get data again"

## 4. NWB conversion, validation and cloud access — score 22.4
- Converting to NWB is error-prone, and fixing metadata afterward is fragile. Extensions and validators confuse users, and lazily streaming large remote NWB/HDF5 datasets is slow or hangs.
- Items: 26 · paying signals: 6 · engagement: 391 · who: academic_lab 21, developer 3, student 2
- ML fit 0.7: The builder already knows spiking-data formats and DANDI-style datasets, and fast cloud reads plus conversion tooling are server and software work.
- Product idea: Hosted NWB conversion-and-validation service with metadata editing and a fast chunked cloud-read API for DANDI data.
- Evidence:
  - [[Feature]: Add `read_nwb` to simplify reading nwbfiles ](https://github.com/NeurodataWithoutBorders/pynwb/issues/1974) (github:NeurodataWithoutBorders/pynwb, 2024-10-23) — "This is a comment that I have gotten from various users: reading and nwbfile is not as easy as it could be."
  - [Need to store video](https://github.com/NeurodataWithoutBorders/pynwb/issues/1647) (github:NeurodataWithoutBorders/pynwb, 2023-02-16) — "For one recording session, we have around 300 short videos"
  - [conversion_factor per channel](https://github.com/NeurodataWithoutBorders/pynwb/issues/1064) (github:NeurodataWithoutBorders/pynwb, 2019-09-13) — "Neuropixel data is very big, so this is really not an ideal solution."
  - [[Documentation]: Streaming NWB files - recommend using remfile as the preferred method](https://github.com/NeurodataWithoutBorders/pynwb/issues/1791) (github:NeurodataWithoutBorders/pynwb, 2023-11-24) — "I created remfile about 3-4 months ago to address the slowness in lazy reading of remote NWB files"
  - [Parallelization in iterative data writing (parallel computing)](https://github.com/NeurodataWithoutBorders/pynwb/issues/1685) (github:NeurodataWithoutBorders/pynwb, 2023-04-06) — "Directly loading the data inside python in order to store it later as an nwb file is very time-consuming"

## 5. Acquisition SDK builds, bindings and platform ports — score 20.3
- BCI SDKs and LSL are hard to build from source (CMake, Qt, submodules), break on ARM, Apple Silicon and Raspberry Pi, fail in Java, .NET, Node and Electron bindings, and lack prebuilt binaries or iOS and browser support.
- Items: 50 · paying signals: 8 · engagement: 366 · who: developer 19, hobbyist 9, academic_lab 8
- ML fit 0.35: This is software-only work, but it means maintaining a large build and CI matrix, which is tedious and far from the builder's ML strengths.
- Product idea: Prebuilt, CI-tested binary distribution matrix (per device × OS × arch) for LSL and BrainFlow apps.
- Evidence:
  - [RuntimeException (Waited 5000ms for... processing.opengl.PSurfaceJOGL)](https://github.com/OpenBCI/OpenBCI_GUI/issues/577) (github:OpenBCI/OpenBCI_GUI, 2019-08-21) — "I scrapped everything and followed the ... guide to a T multiple times"
  - [A detailed tutorial of windows configuration environment is suggested](https://github.com/brainflow-dev/brainflow/issues/425) (github:brainflow-dev/brainflow, 2022-03-18) — "I tried for a long time without success"
  - [Failed to install build.py file](https://github.com/brainflow-dev/brainflow/issues/708) (github:brainflow-dev/brainflow, 2024-03-07) — "Tried it multiple times but the same error still occurs"
  - [Support for Mac M1 and M2 processors, ARM64](https://github.com/brainflow-dev/brainflow/issues/628) (github:brainflow-dev/brainflow, 2023-05-15) — "You are my only hope"
  - [iOS SDK and instructions](https://github.com/brainflow-dev/brainflow/issues/769) (github:brainflow-dev/brainflow, 2025-05-09) — "None apart from us implementing the subset of BrainFlow features we would need without BrainFlow"

## 6. MATLAB/EEGLAB plugin and environment breakage — score 18.75
- EEGLAB's plugin manager depends on a fragile server. Toolboxes shadow each other, paid MATLAB add-ons are required, STUDY group pipelines fail cryptically, and versions change results.
- Items: 60 · paying signals: 15 · engagement: 471 · who: academic_lab 42, student 11, developer 6
- ML fit 0.25: This is tied to the MATLAB ecosystem the builder likely doesn't use, and the fixes belong upstream in EEGLAB.
- Product idea: Pinned, containerized EEGLAB+plugins environment (MATLAB Runtime) with a health-check script.
- Evidence:
  - [ICLabel issue when using BrainBeats ](https://github.com/sccn/eeglab/issues/707) (github:sccn/eeglab, 2023-12-06) — "I've solved a lot of previous error messages by installing plug ins, but I am new to EEGLAB and at a loss how to fix this one"
  - [std_rmalldatafields() line 65](https://github.com/sccn/eeglab/issues/470) (github:sccn/eeglab, 2022-05-08) — "I did a trial with the first 3 subjects and it worked perfectly, but when I am adding the 18 subjects I have this error."
  - [std_preclust error: subscripted assignment dimension mismatch](https://github.com/sccn/eeglab/issues/138) (github:sccn/eeglab, 2020-03-05) — "I keep getting a bug where in STUDY.cluster.sets I get NAN in the same sets, and I manually fix this matrix"
  - [wrong number of arguments error while using GUI](https://github.com/sccn/eeglab/issues/36) (github:sccn/eeglab, 2019-08-07) — "I temporarily fixed the issue last week by uninstalling MATLAB on both machines and reinstalling the newest version. Then it began occurring again"
  - [error in function std_precomp()](https://github.com/sccn/eeglab/issues/739) (github:sccn/eeglab, 2024-03-04) — "EEGLAB worked well last year"

## 7. Multi-device timestamp sync and dejittering — score 18.0
- Aligning EEG with eye trackers, video, VR, physiological sensors and multiple amplifiers breaks because of jitter, clock offsets, timestamp jumps, relative clocks and opaque XDF sync settings.
- Items: 30 · paying signals: 6 · engagement: 224 · who: academic_lab 25, student 2, startup 1
- ML fit 0.5: Offline repair and validation of clocks is signal-processing software the builder can write, but validating it against ground truth needs real multi-device setups.
- Product idea: XDF/LSL sync auditor that detects jumps and drift, fixes alignment, and reports a sync-quality certificate.
- Evidence:
  - [Very specific LSL sync issues](https://github.com/sccn/labstreaminglayer/issues/13) (github:sccn/labstreaminglayer, 2019-01-27) — "I recorded 20 subjects worth of EEG data"
  - [OpenBCI x Emotibit xdf file import error](https://github.com/sccn/eeglab/issues/826) (github:sccn/eeglab, 2024-11-13) — "Since i'm not dependent on using eeglab for this purpose, is there any other way of using Emotibit data with other data in an xdf file?"
  - [LSL manual timestamping interferes with LSL clock_offset correction](https://github.com/OpenBCI/OpenBCI_GUI/issues/775) (github:OpenBCI/OpenBCI_GUI, 2020-05-21) — "I'm one of the LSL maintainers. I'm trying to help a user with a problem."
  - [time stamp jump bug](https://github.com/sccn/labstreaminglayer/issues/102) (github:sccn/labstreaminglayer, 2022-09-09) — "it does cause an extra hassle when running at least 40+ sessions"
  - [LSL timestamps "jump" backward and forward](https://github.com/sccn/labstreaminglayer/issues/131) (github:sccn/labstreaminglayer, 2025-07-17) — "I used LSL to record EEG data from a LiveAmp 64 EEG device (Brain Products) and gaze data from a Pupil Labs Neon eye tracker for my study"

## 8. Managed spike sorting for high-density probes — score 18.0
- Kilosort and other sorters need fragile CUDA/MATLAB alignment, containers fail, Neuropixels and HD-MEA data are compute-bound, export to Phy breaks, and upgrades invalidate cached results.
- Items: 17 · paying signals: 7 · engagement: 572 · who: academic_lab 13, student 3, developer 1
- ML fit 0.75: The builder has spiking-data experience and can run GPU servers, and a managed service avoids users' environment problems.
- Product idea: Upload-and-sort GPU service with pinned sorter versions, reproducible provenance and Phy/NWB export.
- Evidence:
  - [Sorting takes extremely long when sorting a four shank probe by property](https://github.com/SpikeInterface/spikeinterface/issues/2625) (github:SpikeInterface/spikeinterface, 2024-03-26) — "it takes 8 hours to sort one of the four shanks and an estimated 160 hours to recompute the spike templates... NVIDIA RTX 4080, 64 GB RAM"
  - [Kilosort error:  sgemm in CUBLAS failed](https://github.com/SpikeInterface/spikeinterface/issues/702) (github:SpikeInterface/spikeinterface, 2022-06-13) — "Matlab R2018a, CUDA 9.0, Visual Studio 2015, NVIDIA RTX A5000"
  - [Unable to open kilosort4 results with phy](https://github.com/SpikeInterface/spikeinterface/issues/2710) (github:SpikeInterface/spikeinterface, 2024-04-11) — "None of above was works"
  - [Improper Probe Configuration when loading OpenEphys](https://github.com/SpikeInterface/spikeinterface/issues/4394) (github:SpikeInterface/spikeinterface, 2026-02-16) — "So far I thought everything was looking good, but when inspecting the units in phy I noticed..."
  - [Saving of ChannelSliceRecordings inefficient/basically unusable](https://github.com/SpikeInterface/spikeinterface/issues/2328) (github:SpikeInterface/spikeinterface, 2023-12-13) — "I then tried to increase the number of cores (up to 72) and the amount of RAM available (up to 1TB), but none of it helped."

## 9. Independent EEG headset comparison and feasibility checks — score 17.55
- Buyers can't compare SNR, SDK quality, raw-data access or real decoding performance before buying, and can't tell whether a use case (motor intent, meditation, accessibility) is feasible on a given device.
- Items: 24 · paying signals: 15 · engagement: 672 · who: hobbyist 14, academic_lab 3, developer 3
- ML fit 0.45: The builder could benchmark public data from each device, but independent testing needs the physical hardware.
- Product idea: Evidence-based headset comparison site with per-use-case feasibility scores from public recordings and decoding results.
- Evidence:
  - [I designed an Open Source, 8-channel EEG board (ESP32-S3 + ADS1299). Works with LSL Brainflow and forked OpenBCI GUI](https://www.reddit.com/r/BCI/comments/1polj4b/i_designed_an_open_source_8channel_eeg_board/) (reddit:r/BCI, 2025-12-17) — "Research gear was wildly unaffordable... For those who don't want to deal with BGA soldering or sourcing components, I do have assembled units available"
  - [The best EEG headset for programming](https://www.reddit.com/r/BCI/comments/p3mz41/the_best_eeg_headset_for_programming/) (reddit:r/BCI, 2021-08-13) — "They are all expensive so I'd hate to buy one and find out it's actually not that good for programming purposes"
  - [is there anyway for a consumer to buy a Dreem 3 headband?](https://www.reddit.com/r/BCI/comments/179tx44/is_there_anyway_for_a_consumer_to_buy_a_dreem_3/) (reddit:r/BCI, 2023-10-17) — "i would pay for it"
  - [The worst case happened: Interaxon does no longer offer the Muse SDK!!!](https://github.com/sccn/labstreaminglayer/issues/30) (github:sccn/labstreaminglayer, 2019-07-18) — "we first have to write a Matlab interface for it"
  - [How well does the Neurosity Crown actually work?](https://www.reddit.com/r/BCI/comments/12h0vu7/how_well_does_the_neurosity_crown_actually_work/) (reddit:r/BCI, 2023-04-10) — "I was hoping to purchase the device to help a family member with MS"

## 10. Silent data-loss and stream integrity monitoring — score 17.4
- Streams stall, drop packets or samples, run at the wrong effective sample rate, write zeros to aux channels, or return data while the device is off. Users usually find out only at analysis time.
- Items: 27 · paying signals: 2 · engagement: 348 · who: academic_lab 13, developer 7, hobbyist 4
- ML fit 0.6: The builder can create software-only anomaly detection on sample counts, timing and signal statistics, and can test it on recorded data.
- Product idea: Drop-in stream watchdog that live-flags gaps, rate drift, flatlines and railing and writes an integrity report next to each recording.
- Evidence:
  - [Is Neurosity Crown streaming at wrong sampling interval? I am clocking 4.0 ms (1000 ms / 250 Hz) instead of 3.90625 ms (1000 ms / 256 Hz).](https://github.com/brainflow-dev/brainflow/issues/341) (github:brainflow-dev/brainflow, 2021-09-04) — "I am testing the Neurosity Crown for recording EEG/ERP data"
  - [Q: how to check if BrainBit works properly and turned on ? I tested device using Java package.](https://github.com/brainflow-dev/brainflow/issues/588) (github:brainflow-dev/brainflow, 2023-01-03) — "I had to tweak builing JAR ... to run java examples properly"
  - [WiFi shield packet loss causes cyclical noise spikes](https://github.com/OpenBCI/OpenBCI_GUI/issues/231) (github:OpenBCI/OpenBCI_GUI, 2017-09-04)
  - [Inconsistency between seconds recording in OpenBCI_GUI and seconds of saved data in .txt file](https://github.com/OpenBCI/OpenBCI_GUI/issues/198) (github:OpenBCI/OpenBCI_GUI, 2017-08-19)
  - [BUG: data streaming with wifi shield: keeps stopping after 1-2minute, have to restart](https://github.com/OpenBCI/OpenBCI_GUI/issues/263) (github:OpenBCI/OpenBCI_GUI, 2017-10-14)

## 11. Domain-aware AI agent for M/EEG analysis and method guidance — score 16.8
- Researchers want help writing MNE pipelines, checking results against references, and answering methodological questions (connectivity, microstates, noise covariance, deconvolution) that now go to forums or paid workshops.
- Items: 16 · paying signals: 5 · engagement: 121 · who: academic_lab 12, student 4
- ML fit 0.8: The builder can build LLM tooling on top of MNE/MOABB, and neural-data expertise helps them build eval sets.
- Product idea: MNE-aware analysis agent (MCP tools) that writes, runs and sanity-checks pipelines against reference outputs.
- Evidence:
  - [Alpha/Beta ratio (PSD) for single epochs EEG for specific electrodes](https://mne.discourse.group/t/alpha-beta-ratio-psd-for-single-epochs-eeg-for-specific-electrodes/4162) (discourse:mne, 2021-12-17) — "I spent hours trying (and reading tutorials) and now feel stuck and desperate."
  - [Estimating second derivative in python](https://mne.discourse.group/t/estimating-second-derivative-in-python/11830) (discourse:mne, 2026-05-14) — "Here I asked AI to help, but I am not sure if this is correct."
  - [Workshop: The A to Z of EEG Analysis with BrainVision Analyzer 2](https://mne.discourse.group/t/workshop-the-a-to-z-of-eeg-analysis-with-brainvision-analyzer-2/11888) (discourse:mne, 2026-07-14) — "three-day BrainVision Analyzer workshop"
  - [OPM-FLUX Toolkit 2026 - Register now!](https://mne.discourse.group/t/opm-flux-toolkit-2026-register-now/11825) (discourse:mne, 2026-05-01) — "4-day OPM-FLUX course at Oxford to meet 'the increasing demand for accessible training'"
  - [Phase amplitude coupling (PAC) results differ between methods](https://mne.discourse.group/t/phase-amplitude-coupling-pac-results-differ-between-methods/11752) (discourse:mne, 2026-03-17) — "the output is not reliable"

## 12. Structured BCI/neural-data learning path and teaching environment — score 16.0
- Newcomers from biology, medicine or data science lack a project-based roadmap, hardware-free starter projects, math bridging, mentorship, and hosted environments for teaching.
- Items: 23 · paying signals: 9 · engagement: 555 · who: student 14, hobbyist 5, academic_lab 2
- ML fit 0.5: The builder can write dataset-only projects and host notebooks, but course content is a crowded market to monetize.
- Product idea: Hosted, dataset-only BCI course with graded notebook projects that run on public data and need no hardware.
- Evidence:
  - [Switching from Finance to Computational Neuroscience — Looking for Learning Partners or Beginner Projects](https://www.reddit.com/r/compmathneuro/comments/1k7qzkx/switching_from_finance_to_computational/) (reddit:r/compmathneuro, 2025-04-25) — "I'm just not sure how to speed up the process of figuring out if this is something I'd enjoy doing long term."
  - [Learning Python and maths for computational neuroscience as a beginner](https://www.reddit.com/r/compmathneuro/comments/1vo3myu/learning_python_and_maths_for_computational/) (reddit:r/compmathneuro, 2026-08-14) — "I have about a year to prepare before starting my PhD"
  - [How do I get into BCI](https://www.reddit.com/r/BCI/comments/1q30oe5/how_do_i_get_into_bci/) (reddit:r/BCI, 2026-01-03) — "I dont rly have money for the hardware"
  - [Online courses on Computational Neuroscience](https://www.reddit.com/r/compmathneuro/comments/wq65ih/online_courses_on_computational_neuroscience/) (reddit:r/compmathneuro, 2022-08-16) — "I've started the Coursera course, but i don't have math knowledge to keep up with it."
  - [Self-studying CompNeuro from a CS/AI background in a developing country - Am I doing this right?](https://www.reddit.com/r/compmathneuro/comments/1nty5ry/selfstudying_compneuro_from_a_csai_background_in/) (reddit:r/compmathneuro, 2025-09-29) — "limited computing resources... limited funding"

## 13. Unified public EEG/BCI dataset catalog and loaders — score 14.45
- ML-ready datasets are scattered, loaders silently misread trials or labels, metadata doesn't match the data, mirrors are slow or offline, and there's no way to download a subset.
- Items: 17 · paying signals: 0 · engagement: 166 · who: academic_lab 9, student 3, unknown 3
- ML fit 0.85: This fits closely with the builder's benchmark experience, and a hosted catalog with verified loaders is server work that fits evening hours.
- Product idea: Verified, mirrored EEG dataset hub with harmonized session/label schema, per-subject streaming download and loader QA badges.
- Evidence:
  - [[No Code] Discover new datasets](https://github.com/NeuroTechX/moabb/issues/1) (github:NeuroTechX/moabb, 2017-06-03)
  - [question about reading Neuropixels data](https://github.com/SpikeInterface/spikeinterface/issues/1811) (github:SpikeInterface/spikeinterface, 2023-07-10)
  - [DOCS: Need help downloading the datasets](https://github.com/NeuroTechX/moabb/issues/36) (github:NeuroTechX/moabb, 2018-04-14)
  - [Lee2019_MI contains the labels in test_run](https://github.com/NeuroTechX/moabb/issues/820) (github:NeuroTechX/moabb, 2025-10-07)
  - [[BUG] Windows is not installing last two moabb versions](https://github.com/NeuroTechX/moabb/issues/670) (github:NeuroTechX/moabb, 2024-10-28)

## 14. Standardized compute-backed BCI decoding benchmark — score 14.25
- Evaluation protocols (cross-subject with calibration, cross-session, pooled) are missing or inconsistent, feature caching is wasteful and buggy, and results depend on hidden preprocessing. There's no interactive leaderboard.
- Items: 12 · paying signals: 3 · engagement: 149 · who: academic_lab 11, student 1
- ML fit 0.95: This is directly the builder's NLB/FALCON benchmarking expertise, applied to EEG.
- Product idea: FALCON-style hosted EEG decoding benchmark with fixed splits, transfer-learning protocols and a submission leaderboard.
- Evidence:
  - [Allow passing fixed transformers to evaluations](https://github.com/NeuroTechX/moabb/issues/367) (github:NeuroTechX/moabb, 2023-05-05) — "The expensive part of the evaluation is the feature extraction"
  - [New CrossSubjecEvaluation that supports transfer learning methods](https://github.com/NeuroTechX/moabb/issues/1077) (github:NeuroTechX/moabb, 2026-06-11) — "I myself am working on a transfer learning cross subject method and all this is motivated by real needs."
  - [Creating a Global Benchmarking Pipeline and Results Page](https://github.com/NeuroTechX/moabb/issues/190) (github:NeuroTechX/moabb, 2021-05-28) — "Will Github Actions be able to handle the running of the benchmark or will it have to be outsourced to some other server to run?"
  - [I am building a BCI Robotic Hand Simulation](https://www.reddit.com/r/BCI/comments/1ug7j9s/i_am_building_a_bci_robotic_hand_simulation/) (reddit:r/BCI, 2026-06-26)
  - [DL pipelines evaluated using dataset's default sampling frequencies](https://github.com/NeuroTechX/moabb/issues/405) (github:NeuroTechX/moabb, 2023-06-22)

## 15. Consumer EEG BLE/device connectivity — score 14.1
- Consumer and low-cost EEG boards (Muse, Ganglion, Crown, Cyton WiFi) often fail to connect or stream reliably over BLE, dongles or WiFi. Failures depend on the OS and hardware combination, error messages are opaque, and many problems show up during session setup.
- Items: 39 · paying signals: 8 · engagement: 426 · who: hobbyist 21, developer 6, student 4
- ML fit 0.3: Fixing these needs physical devices across many OS and radio setups and firmware-level debugging, which is hardware-bound, slow to iterate on, and not ML work.
- Product idea: Cross-platform connection doctor that probes adapters, ports and firmware and prints an actionable diagnosis.
- Evidence:
  - [testing 4.1.2 with wi-fi shield](https://github.com/OpenBCI/OpenBCI_GUI/issues/555) (github:OpenBCI/OpenBCI_GUI, 2019-07-05) — "I need to start the system 3 times, before it starts working"
  - [AAVAA board: native BLE does not connect to device on MacOS](https://github.com/brainflow-dev/brainflow/issues/667) (github:brainflow-dev/brainflow, 2023-08-17) — "AAVAA-Inc maintaining a fork (AAVAAflow) to add their board"
  - [Muse S Athena on Windows 11: Failed to notify characteristic 273e0014 using MUSE_S_ATHENA_BOARD](https://github.com/brainflow-dev/brainflow/issues/835) (github:brainflow-dev/brainflow, 2026-05-19) — "Bluetooth adapter: TP-Link UB500 (Bluetooth 5.4) / Intel Bluetooth disabled"
  - [GUI freezes at start on Mac OS Sierra 10.12.3](https://github.com/OpenBCI/OpenBCI_GUI/issues/118) (github:OpenBCI/OpenBCI_GUI, 2017-02-02) — "should I downgrade my OS or is there a quick fix?"
  - [Channels 9-16 don't work with Cyton/Daisy/Wifi](https://github.com/OpenBCI/OpenBCI_GUI/issues/837) (github:OpenBCI/OpenBCI_GUI, 2020-07-23) — "I've confirmed data from these sensors works when using a different software"

## 16. Python dependency churn and reproducible environments — score 14.0
- NumPy 2, scikit-learn, pyRiemann, MNE and braindecode version conflicts and tight pins break examples, spike-sorting caches and published pipelines, and HPC setups break on home-directory assumptions.
- Items: 21 · paying signals: 7 · engagement: 256 · who: academic_lab 15, developer 4, student 2
- ML fit 0.5: The builder can maintain lockfiles, containers and CI, but it's low-differentiation maintenance work.
- Product idea: Curated, CI-tested lockfile/container images for the MNE/MOABB/braindecode/SpikeInterface stack, with nightly compatibility reports.
- Evidence:
  - [using read_intan with timestamp gaps](https://github.com/SpikeInterface/spikeinterface/issues/3375) (github:SpikeInterface/spikeinterface, 2024-09-06) — "I have already sorted them with Kilosort... Since the update, I have been unable to load these two recordings."
  - [Expected dtype object, got 'numpy.dtype[float64]'](https://mne.discourse.group/t/expected-dtype-object-got-numpy-dtype-float64/3151) (discourse:mne, 2021-05-18) — "I used read_raw_bids in the last few days. But it did not work today"
  - [support h5py 3.x](https://github.com/NeurodataWithoutBorders/pynwb/issues/1319) (github:NeurodataWithoutBorders/pynwb, 2020-11-19) — "multiple environments, but that's not always super helpful"
  - [Installing MOABB sneakly uninstalls other up-to-date packages](https://github.com/NeuroTechX/moabb/issues/244) (github:NeuroTechX/moabb, 2021-10-13) — "a pain for users that have to keep reinstalling such libraries constantly and recreating new environments"
  - [Lock-file access error, define location of lockfiles?](https://mne.discourse.group/t/lock-file-access-error-define-location-of-lockfiles/11759) (discourse:mne, 2026-03-19) — "cluster which spawns >100 processes running mne.stats.permutation_t_test in long loops"

## 17. Real-time closed-loop BCI and neurofeedback pipelines — score 13.3
- Builders stitch together acquisition, artifact correction, decoding and feedback by hand. Node graphs are hard to debug, there are no reusable recipes for band power or controls, and embedded or low-power targets have no support.
- Items: 16 · paying signals: 3 · engagement: 104 · who: developer 8, hobbyist 5, student 2
- ML fit 0.7: Real-time decoding pipelines are close to the builder's skills and can be developed against simulated streams from recorded data.
- Product idea: Lightweight real-time decoding runtime with replay-simulation, prebuilt recipes (band power, blink/jaw controls) and a web dashboard.
- Evidence:
  - [My current project (Looking for advice!)](https://www.reddit.com/r/BCI/comments/1wgdf58/my_current_project_looking_for_advice/) (reddit:r/BCI, 2026-09-14) — "was there a cheaper option than the 250 dollars kit ... Also is there a place I can hire someone to help me for this?"
  - [MNE-RT: an open-source real-time neurofeedback/BCI framework](https://mne.discourse.group/t/mne-rt-an-open-source-real-time-neurofeedback-bci-framework/11898) (discourse:mne, 2026-07-19) — "It covers the entire closed-loop pipeline in a single, researcher-friendly API"
  - [BCI for a 3 year old?](https://www.reddit.com/r/OpenBCI/comments/1dgs683/bci_for_a_3_year_old/) (reddit:r/OpenBCI, 2024-06-15) — "I'm looking for some guidance in setting up a BCI controller for a laptop to help my daughter with a degenerative disease speak."
  - [Built a live EEG-controlled robotic painting arm for someone with EDS and demoed it at a conference last weekend. Some notes + looking for BCI folks in SG](https://www.reddit.com/r/BCI/comments/1thw89o/built_a_live_eegcontrolled_robotic_painting_arm/) (reddit:r/BCI, 2026-05-19)
  - [Major performance problems with latest brainflow](https://github.com/brainflow-dev/brainflow/issues/266) (github:brainflow-dev/brainflow, 2021-04-04)

## 18. Source localization, coregistration and montage setup — score 13.2
- FreeSurfer and BEM chains are fragile, and coordinate frames and templates are confusing. Electrode files for commercial caps are missing or inconsistent, and beamformer and regularization parameters are opaque.
- Items: 30 · paying signals: 3 · engagement: 351 · who: academic_lab 21, student 5, developer 2
- ML fit 0.4: This is software, but deep MEG/EEG forward-modeling expertise is outside the builder's decoding background.
- Product idea: Hosted template-based source pipeline: upload EEG plus cap model and get a validated forward model and source estimates.
- Evidence:
  - [Large peaks in resting state EEG source time course](https://mne.discourse.group/t/large-peaks-in-resting-state-eeg-source-time-course/11712) (discourse:mne, 2026-02-25) — "I've tried varying the lambda parameter value and the distributed source method I used (eLORETA, sLORETA, dSPM, MNE)"
  - [The forward solution gives me an unplausible gain matrix.](https://mne.discourse.group/t/the-forward-solution-gives-me-an-unplausible-gain-matrix/11692) (discourse:mne, 2026-02-11) — "I run the Freesurfers recon-all pipeline I then used Blender to make slight adju[stments]"
  - [Forward modelling EEG from simulated sources](https://mne.discourse.group/t/forward-modelling-eeg-from-simulated-sources/11652) (discourse:mne, 2026-01-09) — "the simulate_raw() function takes ages"
  - [Create canonical template channel locations](https://github.com/mne-tools/mne-python/issues/7472) (github:mne-tools/mne-python, 2020-03-18)
  - [Issue with Co-Registration when combining MEG and EEG data into a single file](https://mne.discourse.group/t/issue-with-co-registration-when-combining-meg-and-eeg-data-into-a-single-file/2892) (discourse:mne, 2021-03-26)

## 19. BIDS conversion, de-identification and dataset sharing — score 12.0
- Converting to BIDS silently changes event IDs and gives little control over sidecar files. Pipelines break on nonstandard structures, de-identification is manual, and large MEG/EEG datasets are hard to share.
- Items: 13 · paying signals: 7 · engagement: 106 · who: academic_lab 11, developer 1, student 1
- ML fit 0.6: Data-engineering work the builder can do, with clear validators to test against.
- Product idea: Guided BIDS curator that converts, de-identifies, validates and diffs metadata before upload to OpenNeuro.
- Evidence:
  - [Error: Compensation grade of ICA (3) and Raw (0) do not match](https://mne.discourse.group/t/error-compensation-grade-of-ica-3-and-raw-0-do-not-match/11731) (discourse:mne, 2026-03-06) — "allow me to replicate (I admit, almost blindly) my reference pipeline via the config file"
  - [Saving compressed data](https://mne.discourse.group/t/saving-compressed-data/11838) (discourse:mne, 2026-05-21) — "'currently the dataset is too large for almost all repositories'"
  - [ICA on multiple runs](https://mne.discourse.group/t/ica-on-multiple-runs/11784) (discourse:mne, 2026-03-31) — "I'm performing it with external code... may force me to abandon"
  - [EEG data format for BIDS – any limitations with EDF vs BrainVision/FIF?](https://mne.discourse.group/t/eeg-data-format-for-bids-any-limitations-with-edf-vs-brainvision-fif/11768) (discourse:mne, 2026-03-25) — "we are building a multimodal dataset (EEG, MRI, genetics, clinical data)"
  - [Standard system of units](https://github.com/sccn/labstreaminglayer/issues/66) (github:sccn/labstreaminglayer, 2021-03-24) — "I have been dealing with with a very annoying issue in a number of projects lately"

## 20. EEG deep-learning training and transfer toolkit — score 11.7
- Users struggle with slow windowed data loading, model-specific input shapes, hyperparameter and augmentation setup, channel sets that differ across subjects, and transferring pretrained models to consumer headsets.
- Items: 11 · paying signals: 2 · engagement: 130 · who: student 5, academic_lab 3, developer 3
- ML fit 0.9: This is core ML engineering, and the builder's transformer and latent-model experience applies directly to channel-agnostic pretrained EEG models.
- Product idea: Channel-agnostic pretrained EEG foundation model plus fine-tune API for small datasets from any headset.
- Evidence:
  - [Problem with create_windows_from_events working on an personal dataset](https://github.com/braindecode/braindecode/issues/135) (github:braindecode/braindecode, 2020-07-06) — "I modified a bit the library ... I added a copy of bnci.py script at moabb datasets"
  - [Question to EEGNet models](https://github.com/braindecode/braindecode/issues/186) (github:braindecode/braindecode, 2020-12-10) — "Since I'm really new to EEG and Deep learning"
  - [Transformer for Dimensionality Reduction ideas](https://www.reddit.com/r/compmathneuro/comments/1o8x6go/transformer_for_dimensionality_reduction_ideas/) (reddit:r/compmathneuro, 2025-10-17)
  - [Analysing the performance of different methods to get windows](https://github.com/braindecode/braindecode/issues/62) (github:braindecode/braindecode, 2020-01-30)
  - [Seeking Feedback on Feasibility of EEG-Based Cognitive Fatigue Detection Project](https://www.reddit.com/r/BCI/comments/1nii0s3/seeking_feedback_on_feasibility_of_eegbased/) (reddit:r/BCI, 2025-09-16)

## 21. Group statistics design and publication figures — score 10.5
- Setting up repeated-measures, cluster-permutation, LIMO and mixed-effects designs is confusing, backends disagree, and difference topomaps and ERP plots with confidence intervals need custom code.
- Items: 19 · paying signals: 2 · engagement: 130 · who: academic_lab 18, student 1
- ML fit 0.5: This is statistics software the builder can write, but domain credibility on method choices matters a lot.
- Product idea: Design-wizard library that builds validated cluster and mixed-effects tests from a condition table and emits figure templates.
- Evidence:
  - [statcond - bootstrap - paired](https://github.com/sccn/eeglab/issues/872) (github:sccn/eeglab, 2025-06-12) — "I spent four days examining this"
  - [STUDY visualisation is slow](https://github.com/sccn/eeglab/issues/290) (github:sccn/eeglab, 2021-05-06) — "Previously it was trivial, each time it took 1-5 minutes... With the switch to single-trial it takes forever... daterp's from my study collectively weigh about 20.7 Gb"
  - [Combining multiple files](https://mne.discourse.group/t/combining-multiple-files/3238) (discourse:mne, 2021-06-11)
  - [ERP visualization -- how to plot confidence intervals/standard error of grand averaged ERP](https://mne.discourse.group/t/erp-visualization-how-to-plot-confidence-intervals-standard-error-of-grand-averaged-erp/2747) (discourse:mne, 2021-02-24)
  - [Repeated measures ANOVA permutation test for multiple subjects?](https://mne.discourse.group/t/repeated-measures-anova-permutation-test-for-multiple-subjects/8449) (discourse:mne, 2024-03-07)

## 22. Recording files, SD-card conversion and long sessions — score 9.9
- SD-card conversion is slow, truncates files or fails. Long sleep recordings are not segmented, files are unorganized or lost, and apps can't replay their own recordings.
- Items: 16 · paying signals: 6 · engagement: 180 · who: academic_lab 7, unknown 6, hobbyist 2
- ML fit 0.45: Robust converters and session managers are straightforward software, but the market is narrow and mostly tied to OpenBCI.
- Product idea: Robust streaming converter and session organizer for OpenBCI/consumer recordings with integrity checks and auto-segmentation.
- Evidence:
  - [SD Card writing is not working ](https://github.com/OpenBCI/OpenBCI_GUI/issues/278) (github:OpenBCI/OpenBCI_GUI, 2017-11-01) — "Tried: 2 different SD cards, Reformatting SD cards (with the SD Association Formatter), Wifi and BLE"
  - [Unable to convert large files from SD card: Out of Memory Error](https://github.com/OpenBCI/OpenBCI_GUI/issues/355) (github:OpenBCI/OpenBCI_GUI, 2018-07-08) — "I'm trying to open a large file I recorded on the SD card during a 8 hours of sleep"
  - [Add support to prevent long recordings](https://github.com/OpenBCI/OpenBCI_GUI/issues/461) (github:OpenBCI/OpenBCI_GUI, 2019-03-19) — "it is laborious and erroneous to start and stop recordings every 20-30 minutes"
  - [Problem finding saved recordings on linux](https://github.com/OpenBCI/OpenBCI_GUI/issues/639) (github:OpenBCI/OpenBCI_GUI, 2019-11-08) — "Any clues would be highly appreciated!"
  - [3.2.0 - Interface freezing when converting from SD format](https://github.com/OpenBCI/OpenBCI_GUI/issues/302) (github:OpenBCI/OpenBCI_GUI, 2017-12-26) — "After 1 hour I give up and end the program, reboot, and tried again."

## 23. Signal-quality and noise-source diagnostics — score 8.4
- Users can't tell whether railed channels, strange spectra or line noise come from electrodes, the reference, muscle or hardware faults. Impedance checks are unreliable, and people rely on forum tribal knowledge.
- Items: 13 · paying signals: 1 · engagement: 97 · who: academic_lab 8, unknown 2, hobbyist 2
- ML fit 0.6: A spectral-signature classifier is feasible for the builder, but labeled fault data is scarce without a lab.
- Product idea: Upload-a-recording diagnostic that classifies likely noise and fault sources per channel with fix suggestions.
- Evidence:
  - [Line Noise(EEG)](https://mne.discourse.group/t/line-noise-eeg/11817) (discourse:mne, 2026-04-23) — "'is it still worth processing and analyzing this dataset?'"
  - [Ganglion Impedance Not working(?)](https://github.com/OpenBCI/OpenBCI_GUI/issues/421) (github:OpenBCI/OpenBCI_GUI, 2019-01-09)
  - [GUI impedance buttons fail on Mac standalone 4.0.3, work with standalone 3.3.2](https://github.com/OpenBCI/OpenBCI_GUI/issues/427) (github:OpenBCI/OpenBCI_GUI, 2019-01-22)
  - [Inputs frequently showing RAILED, high input amplitude](https://github.com/OpenBCI/OpenBCI_GUI/issues/257) (github:OpenBCI/OpenBCI_GUI, 2017-10-05)
  - [Feature: Cyton Impedance Check Headplot](https://github.com/OpenBCI/OpenBCI_GUI/issues/648) (github:OpenBCI/OpenBCI_GUI, 2019-11-14)

## 24. 3D visualization and headless QC reports — score 5.4
- PyVista, VTK and mayavi backends fail to install or render, crash on HPC, in Docker and in notebooks, and block coregistration checks and batch QC report generation.
- Items: 12 · paying signals: 0 · engagement: 158 · who: academic_lab 8, student 3, developer 1
- ML fit 0.45: This is server and rendering setup the builder can handle, but it's graphics-stack debugging rather than ML.
- Product idea: Hosted rendering service that turns MNE objects into 3D brain, coregistration and QC HTML reports without local graphics.
- Evidence:
  - [How to solve "can not import name 'Brain' from 'Surfer'](https://mne.discourse.group/t/how-to-solve-can-not-import-name-brain-from-surfer/4390) (discourse:mne, 2022-02-09)
  - [GUI and display [not working as intended]](https://mne.discourse.group/t/gui-and-display-not-working-as-intended/4325) (discourse:mne, 2022-01-27)
  - [3D figure closed immediately after plotting](https://mne.discourse.group/t/3d-figure-closed-immediately-after-plotting/3453) (discourse:mne, 2021-07-23)
  - [Support for 3D brain visualization in headless mode?](https://mne.discourse.group/t/support-for-3d-brain-visualization-in-headless-mode/4375) (discourse:mne, 2022-02-07)
  - [How to save figures in a loop without displaying	them?](https://mne.discourse.group/t/how-to-save-figures-in-a-loop-without-displaying-them/798) (discourse:mne, 2014-08-16)

## 25. Stimulus trigger and event-marker timing — score 4.5
- Hardware triggers are noisy or add artifacts, markers go missing from recordings, and stimulus-to-signal delays (audio onset, photosensor) need manual measurement and correction.
- Items: 13 · paying signals: 5 · engagement: 161 · who: academic_lab 9, student 2, developer 1
- ML fit 0.25: This mostly needs hardware timing tests with photodiodes and trigger boxes, which is outside a software-only setup.
- Product idea: Software that estimates trigger delay from recorded photodiode or audio channels and corrects the event latencies.
- Evidence:
  - [Not getting Trigger data using wifi shield connected to Cyton and daisy combination](https://github.com/OpenBCI/OpenBCI_GUI/issues/272) (github:OpenBCI/OpenBCI_GUI, 2017-10-24) — "Any help you can provide in this regard is much appreciated"
  - [Markers sent from computer with "`n" (n=1..9) create important noise on the 16 channels](https://github.com/OpenBCI/OpenBCI_GUI/issues/297) (github:OpenBCI/OpenBCI_GUI, 2017-12-13) — "sending Markers makes a huge noise on ALL electrodes at marker onset"
  - [Error when cropping raw object](https://mne.discourse.group/t/error-when-cropping-raw-object/11556) (discourse:mne, 2025-10-28) — "I'm having a lot of issues when using events later in my code, as the events are not updated accordingly when the data is cropped."
  - [find_delay: A small Python package to find the delay between time series](https://mne.discourse.group/t/find-delay-a-small-python-package-to-find-the-delay-between-time-series/11727) (discourse:mne, 2026-03-04) — "A few years ago, during my PhD ... I developed a small Python package called find_delay"
  - [Stream Muse 5th (AUX) EEG Channels](https://github.com/brainflow-dev/brainflow/issues/504) (github:brainflow-dev/brainflow, 2022-06-03) — "Using bluemuse is currently"

## 26. Lightweight clinical EEG review, annotation and biomarkers — score 4.5
- Clinical viewers are costly or heavy, bulk sleep-staging correction is slow, qualified readers are hard to find, HFO and biomarker detectors are scattered, and patients can't get deeper analysis of their own EEG.
- Items: 6 · paying signals: 4 · engagement: 60 · who: clinician 3, academic_lab 3
- ML fit 0.45: Browser viewers and ML pre-annotation fit the builder, but clinical validation and regulatory needs are a large barrier.
- Product idea: Browser-based EDF viewer with ML pre-annotation (sleep stages, artifacts) and bulk-edit review workflow.
- Evidence:
  - [Seeking Epileptologist for Independent Review of OpenNeuro EEG Recordings](https://mne.discourse.group/t/seeking-epileptologist-for-independent-review-of-openneuro-eeg-recordings/11875) (discourse:mne, 2026-06-30) — "The review would be compensated."
  - [Seeking guidance on EEG analysis for SCN2A mutation clinical case (Beginner with programming)](https://mne.discourse.group/t/seeking-guidance-on-eeg-analysis-for-scn2a-mutation-clinical-case-beginner-with-programming/11882) (discourse:mne, 2026-07-10) — "I have no prior background in Python ... but I am highly motivated to learn"
  - [Is there a way to select and edit annotations in raw.plot() at the same time? If not, would that be an upcoming feature in a future update?(Holding shift and selecting multiple annotations)](https://mne.discourse.group/t/is-there-a-way-to-select-and-edit-annotations-in-raw-plot-at-the-same-time-if-not-would-that-be-an-upcoming-feature-in-a-future-update-holding-shift-and-selecting-multiple-annotations/11559) (discourse:mne, 2025-10-30) — "I feel that would save a tremendous amount of time"
  - [I built a free, open-source EEG annotation tool that runs on any laptop (Windows/macOS) — no hospital workstation needed](https://mne.discourse.group/t/i-built-a-free-open-source-eeg-annotation-tool-that-runs-on-any-laptop-windows-macos-no-hospital-workstation-needed/11753) (discourse:mne, 2026-03-18) — "EDF viewers either cost money, require a powerful machine, or are painful to install."
  - [Scaling - Sensitivity (uV/mm)](https://mne.discourse.group/t/scaling-sensitivity-uv-mm/5079) (discourse:mne, 2022-06-15)

## 27. Affordable large-scale labeled neural data collection — score 2.0
- Startups and hobbyists lack the money for research-grade hardware and for recruiting participants to collect the large, diverse labeled EEG datasets needed to train decoders.
- Items: 5 · paying signals: 5 · engagement: 203 · who: startup 3, hobbyist 2
- ML fit 0.2: This needs hardware, participants and in-person operations, which the builder doesn't have.
- Product idea: Marketplace connecting distributed consumer-headset owners to paid, standardized remote recording tasks.
- Evidence:
  - [Please Join Our Thought-To-Text Research!](https://www.reddit.com/r/BCI/comments/1kmq5vm/please_join_our_thoughttotext_research/) (reddit:r/BCI, 2025-05-14) — "we're paying up to $500"
  - [Starting a BCI company with (almost) no money](https://www.reddit.com/r/BCI/comments/1lrgdgr/starting_a_bci_company_with_almost_no_money/) (reddit:r/BCI, 2025-07-04) — "Starting a BCI company with (almost) no money"
  - [Would you want to make money selling your brain data?](https://www.reddit.com/r/BCI/comments/1p13oqj/would_you_want_to_make_money_selling_your_brain/) (reddit:r/BCI, 2025-11-19) — "BCI companies get access to diverse datasets to accelerate their development"
  - [Rate my first BCI project please](https://www.reddit.com/r/BCI/comments/1tuu5hy/rate_my_first_bci_project_please/) (reddit:r/BCI, 2026-06-02) — "I am too broke for eeg headset yet."
  - [Who else wants to build their own EEG?](https://www.reddit.com/r/OpenBCI/comments/1aih4pq/who_else_wants_to_build_their_own_eeg/) (reddit:r/OpenBCI, 2024-02-04) — "I'm broke lol."
