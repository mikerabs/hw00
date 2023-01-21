# Author: Mike Rabayda
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize
import cmudict

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
        d = cmudict.dict()
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
        d = cmudict.dict()

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

        for k in range(len(b_phonemes)):#for all pronunciations of b
            for i in range(len(b_phonemes[k])):#go through b's phonemes at pronunciation k
                if i < len(b_icons[k]) :#we're skipping the indexes of the initial consonants of b
                    continue
                #i value must be at first vowel after initial consonant cluster for b, so loop through a's phonemes till we find a match
                if i > len(b_icons[k]):
                    break
                

                for l in range(len(a_phonemes)):#check all pronunciations of a
                    for j in range(len(a_phonemes[l])):#go through phonemes of pronunciation l of word a
                        if j < len(a_icons[l]):#we're skipping the indexes of the initial consonants of a
                            continue 
                        if j > len(a_icons[l]):
                            break
                        #j value must be at or after first vowel after initial consonant cluster for a
                        if a_phonemes[l][j] == b_phonemes[k][i] : # if any of the phonemes after initial consonant cluster match, set the matching index to j and break the for loop
                            matchflag = True
                            matchindex = j
                            break
                    #check here for rest of word using a loop, if everything lines up for b[i] and a[matchindex] for both then return True
                    if matchflag == True:
                        #check here if the number of phonemes matches up, must have identical lengths -> wine and rind, but reset matchindex and matchflag and continue 
                        if((len(a_phonemes[l])-matchindex) != (len(b_phonemes[k])-i)):
                            matchflag = False
                            matchindex = 0
                            continue
                        for j in range(len(a_phonemes[l])-matchindex):#both should have the same length if they do rhyme, so iterate
                            if(b_phonemes[k][i+j] != a_phonemes[l][matchindex+j]):
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

        return False

if __name__ == "__main__":
    ex = "eleven"
    l = LimerickDetector
    print(l.num_syllables(l, ex))

    ex2 = "seven"
    print(l.rhymes(l,ex,ex2))

    ex3 = "asdf"
    d = cmudict.dict()
    print(len(d[ex3.lower()]))

    #buffer = ""
    #inline = " "
    #while inline != "":
        #buffer += "%s\n" % inline
        #inline = input()

    #ld = LimerickDetector()
    #print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))