import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))
