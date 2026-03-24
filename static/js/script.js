/* write_review */
/* set star buttons to rating field in form */
document.querySelectorAll('.star-rating:not(.readonly) label').forEach(star => {
    star.addEventListener('click', function() {
        this.style.transform = 'scale(1.2)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 200);
    });
});

/* film_detail */
document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function() {
            const reviewId = this.dataset.reviewId;
            const voteType = this.dataset.vote;

            fetch(`/review/${reviewId}/vote/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    vote_type: voteType
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`up-${reviewId}`).innerText = data.up_votes;
                document.getElementById(`down-${reviewId}`).innerText = data.down_votes;
            });
        });
    });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}