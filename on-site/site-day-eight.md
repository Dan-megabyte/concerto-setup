
# Day eight: The wrap-up, and last minute bugs

Since day seven, I looked around the concerto administration looking
for things to improve the site and remembered part of my reason for
joining, namely the addition of an RPI Eventhub feed source for the
sidebar. While the sidebar was currently empty (the weather feed was
in the administration portal but not in the frontend), I could try
to add an RSS feed and (if it works) figure out the difference between
the Eventhub feed and the weather static request.

So I simply added that and checked the difference:

- The eventhub RSS feed generates multiple `html` 'RichText' Contents
  that contain both `<h1>` and `<p>` tags.
- Meanwhile, the Weather feed contains a single `html` 'RichText' content
  that contains two `<h1>` tags, a `<div>` tag, and a `<p>` tag.

This led me to believe that the problem had something to do with `<div>`
interpretation (basically it wasn't displaying any item that had a div tag).

However, when I tried to change the text to a simpler `<h1>Today in Troy</h1><p>Currently 48.0 F</p>`
it still didn't work.

I'll try looking at the backend logs on the server next time and search
for issues on content fetching. I'll also try to replicate the error locally.
