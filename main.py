from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'img'

main = Flask(__name__)
main.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(main)


def read_posts_from_file():
  try:
    with open('data.json', 'r') as file:
      content = file.read()
      posts = json.loads(content) if content else []
      return posts if isinstance(posts, list) else []
  except FileNotFoundError:
    return []
  except json.JSONDecodeError as e:
    print("Error decoding JSON:", str(e))
    return []


@main.route('/')
def index():
  return render_template('index.html')


@main.route('/posts')
def display_posts():
  posts = read_posts_from_file()
  return render_template('posts.html', posts=posts)


@main.route('/post', methods=['POST'])
def create_post():
  try:
    title = request.form.get('title')
    text = request.form.get('text')
    photo = request.files['photo']

    posts = read_posts_from_file()
    try:
      if photo:
        filename = secure_filename(photo.filename)
        filepath = os.path.join('static', 'img', filename)
        photo.save(filepath)
      else:
        filename = None
    except (FileNotFoundError, PermissionError) as e:
      print("Error saving file:", str(e))
      return jsonify({"error": f"Error saving file: {str(e)}"}), 500

    new_post = {
        "title": title,
        "text": text,
        "photo": f"/static/img/{filename}"
    }
    posts.append(new_post)

    with open('data.json', 'w') as file:
      json.dump(posts, file, indent=2)

    return jsonify({"message": "Post created successfully"})
  except Exception as e:
    print("Error creating post:", str(e))
    return jsonify({"error": "Error creating post"}), 500


@main.route('/delete-post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
  try:
    posts = read_posts_from_file()

    if 0 < post_id <= len(posts):
      deleted_post = posts.pop(post_id - 1)

      with open('data.json', 'w') as file:
        json.dump(posts, file, indent=2)

      return jsonify({
          "message": "Post deleted successfully",
          "deleted_post": deleted_post
      })
    else:
      return jsonify({"error": "Invalid post ID"}), 400
  except Exception as e:
    print("Error deleting post:", str(e))
    return jsonify({"error": "Error deleting post"}), 500


if __name__ == '__main__':
  main.run(debug=True)

# host='0.0.0.0', port=5000, 