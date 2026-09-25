## 6. MATLAB/EEGLAB environment breakage (pinned container + health check)
- **Free:** EEGLAB's compiled Win/Mac/Linux build runs on MATLAB Runtime with no license [eeglab.org](https://eeglab.org/others/Compiled_EEGLAB.html); Neurodesk EEGLAB container [neurodesk.org](https://neurodesk.org/getting-started/neurocontainers/); NSG runs EEGLAB and plugins on free HPC, non-commercial [eeglab.org](https://eeglab.org/plugins/nsgportal/); EEGLAB as a MATLAB Online add-on, GUI partly broken [MATLAB Answers](https://www.mathworks.com/matlabcentral/answers/214610-is-there-someway-i-can-use-the-eeglab-toolbox-with-matlab-online); community MATLAB Runtime Docker images [demartis](https://github.com/demartis/matlab_runtime_docker).
- **Paid reference:** EmotivPRO Standard $1,068/yr [emotiv.com](https://www.emotiv.com/pro-licensing-table-v1), a vendor tool rather than a direct competitor. MATLAB academic pricing is quote-only [mathworks.com](https://www.mathworks.com/campaigns/offers/matlab-toolbox-price-request.html).
- **Reachable base:** 4,247 on the EEGLAB discussion list, 9,265 on the news list, ~100k downloads since 2003 [inc.ucsd.edu](https://inc.ucsd.edu/events/eeglab/eeglab.php).
- **Pays?** No evidence found for environment fixing.
- **Price:** $240/yr per lab (ASSUMPTION; must sit far below EmotivPRO because free builds exist).
- **Customers @24mo:** 3 / 10 / 30 = 0.03% / 0.1% / 0.3% of news-list subscribers (ASSUMPTION). **ARR:** $720 / $2,400 / $7,200.
- **Hours:** MVP 120h + 3 h/wk (ASSUMPTION) ≈ 410h. **Infra:** ~$10/mo (ASSUMPTION).
- **ROI:** $2,400 ÷ 410h ≈ **$6/h**.
- **Risk:** compiled EEGLAB, Neurodesk and NSG are free, and the real bugs are in EEGLAB's STUDY code, which a container can't fix.

## 7. Multi-device timestamp sync (XDF/LSL sync auditor)
- **Free:** pyxdf / xdf-Matlab already do clock-offset correction and dejittering on import [LSL docs](https://labstreaminglayer.readthedocs.io/info/time_synchronization.html); a pyxdf fork adds chunk dejittering [github](https://github.com/MKnierim/pyxdf); Brain Products LSL Viewer [brainproducts.com](https://www.brainproducts.com/support-resources/tips-and-tricks-for-lsl/).
- **Paid:** iMotions (EEG + eye-tracking + sensor sync) from $2,900/yr [sourceforge](https://sourceforge.net/software/product/iMotions/), [imotions.com](https://imotions.com/products/pricing/); Cedrus StimTracker bundle $1,795 [store.cedrus.com](https://store.cedrus.com/products/stimtracker); BIOPAC sells LSL for AcqKnowledge as a licensed add-on [biopac.com](https://www.biopac.com/product/lsl-license-for-acqknowledge/).
- **Pays?** Yes. Diademics (founded by an LSL lead developer) does paid LSL consulting [diademics.com](http://www.diademics.com/), [workshop PDF](https://sccn.ucsd.edu/githubwiki/files/20210615-EEGLAB_workshop.pdf), and iMotions and StimTracker show labs pay for sync.
- **Reachable base:** LSL mentioned in 2,300+ articles by mid-2025, 150+ device classes [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12434378/). No lab count found.
- **Price:** $500/yr per lab (ASSUMPTION; ~1/6 of iMotions, software-only and offline).
- **Customers @24mo:** 5 / 15 / 40 (ASSUMPTION). **ARR:** $2.5k / $7.5k / $20k.
- **Hours:** MVP 200h including a cheap two-device test rig + 3 h/wk (ASSUMPTION) ≈ 490h. **Infra:** ~$10/mo (ASSUMPTION).
- **ROI:** $7.5k ÷ 490h ≈ **$15/h**.
- **Risk:** without ground-truth hardware (photodiode/TTL) the "certificate" is hard to trust, and pyxdf covers the common case for free.

## 8. Managed spike sorting (upload-and-sort GPU service)
- **Free:** Kilosort4, including Colab [docs](https://kilosort.readthedocs.io/); SpikeInterface [github](https://github.com/SpikeInterface/spikeinterface); NeuroCAAS free cloud analysis [Neuron](https://www.cell.com/neuron/fulltext/S0896-6273(22)00587-6); Allen Institute's open Nextflow pipeline on Code Ocean/AWS [eLife](https://elifesciences.org/articles/110170).
- **Paid:** Plexon Offline Sorter, USB license key, price not public [plexon.com](https://plexon.com/news-and-events/special-pricing-on-offline-sorter-upgrades/); 3Brain BrainWave (HD-MEA), price not public [3brain.com](https://www.3brain.com/products/software/brainwave-6); CatalystNeuro paid SpikeInterface/NWB pipeline consulting, Simons-funded projects [catalystneuro.com](https://catalystneuro.com/), [INCF](https://www.incf.org/partners/catalystneuro).
- **Compute cost:** a 2h, 6-probe session ≈ $66 on AWS, ~$5.50 per probe-hour [eLife/PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13441294/).
- **Reachable base:** 850+ labs have used Neuropixels since 2017 [DataJoint](https://datajoint.com/neuropixels-plainly-explained/); imec says "more than 400" / "450 labs" [imec](https://www.imec-int.com/en/press/latest-neuropixels-probes-can-track-neurons-over-weeks), [HHMI](https://www.hhmi.org/news/new-silicon-probes-record-activity-hundreds-neurons-simultaneously). A Neuropixels 1.0 probe costs ~$1,400 [Simons](https://www.simonsfoundation.org/2021/07/19/a-new-era-in-neural-recording/).
- **Price:** ~$250/mo per lab ($3k/yr) including ~40 probe-hours (ASSUMPTION).
- **Customers @24mo:** 3 / 8 / 20 = 0.35% / 1% / 2.4% of 850 labs (ASSUMPTION). **ARR:** $9k / $24k / $60k.
- **Hours:** MVP 250h (upload, queue, GPU runner, Phy/NWB export, provenance) + 5 h/wk (ASSUMPTION) ≈ 730h. **Infra:** ~$150/mo baseline (ASSUMPTION) + GPU passed through at ~$5.50/probe-hour.
- **Upload friction (own arithmetic):** 384 ch × 30 kHz × 2 B ≈ 83 GB per probe-hour of raw AP data.
- **ROI:** $24k ÷ 730h ≈ **$33/h**.
- **Risk:** the free Allen/Code Ocean pipeline and in-lab GPUs undercut it, and institutional data policies plus 80+ GB uploads slow adoption.

## 9. Independent EEG headset comparison site
- **Free:** Mindtecstore comparison table [mindtecstore](https://www.mindtecstore.com/EEG-Headset-comparison-table); vendor guides from Emotiv [emotiv.com](https://www.emotiv.com/blogs/news/bci-headset-for-developers), Neurosity [neurosity.co](https://neurosity.co/guides/neurosity-crown-vs-sensai) and Muse [choosemuse.com](https://choosemuse.com/blogs/news/top-brain-training-devices-2026); AJProTech ranking [ajprotech.com](https://ajprotech.com/blog/articles/top-10-eeg-devices-of-2025.html); academic comparisons [PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0291186), [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11679099/), [ResearchGate](https://www.researchgate.net/publication/399129177_Beyond_the_lab_real-world_benchmarking_of_wearable_EEGs_for_passive_brain-computer_interfaces).
- **Pays?** No evidence for paid reviews. Only affiliate programs: Muse [choosemuse.com](https://choosemuse.com/pages/partnerships) (10% commission per a search summary, unverified), OpenBCI by email inquiry [docs.openbci.com](https://docs.openbci.com/FAQ/GenFAQ/).
- **Reachable base:** Muse 500k+ users [Wikipedia](https://en.wikipedia.org/wiki/Muse_(headband)); NeuroTechX 6,000+ Slack members [neurotechx.com](https://neurotechx.com/community/); OpenBCI users in 60+ countries [openbci.com](https://openbci.com/).
- **Price:** free site + $49 feasibility report + affiliate income (ASSUMPTION).
- **Volume @24mo:** 20 / 60 / 200 reports/yr + 20 / 50 / 150 referrals × $300 × 10% (ASSUMPTION). **Revenue:** ~$1.6k / $4.4k / $14.3k per year, mostly not recurring.
- **Hours:** MVP 150h (public-dataset decoding benchmarks per device) + 3 h/wk (ASSUMPTION) ≈ 440h. **Infra:** ~$10/mo (ASSUMPTION).
- **ROI:** $4.4k ÷ 440h ≈ **$10/h**.
- **Risk:** without the hardware it isn't independent testing, and vendor content dominates search.

## 10. Stream integrity watchdog
- **Free:** Brain Products LSL Viewer, plus their advice to monitor sample counters online [brainproducts.com](https://www.brainproducts.com/support-resources/tips-and-tricks-for-lsl/); MNE-LSL [mne.tools](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.lsl.StreamInlet.html); BrainFlow and OpenBCI GUI; the published EEG Quality Index method [IEEE](https://ieeexplore.ieee.org/iel7/8932636/8936133/08936246.pdf).
- **Paid:** EmotivPRO shows real-time signal quality, $89/mo or $1,068/yr Standard, locked to Emotiv hardware [emotiv.com](https://www.emotiv.com/pro-licensing-table-v1), [guide](https://www.emotiv.com/blog/eeg-data-acquisition-software-guide).
- **Pays?** Only EmotivPRO's bundled display; the mining report has just 2 paying signals here, and no standalone commercial monitor was found.
- **Reachable base:** LSL 2,300+ citing articles [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12434378/); OpenBCI 60+ countries [openbci.com](https://openbci.com/). No count of active streaming labs.
- **Price:** $150/yr per seat (ASSUMPTION; ~1/7 of EmotivPRO, narrow function).
- **Customers @24mo:** 5 / 20 / 60 (ASSUMPTION). **ARR:** $750 / $3k / $9k.
- **Hours:** MVP 120h (testable on recorded files) + 2 h/wk (ASSUMPTION) ≈ 310h. **Infra:** ~$10/mo, local + license server (ASSUMPTION).
- **ROI:** $3k ÷ 310h ≈ **$10/h**.
- **Risk:** it's a small feature BrainFlow, OpenBCI GUI or LSL could ship free, and willingness to pay is barely evidenced.

## Summary (6–10)
- **Base-case ROI:** spike sorting ~$33/h > sync ~$15/h > integrity monitoring ~$10/h ≈ headset comparison ~$10/h > EEGLAB containers ~$6/h.
- Hours assume 15 h/wk over 104 weeks (~1,560h available), MVP + maintenance; $/h figures exclude infra.
- All customer counts, prices and hours are assumptions; only competitor, cost and market-size facts are sourced.
