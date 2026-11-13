#!/usr/bin/env python3
"""Generate five seconds of mono, 16-bit PCM audio using Python only."""
import math
from pathlib import Path
import sys
import wave

if len(sys.argv) != 4:
    raise SystemExit("Usage: python3 sound.py sine|square FREQUENCY OUTPUT.wav")
kind, frequency_text, output = sys.argv[1:]
frequency = float(frequency_text)
if not 20 <= frequency <= 2000:
    raise SystemExit("For this lab please choose a frequency between 20 and 2000 Hz")
if kind not in ("sine", "square"):
    raise SystemExit("Wave type must be sine or square")

rate = 44100       # samples per second
seconds = 5
amplitude = 7000   # modest volume, within 16-bit signed range

samples = bytearray()
for i in range(rate * seconds):
    t = i / rate
    value = math.sin(2 * math.pi * frequency * t)
    if kind == "square":
        # TODO (your task): a square wave should be +1 when
        # the sine is non-negative, and -1 otherwise.
        raise NotImplementedError("Please implement the square wave")
    sample = round(amplitude * value)
    samples.extend(int(sample).to_bytes(2, byteorder="little", signed=True))

Path(output).parent.mkdir(parents=True, exist_ok=True)
with wave.open(output, "wb") as audio:
    audio.setnchannels(1)
    audio.setsampwidth(2)
    audio.setframerate(rate)
    audio.writeframes(samples)
print(f"Wrote {output} ({seconds} seconds, {rate} Hz sample rate)")
