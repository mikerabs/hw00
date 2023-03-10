# Author: Mike Rabayda
# Date: 1/22/2023

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        d = self._pronunciations
        phonemes = d[word.lower()]#gives us the pronunciation in a list
        #example turns into [['IH0', 'G', 'Z', 'AE1', 'M', 'P', 'AH0', 'L']]

        if(len(phonemes)==0):#word is not in cmu, give length 1
            return 1

        numSyllables = [len(list(y for y in x if y[-1].isdigit())) for x in phonemes]
        #since the digits at the end of the phonemes indicate stresses in a word, we can check to see how many of those phonemes there are and return it as number of syllables
        return numSyllables[0]

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        d = self._pronunciations

        a_phonemes = d[a.lower()]#all phonemes of word a
        b_phonemes = d[b.lower()]#all phonemes of word b

        a_icons = [[]]#initial consonants of a
        b_icons = [[]]#initial consonants of b

        a_start_vowel = True
        b_start_vowel = True

        vowels = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY','OW','OY','UH','UW',
        'AA0','AE0','AH0','AO0','AW0','AY0','EH0','ER0','EY0','IH0','IY0','OW0','OY0','UH0','UW0',
        'AA1','AE1','AH1','AO1','AW1','AY1','EH1','ER1','EY1','IH1','IY1','OW1','OY1','UH1','UW1',
        'AA2','AE2','AH2','AO2','AW2','AY2','EH2','ER2','EY2','IH2','IY2','OW2','OY2','UH2','UW2']#isn't taking into account the cases in which the vowel phonemes are stressed

        # check if the first phoneme is a vowel or not, not sure if I need this
        if a_phonemes[0] not in vowels:
            a_start_vowel = False
        if b_phonemes[0] not in vowels:
            b_start_vowel = False


         # find the initial consonant clusters for each word
        for k in range(len(a_phonemes)):#for all combinations of phonemes in a phoneme combos
            a_icons.append([])
            for i in range(len(a_phonemes[k])):
                if a_phonemes[k][i] not in vowels:
                    a_icons[k].append(a_phonemes[k][i])
                else:
                    break #break once first vowel found, initial consonant cluster is over

        for k in range(len(b_phonemes)):#for all combinations of phonemes in b phoneme combos
            b_icons.append([])
            for i in range(len(b_phonemes[k])):
                if b_phonemes[k][i] not in vowels:
                    b_icons[k].append(b_phonemes[k][i])
                else:
                    break #break once first vowel found, initial consonant cluster is over
        

        matchindex = 0#find a matching pair of phonemes after icc, initialized to 0 for now
        matchflag = False


        if len(a_phonemes[0])<=len(b_phonemes[0]):
            for k in range(len(b_phonemes)):#for all pronunciations of b
                for i in range(len(b_phonemes[k])):#go through b's phonemes at pronunciation k

                    #skip the indexes of the initial consonants of b
                    if i < len(b_icons[k]) :
                        continue

                    #i value must be at first vowel after initial consonant cluster for b, so loop through a's phonemes till we find a match

            
                    #since a is less than b in number of phonemes, let's go throuhg the pronunciations of a and see if they line up with the kth pronunciation of b
                    for l in range(len(a_phonemes)):#check all pronunciations of a
                        for j in range(len(a_phonemes[l])):#go through phonemes of pronunciation l of word a


                            if j < len(a_icons[l]):#we're skipping the indexes of the initial consonants of a
                                continue 
                            
                            #j value must be at or after first vowel after initial consonant cluster for a
                            if a_phonemes[l][j] == b_phonemes[k][i] : # if any of the phonemes after initial consonant cluster match, set the matching index to j and break the for loop
                                matchflag = True
                                matchindex = j
                                break

                        #if matching phonemes were found, matchflag will be true
                        if matchflag == True:
                            #check here if the number of phonemes matches up, must have identical lengths -> wine and rind, but reset matchindex and matchflag and continue 
                            if((len(a_phonemes[l])-matchindex) != (len(b_phonemes[k])-i)):
                                matchflag = False
                                matchindex = 0
                                continue
                            #in the case of bagel and sail, this should stop words from rhyming with last phonemes
                            if((a_phonemes[l][matchindex] not in vowels and b_phonemes[k][i] not in vowels) and(matchindex == len(a_phonemes[l])-1 or i == len(b_phonemes[k])-1)):
                                matchflag = False
                                matchindex = 0
                                continue
                            for j in range(len(a_phonemes[l])-matchindex):#both should have the same length if they do rhyme, so iterate
                                if(b_phonemes[k][i+j] != a_phonemes[l][matchindex+j]):
                                    return False
                            return True
            return False    

        else:#this is the case in which a is larger than b, so find b in a instead of the other way around
            for k in range(len(a_phonemes)):#for all pronunciations of a
                for i in range(len(a_phonemes[k])):#go through a's phonemes at pronunciation k

                    #skip the indexes of the initial consonants of a
                    if i < len(a_icons[k]) :
                        continue

                    #i value must be at first vowel after initial consonant cluster for a, so loop through a's phonemes till we find a match

                    
            
                    #since b is less than a in number of phonemes, let's go throuhg the pronunciations of b and see if they line up with the kth pronunciation of a
                    for l in range(len(b_phonemes)):#check all pronunciations of b
                        for j in range(len(b_phonemes[l])):#go through phonemes of pronunciation l of word b


                            if j < len(b_icons[l]):#we're skipping the indexes of the initial consonants of b
                                continue 
                            
                            #j value must be at or after first vowel after initial consonant cluster for b
                            if b_phonemes[l][j] == a_phonemes[k][i] : # if any of the phonemes after initial consonant cluster match, set the matching index to j and break the for loop
                                matchflag = True
                                matchindex = j
                                break

                        #if matching phonemes were found, matchflag will be true
                        if matchflag == True:
                            #check here if the number of phonemes matches up, must have identical lengths -> wine and rind, but reset matchindex and matchflag and continue 
                            if((len(b_phonemes[l])-matchindex) != (len(a_phonemes[k])-i)):
                                matchflag = False
                                matchindex = 0
                                continue
                            if((b_phonemes[l][matchindex] not in vowels and a_phonemes[k][i] not in vowels) and(matchindex == len(b_phonemes[l])-1 or i == len(a_phonemes[k])-1)):
                                matchflag = False
                                matchindex = 0
                                continue
                            for j in range(len(b_phonemes[l])-matchindex):#both should have the same length if they do rhyme, so iterate
                                if(a_phonemes[k][i+j] != b_phonemes[l][matchindex+j]):
                                    return False
                            return True
            return False 

        


        
 

   
    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        strings = text.split('\n')
        if(len(strings) != 5):#limericks must have 5 lines to be a limerick
            return False

        #tokenize the words from sentences
        for i in range(len(strings)):
            strings[i] = word_tokenize(strings[i])
        
        #clean out the punctuations
        punctuation = [',', '.',':', '"']
        for i in range(len(strings)):
            for token in strings[i]:
                if token in punctuation:
                    strings[i].remove(token)
                    
        #check lines


        #check A1 and A2 rhyme
        if(self.rhymes(strings[0][len(strings[0])-1], strings[1][len(strings[1])-1]) == False):
            return False
        #check that A2 and B1 DO NOT rhyme
        if(self.rhymes(strings[1][len(strings[1])-1], strings[2][len(strings[2])-1]) == True):
            return False
        #check if B1 and B2 rhyme
        if(self.rhymes(strings[2][len(strings[2])-1], strings[3][len(strings[3])-1]) == False):
            return False
        #check if A2 and A3 rhyme
        if(self.rhymes(strings[1][len(strings[1])-1], strings[4][len(strings[4])-1]) == False):
            return False
        return True

    

    
if __name__ == "__main__":
    ex = "weigh"
    l = LimerickDetector
    print(l.num_syllables(l, ex))

    ex2 = "fey"
    print(l.rhymes(l,ex,ex2))

    ex3 = "asdf"
    d = cmudict.dict()
    print(len(d[ex3.lower()]))

    a = """a woman whose friends called a prude
on a lark when bathing all nude
saw a man come along
and unless we are wrong
you expected this line to be lewd"""

    b = """while it's true all i've done is delay
in defense of myself i must say
today's payoff is great
while the workers all wait"""

    c = """this thing is supposed to rhyme
but I simply don't got the time
who cares if i miss,
nobody will read this
i'll end this here poem potato"""

    d = """There was a young man named Wyatt
whose voice was exceedingly quiet
And then one day
it faded away"""

    e = """An exceedingly fat friend of mine,
When asked at what hour he'd dine,
Replied, "At eleven,
At three, five, and seven,
And eight and a quarter past nine"""

    f = """A limerick fan from Australia
regarded his work as a failure:
his verses were fine
until the fourth line"""

    g = """There was a young lady one fall
Who wore a newspaper dress to a ball.
The dress caught fire
And burned her entire
Front page, sporting section and all."""


    print(l.is_limerick(l,a))
    print(l.is_limerick(l,b))
    print(l.is_limerick(l,c))
    print(l.is_limerick(l,d))
    print(l.is_limerick(l,e))#index out of range
    print(l.is_limerick(l,f))
    print(l.is_limerick(l,g))

    #print(l.dotheyrhyme(l,ex,ex2))
    #buffer = ""
    #inline = " "
    #while inline != "":
        #buffer += "%s\n" % inline
        #inline = input()

    #ld = LimerickDetector()
    #print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))