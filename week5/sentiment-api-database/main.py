from transformers import pipeline

# 감정분류하기 
def sentiment(text):
    classifier = pipeline("text-classification",model='./model', top_k = 2)
    prediction = classifier(text)
    label_1, label_2 = prediction[0][0]['label'], prediction[0][1]['label']
    score_1, score_2 = round(prediction[0][0]['score'],3), round(prediction[0][1]['score'],3)
    return (label_1, label_2 ,score_1, score_2)

if __name__ == '__main__':
    text = "This summer is so long because I hate hot weather."
    label_1, label_2 ,score_1, score_2 = sentiment(text)
    print(label_1 ,score_1,label_2, score_2)
