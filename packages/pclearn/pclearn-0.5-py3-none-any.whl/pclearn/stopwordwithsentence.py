from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#print(stopwords.words("english"))
eg=input("Enter the sentence: ")
eg=eg.lower()
word=word_tokenize(eg)
stop_words=set(stopwords.words("english"))
#filt=[w for w in word if not w.lower in stop_words]
filt=[]
for w in word:
 if w not in stop_words:
    filt.append(w)
#print(word)
print(filt)
