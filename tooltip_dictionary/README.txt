PLEASE NOTE MANY OF THESE DEFINITIONS MAY BE WRONG OR INCOMPLETE - THIS WAS NEVER INTENDED TO BE A FINAL VERSION.

Each line in the dictionary file has one word definition, with the formatting (spliced on the first comma):

WORD,DEFINITION

"WORD" is a regular expression designed to match instances of that word, and "DEFINITION" is the tooltip definition for that word.

Special notes:

1) "DEFINITION" may contain additional commas. For example:

car,a device for locomotion, which typically does not fly

2) In "DEFINITION," apostrophes are escaped with a backslash (for examples, "the car\'s engine," rather than "the car's engine"). There may be some instances where this isn't true (this didn't cause the tooltip plugin to crash, simply to incorrectly render that one definition).

3) Note that due to the way to the tooltip plugin works, the regular expressions used in "WORD" are somewhat nonstandard. Luckily, going from my regular expressions to normal regular expressions is in general easy - they will work in a general regular expression interpreter 99% of the time (after first casting all strings to lowercase). However, note that apostrophes appearing in "WORD" are viewed as wildcards in my code, where they represent any character that ISN'T a letter or space. This is a little confusing, so for an example, here's a real definition:

b'?h$,(Baruch Hashem) Blessed is the Name [of God]

Note that the $ requires that the word end with the h. The following are examples of strings the tooltip plugin recognizes as matching this word:

b"h
b'h
b.h
b7h
b-h
bh <--- due to the ? in the regex

Although this seems like strange behavior, the plugin code (which is run every time someone with the plugin opens any page in the /r/Judaism subreddit) runs faster the way it is written, and it's in general uncommon for someone to type out something like "b7h" on purpose.

Note that the following are NOT picked up by the plugin as matching the word:

bah
b h
bzh

Using this rule in a normal regex interpreter is as simple as replacing each instance of ' in each "WORD" with [^a-z ]. So, for example:

b[^a-z ]?h$,(Baruch Hashem) Blessed is the Name [of God]

Alternatively, each instance of ' in "WORD" could be replaced with something more appropriate (this word will probably only ever be written as b'h or b"h in practice) but this requires manual work.

Finally, note that "$" in this dictionary is also slightly non-standard and simply means that the match is not followed by any other letters. In the above example:

b"h.

should be recognized, but

b"hz

should not. This may need to be slightly modified for other purposes as well (stripping out every $ and starting over may be easiest, but a simple fix like the one presented above for ' could work as well).
