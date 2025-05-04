import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# 1. Sample phishing vs safe email data
data = {
    'text': [
        'Urgent! Your account is compromised, click here to reset.',
        'Congratulations! You won a $1000 gift card. Click now!',
        'Your Amazon order has been shipped.',
        'Meeting scheduled for tomorrow at 10 AM.',
        'Verify your PayPal account now!',
        'Reminder: your electricity bill is due tomorrow.'
    ],
    'label': [1, 1, 0, 0, 1, 0]  # 1 = Phishing, 0 = Safe
}

df = pd.DataFrame(data)

# 2. Preprocess
X = df['text']
y = df['label']

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# 3. Train model
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.3, random_state=42)
model = MultinomialNB()
model.fit(X_train, y_train)

# 4. Test accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# 5. Save model and vectorizer
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/phish_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Model and vectorizer saved!")

