# -*- coding: utf-8 -*-
"""Project1 SDM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nb7G6HdsH_joViT2-Svh-vhko8QAGUJ8
"""

from essential_generators import DocumentGenerator

import pandas as pd
import numpy as np
import random
from google.colab import drive
drive.mount('/content/gdrive')

"""## STEP 1: CREATING TABLE OF ARTICLES (PAPERS)"""

articles=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_article.csv', delimiter=';')
header=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_article_header.csv',  delimiter=';')
articles.columns=header.columns

articles=articles[['article:ID', 'author:string[]','title:string', 'year:int', 'journal:string', 'key:string', 'mdate:date', 'url:string', 'volume:string']].dropna()

articles.columns=map(lambda x: x.split(':')[0], articles.columns.tolist())

articles.rename(columns={'article':'article_ID'}, inplace=True)

articles.drop(columns=['year', 'key', 'url'], inplace=True)

articles.reset_index(drop=True, inplace=True)
articles=articles.loc[:300, :]
articles.head()

articles.loc[13,'journal']='ANSI X3H2'
articles.loc[17,'journal']='ANSI X3H2'

authors_repeated=articles.loc[[0,1,2,3,4,56,7,8,47,48,59,12,14,15,16,17],['author', 'journal', 'volume']].reset_index(drop=True)

authors_repeated.reset_index(drop=True, inplace=True)

for i in range(201,300,1):
  j=np.random.randint(0,10,1)
  articles.loc[i,'journal']=authors_repeated.loc[j,'journal'].values[0]
  articles.loc[i,'author']=authors_repeated.loc[j,'author'].values[0]
  articles.loc[i,'volume']=authors_repeated.loc[j,'volume'].values[0]

authors_repeated

articles.loc[200:,'journal'].unique()

authors=[]
coauthors=[]
for i, row in articles.iterrows():
  au=row.author.split('|')
  authors.append(au[0])
  if len(au)>1:
    coauthors.append(au[1])
  else:
    coauthors.append('Null')



articles.author=authors
articles['coauthor']=coauthors

articles.head()

"""We add Abstract and Topic columns to each article"""

from essential_generators import DocumentGenerator
main = DocumentGenerator()
abstracts = [main.gen_sentence() for x in range(len(articles))]
articles['abstract'] = abstracts

articles.to_csv('./gdrive/MyDrive/Project1_sdm/articles.csv', index=False)

"""## STEP 2: Creatinc tables of topics and relationships"""

import pandas as pd

articles_final=pd.read_csv('./gdrive/MyDrive/Project1_sdm/articles.csv')
data = [[0, 'Data Managment'], [1, 'Indexing'], [2, 'Data Modelling'], [3, 'Big Data'], [4, 'Data Processing'], [5, 'Data Storage'], [6, 'Data Queryng'], [7,'Machine Learning'], [8, 'Algorithmics'], [9, 'Multivariate Analysis'], [10, 'Process Mining'], [11, 'Statistical Inference'], [12, 'Unstructred Data'], [13, 'NLP'], [14, ['Time Series']]]
topics = pd.DataFrame(data, columns = ['Topics_ID', 'Topics'])
topics

articles_id = list(articles_final['article_ID'])
articles_id_list = []
for _ in range(100):
    articles_id_list.append(random.choice(articles_id))
articles_id.extend(articles_id_list)

topics_id = list(topics['Topics_ID'])
N = len(articles_id) - len(topics)
keywords_id_list = []
for _ in range(N):
    keywords_id_list.append(random.choice(topics_id))
topics_id.extend(keywords_id_list)

random.shuffle(articles_id)
random.shuffle(topics_id)

relations_topics = pd.DataFrame(list(zip(topics_id,articles_id)), columns=['Topic_ID','Article_ID'])
relations_topics = relations_topics.drop_duplicates()

relations_topics

relations_topics[relations_topics['Article_ID'] == 28797]
#coauthors_final[coauthors_final['coauthor_ID'] == 8997431]

topics.to_csv('./gdrive/MyDrive/Project1_sdm/topics.csv', index=False)
relations_topics.to_csv('./gdrive/MyDrive/Project1_sdm/relations_topics_articles.csv', index=False)

"""## STEP 3: CREATING TABLE OF AUTHORS AND CO-AUTHORS"""

articles_final=pd.read_csv('./gdrive/MyDrive/Project1_sdm/articles.csv')

articles_final

names = list(set(articles_final['author']))

names_coauthors=list(set(articles_final['coauthor']))

names_coauthors.remove('Null')

authors=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_author.csv', delimiter=';')
co_authors=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_author.csv', delimiter=';')

authors.head()

authors.set_axis(authors['author:string'], inplace=True)
authors=authors.loc[names]
co_authors.set_axis(co_authors['author:string'], inplace=True)
co_authors=co_authors.loc[names_coauthors]

authors.head()

co_authors.reset_index(drop=True, inplace=True)
co_authors.rename(columns={':ID':'coauthor_ID', 'author:string':'coauthor'}, inplace=True)
co_authors.drop_duplicates(subset=['coauthor_ID'],inplace=True)

co_authors

authors.reset_index(drop=True, inplace=True)
authors.rename(columns={':ID':'author_ID', 'author:string':'author'}, inplace=True)
authors.head()
authors.drop_duplicates(subset='author_ID', inplace=True)

articles['journal'].unique()

authors.to_csv('./gdrive/MyDrive/Project1_sdm/authors.csv', index=False)
co_authors.to_csv('./gdrive/MyDrive/Project1_sdm/co_authors.csv', index=False)

"""## STEP 4: CREATING AUTHORED_BY AND CO_AUTHORED_BY"""

authors = pd.read_csv('./gdrive/MyDrive/Project1_sdm/authors.csv')
co_authors=pd.read_csv('./gdrive/MyDrive/Project1_sdm/co_authors.csv')

co_authors

authored_by=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_author_authored_by.csv', delimiter=';')

start=authored_by[':START_ID']
authored_by.set_index(start, inplace=True)
authored_by = authored_by.loc[articles_final['article_ID']]
authored_by.reset_index(drop=True, inplace=True)

end=authored_by[':END_ID']
authored_by.set_index(end, inplace=True)
authored_by = authored_by.loc[authors['author_ID']]
authored_by.reset_index(drop=True, inplace=True)

authored_by.rename(columns={':END_ID':"AUTHOR_ID", ":START_ID":"ARTICLES_ID"}, inplace=True)
print(len(authored_by))

authored_by_final=pd.DataFrame(columns=authored_by.columns)
co_authored_by=pd.DataFrame(columns=authored_by.columns)
for i, row in authored_by.iterrows():
  articles_fila=articles.loc[articles['article_ID']==row['ARTICLES_ID']]
  auto=authors[authors['author']==articles_fila['author'].reset_index(drop=True)[0]]['author'].reset_index(drop=True)[0]
  if articles_fila['coauthor'].reset_index(drop=True)[0]!='Null':
      co_auto=co_authors[co_authors['coauthor']==articles_fila['coauthor'].reset_index(drop=True)[0]]['coauthor'].reset_index(drop=True)[0]
  else : co_auto='Null'
  if articles_fila['author'].reset_index(drop=True)[0]==auto and articles_fila['coauthor'].reset_index(drop=True)[0]==co_auto and co_auto!='Null':
    authored_by_final= authored_by_final.append({'ARTICLES_ID':row['ARTICLES_ID'], 'AUTHOR_ID':authors[authors['author']==auto].reset_index(drop=True).loc[0,'author_ID']}, ignore_index=True)
    co_authored_by = co_authored_by.append({'ARTICLES_ID':row['ARTICLES_ID'],'AUTHOR_ID': co_authors[co_authors['coauthor']==co_auto].reset_index(drop=True).loc[0,'coauthor_ID']}, ignore_index=True)
  else:
    authored_by_final= authored_by_final.append({'ARTICLES_ID':row['ARTICLES_ID'], 'AUTHOR_ID':authors[authors['author']==auto].reset_index(drop=True).loc[0,'author_ID']}, ignore_index=True)

co_authored_by[co_authored_by['ARTICLES_ID'] == 28624]

co_authors[co_authors['coauthor_ID'] == 8997084]

co_authored_by.rename(columns={'AUTHOR_ID':'COAUTHOR_ID'}, inplace=True)
authored_by=authored_by_final

co_authored_by

authored_by.drop_duplicates(subset=['ARTICLES_ID'],inplace=True)

co_authored_by.drop_duplicates(subset=['ARTICLES_ID'],inplace=True)

authored_by[authored_by['AUTHOR_ID']==8980227]

authored_by.to_csv('/content/gdrive/MyDrive/Project1_sdm/authored_by.csv', index=False)
co_authored_by.to_csv('/content/gdrive/MyDrive/Project1_sdm/co_authored_by.csv', index=False)

"""## STEP 5: CREATING CITED_BY"""

articles_final = pd.read_csv('./gdrive/MyDrive/Project1_sdm/articles.csv')

len(articles_final)

list_ID = list(articles_final['article_ID'])
len(list_ID)

list_2 = []
for i in range(len(list_ID)):
  list_2.append(random.sample(list_ID, 1)[0])

list_2

cited_by = pd.DataFrame(zip(list_ID, list_2), columns=['article_ID1', 'article_ID2'])
cited_by.drop_duplicates()

idx_rm = []

for i in range(len(list_2)):
  a1 = list_ID[i]
  b1 = list_2[i]
  for j in range(len(list_2)):
    if (b1 == list_ID[j]) and (a1 == list_2[j]):
      idx_rm.append(j)
      print(b1, a1)

cited_by = cited_by.drop(labels=idx_rm, axis=0)

cited_by

cited_by.to_csv('/content/gdrive/MyDrive/Project1_sdm/cited_by.csv', index=False)

"""## STEP 5: CREATING JOURNALS"""

journals=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_journal.csv', delimiter=';')
journals_published_in=pd.read_csv('./gdrive/MyDrive/Project1_sdm/journal_volum1_I_journal_published_in.csv', delimiter=';')

articles_final = pd.read_csv('./gdrive/MyDrive/Project1_sdm/articles.csv')

journals.head()

journals_published_in

articles_final.head()

articles_with_journals = articles_final[:round(len(articles_final)/2)+1]

articles_with_journals

journals_list = list(articles_with_journals['journal'].unique())
journals_final_v1 = journals[journals['journal:string'].isin(journals_list)]
journals_final_v1.reset_index(drop=True, inplace=True)
journals_final_v1.rename(columns={':ID':"Journals_ID", "journal:string":"Journals"}, inplace=True)
journals_final_v1

articles_extract_journals = articles_with_journals[['article_ID','journal', 'mdate', 'volume']][:round(len(articles_final)/2)+1]
articles_extract_journals

for dif,journal in zip([4,3,10],list(articles_extract_journals['journal'].unique())):
  l=articles_extract_journals[articles_extract_journals['journal']==journal].shape[0]
  articles_extract_journals.loc[articles_extract_journals['journal']==journal,'volume']=np.random.randint(1,dif,l)

list(articles_extract_journals['journal'].unique())

journals_final_v1 = pd.merge(left=journals_final_v1, right=articles_extract_journals, how='right', left_on='Journals', right_on='journal')
journals_final_v1['mdate'] = journals_final_v1['mdate'].apply(lambda x: x.split('-')[0])
journals_final_v1.rename(columns={'mdate':"year"}, inplace=True)

journals_final_v1

journals_final_v1['Volume_ID']=journals_final_v1["Journals_ID"].map(str) +'_'+ journals_final_v1["volume"].map(str)
journals_final_v1[journals_final_v1['journal']=='Sci. Eng. Ethics']['year'].unique()

# creating volumes table
volumes = journals_final_v1[['Volume_ID', 'volume']]
volumes = volumes.drop_duplicates().reset_index(drop=True)

# relations paper_volume
articles_volume_relation = journals_final_v1[['Journals_ID', 'Volume_ID']]

# creating journal table
journal = journals_final_v1[['Journals_ID', 'Journals']]
journal = journal.drop_duplicates().reset_index(drop=True)

# relations volume_journal
volum_journal_relation = journals_final_v1[['Volume_ID', 'Journals_ID']]

volumes.to_csv('./gdrive/MyDrive/Project1_sdm/volumes.csv', index=False)
articles_volume_relation.to_csv('./gdrive/MyDrive/Project1_sdm/articles_volume_relation.csv', index=False)
journal.to_csv('./gdrive/MyDrive/Project1_sdm/journals.csv', index=False)
volum_journal_relation.to_csv('./gdrive/MyDrive/Project1_sdm/volum_journal_relation.csv', index=False)

journals_final_v1

journals_final_v1[['year', 'Journals_ID']].value_counts()

journals = list(journals_final_v1['Journals_ID'])
years = list(journals_final_v1['year'])

list_y = []
list_j = []

counter = 0

for i in range(len(years)):
  if ((years[i] == '2020') and (journals[i] == 12016295) and (counter < 30)):
    list_y.append('2019')
    counter += 1
  elif ((years[i] == '2020') and (journals[i] == 12016295) and (counter >30 and counter < 60)):
    list_y.append('2021')
    counter += 1
  else:
    list_y.append(years[i])

len(list_y)

journals_final_v1['year'] = list_y

journals_final_v1[['year', 'Journals_ID']].value_counts()

journals_final_v1['year'].unique()

# relations year and volume
year_volum_relation = journals_final_v1[['year', 'Volume_ID']]
year_volum_relation = year_volum_relation.drop_duplicates()
year_volum_relation = year_volum_relation.reset_index(drop=True)

# year
years = journals_final_v1[['year']]
years = years.drop_duplicates()
years = years.reset_index(drop=True)
years

year_volum_relation.to_csv('./gdrive/MyDrive/Project1_sdm/year_volum_relation.csv', index=False)
years.to_csv('./gdrive/MyDrive/Project1_sdm/years.csv', index=False)

"""## STEP 6: CREATING CONFERENCES"""

articles_final = pd.read_csv('./gdrive/MyDrive/Project1_sdm/articles.csv')
articles_with_conferences = articles_final[round(len(articles_final)/2)+1:]

frank=articles_with_conferences[articles_with_conferences['author']=='Frank Manola'].loc[:,'article_ID'].tolist()

conference_list = ['Jungle Meet', 'Barrel Brigade', 'Furious Forum'] * 4

num_editions = list(range(4))
list_editions = []
for i in num_editions:
  value = [i] * 3
  for j in value:
    list_editions.append(j)

year_list = ([2015, 2016, 2017] * 4)
city_list = ['Tokyo', 'Jakarta', 'Delhi', 'Mumbai', 'Manila', 'Shanghai', 'Sao Paulo', 'Seoul', 'Mexico City', 'Guangzhou', 'Beijing', 'Barcelona', 'Madrid', 'Andorra La Vella']

import random

cities = []
for i in range(4):
  sample = random.sample(city_list, 4)
  for j in range(len(sample)):
    cities.append(sample[j])

conference_ID_list = list(range(len(city_list)))

conferences_final = pd.DataFrame(zip(conference_ID_list, conference_list, list_editions, year_list, cities), columns=['conference_ID', 'conference', 'edition', 'year', 'city'])

conferences_final

article_id = list(articles_with_conferences['article_ID'])
conference_id = list(conferences_final['conference_ID'])

conf_id = []
for i in range(len(article_id)):
  id =str(random.sample(conference_id, 1))
  conf_id.append(int(id[1]))

conferences_relationhip = pd.DataFrame(zip(conf_id, article_id), columns=['conference_ID', 'article_ID'])
conferences_relationhip.groupby(by='conference_ID').size().sum()

frank_conf=conferences_relationhip.set_index(conferences_relationhip['article_ID'])

frank_conf.loc[frank].groupby(by='conference_ID').size()

l1 = list(conferences_relationhip['conference_ID'].unique())
l2 = list(conferences_final['conference_ID'].unique())

set(l1)

set(l2)

idx=conferences_final['conference_ID']
conferences_final.set_index(idx, inplace=True)
conferences_final

ll1 = list(set(l1))
ll2 = list(set(l2))
ll2
for i in ll2:
  if i not in ll1:
    conferences_final = conferences_final.drop([i])

conferences_final.reset_index(drop=True, inplace=True)
conferences_final

conferences_final.to_csv('/content/gdrive/MyDrive/Project1_sdm/conferences.csv', index=False)
conferences_relationhip.to_csv('/content/gdrive/MyDrive/Project1_sdm/conferences_relationship.csv', index=False)

import pandas as pd

"""## STEP 7: CREATING REVIEWERS RELATIONSHIP BETWEEN PERSONS AND PAPERS"""

articles=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/articles.csv')
authors=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/authors.csv')
co_authors=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/co_authors.csv')
co_authored_by=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/co_authored_by.csv')
authored_by=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/authored_by.csv')

import random
articles_list=articles['article_ID'].drop_duplicates().tolist()
authors_list=authors['author_ID'].drop_duplicates().tolist()
co_authors_list=co_authors['coauthor_ID'].drop_duplicates().tolist()
co_authored_by.reset_index(drop=True, inplace=True)
authored_by.reset_index(drop=True, inplace=True)
reviewers=pd.DataFrame()

for i,row in authored_by.iterrows():
  j=random.randint(0,len(authored_by['AUTHOR_ID'].tolist())-1)
  if authored_by.loc[i, 'AUTHOR_ID']!=row['AUTHOR_ID']:
    reviewers=reviewers.append(pd.Series([row['ARTICLES_ID'], authored_by.loc[i]]), ignore_index=True)
  else:
    k=random.randint(0,len(authored_by['AUTHOR_ID'].tolist())-1)
    reviewers=reviewers.append(pd.Series([row['ARTICLES_ID'], authored_by.loc[k, 'AUTHOR_ID']]), ignore_index=True)

for i,row in co_authored_by.iterrows():
  j=random.randint(0,len(co_authored_by['COAUTHOR_ID'].tolist())-1)
  if co_authored_by.loc[i, 'COAUTHOR_ID']!=row['COAUTHOR_ID']:
    reviewers=reviewers.append(pd.Series([row['ARTICLES_ID'], co_authored_by.loc[i]]), ignore_index=True)
  else:
    k=random.randint(0,len(co_authored_by['COAUTHOR_ID'].tolist())-1)
    reviewers=reviewers.append(pd.Series([row['ARTICLES_ID'], co_authored_by.loc[k, 'COAUTHOR_ID']]), ignore_index=True)

reviewers=pd.read_csv('/content/gdrive/MyDrive/Project1_sdm/reviewers.csv')

reviewers.rename(columns={0:'Article', 1:'Reviewer'}, inplace=True)

reviewers=reviewers.astype(int)

from essential_generators import DocumentGenerator
main = DocumentGenerator()
abstracts = [main.gen_sentence() for x in range(len(reviewers))]
reviewers['abstract'] = abstracts

articles_r=reviewers['Article'].unique().tolist()

decision=[]
for art in articles_r:
  l=len(reviewers[reviewers['Article']==art])
  if l%2==0:
    decision=decision+['Positive']*l
  else:
    decision=decision+['Positive']*(l-1)+['Negative']

reviewers['Decision']=decision

reviewers.to_csv('/content/gdrive/MyDrive/Project1_sdm/reviewers_with_review.csv', index=False)

co_authors.rename(columns={'coauthor_ID': 'author_ID', 'coauthor':'author'}, inplace=True)
co_authors
people=pd.concat([authors, co_authors], axis=0)
people.drop_duplicates(inplace=True)

affi=['UPC', 'UPF', 'UAB', 'UB', 'URL',
              'ESADE', 'AALTO', 'ULB', 'UPV', 'ITHINKUPC', 'KPMG', 'DELOITTE', 
              'APPLE', 'GOOGLE', 'APPLE', 'HP', 'PWC', 'IBM', 'KTH', 'UIC', 'HP']

affiliations=pd.DataFrame()
affiliations['name']=affi
affiliations['ID']=list(range(len(affi)))

import random

people['AFFILIATION_ID']=0
for i, row in people.iterrows():
  j=random.randint(0,20)
  people.loc[i,'AFFILIATION_ID']=affiliations.loc[j,'ID']

people.drop(columns='author', inplace=True)

people.to_csv('/content/gdrive/MyDrive/Project1_sdm/affiliated_in.csv', index=False)

affiliations.to_csv('/content/gdrive/MyDrive/Project1_sdm/affiliations.csv', index=False)

people