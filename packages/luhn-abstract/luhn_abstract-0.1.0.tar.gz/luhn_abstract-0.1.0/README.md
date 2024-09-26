# Luhn Auto-Abstract
Implementation of Luhn paper from 1958.

Citation:
Luhn, Hans Peter. "The Automatic Creation of Literature Abstracts." __IBM Journal of Research and Development 2.2__ (1958): 159-165.


**luhn_abstract** is a Python module for automatically generating an abstract from a document using unsupervised techniques.  The Luhn paper was published in 1958, and the general concept of the algorithm is outlined in the diagram below.

![algorithm](./images/image_001.png)

# Dependencies
~~~~~~~~~~~~
luhn_abstract requires:

- Python (>=3.6)
- NumPy
- NLTK
- Pandas
~~~~~~~~~~~~

# Example

```python
val_text = scrape_page_wikipedia(val_url='https://en.wikipedia.org/wiki/natural_language_processing')
df_sents,df_words = la.luhn_abstract.tokenize(val_text=val_text,is_remove_stopwords=False)
df_words_scored = la.luhn_abstract.calc_signifcance_words(df=df_words,is_use_luhn_tf=True,is_remove_stopwords=False)
val_sig_lower,val_sig_upper = la.luhn_abstract.word_freq_cutoffs(df=df_words_scored,val_lower=val_quant_lower,val_upper=val_quant_upper)
df_words_scored['score'] = [la.luhn_abstract.calc_word_score(val_sig=x,val_lower=val_sig_lower,val_upper=val_sig_upper) for x in df_words_scored['significance']]
df_sentences_scored = la.luhn_abstract.calc_sentence_score_all(df=df_words_scored,val_num_apart=val_n,func_summary=None)
vec_scores,vec_sents = la.luhn_abstract.summarize(df_sentences=df_sents,df_scores=df_sentences_scored,val_num_sentences=val_k)
print('-'*50)
str_rtn = la.luhn_abstract.print_summary(vec_scores=vec_scores,vec_sentences=vec_sents)
```

```
Quantile Significance Lower = 1.00001
Quantile Significance Upper = 31.0
--------------------------------------------------
[57] Likewise, ideas of cognitive NLP are inherent to neural models multimodal NLP
(although rarely made explicit)[58] and developments in artificial intelligence,
specifically tools and technologies using large language model approaches[59] and
new directions in artificial general intelligence based on the free energy principle[60]
by British neuroscientist and theoretician at University College London Karl J.
Friston. [15.6250] [9] In 2010, Tomáš Mikolov (then a PhD student at Brno University
of Technology) with co-authors applied a simple recurrent neural network with a single
hidden layer to language modelling,[10] and in the following years he went on to
develop Word2vec. [14.2258] It is primarily concerned with providing computers with
the ability to process data encoded in natural language and is thus closely related
to information retrieval, knowledge representation and computational linguistics, a
subfield of linguistics. [12.9706] Major tasks in natural language processing are
speech recognition, text classification, natural-language understanding, and
natural-language generation. [12.5000] Machine learning approaches, which include
both statistical and neural networks, on the other hand, have many advantages over
the symbolic approach:  Although rule-based systems for manipulating symbols were
still in use in 2020, they have become mostly obsolete with the advance of LLMs in
2023. [12.2500]
```