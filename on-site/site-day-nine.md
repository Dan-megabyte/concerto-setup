
# Day 9: The Reckoning + finding the hidden problem

I've finally figured out why it isn't working. Concerto apparently
has an arbitrary mininum of characters below which it just decides
not to display the Rich text. [See the code](https://github.com/concerto/concerto/blob/0ae90c8fb559382aca324bd0ef0634544adb8944/app/models/rich_text.rb#L42)
? Well this arbitrary heuristic cost me about two days worth of work
to find, since I ended up retrofitting the weather service to serve
RSS instead of JSON (a stupid decision, in hindsight).

Now that I succeeded in finding the issue, I'm not entirely sure how
to fix it. I could just add 100x spaces and call it a day, mostly
because the heuristic is maybe there for a reason? It prevented the
RSS feed from spitting out incorrect information, so thats a win.

For today, I'll update the new weather script to include some extraneous
spaces, and check to see if that works the next day.
