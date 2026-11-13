# A little piece of the Internet: RSS and your own podcast

## Introduction

You all have already used HTTP, and we have also talked a little about XML. In this lab we shall put these two things together. We'll publish something on the Internet, and then read it on a phone. No social network, blogging service, or podcast hosting account is needed.

First, you will make a tiny news feed. Afterwards, you will make a tiny *podcast*, but instead of speaking into a microphone, you will make your computer produce the sound. The whole thing will run from your Unix account on `the.hell.am`.

We are going to do this in **two parts**. Please don't jump straight to the podcast. The first part explains the second one.

You need an SSH connection to `the.hell.am`, Python 3, and a phone with an RSS reader and a podcast client. If you don't have a suitable phone, use an RSS/podcast client on a computer, or work with another student for the phone portion. **Each of you must still publish your own feeds.**

## Part I. A blog that has no blogging software

### 1. A little public_html directory

The blog has nothing to do with that thing that starts with ins and ends with ram.
The blog is something that has a feed. RSS or Atom XML feed.

To read it you don't need an account, you don't need to register.

You just need a program that would fetch the xml and show you the news.

So lets start.

Connect to the server using your student account:

```sh
ssh YOUR_USERNAME@the.hell.am
```

Apache is already running on the server. It understands a useful Unix convention: a file placed in `~/public_html` can be accessed through a URL containing `~username`.

Tilda stands for your home path.

Make that directory:

```sh
mkdir -p ~/public_html
chmod 755 ~/public_html
printf 'Hello from my little website!\n' > ~/public_html/index.html
```

Now open this address in a browser (put your actual username in place of `YOUR_USERNAME`):

Of course we talk about your username that is on the server, not github.

```text
http://the.hell.am/~YOUR_USERNAME/
```

See? You now have a website. And you did not have to register an account with any website-creation service.

You can also try:

```sh
curl -i http://the.hell.am/~YOUR_USERNAME/
```

What does `200 OK` mean? What is the `Content-Type` header telling you?

*Note:* Everything in `public_html` is public. Don't put passwords, private documents, or other people's files there.

### 2. What is RSS?

RSS is a way to publish a list of updates in a form that another application can read. It is commonly used by blogs, news sites, and podcasts. An RSS 2.0 feed is an XML document.

Here is a very small one:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>My little news</title>
    <link>http://example.org/</link>
    <description>News from my computer</description>
    <item>
      <title>Hello!</title>
      <description>My first message.</description>
      <guid isPermaLink="false">first-message</guid>
    </item>
  </channel>
</rss>
```

Notice the `<channel>` element, and the `<item>` inside it. A channel describes the feed. Items describe its entries. You may have as many items as you like.

You could write this XML by hand. But who wants to repeat all these tags every time a new article is published? We can let a program do it for us.

### 3. Let's publish our first RSS entry

In the repository for this lab you will find `news.txt` and `make_news.py`. Look at both files.

The text file has one post per line, in this format:

```text
Title of post|Text of the post
```

Change the example entry. Write something of your own, and include your Unix username or another recognizable identifier in the title. Please keep each post on one line; `|` separates the title from the text.

Then run, from your lab repository directory:

```sh
python3 make_news.py
```

The program reads `news.txt` and writes a real RSS feed to `~/public_html/news.xml`.

Try looking at it:

```sh
cat ~/public_html/news.xml
curl -i http://the.hell.am/~YOUR_USERNAME/news.xml
```

Is the XML structure familiar? Find the title and text you wrote. Also find the `<guid>` element. Think of it as an identity for an entry: a feed reader uses it to tell one entry from another.

### 4. Subscribe from your phone

Install an RSS reader, or use one you already have:

- **Android:** [Feeder](https://play.google.com/store/apps/details?id=com.nononsenseapps.feeder.play) (also on [F-Droid](https://f-droid.org/packages/com.nononsenseapps.feeder/)).
- **iPhone/iPad:** [NetNewsWire](https://apps.apple.com/us/app/netnewswire-rss-reader/id1480640210).

There are many, these are those I knew.

Because unlike the thing that starts with ins and ends with ram,
rss is a standard. Not a company.
Just like HTTP, XMPP or IRC is a standard, not a messenger. And not an "app".

In the RSS reader app, choose the option to **add a feed by URL** or something
like that. Enter:

```text
http://the.hell.am/~YOUR_USERNAME/news.xml
```

Your post should appear. If it does not, first try the same URL in your phone's browser and check your XML. Feel free to help your neighbors; it is easy to make a tiny XML mistake.

Now edit `news.txt` again. **Keep the first line and add a second post on a new line.** Run `python3 make_news.py` once more. Refresh the feed in your reader.

Did the second post appear? Good! You have just published news without having to notify each subscriber yourself. Your reader fetches the XML and notices the new item. (Some apps cache feeds, so a refresh may not be immediate.)

**Before continuing:** Open `answers.md` and write down your RSS URL, the app you used, and your answers to questions 1–3. Take a screenshot showing **both posts** in your RSS reader. Save it as `screenshots/rss.png` or `screenshots/rss.jpg` in your repository.

## Part II. A podcast without a microphone

### 5. Where does a podcast fit in?

Most podcast feeds are also RSS feeds. The interesting difference is that each episode has an **enclosure**: a link to an audio file, together with its size in bytes and its media type.

For example, an episode may include:

```xml
<enclosure url="https://example.org/episode1.mp3"
           length="12345" type="audio/mpeg" />
```

Here `12345` is only an example. In a real podcast feed, it must be the **actual size of the MP3 file in bytes**.

The podcast client downloads the RSS to discover the episodes and then downloads or streams the MP3 when you want to listen.

What shall we use as our audio? You could record your own voice, but today we'll produce sound mathematically.

### 6. Make sounds

Look at `sound.py`. It writes a five-second WAV file using Python's standard `wave` module. We won't need to install any Python libraries.

Try:

```sh
python3 sound.py sine 440 first.wav
```

This makes a **440 Hz sine wave**. If you have listened to a tuning tone before, the result might be familiar.

WAV stores uncompressed sound samples. To make a smaller, compressed audio file, use an encoder. On the server we shall use `lame` for MP3:

```sh
lame --quiet -V 5 first.wav first.mp3
ls -lh first.wav first.mp3
```

The WAV should be larger. Why? You can also use `oggenc` to make an Ogg Vorbis file if it is installed:

```sh
oggenc -q 4 -o first.ogg first.wav
```

Ogg Vorbis is a nice format, but we shall publish **MP3** for the podcast because it works in the podcast applications we want to use, including Apple Podcasts.

You don't have to understand all of digital audio today, but look at these variables in `sound.py`: `rate`, `seconds`, and `amplitude`. What do they do? Please listen at a comfortable volume.

### 7. Publish your first episode

Now open `episodes.txt`. Each line describes an episode:

```text
Title of episode|wave type|frequency
```

The starter file contains:

```text
My first sine wave|sine|440
```

Change the title to something of your own. Then run:

```sh
python3 make_podcast.py
```

The script invokes your `sound.py`, encodes the WAV as MP3, and writes a podcast feed to `~/public_html/podcast.xml`. It also copies the supplied `cover.png` image. The generated files are in your public web directory.

Take a look:

```sh
ls -lh ~/public_html/
cat ~/public_html/podcast.xml
curl -I http://the.hell.am/~YOUR_USERNAME/episode1.mp3
```

Find the enclosure in the XML. Does the length match the real file size? Why doesn't a regular news post need an MP3 enclosure?

**Important:** Existing MP3 files are deliberately not regenerated when you run `make_podcast.py` again. This keeps old episodes unchanged. If you are experimenting *before publishing* and really need to regenerate one, you can delete its WAV and MP3 in `public_html` and rerun the script. Once you have published an episode, don't replace its audio under the same URL.

### 8. Subscribe to your podcast

Use a real podcast app:

- **Android:** [AntennaPod](https://antennapod.org/) — choose **Add Podcast**, then the option to add it by an RSS address. Get it [here on play](https://play.google.com/store/apps/details?id=de.danoeh.antennapod&hl=en-US)
- **iPhone:** **Apple Podcasts** — open **Library**, open the **More (`...`)** menu and choose **Follow a Show by URL**.

In different IOS devices this page where you can add a link is in a bit different place. It's hard to find. But possible.

Enter your podcast's address:

```text
http://the.hell.am/~YOUR_USERNAME/podcast.xml
```

The podcast should appear. Play the first episode. Yes, that strange noise is a podcast episode that you published yourself!

P. S. I have installed a TLS certificate, so https also works.
You can try https links in your podcast or rss client, if http doesnt work.


### 9. A second episode, and a different wave

Open `sound.py` again. You will notice a `TODO` in the code for a *square wave*.

A sine wave changes smoothly. A square wave alternates abruptly between two values. In our program you already have the sine value `value`. To create a square wave, replace that `TODO` so that `value` is `1` when it is non-negative and `-1` otherwise. You do not need to change the rest of the file.

Try it:

```sh
python3 sound.py square 220 second.wav
```

Now add a new line to `episodes.txt` **without removing the first episode**:

```text
My second episode|square|220
```

Run:

```sh
python3 make_podcast.py
```

What changed in `podcast.xml`? Look for two different `<item>` elements, two GUIDs, and two enclosure URLs. Now refresh your podcast app and play the second episode.

See? Your Unix account is now publishing a little podcast with two episodes. It required no podcasting platform: just XML files, MP3 files and a web server.

**Before finishing:** Complete answers 4–7 in `answers.md`. Take another screenshot showing **both episodes** in your podcast application and save it in `screenshots/` as `podcast.png` or `podcast.jpg`.

## What to submit

Your public feeds are part of the assignment, because the instructor will access them over HTTP. **Do not delete `~/public_html/news.xml`, `~/public_html/podcast.xml` or the MP3 files after you submit.**

In your GitHub Classroom repository, submit:

- `news.txt` — two (or more) original posts.
- `episodes.txt` — two episodes using different wave types.
- Your modified `sound.py` with a working square-wave implementation.
- `answers.md`, with **both public URLs** and written answers to all seven questions.
- Two screenshots: `screenshots/rss.png` and `screenshots/podcast.png` (JPG is fine too).
- A copy of each final generated feed (`news.xml` and `podcast.xml`). Copy them from `public_html` before committing:

```sh
cp ~/public_html/news.xml .
cp ~/public_html/podcast.xml .
```

Commit and push your changes. You can use `git add` and `git push` as in the previous labs. If you took screenshots on your phone, transfer them into the repository using any method convenient to you (USB, file sharing, or GitHub's upload feature).

I will check that the two public XML files can be fetched, that they contain two items each, and that the podcast's MP3 files really exist and can be downloaded. The screenshots show that **you actually subscribed** using the two applications. The server cannot reliably prove that from an XML file alone.

## Some things to think about

- Why does an RSS reader need `<guid>`? What would happen if a script gave every entry the same GUID?
- Why do podcast enclosures need a **URL** rather than a filename on your disk?
- What happens if somebody else knows the address of your feed, but you never told them about a new post?
- What happens if `podcast.xml` exists, but the MP3 URL gives `404 Not Found`?
- How would you implement an RSS feed reader using `curl` and an XML parser?

If you have time, subscribe to a neighbor's feed as well. There is no special permission required for reading a public RSS feed — knowing the URL is enough.

## References

- [RSS 2.0 specification](https://www.rssboard.org/rss-specification)
- [NetNewsWire: adding an RSS feed](https://netnewswire.com/help/ios/6.1/en/adding-feeds.html)
- [AntennaPod: subscribing to a podcast](https://antennapod.org/documentation/getting-started/subscribe)
- [Apple Podcasts: follow a show by URL](https://podcasters.apple.com/support/5108-how-apple-podcasts-distributes-your-shows-to-listeners)
- [Apple Podcasts: podcast RSS technical requirements](https://podcasters.apple.com/support/823-podcast-requirements)
