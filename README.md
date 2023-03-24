# P300 Stimulus

A Stimulus for Brain-Computer Interface Spelling

The P300 speller is a brain-computer interface that allows users to type characters by selecting them from a matrix of flashing characters. This interface utilizes EEG signals to detect which character the user is focusing on and uses machine learning algorithms to translate these signals into text.

This code generates the matrix of flashing characters and randomizes the order in which rows and columns flash, in line with academic research.

To use this code with a Mentalab Explore device to record EEG data, run the following command:

python game_with_eeg -n [device_name] -f [output_file_name]

Alternatively, if you do not have access to the device or simply want to modify the pygame code, run:

python game_with_eeg -m true

With this code, users can experiment with the P300 speller and potentially improve the design of this brain-computer interface.
