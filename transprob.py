import data
import nltk

START = "START"
STOP = "STOP"

def pad(utt):
    """Applies bigram padding with NLTK"""
    return list(nltk.pad_sequence(utt,2,
                                  pad_left=True,
                                  pad_right=True,
                                  left_pad_symbol=START,
                                  right_pad_symbol=STOP))


def get_bigrams(tokenized):
    """Returns padded bigrams for a tokenized utterance"""
    padded = pad(tokenized)
    return list(nltk.bigrams(padded))


def flatten(utts):
    """Flattens a list of lists of bigrams into a list of bigrams"""
    return [bigram for utt in utts for bigram in utt]


def get_bigramprobdict(utterances):
    """Creates a bigram probability dictionary {context:{completion:prob}} using NLTK"""
    bigrams = flatten([get_bigrams(data.tokenize_syllables(utt)) for utt in utterances])
    freqdist = nltk.ConditionalFreqDist(bigrams)
    probdist = nltk.ConditionalProbDist(freqdist, nltk.MLEProbDist)
    probdict = {condition:{sample:probdist[condition].prob(sample)
                           for sample in probdist[condition].samples()}
                for condition in probdist.conditions()}
    return probdict
    

###
### YOUR FUNCTIONS
###

def get_tp_sequence(tokenized, probdict):
    """Creates a sequence of transitional probabilties
    input:
        tokenized (list): tokenized utterance
        probdict (dict:dict:float): dictionary of bigram probabilities
    returns:
        (seq): sequence of transitional probabilities corresponding to 
               each utterance-internal bigram in the input"""
    # Instructor solved this in 6 lines including the return
    bigrams = get_bigrams(tokenized)
    tpseq = []
    ### YOUR CODE HERE
    #for each bigram in the utterance except START and STOP bigrams
    for prev, curr in bigrams[1:-1]:
        tp = probdict.get(prev, {}).get(curr, 0) #get its transprob from probdict, default 0
        tpseq.append(tp) #add to list
    return tpseq 


def get_local_minima(tpseq):
    """Finds local minima in a sequence of probabilities. These are segmentation points.
    input: 
        tpseq (seq): sequence of probabilities
    return:
        (set): set of segmentation points (indices of local minima in the input
    """
    # Instructor solved this in 10 lines including the return
    ### YOUR CODE HERE
    minima = set() #set of indices of local minima
    #for each in tpseq except the first and last,
    for i in range(1, len(tpseq) - 1):
        #if value at i is < values before and after it,
        if tpseq[i] < tpseq[i - 1] and tpseq[i] < tpseq[i + 1]:
            minima.add(i) #add to minima set
    #check beginning
    if len(tpseq) >= 2 and tpseq[0] < tpseq[1]:
        minima.add(0) #add to minima set at index 0
    #check end
    if len(tpseq) >= 2 and tpseq[-1] < tpseq[-2]:
        minima.add(len(tpseq) - 1) #add to minima set at last index
    return minima


def get_segpoints(tokenizeds, probdict):
    """Gets the segmentation points for each tokenized utterance
    input:
        tokenizeds (list of lists): A list of utterances. Each is a list of syllables
        probdict (dict:dict:float): A dictionary of bigram probabilities
    return:
        (list of sets): a list of segmentation point sets, one for each input utterance
    """
    # Instructor solved this in 3 lines
    allsegpoints = []
    ### YOUR CODE HERE
    #for each utterance in tokenizeds, get its tpseq and then its local minima
    allsegpoints = [get_local_minima(get_tp_sequence(utt, probdict)) for utt in tokenizeds]
    return allsegpoints


def main():
    train_utts = data.read_file("Brown_train_unseg.txt")
    probdict = get_bigramprobdict(train_utts)

    test_utts = data.read_file("Brown_test_unseg.txt")
    goldsegs_train = data.get_goldsegs("Brown_train_gold.txt")
    goldsegs_test = data.get_goldsegs("Brown_test_gold.txt")

    for utts, goldsegs, title in ((train_utts, goldsegs_train, "Training"), (test_utts, goldsegs_test, "Testing")):
        sylls = [data.tokenize_syllables(utt) for utt in utts]
        segs = get_segpoints(sylls, probdict)

        # Use data.apply_boundaries() to help visualize
        # the segmentations for debugging
        # and answering analysis questions

        stats = data.evaluate(goldsegs, segs)
        print(title)
        print("P: %s\tR: %s\t\tF1: %s\n" % tuple([round(stat*100, 2) for stat in stats]))


if __name__ == "__main__":
    main()


