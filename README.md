# HW00
The goal of this program was to write code to determine whether a poem is a limerick or not. To do this, we used be using the CMU pronunciation dictionary. NLTK is a common python library used for text processing.). We also used the NLTK library to tokenize text.

A limerick is defined as a poem with the form AABBA, where the A lines rhyme with each other, the B lines rhyme with each other (and not the A lines). (English professors may disagree with this definition, but that’s what we’re using here to keep it simple. There are also constraints on how many syllables can be in a line.)

Below is a list of questions and answers we used to frame the work of our assignment:

What does it mean for two words to rhyme? 
They should share the same sounds in their pronunciation except for their initial consonant sound(s). (This is a very strict definition of rhyming. This makes the assignment easier.) If one word is longer than the other, then the sounds of shorter word (except for its initial consonant cluster) should be a suffix of the sounds of the longer. To further clarify, when we say “one word is longer than the other”, we are using number of phonemes as the metric, not number of syllables or number of characters.


What if a word isn’t in the pronouncing dictionary? 
Assume it doesn’t rhyme with anything and only has one syllable.

What if a word has multiple pronunciations? 
If a word like “fire” has multiple pronunciations, then you should say that it rhymes with another word if any of the pronunciations rhymes.

What if a word starts with a vowel?
Then it has no initial consonant, and then the entire word should be a suffix of the other word.

What about end rhymes?
End rhymes are indeed a rhyme, but they make for less interesting limericks. So “conspire” and “fire” do rhyme.

What about stress? 
The stresses of rhymes should be consistent.

What if a word has no vowels? 
Then it doesn’t rhyme with anything.