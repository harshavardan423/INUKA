// Add smooth scroll effect with a delay
document.addEventListener("DOMContentLoaded", function() {
    var elements = document.querySelectorAll('.overlay');
  
    function isInViewport(element) {
      var rect = element.getBoundingClientRect();
      return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
      );
    }
  
    function handleScroll() {
      elements.forEach(function(element) {
        if (isInViewport(element)) {
          element.classList.add('visible');
        }
      });
    }
  
    // Initial check on page load
    handleScroll();
  
    // Add scroll event listener
    window.addEventListener('scroll', function() {
      handleScroll();
    });
  });
  