document.addEventListener('DOMContentLoaded', function() {
    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Hover Effects for Movie Cards
    const movieCards = document.querySelectorAll('.card');
    movieCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.classList.add('shadow-lg');  // Add shadow on hover
        });
        card.addEventListener('mouseout', () => {
            card.classList.remove('shadow-lg');  // Remove shadow when not hovering
        });
    });

    
});
