#!/bin/bash
# Run each top-15 cluster through ../validation-tool phase1 report → validation/<n>_<slug>.json
cd "$(dirname "$0")"
PY=/home/ubuntu/miniconda3/bin/python
TOOL=../validation-tool/phase1/validation_tool.py
SUBS=r/BCI,r/neuroscience,r/OpenBCI,r/neurotechnology
while IFS='|' read -r n slug query trends; do
  out=validation/${n}_${slug}.json
  [ -s "$out" ] && continue
  echo "== $n $slug"
  $PY $TOOL report --query "$query" --trends-query "$trends" --reddit-subreddits $SUBS < /dev/null > $out.tmp && mv $out.tmp $out || echo "failed $n"
done <<'LIST'
01|eeg_preprocessing|automated EEG preprocessing artifact removal software|EEG artifact removal
02|eeg_format_conversion|EEG file format converter|EEG file converter
03|lsl_relay|lab streaming layer cloud relay websocket|lab streaming layer
04|nwb_conversion|NWB neurodata without borders conversion service|neurodata without borders
05|sdk_builds|brainflow liblsl prebuilt binaries support|brainflow
06|eeglab_container|EEGLAB MATLAB environment container|EEGLAB
07|timestamp_sync|EEG multi-device timestamp synchronization|EEG synchronization
08|spike_sorting|cloud spike sorting service neuropixels|spike sorting
09|headset_comparison|EEG headset comparison|EEG headset
10|stream_integrity|EEG signal quality monitoring data loss|EEG signal quality
11|eeg_ai_agent|AI assistant for EEG MEG analysis MNE|EEG analysis
12|bci_course|brain computer interface online course|brain computer interface course
13|eeg_dataset_catalog|public EEG dataset catalog|EEG dataset
14|bci_benchmark|BCI EEG decoding benchmark leaderboard|EEG decoding
15|ble_eeg_connectivity|Muse OpenBCI bluetooth connection troubleshooting|Muse headband
LIST
echo done
