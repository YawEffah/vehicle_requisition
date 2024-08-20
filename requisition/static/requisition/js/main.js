

//Automatically hide a message alert after 5seconds
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        const alert = document.querySelector('.sys-feedback');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 7000);
  });
  
  
  function w3_open() {
      document.getElementById("mySidebar").style.display = "block";
    }
    
  function w3_close() {
      document.getElementById("mySidebar").style.display = "none";
    }
  
  
  // Get the button:
  let topBtn = document.getElementById("topBtn");
  
  // When the user scrolls down 200px from the top of the document, show the button
  window.onscroll = function() {scrollFunction()};
  
  function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 200) {
      topBtn.style.display = "block";
    } else {
      topBtn.style.display = "none";
    }
  }
  
  // When the user clicks on the button, scroll to the top of the document
  function topFunction() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  }
  
  
// Get all summary info items
const summaryItems = document.querySelectorAll('.scroll-animation ');

// Function to check if an element is in the viewport
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// Function to handle scroll event and add animation class
function handleScroll() {
  summaryItems.forEach(item => {
    if (isInViewport(item)) {
      item.classList.add('animated');
    } else {
      item.classList.remove('animated');
    }
  });
}

// Listen for scroll events
window.addEventListener('scroll', handleScroll);

// Initial check in case elements are already in viewport on page load
handleScroll();


// Toggle sidebar function
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
}


