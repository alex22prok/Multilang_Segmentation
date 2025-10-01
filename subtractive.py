import data
import re



def build_lexicon(utts):
    """The core lexicon-building algorithm. Returns a dictionary of words with their scores"""
    lexicon = {}
    # Utterance loop
    for utt in utts:
        # Subtraction loop
        remainder = utt
        while remainder:
            # Get all the possible subtractions
            matchedwords = set()
            syllindices = [i for i, syllseg in enumerate(remainder) if syllseg == "."]
            for i in syllindices:
                candidate = remainder[:i].strip()
                if candidate in lexicon:
                    matchedwords.add(candidate)
            # Do subtraction and lexicon updating
            if matchedwords: # If at least one subtraction is found
                # Get the best one
                beststartword = get_bestmatch(matchedwords, lexicon)
                # Do the subtraction
                remainder = subtract(beststartword, remainder)
                # Update the subtracted word in the lexicon
                update_lexicon(lexicon, beststartword)
            else: # No subtraction was found
                # Update the lexicon with the remainer and move to the next utterance
                update_lexicon(lexicon, remainder)
                break
    return lexicon


def get_utt_segpoints(lexicon, utt):
    """Actually segments an utterance given the lexicon. 
    Returns the segmented utterance and a set of segmentation points"""
    remainder = utt
    wordseq = []
    # Loop to subtract utterance-initial words
    while remainder:
        syllindices = [i for i, syllseg in enumerate(remainder) if syllseg == "."]
        found = False
        for i in syllindices:
            candidate = remainder[:i].strip()
            # Subtract the shortest possible word
            if candidate in lexicon:
                # Do the subtraction
                remainder = subtract(candidate, remainder)
                # Add
                wordseq.append(candidate)
                found = True
                break
        # Give up when nothing left can be subtracted
        if not found:
            wordseq.append(remainder)
            break
    # Reconstitute the utterance with word boundaries
    joined = " | ".join(wordseq)
    return joined, data.get_boundary_indices(joined)


###
### YOUR FUNCTIONS
###

def get_bestmatch(matchedwords, lexicon):
    """Given a set of words that matched the start of the utterance,
    returns the one with the highest score
    input:
        matchedwords (set): a set of words from the lexicon
        lexicon (dict str:int): a dictionary of words and scores
    return:
        (str): return the word from matchedwords with the best score in the lexicon.
               If two words are tied for best score, return the one with the fewest syllables"""
    # Instructor solved this in 16 lines including the return
    bestscore = -1 #changed to -1 from 0
    bestword = ""
    ### YOUR CODE HERE
    for word in matchedwords:
        score = lexicon[word]
        syllcount = word.count(".") + 1
        if score > bestscore or (score == bestscore and syllcount < bestword.count(".") + 1):
            bestscore = score
            bestword = word
    return bestword


def update_lexicon(lexicon, word):
    """Updates the lexicon with a word. Add it with score=1 if it's new, increment score if not new
    input:
        lexicon (dict str:int): dictionary of words and scores
        word (str): word to update lexicon with
    return:
       (none): lexicon is updated by reference"""
    # Instructor solved this in 4 lines including the return
    ### YOUR CODE HERE
    if word in lexicon: #if word already in lexicon 
        lexicon[word] += 1 #reward: increment its score
    else: lexicon[word] = 1 #else, add it with score of 1
    return


def subtract(beststartword, utt):
    """Removes word from beginning of utterance. Returns the remainder. Remember to remove any extra periods or whitespace from the ends
    input:
        beststartword (str): word to remove from start of utt
        utt (str): utterance to remove beginning of
    return:
        (str): utterance with beststartword removed from the beginning. Remove any extra period or space from the ends"""
    # Instructor solved this in 3 lines including the return
    remainder = ""
    ### YOUR CODE HERE
    #slice utt from len of beststartword to end, 
        #then strip leading ". " and trailing whitespace
    remainder = utt[len(beststartword):].lstrip(". ").strip()
    return remainder


def get_segpoints(lexicon, utts):
    """Segments each utterance using the lexicon. Returns a segmented copy of each utterance and a set of segmentation points for each utterance
    input:
        lexicon (dict str:int): dictionary of words and scores
        utts (list of str): list of utterances
    return:
        (list of str): list of segmented utterances (. replaced with | on word boundaries)
        (list of set): list of sets of segmentation point indices"""
    # Instructor solved this in 7 lines including the return
    allsegpoints = []  #list of sets of segmentation points for each utterance
    alljoinedutts = [] #list of segmented utterances as strings
    # For each utterance, 
    for utt in utts:
        joined, segpoints = get_utt_segpoints(lexicon, utt) #segment it using the lexicon
        alljoinedutts.append(joined) #add segmented utterance to list
        allsegpoints.append(segpoints) #add segmentation points to list
    return alljoinedutts, allsegpoints


def main():
    train_utts = data.read_file("Brown_train_unseg.txt")
    lexicon = build_lexicon(train_utts[:])

    test_utts = data.read_file("Brown_test_unseg.txt")
    goldsegs_train = data.get_goldsegs("Brown_train_gold.txt")
    goldsegs_test = data.get_goldsegs("Brown_test_gold.txt")

    for utts, goldsegs, title in ((train_utts, goldsegs_train, "Training"), (test_utts, goldsegs_test, "Testing")):
        joineds, segs = get_segpoints(lexicon, utts)
        print(segs[0:10])
        print(goldsegs[0:10])

        stats = data.evaluate(goldsegs, segs)
        print(title)
        print("P: %s\tR: %s\t\tF1: %s\n" % tuple([round(stat*100, 2) for stat in stats]))


if __name__ == "__main__":
    main()


