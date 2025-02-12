document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript loaded and running.");
    // Hide flash messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(function() {
                alert.remove();
            }, 500);  // Wait for the transition to finish before removing the element
        });
    }, 5000);  // 5000 milliseconds = 5 seconds
});
$(document).ready(function() {
    $('select').select2();
});
$(document).ready(function() {
    $('.select2').select2();

    // Auto-hide flash messages
    setTimeout(function() {
        $('.alert-container').fadeOut('slow');
    }, 5000); // Adjust time as needed
});
// main.js

document.addEventListener('DOMContentLoaded', () => {
    const acc = document.getElementsByClassName('accordion');
    
    for (let i = 0; i < acc.length; i++) {
        acc[i].addEventListener('click', function() {
            this.classList.toggle('active');
            const panel = this.nextElementSibling;
            if (panel.style.display === 'block') {
                panel.style.display = 'none';
            } else {
                panel.style.display = 'block';
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function() {
    const questionCards = document.querySelectorAll('.question-card');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const submitButton = document.getElementById('submit-button');

    let currentIndex = 0;

    function showQuestion(index) {
        questionCards.forEach((card, i) => {
            card.style.display = i === index ? 'block' : 'none';
        });

        prevButton.disabled = index === 0;
        nextButton.disabled = index === questionCards.length - 1;
        submitButton.style.display = index === questionCards.length - 1 ? 'block' : 'none';
    }

    showQuestion(currentIndex);

    prevButton.addEventListener('click', function() {
        if (currentIndex > 0) {
            currentIndex--;
            showQuestion(currentIndex);
        }
    });

    nextButton.addEventListener('click', function() {
        if (currentIndex < questionCards.length - 1) {
            currentIndex++;
            showQuestion(currentIndex);
        }
    });
});
