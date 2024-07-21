import customtkinter as ctk
from tkinter import scrolledtext
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')

def text_summarizer(text, num_sentences):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word.isalnum() and word not in stop_words]

    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(sentences)
    sentence_scores = {}

    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            word = stemmer.stem(word)
            if word in tfidf.vocabulary_:
                sentence_scores[i] = sentence_scores.get(i, 0) + tfidf_matrix[i, tfidf.vocabulary_[word]]

    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentence_indices = [x[0] for x in sorted_sentences[:num_sentences]]
    top_sentence_indices.sort()

    summary = ' '.join([sentences[i] for i in top_sentence_indices])

    return summary

def generate_summary():
    text = text_input.get("1.0", "end-1c")
    num_sentences = int(num_sentences_input.get())
    summary = text_summarizer(text, num_sentences)
    result_text.delete("1.0", "end")
    result_text.insert("end", summary)

# GUI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Text Summarizer")
window.geometry("800x600")

text_input = ctk.CTkTextbox(window, height=200, width=600, wrap="word")
text_input.pack(pady=20)

num_sentences_label = ctk.CTkLabel(window, text="Number of Sentences:", font=("Arial", 16))
num_sentences_label.pack()

num_sentences_input = ctk.CTkEntry(window, justify='center', font=("Arial", 16), width=200)
num_sentences_input.pack(pady=10)

generate_button = ctk.CTkButton(window, text="Generate Summary", command=generate_summary, font=("Arial", 16))
generate_button.pack(pady=20)

result_text = ctk.CTkTextbox(window, height=200, width=600, wrap="word")
result_text.pack(pady=10)

window.mainloop()
