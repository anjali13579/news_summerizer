import tkinter as tk
from textblob import TextBlob
from newspaper import Article
import nltk

nltk.download('punkt')

def summarize():
    url = utext.get("1.0", "end").strip()

    if not url:
        summary.config(state='normal')
        summary.delete('1.0', 'end')
        summary.insert('1.0', "Please enter a valid URL.")
        summary.config(state='disabled')
        return

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        title.config(state='normal')
        authors.config(state='normal')
        publication.config(state='normal')
        summary.config(state='normal')
        sentiment.config(state='normal')

        title.delete('1.0', 'end')
        authors.delete('1.0', 'end')
        publication.delete('1.0', 'end')
        summary.delete('1.0', 'end')
        sentiment.delete('1.0', 'end')

        title.insert('1.0', article.title)
        authors.insert('1.0', ', '.join(article.authors))
        publication.insert('1.0', str(article.publish_date))
        summary.insert('1.0', article.summary)

        analysis = TextBlob(article.text)
        polarity = analysis.sentiment.polarity
        sentiment_label = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
        sentiment.insert('1.0', f"Polarity: {polarity:.2f}, Sentiment: {sentiment_label}")

        title.config(state='disabled')
        authors.config(state='disabled')
        publication.config(state='disabled')
        summary.config(state='disabled')
        sentiment.config(state='disabled')

    except Exception as e:
        summary.config(state='normal')
        summary.delete('1.0', 'end')
        summary.insert('1.0', f"Error fetching article:\n{str(e)}")
        summary.config(state='disabled')

root = tk.Tk()
root.title("News Summarizer")
root.geometry('1200x600')

tk.Label(root, text="Title").pack()
title = tk.Text(root, height=1, width=140, bg='#dddddd')
title.config(state='disabled')
title.pack()

tk.Label(root, text="Authors").pack()
authors = tk.Text(root, height=1, width=140, bg='#dddddd')
authors.config(state='disabled')
authors.pack()

tk.Label(root, text="Publication Date").pack()
publication = tk.Text(root, height=1, width=140, bg='#dddddd')
publication.config(state='disabled')
publication.pack()

tk.Label(root, text="Summary").pack()
summary = tk.Text(root, height=10, width=140, bg='#dddddd')
summary.config(state='disabled')
summary.pack()

tk.Label(root, text="Sentiment Analysis").pack()
sentiment = tk.Text(root, height=1, width=140, bg='#dddddd')
sentiment.config(state='disabled')
sentiment.pack()

tk.Label(root, text="URL").pack()
utext = tk.Text(root, height=2, width=140)
utext.pack()

tk.Button(root, text="Summarize", command=summarize).pack()

root.mainloop()

