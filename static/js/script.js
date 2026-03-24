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