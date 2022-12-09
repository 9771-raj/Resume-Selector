import numpy as np
import pandas as pd
import sklearn
import re,os
import PyPDF2
import nltk 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
import re
from wordcloud import WordCloud

stop=stopwords.words("english")


def remove_specialChar(x):
    text=re.sub(r"http\S+", "", x)
    text=re.sub('[^A-Za-z0-9]+', ' ',text)
    return text

def remove_stopwords(data):
    data=data.split()
    a=[]
    for i in data:
        if i not in stop:
            a.append(i)
    return " ".join(a)

def onlyText(data):
    data=data.split()
    a=[]
    token_pattern="[^\W\d_]+"
    for i in data:
        if i not in token_pattern and len(i)>2 and not i.isnumeric():
            a.append(i)
    return " ".join(a)


def prediction(path,skills):
    total_files=os.listdir(path)

    resume_dict={}

    for files in total_files:
        if re.search("\.pdf",files):
            reader=PdfReader(path+files)
            num_pages=len(reader.pages)
            # for only single page
            file_txt=""
            for i in range(num_pages):
                page=reader.pages[i]
                text=page.extract_text()
                file_txt+=text
            resume_dict[files]=file_txt

    
    resume_dict["requiredSkill"]=skills

    df=pd.DataFrame(resume_dict.items(),columns=["name","content"])

    df["content"]=df["content"].apply(lambda x:x.lower())
    df["content"]=df["content"].apply(remove_specialChar)
    df["content"]=df["content"].apply(remove_stopwords)
    df["content"]=df["content"].apply(onlyText)
    

    cv=CountVectorizer(max_features=5000,stop_words="english",token_pattern="[^\W\d_]+")
    vectors=cv.fit_transform(df["content"]).toarray()

    similarity=cosine_similarity(vectors)
    result=sorted(list(enumerate(similarity[df.shape[0]-1])),reverse=True,key=lambda x:x[1])[:]
    
    resumeIdName=df["name"].values.tolist()

    predict={"resume_dict":resume_dict,"result":result,"resumeName":resumeIdName}
    
    # word cloud 
    word_cloud = WordCloud(collocations = True, background_color = 'black').generate(df['content'].iloc[-1])

    img_path="E:\\wordcloudGenerator\\resumePro\\resumeBest\\static\\"

    word_cloud.to_file(os.path.join(img_path,"alice.png"))


    return predict




#

if __name__== '__main__':
    remove_specialChar(str)
    remove_stopwords(str)
    onlyText(str)
    prediction(str,str)