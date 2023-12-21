from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl', 'rb'))
pivot_table = pickle.load(open('pivot_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].values.tolist(),
                           author=popular_df['Book-Author'].values.tolist(),
                           image=popular_df['Image-URL-M'].values.tolist(),
                           votes=popular_df['num_ratings'].values.tolist(),
                           ratings=popular_df['avg_ratings'].values.tolist(),
                           )



@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(pivot_table.index == user_input)[0][0]
    distances = similarity_score[index]
    similar_books = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:5]
    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pivot_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)