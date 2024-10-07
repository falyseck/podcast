// Function to display comments
function displayComments() {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = ''; // Clear existing comments

    const comments = JSON.parse(localStorage.getItem('comments')) || [];
    comments.forEach((comment, index) => {
        const commentDiv = document.createElement('div');
        commentDiv.className = 'comment';
        commentDiv.textContent = comment;

        // Create a delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'delete-comment';
        deleteButton.onclick = () => deleteComment(index); // Call deleteComment with the index

        commentDiv.appendChild(deleteButton);
        commentsList.appendChild(commentDiv);
    });
}

// Function to delete a comment
function deleteComment(index) {
    const comments = JSON.parse(localStorage.getItem('comments')) || [];
    comments.splice(index, 1); // Remove the comment at the specified index
    localStorage.setItem('comments', JSON.stringify(comments)); // Update local storage
    displayComments(); // Refresh the comments display
}

// Function to add a comment (same as before)
function addComment() {
    const commentInput = document.getElementById('comment-input');
    const comment = commentInput.value.trim();

    if (comment) {
        const comments = JSON.parse(localStorage.getItem('comments')) || [];
        comments.push(comment);
        localStorage.setItem('comments', JSON.stringify(comments));
        commentInput.value = ''; // Clear input
        displayComments(); // Refresh the comments display
    } else {
        alert("Please enter a comment."); // Alert if the comment is empty
    }
}

// Event listener for the submit button
document.getElementById('submit-comment').addEventListener('click', addComment);

// Display comments on page load
window.onload = displayComments;
