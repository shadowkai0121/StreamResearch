from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax

SENTIMENT_MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
sentiment_config = AutoConfig.from_pretrained(SENTIMENT_MODEL)
# PT
sentiment_model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)

def get_sentiment(message):
    encoded_input = sentiment_tokenizer(message, return_tensors='pt')
    output = sentiment_model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    sentiment_scores = {}
    
    for i in range(scores.shape[0]):
        l = sentiment_config.id2label[i]
        sentiment_scores[l.lower()] = float(scores[i])

    sentiment = max(sentiment_scores, key=sentiment_scores.get)
    return sentiment_scores['neutral'], sentiment_scores['negative'], sentiment_scores['positive'], sentiment