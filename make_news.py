#!/usr/bin/env python3
"""Publish news.txt as a small RSS 2.0 feed in ~/public_html/news.xml."""
from pathlib import Path
import getpass
import os
import xml.etree.ElementTree as ET

user = getpass.getuser()
base = os.environ.get("PUBLISH_BASE_URL", "http://the.hell.am").rstrip("/")
home = f"{base}/~{user}/"
public = Path(os.environ.get("PUBLISH_DIR", str(Path.home() / "public_html")))
public.mkdir(parents=True, exist_ok=True)
public.chmod(0o755)

entries = []
for number, raw in enumerate(Path("news.txt").read_text(encoding="utf-8").splitlines(), 1):
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    if "|" not in line:
        raise SystemExit(f"news.txt line {number}: expected TITLE|TEXT")
    title, body = (part.strip() for part in line.split("|", 1))
    if not title or not body:
        raise SystemExit(f"news.txt line {number}: title and text must not be empty")
    entries.append((title, body))

if not entries:
    raise SystemExit("Please write at least one entry in news.txt")

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = f"{user}'s little RSS feed"
ET.SubElement(channel, "link").text = home
ET.SubElement(channel, "description").text = "News published from a Unix shell"
ET.SubElement(channel, "language").text = "en"

# Numbering is stable as long as older lines aren't moved or removed.
for index in range(len(entries), 0, -1):
    title, body = entries[index - 1]
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = body
    ET.SubElement(item, "guid", isPermaLink="false").text = f"{home}news-item-{index}"

ET.indent(rss, space="  ")
output = public / "news.xml"
ET.ElementTree(rss).write(output, encoding="utf-8", xml_declaration=True)
output.chmod(0o644)
print(f"Published {len(entries)} article(s) at {home}news.xml")
