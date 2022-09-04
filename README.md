# P300_pygame

Pygame portion for a P300 speller.

The code is designed to be adjustible so that the the timings, letters and loops can be changed.

The game will run through each row and column `n_cycles_in_epoch` times, after which it will either wait `break_time` seconds before starting a new epoch or wait until the user presses space, depending of if `auto_epoch` is true.

## Command

Run with recording daata from Mentalab Explore device

`python game_with_eeg -n [device_name] -f [output_file_name]`

If you don't have access to the device or just want to make change to pygame code:

`python game_with_eeg -m true`
