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

//=======================================================================================================
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

//===============================================================================================

//category fetch

 // Get references to the checkbox elements
 const SmartPhoneCheckbox = document.getElementById('Smart PhoneCheckbox');
 const LaptopCheckbox = document.getElementById('LaptopCheckbox');
 const SmartTVCheckbox = document.getElementById('Smart TVCheckbox');

 // Add event listeners to the checkboxes
 if (SmartPhoneCheckbox){
  SmartPhoneCheckbox.addEventListener('change', sendRequest);
 }
 if(LaptopCheckbox){

  LaptopCheckbox.addEventListener('change', sendRequest);
 }
 if (SmartPhoneCheckbox){

  SmartTVCheckbox.addEventListener('change', sendRequest);
 }


 // Function to send the request when a checkbox is clicked
 function sendRequest(event) {
  
     const checkbox = event.target;
     const isChecked = checkbox.checked;
     const category = checkbox.id; // Remove "Checkbox" from the ID
     
     if (isChecked) {
      // Construct the URL with the selected category
      const url = `/all_products/${category}/`;
      console.log(url)
      // Send a fetch request to the constructed URL
      fetch(url)
  .then(response => {

    if (response.ok) {
      window.location.href=url
      console.log('Request successful');
    } else {
      console.error('Request failed with status:', response.status);
    }
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
  }
 }





 //console.log('check category and brand')

//==========================================================================================================

    // for brand wise sorting , Define a mapping of checkbox IDs to their corresponding URLs
  

    //for brand 
    var checkboxes = document.querySelectorAll('.custom-control-input');


    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('click', function() {
            // Get the ID of the clicked checkbox
            var checkboxId = this.id;
            const brand = checkbox.id.replace('brand-', '');
          
            // Check if the checkbox is checked
            if (this.checked) {
                // Construct the URL with the selected category
      const url = `/all_products/${brand}/`;
      console.log(url)
      // Send a fetch request to the constructed URL
      fetch(url)
  .then(response => {

    if (response.ok) {
      window.location.href=url
      console.log('Request successful');
    } else {
      console.error('Request failed with status:', response.status);
    }
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });

            } 
        });
    });

//======================================================================================================
    //sorting option for filtering url (user/category.html)
    //getting the select 
    const sortbySelect = document.getElementById('sortby');
   

    //if select object in the dom
    if (sortbySelect) {

        // Add an event listener to detect changes in the select element
        sortbySelect.addEventListener('change', function () {

            // Get the selected value
            const selectedValue = sortbySelect.value;
            console.log('--------------------',selectedValue,'-----------------')
            let url = null;
    
            // Construct the URL for your fetch request
            const currentURL = window.location.href;

          //console.log('selected value ', selectedValue,'   current url  ',currentURL)

          if (currentURL=='/all_products/'){//check if url is for all products
            url = currentURL + selectedValue;
          }
          else if (currentURL.startsWith('/all_products/price')){ //second , all products with price filter option
            if (currentURL.includes("price_low_to_high")) {

              // Split the URL by "/"
              const urlParts = currentURL.split("/");

              // Remove "price_low_to_high/" if it exists in the URL
              const newUrlParts = urlParts.filter(part => part !== "price_low_to_high");

              // Reconstruct the modified URL
              const newURL = newUrlParts.join("/");
              url = newURL+selectedValue;
              console.log(newURL);
          } else {
              // Split the URL by "/"
              const urlParts = currentURL.split("/");

              // Remove "price_low_to_high/" if it exists in the URL
              const newUrlParts = urlParts.filter(part => part !== "price_high_to_low");

              // Reconstruct the modified URL
              const newURL = newUrlParts.join("/");
              url = newURL+selectedValue;
              console.log(newURL);
          }
            
          }
            else if (currentURL.includes("price")) {
                // If the URL contains "price," do something
                if (currentURL.includes("price_low_to_high")) {
                    // Split the URL by "/"
                    const urlParts = currentURL.split("/");
    
                    // Remove "price_low_to_high/" if it exists in the URL
                    const newUrlParts = urlParts.filter(part => part !== "price_low_to_high");
    
                    // Reconstruct the modified URL
                    const newURL = newUrlParts.join("/");
                    url = newURL+selectedValue;
                    console.log(newURL);
                } else {
                    // Split the URL by "/"
                    const urlParts = currentURL.split("/");
    
                    // Remove "price_low_to_high/" if it exists in the URL
                    const newUrlParts = urlParts.filter(part => part !== "price_high_to_low");
    
                    // Reconstruct the modified URL
                    const newURL = newUrlParts.join("/");
                    url = newURL+selectedValue;
                    console.log(newURL);
                }
            } else {
                // If the URL does not contain "price," do something else
                //adding filter option with url
                url = currentURL + selectedValue;
                console.log(url);
            }
    
            // Perform the fetch request
            fetch(url)
                .then(response => {
                    if (response.ok) {
                        window.location.href = url;
                        console.log('Request successful');
                    } else {
                        console.error('Request failed with status:', response.status);
                    }
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        });
    }
    