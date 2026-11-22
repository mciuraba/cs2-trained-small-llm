from wordcloud import WordCloud
import matplotlib.pyplot as plt

from src.processing.data_operations import (
    analyze_words_from_db,
    remove_words_from_dict,
    get_count_from_dict
)

words = analyze_words_from_db("data/cs2.db")
words_after = remove_words_from_dict(words)

print("Unique words:", len(words_after))

print(
    sorted(
        words_after.items(),
        key=lambda x: x[1],
        reverse=True
    )[:30]
)

#print("Exact word count:", get_count_from_dict(words_after, "nice"))

wordcloud = WordCloud(
    width=1600,
    height=1600,
    background_color="black",
    colormap="plasma",
    margin=30,
    prefer_horizontal=0.95,
    relative_scaling=0.5,
    max_words=600
).generate_from_frequencies(words_after)

plt.figure(figsize=(16, 9))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()