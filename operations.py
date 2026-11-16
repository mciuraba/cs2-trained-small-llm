from process_data import analyze_words, remove_stop_words_from_dict

from wordcloud import WordCloud
import matplotlib.pyplot as plt


words = analyze_words("messages.jsonl")
words_after = remove_stop_words_from_dict(words)

print(type(words_after))
print(len(words_after))
print(list(words_after.items())[:10])
wordcloud = WordCloud(
    width=1600,
    height=1600,
    background_color="black",
    colormap="plasma"
).generate_from_frequencies(words_after)

plt.figure(figsize=(16, 9))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()