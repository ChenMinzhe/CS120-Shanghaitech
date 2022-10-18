# Project 1: Acoustic Link

This part do on parts on physical layer of the Athernet.

## Files

[CS120_Project1.pdf](CS120_Project1.pdf)
The requirements.

[rec_and_play.py](rec_and_play.py)
Infrastructure for playing and recording audio.
Run directly to finish part 1.

[fixed_signal.py](fixed_signal.py)
Part 2 of the project.

[casegen.py](casegen.py)
The case generator for part 3 and later.
Usage: `python casegen.py [length] > output.file`

[psk_modulator.py](psk_modulator.py)
The PSK modem.

[sender.py](sender.py) and [receiver.py](receiver.py)
Sender sends the bits in `case.txt`.
Receiver receives the bits and store them in `output.txt`

[diff.py](diff.py)
diff between `case.txt` and `output.txt`.
