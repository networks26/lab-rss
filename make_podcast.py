#!/usr/bin/env python3
"""Publish episodes.txt as a podcast, generating WAV/MP3 as needed."""
from datetime import datetime, timezone
from email.utils import format_datetime
import getpass
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ET.register_namespace("itunes", ITUNES_NS)

def itunes(parent, name, **attributes):
    return ET.SubElement(parent, f"{{{ITUNES_NS}}}{name}", attributes)

user = getpass.getuser()
base = os.environ.get("PUBLISH_BASE_URL", "http://the.hell.am").rstrip("/")
home = f"{base}/~{user}/"
public = Path(os.environ.get("PUBLISH_DIR", str(Path.home() / "public_html")))
public.mkdir(parents=True, exist_ok=True)
public.chmod(0o755)

if shutil.which("lame") is None:
    raise SystemExit("lame is not installed. Ask the instructor to install it on the server.")

entries = []
for number, raw in enumerate(Path("episodes.txt").read_text(encoding="utf-8").splitlines(), 1):
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    fields = [part.strip() for part in line.split("|")]
    if len(fields) != 3 or not all(fields):
        raise SystemExit(f"episodes.txt line {number}: expected TITLE|sine-or-square|FREQUENCY")
    title, kind, frequency = fields
    if kind not in ("sine", "square"):
        raise SystemExit(f"episodes.txt line {number}: wave must be sine or square")
    try:
        if not 20 <= float(frequency) <= 2000:
            raise ValueError()
    except ValueError:
        raise SystemExit(f"episodes.txt line {number}: frequency must be 20..2000")
    entries.append((title, kind, frequency))

if not entries:
    raise SystemExit("Please write at least one episode in episodes.txt")

cover = Path(__file__).with_name("cover.png")
if not cover.exists():
    raise SystemExit("Missing cover.png from the starter files")
shutil.copyfile(cover, public / "cover.png")
(public / "cover.png").chmod(0o644)

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = f"{user}'s sound experiments"
ET.SubElement(channel, "link").text = home
ET.SubElement(channel, "description").text = "Five-second waveforms generated with Python on a Unix server"
ET.SubElement(channel, "language").text = "en"
itunes(channel, "author").text = user
itunes(channel, "summary").text = "A little podcast for a network programming lab."
itunes(channel, "explicit").text = "false"
itunes(channel, "category", text="Technology")
itunes(channel, "image", href=home + "cover.png")
image = ET.SubElement(channel, "image")
ET.SubElement(image, "url").text = home + "cover.png"
ET.SubElement(image, "title").text = f"{user}'s sound experiments"
ET.SubElement(image, "link").text = home

for index in range(len(entries), 0, -1):
    title, kind, frequency = entries[index - 1]
    wav_file = public / f"episode{index}.wav"
    mp3_file = public / f"episode{index}.mp3"
    # Preserve existing published media: URLs, GUIDs and dates should stay stable.
    if not mp3_file.exists():
        subprocess.run([sys.executable, str(Path(__file__).with_name("sound.py")),
                        kind, frequency, str(wav_file)], check=True)
        subprocess.run(["lame", "--quiet", "-V", "5", str(wav_file), str(mp3_file)], check=True)
    mp3_file.chmod(0o644)
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = f"A {frequency} Hz {kind} wave, lasting five seconds."
    ET.SubElement(item, "guid", isPermaLink="false").text = f"{home}episode-{index}"
    date = datetime.fromtimestamp(mp3_file.stat().st_mtime, tz=timezone.utc)
    ET.SubElement(item, "pubDate").text = format_datetime(date)
    ET.SubElement(item, "enclosure", url=home + mp3_file.name,
                  length=str(mp3_file.stat().st_size), type="audio/mpeg")
    itunes(item, "duration").text = "00:00:05"
    itunes(item, "explicit").text = "false"

ET.indent(rss, space="  ")
output = public / "podcast.xml"
ET.ElementTree(rss).write(output, encoding="utf-8", xml_declaration=True)
output.chmod(0o644)
print(f"Published {len(entries)} episode(s) at {home}podcast.xml")
