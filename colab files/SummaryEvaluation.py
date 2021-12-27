from rouge_score import rouge_scorer
import string
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.translate import bleu

#summary = "The quick brown fox jumps over the lazy dog."
summary = "Hinata, a junior high school student, becomes enamoured with volleyball after seeing Karasuno High School compete in Nationals on TV. Hinata, who is diminutive in stature, is inspired by Karasuno's little but talented wing spiker, dubbed 'The Little Giant' by the pundits. Hinata is athletic and has an amazing vertical jump despite her inexperience. He joins his school's volleyball club, only to discover that he is the only one there, requiring him to spend the next two years trying to get other students to practise with him. Some of Hinata's pals agree to join the club in his third and final year of junior high so that he can compete in a tournament. They lose their first official game to the tournament favourites, which included third-year Tobio Kageyama, a prodigy setter nicknamed The King of the Court for both his talent and his charisma."
reference = "Junior high school student, Shōyō Hinata, becomes obsessed with volleyball after catching a glimpse of Karasuno High School playing in Nationals on TV. Of short stature himself, Hinata is inspired by a player the commentators nickname 'The Little Giant', Karasuno's short but talented wing spiker. Though inexperienced, Hinata is athletic and has an impressive vertical jump. He joins his school's volleyball club – only to find he is its sole member, forcing him to spend the next two years trying to convince other students to help him practice. In third and final year of junior high, some of Hinata's friends agree to join the club so he can compete in a tournament. In his first official game ever, they suffer a crushing defeat to the team favored to win the tournament – that included third-year Tobio Kageyama, a prodigy setter nicknamed The King of the Court for both his skill and his brutal play style."
#reference = 'The quick brown dog jumps on the log.'
def calculateRougeScore(summary, reference):
    #Rouge N: N-gram scoring
    #Rouge L: sentence-level: Compute longest common subsequence (LCS) between two pieces of text. Newlines are ignored.
    #RougeLsum: summary-level: Newlines in the text are interpreted as sentence boundaries, and the LCS is computed between each pair of reference and candidate sentences, and something called union-LCS is computed.
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeLsum', 'rougeL'], use_stemmer=True)
    scores = scorer.score(summary,reference)
    return scores


def getTokens(test):
    test = test.translate(str.maketrans('','',string.punctuation))
    test_list = word_tokenize(test)
    return test_list

def calculateBleuScore(summary, reference):
    summary_tokens = getTokens(summary)
    reference_tokens = getTokens(reference)
    reference_tokens = [reference_tokens]
    smoothie = SmoothingFunction().method1
    weights = [(1, 0, 0, 0), (1./2., 1./2.), (1./3., 1./3., 1./3.), (1./4., 1./4., 1./4., 1./4.) ]
    #print("\nsummary tokens", summary_tokens)
    #print("\nreference tokens", reference_tokens)
    bleu_score = sentence_bleu(reference_tokens,summary_tokens,smoothing_function=smoothie, weights = weights) #BLEU-1,2,3,4
    return bleu_score
    
rouge_scores = calculateRougeScore(summary, reference)
bleu_scores = calculateBleuScore(summary, reference)
print("\nRouge Scores: ", rouge_scores)
print("\nBleu Scores: ", bleu_scores)
