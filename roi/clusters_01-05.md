## 1. Automated EEG preprocessing & artifact QC
- **Free alternatives:** MNE-Python (BSD, commercial use OK) [ref](https://pmc.ncbi.nlm.nih.gov/articles/PMC12664388/); EEG-cleanse, RELAX, BEST automated pipelines [EEG-cleanse](https://pmc.ncbi.nlm.nih.gov/articles/PMC12664388/); NeuroPype Academic Edition is free for academic research [neuropype.io](https://www.neuropype.io/academic-edition).
- **Paid:** EmotivPRO $89/mo or $1,068/yr Standard, $2,689/yr Performance [emotiv.com](https://www.emotiv.com/pages/pro-licensing-table-v1). BESA Research 2013 list €3,950 Basic / €11,600 Complete [price list](https://www.biosemi.com/publications/pdf/BESA%20Research%206.0%20-%20Price%20List%20Euro%20-%20April%20%202013.pdf); Complete perpetual now $21,401 at a reseller [neurospec](https://shop.neurospec.com/besa-research-complete). BrainVision Analyzer educational dongle €500 [brainproducts](https://www.brainproducts.com/support-resources/brainvision-analyzer-educational-license/). NeuroPype Startup/Personal $79–99/mo per a search summary, unverified (403) [intheon](https://www.intheon.io/buzz/48-neuropype-startup-edition-release).
- **Reachable base:** EEGLAB: 6,500 discussion-list users in 2017 [sccn](https://sccn.ucsd.edu/githubwiki/files/eeglab2017_ad_eeglab_overview2.pdf); ~400k downloads over 10 years, 140k sessions/month in 2021 [sccn](https://sccn.ucsd.edu/githubwiki/files/EEGLAB_overview2021.pdf). MNE-Python cited by ~4,153 papers (OpenAlex, 2026-09-09) [mne.tools](https://mne.tools/stable/documentation/cited.html). No reliable count of EEG labs found.
- **Pays?** Labs pay for GUI analysis suites (BESA, Analyzer, EmotivPRO). No product found sold specifically for automated QC.
- **Price:** $1,200/yr per lab (ASSUMPTION; just above EmotivPRO Standard, well below BESA Basic).
- **Customers @24mo:** 5 / 20 / 60; base assumes ~0.2% of ~10k active EEGLAB/MNE users convert (ASSUMPTION). **ARR:** $6k / $24k / $72k.
- **Hours:** MVP 300h + 6 h/wk maintenance (ASSUMPTION) ≈ 804h over 24mo. **Infra:** ~$150/mo, CPU API plus occasional GPU (ASSUMPTION).
- **ROI:** $24k ÷ 804h ≈ **$30/h**.
- **Risk:** academics default to free MNE/EEGLAB plugins, and labs won't trust "validated" without published benchmarks.

## 2. EEG file-format conversion
- **Free:** EDFbrowser, a free open-source universal viewer/toolbox [teuniz.net](https://www.teuniz.net/edfbrowser/); MNE, EEGLAB/BIOSIG and Neo readers.
- **Paid:** Persyst reads ~70 formats and is bundled by major EEG vendors; price not published [persyst.com](https://www.persyst.com/supported-formats-2/).
- **Reachable base:** overlaps cluster 1; no separate data.
- **Pays?** Only when bundled inside clinical review suites (Persyst). No standalone paid EEG converter found.
- **Price:** $300/yr per user (ASSUMPTION; free tools cap willingness to pay).
- **Customers @24mo:** 10 / 30 / 100, mostly users stuck on MFF, Nihon Kohden or legacy files (ASSUMPTION). **ARR:** $3k / $9k / $30k.
- **Hours:** MVP 250h + 5 h/wk to keep up with vendor quirks (ASSUMPTION) ≈ 685h. **Infra:** ~$30/mo (ASSUMPTION).
- **ROI:** $9k ÷ 685h ≈ **$13/h**.
- **Risk:** MNE and Neo keep adding readers for free, and labs are reluctant to upload clinical data to a web converter.

## 3. LSL connectors & web/cloud relay
- **Free:** LSL supports 150+ device classes and has a JS client [bioRxiv](https://www.biorxiv.org/content/10.1101/2024.02.13.580071v1.full) (figure from a search snippet; full text rate-limited); Timeflux [docs](https://doc.timeflux.io/en/stable/api/timeflux/nodes/lsl/index.html); MEDUSA LSL bridges [docs](https://docs.medusabci.com/platform/v2022/lslbridges.php); Neurosity SDKs are open source [neurosity](https://neurosity.co/developers).
- **Paid:** none found for a hosted LSL relay.
- **Reachable base:** no published LSL, OpenBCI or Muse user counts. OpenBCI has 26 employees [cbinsights](https://www.cbinsights.com/company/openbci).
- **Pays?** No evidence found for a relay.
- **Price:** $29/mo dev, $99/mo team; blended ~$600/yr (ASSUMPTION).
- **Customers @24mo:** 3 / 12 / 40, mostly VR/web developers and neurotech startups (ASSUMPTION). **ARR:** $1.8k / $7.2k / $24k.
- **Hours:** MVP 200h + 5 h/wk (ASSUMPTION) ≈ 655h. **Infra:** $50–200/mo, mostly bandwidth (ASSUMPTION).
- **ROI:** $7.2k ÷ 655h ≈ **$11/h**.
- **Risk:** LSL is local-network by design, so few labs want cloud streaming, and those that do can self-host a Node bridge.

## 4. NWB conversion, validation & cloud access
- **Free:** NWB GUIDE no-code converter [github](https://github.com/NeurodataWithoutBorders/nwb-guide); NeuroConv [github](https://github.com/catalystneuro/neuroconv); Neurosift streams DANDI data in the browser [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13343578/).
- **Paid:** CatalystNeuro has done conversions with 69 labs, funded by NIH, Simons/SCGB and ASAP; no prices published [catalystneuro](https://catalystneuro.com/nwb-conversions/). DataJoint raised a $4.9M seed and has a cloud platform; no prices published [prnewswire](https://www.prnewswire.com/news-releases/datajoint-closes-49m-seed-funding-to-revolutionize-data-management-and-ai-in-academic-and-life-sciences-pharma-302568792.html).
- **Reachable base:** DANDI holds 1,141 dandisets / 965 TB [dandi](https://zenodo.org/records/15312970) (figure from a search snippet). 850+ labs have used Neuropixels since 2017 [wikipedia](https://en.wikipedia.org/wiki/Neuropixels).
- **Pays?** Strongest of clusters 1–5. The NIH Data Management and Sharing Policy lets grants budget for data curation and formatting [UMD guide](https://guides.hshsl.umaryland.edu/nih-dmsp2023/costs); NIH funds NWB dissemination via CatalystNeuro (U24NS120057) [nwb.org](https://nwb.org/grants-and-projects/).
- **Price:** ~$5k per lab conversion engagement plus optional hosted validation (ASSUMPTION; CatalystNeuro rates unpublished).
- **Customers @24mo:** 2 / 6 / 15 contracts/yr, from labs with grant data-sharing obligations (ASSUMPTION). **ARR:** $10k / $30k / $75k.
- **Hours:** MVP 250h on top of NeuroConv + 4 h/wk + ~40h delivery per contract (ASSUMPTION) ≈ 838h. **Infra:** ~$100/mo (ASSUMPTION).
- **ROI:** $30k ÷ 838h ≈ **$36/h**.
- **Risk:** CatalystNeuro and the NWB team give grant-funded help at no cost to labs, and this is consulting, so revenue is capped by your hours.

## 5. Acquisition SDK builds & platform ports
- **Free:** BrainFlow ships one 31 MB py3-none-any wheel for all platforms (v5.23.0, 2026-09-13) [pypi](https://pypi.org/project/brainflow/). liblsl is on conda-forge (osx-arm64 since 2020) and Homebrew [feedstock](https://github.com/conda-forge/liblsl-feedstock), [conda-forge](https://conda-forge.org/blog/posts/2020-10-29-macos-arm64/). pylsl dropped Linux wheels [github](https://github.com/marcus-nystrom/liblsl-Python), leaving a Linux/ARM gap.
- **Pays?** Strongly negative. BrainFlow's Open Collective has raised $23.1k total, almost all from OpenBCI (~$23.5k since 2022) [opencollective](https://opencollective.com/brainflow). The $500/mo sponsor tier (includes tech support) is the only price anchor found.
- **Reachable base:** no data found.
- **Price:** $1,000/yr support + binaries subscription (ASSUMPTION).
- **Customers @24mo:** 0 / 3 / 10 (ASSUMPTION). **ARR:** $0 / $3k / $10k.
- **Hours:** MVP 200h + 8 h/wk to keep the CI matrix green (ASSUMPTION) ≈ 928h. **Infra:** ~$50/mo for CI with macOS/ARM runners (ASSUMPTION).
- **ROI:** $3k ÷ 928h ≈ **$3/h**.
- **Risk:** upstream fixes remove the need, the ecosystem has shown it barely funds this, and it plays least to your ML skills.

## Summary (1–5)
- **Base-case ROI:** NWB conversion ~$36/h > preprocessing QC ~$30/h > format conversion ~$13/h > LSL relay ~$11/h > SDK builds ~$3/h.
- All five fit within ~1,560h of capacity over 24 months (15 h/wk).
- **Data gaps:** no published counts of EEG labs or of OpenBCI/Muse/LSL users. Quote-only vendors publish no prices: Persyst, CatalystNeuro, DataJoint, and current BESA/Analyzer list prices.
- EEG-analysis-software market reports (e.g. [360researchreports](https://www.360researchreports.com/market-reports/eeg-analysis-software-market-201466)) were left out because their 2025 estimates range from $0.7B to $1.8B.
