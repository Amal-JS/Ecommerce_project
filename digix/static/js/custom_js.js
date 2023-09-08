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


  if (owlCarousel ) {
    const url =window.location.pathname  // there is href for full url and pathname for '/'
    //console.log('home urls :---',url,'-------------------------')
    if ( url  === '/'){
      
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
    
//===========================================================================================================
//product page zoom and  picture selection

    document.addEventListener('DOMContentLoaded', function () {
      const productZoom = document.getElementById('product-zoom');
      const galleryItems = document.querySelectorAll('#product-zoom-gallery .product-gallery-item');

      galleryItems.forEach(item => {
          item.addEventListener('click', function (e) {
              e.preventDefault();
              const newSrc = this.getAttribute('data-image');
              const newZoomImage = this.getAttribute('data-zoom-image');
              // console.log(newSrc)
              // console.log(newZoomImage)

              // Update the src and data-zoom-image attributes of the product-zoom element
              productZoom.src = newSrc;
              productZoom.setAttribute('data-zoom-image', newZoomImage);
          });
      });
  });

//======================================================================================


//product page variant displaying
//======================================================================================
document.addEventListener('DOMContentLoaded', function () {
  const url = window.location.pathname;

  // Check if the current URL matches the /product page
  if (url.startsWith('/product/')) {
    // Extract the product ID from the URL
    const urlParts = url.split('/');
    const productId = urlParts[2];

   // console.log(productId); product id 

    // Construct the fetch URL with the product ID
    const fetchUrl = `/product/simillar_variants/${productId}/`;

    fetch(fetchUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Handle the JSON data here
        console.log(data);
       
        // Select the variant-div element
        const variantDiv = document.getElementById('variant-div');

        // Iterate over the data and create HTML elements
        data.forEach(variant => {
          const variantElement = document.createElement('div');
          variantElement.className = 'd-flex p-2 justify-content-between align-items-center mt-1 mb-3';

          const variantDetails = document.createElement('div');
          variantDetails.className = 'd-flex justify-content-center align-items-center';

          // Create label and value elements for color, ram, and storage
          const colorLabel = document.createElement('label');
          colorLabel.textContent = 'Color :';

          const colorValue = document.createElement('div');
          colorValue.className = 'product-nav product-nav-dots d-flex';

          const colorDot = document.createElement('a');
          colorDot.href = `/product/${variant.id}/`;
          colorDot.className = 'active';
          colorDot.style.background = variant.color;
          colorDot.innerHTML = '<span class="sr-only">Color name</span>';

          colorValue.appendChild(colorDot);

          // Similarly, create label and value elements for ram and storage
          const ramLabel = document.createElement('label');
          ramLabel.textContent = 'RAM:';
          const ramValue = document.createElement('div');
          
          const ramValueAnchor = document.createElement('a');
          ramValueAnchor.href = `/product/${variant.id}/`; // Replace with the actual URL
          ramValueAnchor.textContent = variant.ram;

          const storageLabel = document.createElement('label');
          storageLabel.textContent = 'Storage:';
          const storageValue = document.createElement('div');
          const storageValueAnchor = document.createElement('a');
         storageValueAnchor.href = `/product/${variant.id}/`; // Replace with the actual URL
         storageValueAnchor.textContent = variant.storage;

          

          // Append label and value elements to variantDetails
          variantDetails.appendChild(colorLabel);
          ramValue.appendChild(ramValueAnchor);
          storageValue.appendChild(storageValueAnchor);
          variantDetails.appendChild(colorValue);
          variantDetails.appendChild(ramLabel);
          variantDetails.appendChild(ramValue);
          variantDetails.appendChild(storageLabel);
          variantDetails.appendChild(storageValue);

          // Append variantDetails to variantElement
          variantElement.appendChild(variantDetails);

          // Append variantElement to variantDiv
          variantDiv.appendChild(variantElement);
          // Add margin to the left and right sides of label elements
          // Iterate over the label elements and add margin to each one
          const labelElements = [colorLabel, ramLabel, storageLabel];
          for (const label of labelElements) {
            label.style.margin = '0 10px'; // 10px margin on both left and right sides

          }

          const valueElements = [colorValue, ramValue, storageValue];
          for (const value of valueElements) {
            value.style.margin = '0 10px'; // 10px margin on both left and right sides
            value.style.fontSize = '1.5rem';
            value.style.fontWeight = '500';

          }
        });
      })
      .catch(error => {
        console.error('Error occurred while getting product variants:', error);
      });
  }
});
