import pandas as pd
import numpy as np
import nltk

def tokenize(val_text,is_remove_stopwords:bool=False,vec_stopwords_add:list=['e','g','it']):
    nltk_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    if(is_remove_stopwords):
        nltk_stopwords = nltk.corpus.stopwords.words('english')
        nltk_stopwords.extend(vec_stopwords_add)
    else:
        nltk_stopwords = []
    nltk_tokens_sent = nltk.sent_tokenize(val_text)
    df_sentences = pd.DataFrame(nltk_tokens_sent)
    df_sentences.columns = ['sentence']
    df_sentences['id_sent'] = df_sentences.index
    df_words = []
    for i,val_sent in enumerate(nltk_tokens_sent):
        nltk_tokens_word = [j.lower() for j in nltk_tokenizer.tokenize(val_sent) if j not in nltk_stopwords]
        vec_id_word = list(range(0,len(nltk_tokens_word)))
        df_words_tmp = pd.DataFrame([nltk_tokens_word,vec_id_word]).T
        df_words_tmp.columns = ['word','id_sent']
        df_words_tmp['id_sent'] = i
        df_words.append(df_words_tmp)
    df_words = pd.concat(df_words,ignore_index=True,sort=False)
    return(df_sentences,df_words)

def word_freq_cutoffs(df:pd.DataFrame,val_lower:float=0.4,val_upper:float=0.9):
    #C
    val_sig_lower = df['significance'].quantile(q=val_lower)
    if(val_sig_lower==df['significance'].min()):
        val_sig_lower = df['significance'].quantile(q=val_lower)+1e-5
    #D
    val_sig_upper = df['significance'].quantile(q=val_upper)
    if(val_sig_upper==df['significance'].max()):
        val_sig_upper = df['significance'].quantile(q=val_upper)-1e-5
    print(f'''Quantile Significance Lower = {val_sig_lower}\nQuantile Significance Upper = {val_sig_upper}''')
    return(val_sig_lower,val_sig_upper)

def calc_signifcance_words(df:pd.DataFrame,is_use_luhn_tf:bool=True,is_remove_stopwords:bool=False,vec_stopwords_add:list=['e','g','it']):
    df_word_cnts = pd.DataFrame(df['word'].value_counts()).reset_index()
    if(is_remove_stopwords):
        nltk_stopwords = nltk.corpus.stopwords.words('english')
        nltk_stopwords.extend(vec_stopwords_add)
        for i,row in df.iterrows():
            if(row['word'] in nltk_stopwords):
                df_word_cnts.at[i,'count'] = 0
    if(is_use_luhn_tf):
        df_word_cnts['significance'] = df_word_cnts['count']
    else:
        #tf = (number of repetitions of word in a document) / (# of words in a document)
        df_word_cnts['significance'] = df_word_cnts['count']/df.shape[0]
    df_rev = pd.merge(left=df,right=df_word_cnts,on='word',how='left')
    return(df_rev)

def calc_word_score(val_sig:float,val_lower:float,val_upper:float):
    val_score = 0
    if(val_sig>=val_lower and val_sig<=val_upper):
        val_score = val_sig
    return(val_score)

def calc_sentence_score(df:pd.DataFrame,val_num_apart:int=4,is_vector_return:bool=False,func_summary=None):
    vec_scores = []
    vec_n_length = []
    val_idx_max = df.index.max()
    vec_indices = df.index.to_list()
    for i,z in enumerate(vec_indices):
        val_idx_last_sig_word = -1
        df_subset = df.loc[vec_indices[i:i+val_num_apart]].copy()
        if(df_subset.iloc[0]['score']>0):
            val_max_i = df_subset.loc[df_subset['score']>0].index.max()
            val_idx_last_sig_word = vec_indices.index(val_max_i)
            is_srching = True
            num_iter = 0
            while(is_srching):
                num_iter += 1
                df_subset_srch = df.loc[vec_indices[i:val_idx_last_sig_word+val_num_apart]].copy()
                val_max_i_rev = df_subset_srch.loc[df_subset_srch['score']>0].index.max()
                val_idx_last_sig_word_rev = vec_indices.index(val_max_i_rev)
                if(val_idx_last_sig_word==val_idx_last_sig_word_rev):
                    is_srching = False
                    df_range = df.loc[vec_indices[i:val_idx_last_sig_word+1]].copy()
                    #vec_scores.append(df_range['score'].sum())
                    #vec_n_length.append(df_range.loc[df_range['score']>0].shape[0])
                    vec_scores.append(np.sum([df_range['score']>0]))
                    vec_n_length.append(val_idx_last_sig_word+1-i)
                else:
                    val_max_i = val_max_i_rev
                    val_idx_last_sig_word = val_idx_last_sig_word_rev
        else:
            vec_scores.append(0.)
            vec_n_length.append(1.)
    if(is_vector_return):
        rtn_val = [vec_scores,vec_n_length]
    else:
        if(func_summary is None):
            val_idx_max = np.argmax(vec_scores)
            rtn_val = (vec_scores[val_idx_max]**2)/vec_n_length[val_idx_max]
        else:
            rtn_val = func_summary(vec_scores)
    return(rtn_val)

def calc_sentence_score_all(df:pd.DataFrame,val_num_apart:int=4,is_vector_return:bool=False,func_summary=None):
    vec_scores_sent_ids = df['id_sent'].unique()
    vec_scores_sent_ids.sort()
    vec_scores_sent = []
    for i in vec_scores_sent_ids:
        vec_scores_sent.append(calc_sentence_score(df=df.loc[df['id_sent']==i].copy(),
                                                        val_num_apart=val_num_apart,
                                                        is_vector_return=is_vector_return,
                                                        func_summary=func_summary))
    if(is_vector_return):
        rtn_val = vec_scores_sent
    else:
        df_sentences_scored = pd.DataFrame([vec_scores_sent_ids,vec_scores_sent]).T
        df_sentences_scored.columns = ['id_sent','score']
        df_sentences_scored.sort_values(by=['score'],ascending=False,inplace=True)
        rtn_val = df_sentences_scored.copy()
    return(rtn_val)

def summarize(df_sentences:pd.DataFrame,df_scores:pd.DataFrame,val_num_sentences:int=5):
    vec_summary_text = []
    vec_summary_scores = []
    df = pd.merge(left=df_sentences,right=df_scores,on='id_sent',how='left')
    df.sort_values(by=['score'],ascending=False,inplace=True)
    for i,row in df.head(val_num_sentences).iterrows():
        vec_summary_scores.append(row['score'])
        vec_summary_text.append(row['sentence'])
    return(vec_summary_scores[:val_num_sentences],vec_summary_text[:val_num_sentences])

def print_summary(vec_scores:list,vec_sentences:list):
    vec_combined = []
    for i in zip(vec_scores,vec_sentences):
        vec_combined.append('{} '.format(i[1].strip().replace('\n',' '))+"\33[31m"+'[{:.4f}]'.format(i[0])+"\33[0m")
    print(' '.join(vec_combined))
    return(vec_combined)

nltk.download('stopwords',quiet=True)