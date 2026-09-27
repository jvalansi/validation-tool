# bci pain points — ranked

Items scanned: 1356 (github 713, reddit 354, discourse 289); labelled as pains: 701.
Score = count × (1 + share with paying signal) × ML fit. ML fit and clustering are Claude judgements, not measurements.

## 1. Installation, build and dependency breakage — score 68.2
- Building from source (CMake/Qt/submodules), missing prebuilt binaries, pinned-dependency conflicts, MATLAB toolbox/path/plugin-manager failures, paid-toolbox dependencies and upgrade churn (NumPy 2, matplotlib) break environments and reproducibility.
- Items: 104 · paying signals: 20 · engagement: 984 · who: academic_lab 48, developer 20, student 19
- Fit 0.55: Curated, version-locked hosted or containerized environments are software the builder can automate, but they compete with free conda/Docker and the ecosystem churns constantly.
- Product idea: Hosted, version-pinned neuro-analysis environments (MNE/EEGLAB-alt/spike sorting) that launch in one click with known-good dependency sets.
- Evidence:
  - [RuntimeException (Waited 5000ms for... processing.opengl.PSurfaceJOGL)](https://github.com/OpenBCI/OpenBCI_GUI/issues/577) (github:OpenBCI/OpenBCI_GUI, 2019-08-21) — "I scrapped everything and followed the ... guide to a T multiple times"
  - [ICLabel issue when using BrainBeats ](https://github.com/sccn/eeglab/issues/707) (github:sccn/eeglab, 2023-12-06) — "I've solved a lot of previous error messages by installing plug ins, but I am new to EEGLAB and at a loss how to fix this one"
  - [wrong number of arguments error while using GUI](https://github.com/sccn/eeglab/issues/36) (github:sccn/eeglab, 2019-08-07) — "I temporarily fixed the issue last week by uninstalling MATLAB on both machines and reinstalling the newest version. Then it began occurring again"
  - [Expected dtype object, got 'numpy.dtype[float64]'](https://mne.discourse.group/t/expected-dtype-object-got-numpy-dtype-float64/3151) (discourse:mne, 2021-05-18) — "I used read_raw_bids in the last few days. But it did not work today"
  - [error in function std_precomp()](https://github.com/sccn/eeglab/issues/739) (github:sccn/eeglab, 2024-03-04) — "EEGLAB worked well last year"

## 2. Multi-device timestamp sync and LSL/XDF alignment — score 55.9
- Aligning EEG with eye trackers, physio sensors, video, VR and stimulus markers across machines is hard. Users hit LSL discovery failures, jittery or jumping timestamps, relative clocks, trigger delays, missing connectors, no browser/cloud relay, and no way to validate sync quality.
- Items: 73 · paying signals: 13 · engagement: 477 · who: academic_lab 48, developer 11, student 6
- Fit 0.65: Offline XDF sync repair, dejittering and a sync-quality report are pure software with a clear value proposition, while live connectors touch hardware.
- Product idea: XDF/multistream sync analyzer that detects clock jumps and drift, dejitters, aligns streams and outputs a sync-quality report plus corrected files.
- Evidence:
  - [Very specific LSL sync issues](https://github.com/sccn/labstreaminglayer/issues/13) (github:sccn/labstreaminglayer, 2019-01-27) — "I recorded 20 subjects worth of EEG data"
  - [Markers sent from computer with "`n" (n=1..9) create important noise on the 16 channels](https://github.com/OpenBCI/OpenBCI_GUI/issues/297) (github:OpenBCI/OpenBCI_GUI, 2017-12-13) — "sending Markers makes a huge noise on ALL electrodes at marker onset"
  - [OpenBCI x Emotibit xdf file import error](https://github.com/sccn/eeglab/issues/826) (github:sccn/eeglab, 2024-11-13) — "Since i'm not dependent on using eeglab for this purpose, is there any other way of using Emotibit data with other data in an xdf file?"
  - [LSL manual timestamping interferes with LSL clock_offset correction](https://github.com/OpenBCI/OpenBCI_GUI/issues/775) (github:OpenBCI/OpenBCI_GUI, 2020-05-21) — "I'm one of the LSL maintainers. I'm trying to help a user with a problem."
  - [Add Support to Polar H10](https://github.com/brainflow-dev/brainflow/issues/670) (github:brainflow-dev/brainflow, 2023-08-30) — "My team is currently working on a project with Muse, EmotiBit, and Polar H10"

## 3. Statistics, source localization and methods expertise gap — score 55.2
- Users struggle with group STUDY designs, repeated-measures and cluster statistics, beamformer and forward-model setup, coordinate frames, connectivity and PAC choices, and spectral units, and they rely on forums for expert judgment.
- Items: 73 · paying signals: 19 · engagement: 723 · who: academic_lab 61, student 12
- Fit 0.6: An LLM agent that knows MNE/FieldTrip can generate and check analysis code, but correctness is hard to guarantee and the audience is niche.
- Product idea: Domain-tuned AI analysis copilot that writes, runs and sanity-checks MNE pipelines and statistical designs on the user's data.
- Evidence:
  - [ENH: encoding models](https://github.com/mne-tools/mne-python/issues/2796) (github:mne-tools/mne-python, 2016-01-19) — "Most of what I've been working on for my thesis has been so-called "encoding" models"
  - [How to realign the CTF MEG runs to a common head position using maxwell_filter?](https://mne.discourse.group/t/how-to-realign-the-ctf-meg-runs-to-a-common-head-position-using-maxwell-filter/4727) (discourse:mne, 2022-04-18) — "concatenate 12 different MEG runs"
  - [std_rmalldatafields() line 65](https://github.com/sccn/eeglab/issues/470) (github:sccn/eeglab, 2022-05-08) — "I did a trial with the first 3 subjects and it worked perfectly, but when I am adding the 18 subjects I have this error."
  - [std_preclust error: subscripted assignment dimension mismatch](https://github.com/sccn/eeglab/issues/138) (github:sccn/eeglab, 2020-03-05) — "I keep getting a bug where in STUDY.cluster.sets I get NAN in the same sets, and I manually fix this matrix"
  - [Loading issue from Paul](https://github.com/sccn/eeglab/issues/362) (github:sccn/eeglab, 2021-08-06) — "I tried letting it run about 20 min (way longer than ever needed before for only 32 subjects)"

## 4. Automated preprocessing and artifact QC — score 53.25
- Researchers don't know the right preprocessing order (filtering, ICA, interpolation, AutoReject). Automated bad-channel and artifact detection is unreliable, ICA review is manual, events desync after cropping, and batch QC reports have to be hand-scripted.
- Items: 55 · paying signals: 16 · engagement: 508 · who: academic_lab 38, student 11, clinician 4
- Fit 0.75: An opinionated, ML-assisted pipeline with automatic QC reports is batch software that scales without per-customer work.
- Product idea: Upload-to-report EEG preprocessing service with a validated default pipeline, ML artifact/ICA classification and reproducible QC reports.
- Evidence:
  - [parallel processing with silence_periods](https://github.com/SpikeInterface/spikeinterface/issues/4038) (github:SpikeInterface/spikeinterface, 2025-07-07) — "written and applied a function to detect these periods"
  - [Thinking about making an open-source SDK for EEG/BCI analysis. Looking for thoughts from BCI/neural data scientists, researchers, or ML engineers.](https://www.reddit.com/r/BCI/comments/1sgct4x/thinking_about_making_an_opensource_sdk_for/) (reddit:r/BCI, 2026-04-09) — "3 weeks to make a b-spline interpolation for bad channels, 2 weeks to detect drowsiness from delta waves, 2 weeks for noise + artifact removal"
  - [Automatic EEG quality check & ICA for blink removal in 19-channel dry EEG](https://mne.discourse.group/t/automatic-eeg-quality-check-ica-for-blink-removal-in-19-channel-dry-eeg/11722) (discourse:mne, 2026-03-03) — "I am not an EEG expert, Visually inspecting every subject's data is difficult"
  - [annotating bad segments, then cropping signal, annotations don't get shifted?](https://mne.discourse.group/t/annotating-bad-segments-then-cropping-signal-annotations-dont-get-shifted/11221) (discourse:mne, 2025-05-23) — "Luckily, my colleague compared the pre/post cropping annotations and noted that they didn`t get shifted."
  - [`eegplot()` extremly slow when plotting later epochs](https://github.com/sccn/eeglab/issues/108) (github:sccn/eeglab, 2020-01-06) — "more than 20 seconds to plot 20 trials - which is honestly unbearable"

## 5. File format import and cross-tool conversion — score 50.25
- EDF+/BDF/BrainVision/MFF/CNT/Nihon Kohden and consumer CSV files fail to import or silently lose annotations, events, units and channel locations. Conversion between EEGLAB, MNE and FieldTrip is lossy, and there's no JS/browser reader.
- Items: 57 · paying signals: 10 · engagement: 590 · who: academic_lab 31, student 16, developer 4
- Fit 0.75: Parsing, validating and converting formats is deterministic software that is easy to test with sample files and suits a self-serve web or API product.
- Product idea: Web/API converter and validator for EEG formats that preserves events, units and montages, with a diff report of anything lost.
- Evidence:
  - [Is there a way to speed up loading EDF files?](https://mne.discourse.group/t/is-there-a-way-to-speed-up-loading-edf-files/8013) (discourse:mne, 2023-12-14) — "Loading these files using mne.io.read_raw takes about 5 minutes, or more. I just tried one that took 11 minutes to open."
  - [Data stream freezes when saving in the BDF+ file type](https://github.com/OpenBCI/OpenBCI_GUI/issues/266) (github:OpenBCI/OpenBCI_GUI, 2017-10-16) — "I want to use the BDF+ file type so I do not have to convert the data in EDFbrowser to BDF for import into EEGLAB"
  - [MFF files imports not working](https://github.com/sccn/eeglab/issues/797) (github:sccn/eeglab, 2024-08-15) — "I have tried different version of Matlab, EEGlab, mffimport plugin. I have also increased the JAVA memory allowance."
  - [MFF bug with old EGI files](https://github.com/sccn/eeglab/issues/263) (github:sccn/eeglab, 2021-03-03) — "EGI data recorded over 10 years ago"
  - [3.2.0 - Interface freezing when converting from SD format](https://github.com/OpenBCI/OpenBCI_GUI/issues/302) (github:OpenBCI/OpenBCI_GUI, 2017-12-26) — "After 1 hour I give up and end the program, reboot, and tried again."

## 6. NWB/BIDS conversion, validation and metadata — score 35.0
- Converting lab data to NWB/BIDS is error-prone. Users report confusing extensions, false validator errors, awkward metadata editing, schema migrations, slow cloud streaming of large HDF5, event IDs altered during conversion, and manual de-identification.
- Items: 38 · paying signals: 12 · engagement: 491 · who: academic_lab 31, developer 4, student 3
- Fit 0.7: Schema-driven conversion, validation and de-identification can be automated with agents and sold self-serve to labs with data-sharing mandates.
- Product idea: Guided NWB/BIDS converter with plain-English validation, metadata editing, de-identification and cloud-optimized output.
- Evidence:
  - [[Feature]: Add `read_nwb` to simplify reading nwbfiles ](https://github.com/NeurodataWithoutBorders/pynwb/issues/1974) (github:NeurodataWithoutBorders/pynwb, 2024-10-23) — "This is a comment that I have gotten from various users: reading and nwbfile is not as easy as it could be."
  - [Error: Compensation grade of ICA (3) and Raw (0) do not match](https://mne.discourse.group/t/error-compensation-grade-of-ica-3-and-raw-0-do-not-match/11731) (discourse:mne, 2026-03-06) — "allow me to replicate (I admit, almost blindly) my reference pipeline via the config file"
  - [Need to store video](https://github.com/NeurodataWithoutBorders/pynwb/issues/1647) (github:NeurodataWithoutBorders/pynwb, 2023-02-16) — "For one recording session, we have around 300 short videos"
  - [conversion_factor per channel](https://github.com/NeurodataWithoutBorders/pynwb/issues/1064) (github:NeurodataWithoutBorders/pynwb, 2019-09-13) — "Neuropixel data is very big, so this is really not an ideal solution."
  - [[Documentation]: Streaming NWB files - recommend using remfile as the preferred method](https://github.com/NeurodataWithoutBorders/pynwb/issues/1791) (github:NeurodataWithoutBorders/pynwb, 2023-11-24) — "I created remfile about 3-4 months ago to address the slowness in lazy reading of remote NWB files"

## 7. Public dataset access and decoder benchmarking — score 31.5
- Public EEG datasets are scattered and hosted on fragile mirrors, and their loaders have silent label/epoch bugs and inconsistent metadata. Benchmarking lacks standard protocols, caching and a compute-backed leaderboard, and it's hard to know whether models transfer to consumer headsets.
- Items: 39 · paying signals: 6 · engagement: 534 · who: academic_lab 22, student 8, developer 4
- Fit 0.7: Mirrored, validated dataset catalogs and hosted benchmark runs are ML-engineering work that fits the builder, though compute costs scale with use.
- Product idea: Harmonized, validated EEG dataset hub with partial downloads and a hosted leaderboard that runs submitted decoders under standard CV protocols.
- Evidence:
  - [Please Join Our Thought-To-Text Research!](https://www.reddit.com/r/BCI/comments/1kmq5vm/please_join_our_thoughttotext_research/) (reddit:r/BCI, 2025-05-14) — "we're paying up to $500"
  - [Would you want to make money selling your brain data?](https://www.reddit.com/r/BCI/comments/1p13oqj/would_you_want_to_make_money_selling_your_brain/) (reddit:r/BCI, 2025-11-19) — "BCI companies get access to diverse datasets to accelerate their development"
  - [Problem with create_windows_from_events working on an personal dataset](https://github.com/braindecode/braindecode/issues/135) (github:braindecode/braindecode, 2020-07-06) — "I modified a bit the library ... I added a copy of bnci.py script at moabb datasets"
  - [Allow passing fixed transformers to evaluations](https://github.com/NeuroTechX/moabb/issues/367) (github:NeuroTechX/moabb, 2023-05-05) — "The expensive part of the evaluation is the feature extraction"
  - [New CrossSubjecEvaluation that supports transfer learning methods](https://github.com/NeuroTechX/moabb/issues/1077) (github:NeuroTechX/moabb, 2026-06-11) — "I myself am working on a transfer learning cross subject method and all this is motivated by real needs."

## 8. Silent data loss and recording integrity — score 30.6
- Recordings silently drop samples, zero auxiliary channels, mis-scale units, corrupt SD-card or BDF/EDF exports, save to unknown locations, or can't be replayed. Long sleep recordings have no segmentation, and impedance/signal-quality checks are untrustworthy.
- Items: 42 · paying signals: 9 · engagement: 630 · who: academic_lab 21, unknown 9, hobbyist 6
- Fit 0.6: A file-level integrity checker (gaps, rate drift, zeroed channels, scaling) is pure software, works on uploaded files and is self-serve.
- Product idea: Upload-and-verify recording QA that flags dropped samples, rate mismatches, dead aux channels and format corruption, with a repaired export.
- Evidence:
  - [Not getting Trigger data using wifi shield connected to Cyton and daisy combination](https://github.com/OpenBCI/OpenBCI_GUI/issues/272) (github:OpenBCI/OpenBCI_GUI, 2017-10-24) — "Any help you can provide in this regard is much appreciated"
  - [SD Card writing is not working ](https://github.com/OpenBCI/OpenBCI_GUI/issues/278) (github:OpenBCI/OpenBCI_GUI, 2017-11-01) — "Tried: 2 different SD cards, Reformatting SD cards (with the SD Association Formatter), Wifi and BLE"
  - [Unable to convert large files from SD card: Out of Memory Error](https://github.com/OpenBCI/OpenBCI_GUI/issues/355) (github:OpenBCI/OpenBCI_GUI, 2018-07-08) — "I'm trying to open a large file I recorded on the SD card during a 8 hours of sleep"
  - [Add support to prevent long recordings](https://github.com/OpenBCI/OpenBCI_GUI/issues/461) (github:OpenBCI/OpenBCI_GUI, 2019-03-19) — "it is laborious and erroneous to start and stop recordings every 20-30 minutes"
  - [Problem finding saved recordings on linux](https://github.com/OpenBCI/OpenBCI_GUI/issues/639) (github:OpenBCI/OpenBCI_GUI, 2019-11-08) — "Any clues would be highly appreciated!"

## 9. Device connection and SDK cross-platform failures — score 22.2
- BLE/WiFi/serial/dongle connections to consumer and research EEG boards fail, hang or silently stall across Windows/macOS/Linux/Raspberry Pi. Errors are opaque, there is no auto-discovery, bindings (Java/.NET/Node/Electron/iOS) are inconsistent, and firmware or OS updates break drivers.
- Items: 60 · paying signals: 14 · engagement: 591 · who: hobbyist 24, academic_lab 13, developer 11
- Fit 0.3: Software can fix it, but the work is tied to physical devices, OS Bluetooth stacks and vendor firmware, so testing needs hardware and support load grows with each device model.
- Product idea: Cross-platform connection doctor that walks through a device/OS diagnostic checklist and maps opaque SDK errors to fixes.
- Evidence:
  - [testing 4.1.2 with wi-fi shield](https://github.com/OpenBCI/OpenBCI_GUI/issues/555) (github:OpenBCI/OpenBCI_GUI, 2019-07-05) — "I need to start the system 3 times, before it starts working"
  - [AAVAA board: native BLE does not connect to device on MacOS](https://github.com/brainflow-dev/brainflow/issues/667) (github:brainflow-dev/brainflow, 2023-08-17) — "AAVAA-Inc maintaining a fork (AAVAAflow) to add their board"
  - [Muse S Athena on Windows 11: Failed to notify characteristic 273e0014 using MUSE_S_ATHENA_BOARD](https://github.com/brainflow-dev/brainflow/issues/835) (github:brainflow-dev/brainflow, 2026-05-19) — "Bluetooth adapter: TP-Link UB500 (Bluetooth 5.4) / Intel Bluetooth disabled"
  - [GUI freezes at start on Mac OS Sierra 10.12.3](https://github.com/OpenBCI/OpenBCI_GUI/issues/118) (github:OpenBCI/OpenBCI_GUI, 2017-02-02) — "should I downgrade my OS or is there a quick fix?"
  - [Muse S Athena Support (MS-03)](https://github.com/brainflow-dev/brainflow/issues/776) (github:brainflow-dev/brainflow, 2025-07-02) — "we have been using the muse 2 for research until the athena dropped, and it has no support yet"

## 10. 3D visualization, montages and publication figures — score 20.15
- The VTK/pyvista 3D backends break, especially on headless or HPC machines. Montage and electrode templates are confusing or conflicting, channel adjacency is unvalidated, and publication figures (ERP CIs, difference topomaps, ROI maps) need custom code.
- Items: 30 · paying signals: 1 · engagement: 384 · who: academic_lab 19, student 5, developer 3
- Fit 0.65: Browser-rendered visualization and a curated montage library are pure software, but willingness to pay is modest.
- Product idea: Web-based figure studio for EEG/MEG (topomaps, 3D sources, montage library) that works without a local graphics stack.
- Evidence:
  - [STUDY visualisation is slow](https://github.com/sccn/eeglab/issues/290) (github:sccn/eeglab, 2021-05-06) — "Previously it was trivial, each time it took 1-5 minutes... With the switch to single-trial it takes forever... daterp's from my study collectively weigh about 20.7 Gb"
  - [Create canonical template channel locations](https://github.com/mne-tools/mne-python/issues/7472) (github:mne-tools/mne-python, 2020-03-18)
  - [Scaling - Sensitivity (uV/mm)](https://mne.discourse.group/t/scaling-sensitivity-uv-mm/5079) (discourse:mne, 2022-06-15)
  - [How to solve "can not import name 'Brain' from 'Surfer'](https://mne.discourse.group/t/how-to-solve-can-not-import-name-brain-from-surfer/4390) (discourse:mne, 2022-02-09)
  - [GUI and display [not working as intended]](https://mne.discourse.group/t/gui-and-display-not-working-as-intended/4325) (discourse:mne, 2022-01-27)

## 11. Structured BCI/neural-data learning paths — score 18.7
- Newcomers from biology, medicine or data science lack a project-based roadmap covering the neuroscience, signal processing, coding, math and hardware choices, and many lack mentorship or labs.
- Items: 23 · paying signals: 11 · engagement: 516 · who: student 14, hobbyist 5, academic_lab 3
- Fit 0.55: Self-serve interactive courses with hosted notebooks and public datasets scale well, but the market is crowded and mentorship pulls toward service work.
- Product idea: Project-based interactive BCI curriculum with hosted notebooks on public datasets and auto-graded checkpoints.
- Evidence:
  - [Switching from Finance to Computational Neuroscience — Looking for Learning Partners or Beginner Projects](https://www.reddit.com/r/compmathneuro/comments/1k7qzkx/switching_from_finance_to_computational/) (reddit:r/compmathneuro, 2025-04-25) — "I'm just not sure how to speed up the process of figuring out if this is something I'd enjoy doing long term."
  - [Learning Python and maths for computational neuroscience as a beginner](https://www.reddit.com/r/compmathneuro/comments/1vo3myu/learning_python_and_maths_for_computational/) (reddit:r/compmathneuro, 2026-08-14) — "I have about a year to prepare before starting my PhD"
  - [How do I get into BCI](https://www.reddit.com/r/BCI/comments/1q30oe5/how_do_i_get_into_bci/) (reddit:r/BCI, 2026-01-03) — "I dont rly have money for the hardware"
  - [Online courses on Computational Neuroscience](https://www.reddit.com/r/compmathneuro/comments/wq65ih/online_courses_on_computational_neuroscience/) (reddit:r/compmathneuro, 2022-08-16) — "I've started the Coursera course, but i don't have math knowledge to keep up with it."
  - [Self-studying CompNeuro from a CS/AI background in a developing country - Am I doing this right?](https://www.reddit.com/r/compmathneuro/comments/1nty5ry/selfstudying_compneuro_from_a_csai_background_in/) (reddit:r/compmathneuro, 2025-09-29) — "limited computing resources... limited funding"

## 12. Real-time BCI and neurofeedback pipeline building — score 18.0
- Closed-loop BCI and neurofeedback apps require stitching acquisition, artifact handling, decoding and feedback by hand. Real-time frameworks are hard to debug and install, there's no browser-native streaming, and game-engine integration, lightweight edge processing and device simulators are missing.
- Items: 30 · paying signals: 6 · engagement: 215 · who: developer 16, hobbyist 7, student 3
- Fit 0.5: A software SDK or low-code builder is feasible, but real-time reliability depends on the device layer, and the hobbyist market has low willingness to pay.
- Product idea: Browser-based low-code real-time BCI builder with a device simulator, reusable feature recipes and exports to Unity/OSC.
- Evidence:
  - [My current project (Looking for advice!)](https://www.reddit.com/r/BCI/comments/1wgdf58/my_current_project_looking_for_advice/) (reddit:r/BCI, 2026-09-14) — "was there a cheaper option than the 250 dollars kit ... Also is there a place I can hire someone to help me for this?"
  - [MNE-RT: an open-source real-time neurofeedback/BCI framework](https://mne.discourse.group/t/mne-rt-an-open-source-real-time-neurofeedback-bci-framework/11898) (discourse:mne, 2026-07-19) — "It covers the entire closed-loop pipeline in a single, researcher-friendly API"
  - [BCI for a 3 year old?](https://www.reddit.com/r/OpenBCI/comments/1dgs683/bci_for_a_3_year_old/) (reddit:r/OpenBCI, 2024-06-15) — "I'm looking for some guidance in setting up a BCI controller for a laptop to help my daughter with a degenerative disease speak."
  - [LSL and Simulink](https://github.com/sccn/labstreaminglayer/issues/11) (github:sccn/labstreaminglayer, 2019-01-17) — "I only found a thing called SimBSI but its unstable and crashes all the time."
  - [FNIRS preprocessing based on Lab Streaming Layer](https://mne.discourse.group/t/fnirs-preprocessing-based-on-lab-streaming-layer/11669) (discourse:mne, 2026-01-21) — "we currently must save data in the .lufr format, then convert it to SNIRF through a MATLAB conversion script ... This multi-step conversion process is cumbersome"

## 13. Spike sorting compute and pipeline fragility — score 12.1
- Neuropixels/HD-MEA sorting is compute-bound, and users hit CUDA/MATLAB version hell, flaky containerized sorters, broken Phy export, file readers that break across versions, and no path on Apple Silicon.
- Items: 15 · paying signals: 7 · engagement: 465 · who: academic_lab 13, developer 1, student 1
- Fit 0.55: Hosted GPU sorting is multi-tenant software, but GPU costs, very large data transfers and per-lab debugging push support hours up.
- Product idea: Cloud spike-sorting service: upload or point to data, pick a sorter, get curated-ready Phy/NWB outputs.
- Evidence:
  - [Sorting takes extremely long when sorting a four shank probe by property](https://github.com/SpikeInterface/spikeinterface/issues/2625) (github:SpikeInterface/spikeinterface, 2024-03-26) — "it takes 8 hours to sort one of the four shanks and an estimated 160 hours to recompute the spike templates... NVIDIA RTX 4080, 64 GB RAM"
  - [Kilosort error:  sgemm in CUBLAS failed](https://github.com/SpikeInterface/spikeinterface/issues/702) (github:SpikeInterface/spikeinterface, 2022-06-13) — "Matlab R2018a, CUDA 9.0, Visual Studio 2015, NVIDIA RTX A5000"
  - [Unable to open kilosort4 results with phy](https://github.com/SpikeInterface/spikeinterface/issues/2710) (github:SpikeInterface/spikeinterface, 2024-04-11) — "None of above was works"
  - [Improper Probe Configuration when loading OpenEphys](https://github.com/SpikeInterface/spikeinterface/issues/4394) (github:SpikeInterface/spikeinterface, 2026-02-16) — "So far I thought everything was looking good, but when inspecting the units in phy I noticed..."
  - [using read_intan with timestamp gaps](https://github.com/SpikeInterface/spikeinterface/issues/3375) (github:SpikeInterface/spikeinterface, 2024-09-06) — "I have already sorted them with Kilosort... Since the update, I have been unable to load these two recordings."

## 14. Headset selection and capability comparison — score 10.8
- Buyers can't compare consumer EEG headsets on signal quality, raw-data access, SDK quality and feasibility for their goal (motor control, meditation, accessibility) before spending hundreds of dollars.
- Items: 16 · paying signals: 8 · engagement: 323 · who: hobbyist 8, student 3, developer 2
- Fit 0.45: A comparison database is easy to build, but it is content- and affiliate-driven with thin monetization and needs ongoing research on hardware.
- Product idea: Structured EEG headset comparison and feasibility checker built from SDK tests and public benchmark data.
- Evidence:
  - [The best EEG headset for programming](https://www.reddit.com/r/BCI/comments/p3mz41/the_best_eeg_headset_for_programming/) (reddit:r/BCI, 2021-08-13) — "They are all expensive so I'd hate to buy one and find out it's actually not that good for programming purposes"
  - [is there anyway for a consumer to buy a Dreem 3 headband?](https://www.reddit.com/r/BCI/comments/179tx44/is_there_anyway_for_a_consumer_to_buy_a_dreem_3/) (reddit:r/BCI, 2023-10-17) — "i would pay for it"
  - [How well does the Neurosity Crown actually work?](https://www.reddit.com/r/BCI/comments/12h0vu7/how_well_does_the_neurosity_crown_actually_work/) (reddit:r/BCI, 2023-04-10) — "I was hoping to purchase the device to help a family member with MS"
  - [Best commercial BCI for research/fun](https://www.reddit.com/r/BCI/comments/1kaa4s3/best_commercial_bci_for_researchfun/) (reddit:r/BCI, 2025-04-28) — "let you download/extract the raw data (without additional subscriptions)"
  - [Roadmap for a CS student looking to make BCI projects](https://www.reddit.com/r/BCI/comments/1hkxq1y/roadmap_for_a_cs_student_looking_to_make_bci/) (reddit:r/BCI, 2024-12-23) — "don't want to drop hundreds of dollars on something that may not be a right fit"

## 15. Affordable, high-quality EEG hardware — score 0.0
- Research-grade EEG boards, caps and electrodes are too expensive, DIY builds have signal-integrity and safety problems, raw data is locked, and there are no rental or try-before-you-buy options.
- Items: 14 · paying signals: 13 · engagement: 423 · who: hobbyist 8, startup 2, developer 2
- Fit 0.1: The core need is physical hardware and logistics. · **excluded: hardware**
- Product idea: Low-cost open EEG board or headset rental program.
- Evidence:
  - [I designed an Open Source, 8-channel EEG board (ESP32-S3 + ADS1299). Works with LSL Brainflow and forked OpenBCI GUI](https://www.reddit.com/r/BCI/comments/1polj4b/i_designed_an_open_source_8channel_eeg_board/) (reddit:r/BCI, 2025-12-17) — "Research gear was wildly unaffordable... For those who don't want to deal with BGA soldering or sourcing components, I do have assembled units available"
  - [Starting a BCI company with (almost) no money](https://www.reddit.com/r/BCI/comments/1lrgdgr/starting_a_bci_company_with_almost_no_money/) (reddit:r/BCI, 2025-07-04) — "Starting a BCI company with (almost) no money"
  - [The worst case happened: Interaxon does no longer offer the Muse SDK!!!](https://github.com/sccn/labstreaminglayer/issues/30) (github:sccn/labstreaminglayer, 2019-07-18) — "we first have to write a Matlab interface for it"
  - [Emotiv epoc flex custom / universal electrode holders](https://www.reddit.com/r/BCI/comments/1h4a9zd/emotiv_epoc_flex_custom_universal_electrode/) (reddit:r/BCI, 2024-12-01) — "Emotiv wanted hundreds for the things.  $80 and some 3D prints and we can now use universal electrodes."
  - [Is it possible to build BCI Electrode Cap from scratch?](https://www.reddit.com/r/BCI/comments/1vy8a2i/is_it_possible_to_build_bci_electrode_cap_from/) (reddit:r/BCI, 2026-08-25) — "I wanted to buy this type of caps but they are too expensive"
