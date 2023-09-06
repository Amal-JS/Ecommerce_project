// console.log('comes')


//nav side bar hidden
menu_vertiacal_container=document.getElementById('menu-vertiacal-container')
menu_vertiacal_container.style.display= 'none';


//nav down arrow

var navDownArrows = document.getElementsByClassName('nav-down-arrow');

for (var i = 0; i < navDownArrows.length; i++) {
    navDownArrows[i].style.marginLeft = '.4rem'; // Adjust the value as needed
}

//grey scale for brands logos

var home_brands = document.getElementById('home_brands');
if (home_brands) {
  home_brands.style.filter = "grayscale(100%)";
}
// console.log('comes2')


//data table for admin side


document.addEventListener("DOMContentLoaded", function () {
  const owlCarousel = document.querySelector(".owl-carousel");

  if (owlCarousel) {
    owlCarousel.style.width="100%";
    owlCarousel.style.height="400px";
    console.log('carousel')
    $(owlCarousel).owlCarousel({
      items: 1, // Number of items to display at once
      autoplay: true, // Autoplay the slider
      loop: true, // Enable looping
      nav: true, // Display navigation arrows
      dots: true, // Display pagination dots
      autoplayTimeout: 3000, // Autoplay interval in milliseconds
      navText: [
        '<span class="custom-nav-icon-prev"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left-fill" viewBox="0 0 16 16"><path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg></span>',
        '<span class="custom-nav-icon-next"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg></span>',
      ],
    });
  }
});



//category fetch

 // Get references to the checkbox elements
 const SmartPhoneCheckbox = document.getElementById('Smart PhoneCheckbox');
 const LaptopCheckbox = document.getElementById('LaptopCheckbox');
 const SmartTVCheckbox = document.getElementById('Smart TVCheckbox');

 // Add event listeners to the checkboxes
 SmartPhoneCheckbox.addEventListener('change', sendRequest);
 LaptopCheckbox.addEventListener('change', sendRequest);
 SmartTVCheckbox.addEventListener('change', sendRequest);

 // Function to send the request when a checkbox is clicked
 function sendRequest(event) {
  
     const checkbox = event.target;
     const isChecked = checkbox.checked;
     const category = checkbox.id.replace('Checkbox', ''); // Remove "Checkbox" from the ID
     
     if (isChecked) {
         
          window.location.href=`/all_products/?page=1&category=${category}`;
     }
 }





 console.log('check category and brand')



    // for brand Define a mapping of checkbox IDs to their corresponding URLs
    var urlMapping = {
        'brand-Apple': '/all_products/?page=1&brand=Apple',
        'brand-Samsung': '/all_products/?page=1&brand=Samsung',
        'brand-MI': '/all_products/?page=1&brand=MI',
        'brand-LG': '/all_products/?page=1&brand=LG',
        'brand-HP': '/all_products/?page=1&brand=HP',
        'brand-ASUS': '/all_products/?page=1&brand=ASUS',
        'brand-Xioami': '/all_products/?page=1&brand=Xioami',
        'brand-Real Me': '/all_products/?page=1&brand=Real Me'
    };


    //for brand and category
    var checkboxes = document.querySelectorAll('.custom-control-input');

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('click', function() {
            // Get the ID of the clicked checkbox
            var checkboxId = this.id;

            // Check if the checkbox is checked
            if (this.checked) {
                // If checked, fetch content from the corresponding URL
                var url = urlMapping[checkboxId];
                if (url) {
                  window.location.href = url;
                }
            } 
        });
    });
