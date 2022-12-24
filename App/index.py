# coding=utf8
from flask import Flask,render_template,request,jsonify
import re
import pickle
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.hi import STOP_WORDS
import json


app=Flask(__name__)
data=pandas.read_csv("../Data/Object_Data/Data.csv")
Vectorizer=TfidfVectorizer()
Total_Vector_Data=Vectorizer.fit_transform(data['Questions'])
Total_Vector_Data=Total_Vector_Data.toarray()
question=""
Regular_expression_definition_for_digits=re.compile('\d+\s|\s\d+|\s\d+\s')
Defined_Stopwords=["मैं","मुझको","मेरा","अपने आप को","हमने","हमारा","अपना","हम","आप","आपका","तुम्हारा","अपने आप","स्वयं","वह","इसे","उसके","खुद को","कि वह","उसकी","उसका","खुद ही","यह","इसके","उन्होने","अपने","क्या","जो","किसे","किसको","कि","ये","हूँ","होता है","रहे","थी","थे","होना","गया","किया जा रहा है","किया है","है","पडा","होने","करना","करता है","किया","रही","एक","लेकिन","अगर","या","क्यूंकि","जैसा","जब तक","जबकि","की","पर","द्वारा","के लिए","साथ","के बारे में","खिलाफ","बीच","में","के माध्यम से","दौरान","से पहले","के बाद","ऊपर","नीचे","को","से","तक","से नीचे","करने में","निकल","बंद","से अधिक","तहत","दुबारा","आगे","फिर","एक बार","यहाँ","वहाँ","कब","कहाँ","क्यों","कैसे","सारे","किसी","दोनो","प्रत्येक","ज्यादा","अधिकांश","अन्य","में कुछ","ऐसा","में कोई","मात्र","खुद","समान","इसलिए","बहुत","सकता","जायेंगे","जरा","चाहिए","अभी","और","कर दिया","रखें","का","हैं","इस","होता","करने","ने","बनी","तो","ही","हो","इसका","था","हुआ","वाले","बाद","लिए","सकते","इसमें","दो","वे","करते","कहा","वर्ग","कई","करें","होती","अपनी","उनके","यदि","हुई","जा","कहते","जब","होते","कोई","हुए","व","जैसे","सभी","करता","उनकी","तरह","उस","आदि","इसकी","उनका","इसी","पे","तथा","भी","परंतु","इन","कम","दूर","पूरे","गये","तुम","मै","यहां","हुये","कभी","अथवा","गयी","प्रति","जाता","इन्हें","गई","अब","जिसमें","लिया","बड़ा","जाती","तब","उसे","जाते","लेकर","बड़े","दूसरे","जाने","बाहर","स्थान","उन्हें ","गए","ऐसे","जिससे","समय","दोनों","किए","रहती","इनके","इनका","इनकी","सकती","आज","कल","जिन्हें","जिन्हों","तिन्हें","तिन्हों","किन्हों","किन्हें","इत्यादि","इन्हों","उन्हों","बिलकुल","निहायत","इन्हीं","उन्हीं","जितना","दूसरा","कितना","साबुत","वग़ैरह","कौनसा","लिये","दिया","जिसे","तिसे","काफ़ी","पहले","बाला","मानो","अंदर","भीतर","पूरा","सारा","उनको","वहीं","जहाँ","जीधर","के","एवं","कुछ","कुल","रहा","जिस","जिन","तिस","तिन","कौन","किस","संग","यही","बही","उसी","मगर","कर","मे","एस","उन","सो","अत"]
def getOutput_fromCosineSimilarity(array):
    array_element_sums=[]
    for i in array:
        array_element_sums.append(sum(i))
    array_element_sums.index(max(array_element_sums))
    return array_element_sums.index(max(array_element_sums))


def getlistofQuestions_fromCosineSimilarity(array):
    array=list(array)
    array_element_sums=[]
    list_of_questions=[]
    for i in array:
        array_element_sums.append(sum(i))
    
    # list_of_questions.append(data['MainQuestion'][array_element_sums.index(max(array_element_sums))])
    if array_element_sums.index(max(array_element_sums))!=0:
        list_of_questions.append(data['MainQuestion'][array_element_sums.index(max(array_element_sums))])
        array_element_sums[array_element_sums.index(max(array_element_sums))]=-1
    if array_element_sums.index(max(array_element_sums))!=0:
        list_of_questions.append(data['MainQuestion'][array_element_sums.index(max(array_element_sums))])
    return list_of_questions




with open('../Models/Vectorizer.pickle',"rb") as f:
    Vectorizer=pickle.load(f)



class SentenceLevelDetection():
    def __init__(self, sentence):
        self.sentence = sentence
        self.word=sentence.split()
        self.word= "".join(self.word)
    def detectlanguage(self):
        counter = 0
        for i in self.word:
            if ord(i) >= 2304 and ord(i) <= 2432:
                counter = counter + 1
        if counter == len(self.word):
            return True
        return False

Hindi_Stop_Words=tuple((STOP_WORDS).union(set(Defined_Stopwords)))
def preprocessing_of_sentence(text):
    text=Regular_expression_definition_for_digits.sub(r" ",text)
    punctuations = [".",",","!","?","'",'"',":",";","*","-","/","+","%","$","#","@","(",")","[","]","{","}"]
    for i in punctuations:
        text = text.replace(i," ")
    text=text.lower().split()
    # text=[word for word in text if word not in Hindi_Stop_Words and len(word)>1]
    print(text)
    return text

def getWholeProcessflow(text):
    text=Regular_expression_definition_for_digits.sub(r" ",text)
    punctuations = [".","=","_","<",">",",","!","?","'",'"',":",";","*","-","/","+","%","$","#","@","(",")","[","]","{","}","\n"]
    for i in punctuations:
        text = text.replace(i," ")
    output={

    }
    sentenceLevelDetection=SentenceLevelDetection(text);
    output['validation']=sentenceLevelDetection.detectlanguage()
    temp_text=""
    for i in text:
        if ord(i) >= 2304 and ord(i) <= 2432:
            temp_text+=i
        if ord(i)==32:
            temp_text+=" "
    output['filtration']=temp_text
    text=text.lower().split()
    output['tokenization']=text
    final_array=[]
    for j in [i for i in Vectorizer.transform(text).toarray()]:
        for k in j:
            final_array.append(k)
    print(final_array)
    output['vectorization']=final_array
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getresponse',methods=['POST','GET'])
def getresponse():
    print("getresponse is requested")
    if request.method=='POST':
        if request.json['question']=="":
            return jsonify({"response":"ERROR"})
        else:
            question=request.json['question']
            input_Text=preprocessing_of_sentence(request.json['question'])
            print(input_Text)
            input_Text=Vectorizer.transform(input_Text)
            print(input_Text)
            cosine_similarity_values=cosine_similarity(Total_Vector_Data,input_Text)
            print(cosine_similarity_values)
            response=data['Answers'][getOutput_fromCosineSimilarity(cosine_similarity_values)]
            print(response)
            output=getWholeProcessflow(question)
            return jsonify({"response":response,"output":json.dumps(output)})
    else:
        return jsonify({"response":"ERROR"})

@app.route('/getsuggestion',methods=['POST','GET'])
def getsuggestedQuestions():
    print("getresponse is requested")
    if request.method=='POST':
        if request.json['question']=="":
            return jsonify({"response":"ERROR"})
        else:
            question=request.json['question']
            input_Text=preprocessing_of_sentence(request.json['question'])
            print(input_Text)
            input_Text=Vectorizer.transform(input_Text)
            print(input_Text)
            cosine_similarity_values=cosine_similarity(Total_Vector_Data,input_Text)
            print(cosine_similarity_values)
            response=getlistofQuestions_fromCosineSimilarity(cosine_similarity_values)
            return jsonify({"response":response})
    else:
        return jsonify({"response":"ERROR"})



if __name__=='__main__':
    app.run(debug=True)
    # webbrowser.open("http://127.0.0.1:5000/")