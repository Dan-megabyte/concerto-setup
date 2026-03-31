
# Weather script working + next steps

After switching the weather script back to the JSON endpoint of the API,
it still didn't work. But after reading the logs a bit, I figured out I
forgot to wrap the JSON response on the server in an array, so it just
decided to ignore it. It would be so much easier if the remote feed gave
an error message to the studio if there were some errors parsing the feed.

Now I need to setup the automatic updating of feeds, specifically either a
system timer that sends a feed refresh event (maybe with a system account?)
to the necessary feeds that need to be reloaded, or something else if that
doesn't work.

However, my project lead told me that one of the concerto clients was down,
derailing my plan for the rest of the day.
