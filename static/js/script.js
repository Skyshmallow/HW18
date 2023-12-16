'use strict';

document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('submit', function (event) {
        if (event.target.classList.contains('delete-post-form')) {
            event.preventDefault();
            const postId = event.target.querySelector('input[name="post_id"]').value;
            deletePost(postId, event.target);
        }
    });
});

function submitPost() {
    const title = document.getElementById('input_title').value;
    const text = document.getElementById('input_textarea').value;
    const photo = document.getElementById('input_img').files[0];

    // Validating data
    if (!title || !text || !photo) {
        displayNotification('Fill everything');
        return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('photo', photo);
    formData.append('text', text);

    fetch("/post", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error posting data");
        }
        return response.json();
    })
    .then(data => {
        displayNotification("Post created successfully!");
        window.location.href = "/posts"; 
    })
    .catch(error => {
        displayNotification("Error creating post.");
        console.error("Error:", error);
    });
}

// Displaying a notification
function displayNotification(message) {
    const notification = document.getElementById("notification");
    notification.innerHTML = message;
}

// redirecting after deleting
function deleteAndRedirect(postId) {
    fetch(`/delete-post/${JSON.parse(postId)}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error deleting post');
        }
        return response.json();
    })
    .then(data => {
        alert('Post deleted successfully');
        window.location.href = "/posts"; 
    })
    .catch(error => {
        alert('Error deleting post.');
        console.error('Error:', error);
    });
}



