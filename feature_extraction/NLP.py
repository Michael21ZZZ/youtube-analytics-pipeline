import string
SUMMARY_WORD_LIST = ["finally", "in a word", "in brief", "briefly", "in conclusion", "in the end", "in the final analysis", 
'on the whole', "thus", "to conclude", "to summarize", "in sum", "to sum up", "in summary", "lastly"]
TRANSITION_WORD_LIST = ['Accordingly', ' as a result', ' and so', ' because', ' consequently', ' for that reason', ' hence', ' on\naccount of', ' since', ' therefore', ' thus', ' after', ' afterwards', ' always', ' at length', ' during', ' earlier', 'following', ' immediately', ' in the meantime', ' later', ' never', ' next', ' once', ' simultaneously', 
                        'so far', ' sometimes', ' soon', ' subsequently', ' then', ' this time', ' until now', ' when', ' whenever', 'while', ' additionally', ' again', ' also', ' and', ' or', ' not', ' besides', ' even more', ' finally', ' first', ' firstly', 'further', ' furthermore', ' in addition', ' in the first place', ' in the second place', ' last', ' lastly', 
                        'moreover', ' next', ' second', ' secondly', ' after all', ' although', ' and yet', ' at the same time', ' but', 'despite', ' however', ' in contrast', ' nevertheless', ' notwithstanding', ' on the contrary', ' on the other hand', ' otherwise', ' thought', ' yet', ' as an illustration', ' e.g.', ' for example', ' for instance', 
                        'specifically', ' to demonstrate', ' to illustrate', ' briefly', ' critically', ' foundationally', ' more importantly', ' of less importance', ' primarily', ' above', ' centrally', ' opposite to', ' adjacent to', 'below', ' peripherally', ' below', ' nearby', ' beyond', ' in similar fashion', ' in the same way', 
                        'likewise', ' in like manner', ' i.e.', ' in other word', ' that is', ' to clarify', ' to explain', ' in fact', ' of course', ' undoubtedly', ' without doubt', ' surely', ' indeed', ' for this purpose', ' so that', ' to this end', ' in order that', ' to that end']


# function calculating the similarity of keyword with video description
def calc_cosine_similarity(word1, word2):
    # Cosine similarity calculation
    # tokenization
    X_list = word_tokenize(word1) 
    Y_list = word_tokenize(word2)
      
    # sw contains the list of stopwords
    sw = stopwords.words('english') 
    l1 =[];l2 =[]
      
    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw} 
    Y_set = {w for w in Y_list if not w in sw}
      
    # form a set containing keywords of both strings 
    rvector = X_set.union(Y_set) 
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0
      
    # cosine formula 
    for i in range(len(rvector)):
        c+= l1[i]*l2[i]
    if float((sum(l1)*sum(l2))**0.5) == 0:
        return "NA"
    else:
        return c / float((sum(l1)*sum(l2))**0.5)

def medical_entity_count(text):
    
    return 0

def count_paragraph_stats(paragraph):
    # Count the number of letters
    letters = sum(c.isalpha() for c in paragraph)

    # Count the number of words
    words = len(paragraph.split())

    # Count the number of unique words
    unique_words = len(set(paragraph.translate(str.maketrans('', '', string.punctuation)).lower().split()))

    # Count the number of sentences
    sentences = paragraph.count('.') + paragraph.count('!') + paragraph.count('?')

    # Count the number of "active" words (defined as words not in a list of stop words)
    stop_words = set(['a', 'an', 'and', 'the', 'is', 'of', 'to', 'that', 'this', 'in', 'for', 'with', 'on', 'at', 'from'])
    active_words = sum(1 for word in paragraph.translate(str.maketrans('', '', string.punctuation)).lower().split() if word not in stop_words)

    # Count the number of "summary" words (defined as the 10 most frequent non-stop words)
    all_words = paragraph.translate(str.maketrans('', '', string.punctuation)).lower().split()
    summary_words = len([word for word in all_words if word.strip() in SUMMARY_WORD_LIST])
    transition_words = len([word for word in all_words if word.strip() in TRANSITION_WORD_LIST])
    # word_counts = {word: all_words.count(word) for word in set(all_words) if word not in stop_words}
    # summary_words = len([word for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]])
    # summary_words = 10
    
    # calculate ARI socre
    letters_per_word = letters / words
    words_per_sent = words / sentences
    ari_score = 4.71 * letters_per_word + 0.5 * words_per_sent - 21.43

    return words, unique_words, sentences, active_words, summary_words, transition_words, ari_score