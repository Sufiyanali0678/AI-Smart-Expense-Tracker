
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data
descriptions = [
    "bought chicken", "bought vegetables", "ordered food",
    "restaurant dinner", "bought milk", "grocery shopping",

    "uber ride", "petrol for bike", "bus ticket",
    "train ticket", "taxi fare",

    "netflix subscription", "movie ticket", "video game",
    "concert ticket",

    "bought medicine", "doctor consultation",
    "hospital bill", "medical checkup",

    "bought clothes", "new shoes", "shopping mall",
    "bought headphones"
]

categories = [
    "Food", "Food", "Food", "Food", "Food", "Food",
    "Transport", "Transport", "Transport", "Transport", "Transport",
    "Entertainment", "Entertainment", "Entertainment", "Entertainment",
    "Healthcare", "Healthcare", "Healthcare", "Healthcare",
    "Shopping", "Shopping", "Shopping", "Shopping"
]

# Train the model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(descriptions)

model = MultinomialNB()
model.fit(X, categories)


# Predict expense category
def predict_category(description):
    data = vectorizer.transform([description])
    prediction = model.predict(data)
    return prediction[0]
