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
   

    // //if select object in the dom
    // if (sortbySelect) {

    //     // Add an event listener to detect changes in the select element
    //     sortbySelect.addEventListener('change', function () {

    //         // Get the selected value
    //         const selectedValue = sortbySelect.value;
    //         console.log('--------------------',selectedValue,'-----------------')
    //         let url = null;
    
    //         // Construct the URL for your fetch request
    //         const currentURL = window.location.href;

    //       //console.log('selected value ', selectedValue,'   current url  ',currentURL)

    //       if (currentURL=='/all_products/'){//check if url is for all products
    //         url = currentURL + selectedValue;
    //       }
    //       else if (currentURL.startsWith('/all_products/price')){ //second , all products with price filter option
    //         if (currentURL.includes("price_low_to_high")) {

    //           // Split the URL by "/"
    //           const urlParts = currentURL.split("/");

    //           // Remove "price_low_to_high/" if it exists in the URL
    //           const newUrlParts = urlParts.filter(part => part !== "price_low_to_high");

    //           // Reconstruct the modified URL
    //           const newURL = newUrlParts.join("/");
    //           url = newURL+selectedValue;
    //           console.log(newURL);
    //       } else {
    //           // Split the URL by "/"
    //           const urlParts = currentURL.split("/");

    //           // Remove "price_low_to_high/" if it exists in the URL
    //           const newUrlParts = urlParts.filter(part => part !== "price_high_to_low");

    //           // Reconstruct the modified URL
    //           const newURL = newUrlParts.join("/");
    //           url = newURL+selectedValue;
    //           console.log(newURL);
    //       }
            
    //       }
    //         else if (currentURL.includes("price")) {
    //             // If the URL contains "price," do something
    //             if (currentURL.includes("price_low_to_high")) {
    //                 // Split the URL by "/"
    //                 const urlParts = currentURL.split("/");
    
    //                 // Remove "price_low_to_high/" if it exists in the URL
    //                 const newUrlParts = urlParts.filter(part => part !== "price_low_to_high");
    
    //                 // Reconstruct the modified URL
    //                 const newURL = newUrlParts.join("/");
    //                 url = newURL+selectedValue;
    //                 console.log(newURL);
    //             } else {
    //                 // Split the URL by "/"
    //                 const urlParts = currentURL.split("/");
    
    //                 // Remove "price_low_to_high/" if it exists in the URL
    //                 const newUrlParts = urlParts.filter(part => part !== "price_high_to_low");
    
    //                 // Reconstruct the modified URL
    //                 const newURL = newUrlParts.join("/");
    //                 url = newURL+selectedValue;
    //                 console.log(newURL);
    //             }
    //         } else {
    //             // If the URL does not contain "price," do something else
    //             //adding filter option with url
    //             url = currentURL + selectedValue;
    //             console.log(url);
    //         }
    
    //         // Perform the fetch request
    //         fetch(url)
    //             .then(response => {
    //                 if (response.ok) {
    //                     window.location.href = url;
    //                     console.log('Request successful');
    //                 } else {
    //                     console.error('Request failed with status:', response.status);
    //                 }
    //             })
    //             .catch(error => {
    //                 console.error('Fetch error:', error);
    //             });
    //     });
    // }



    //if select object in the dom
    if (sortbySelect) {

      // Add an event listener to detect changes in the select element
      sortbySelect.addEventListener('change', function () {

          // Get the selected value
          const selectedValue = sortbySelect.value;
          console.log('--------------------',selectedValue,'-----------------')
          let url = '';
          let newURL='';
  
          // Construct the URL for your fetch request
          const currentURL = window.location.pathname;

        //console.log('selected value ', selectedValue,'   current url  ',currentURL)

       if (currentURL.includes("page")){ //second , all products with price filter option
          

            // Split the URL by "/"
            const urlParts = currentURL.split("/");
            //console.log('page parts :',urlParts)

            // Remove "price_low_to_high/" if it exists in the URL
            const newUrlParts = urlParts.filter(part =>  !part.includes('page'));

          

            // Reconstruct the modified URL
             uRL = newUrlParts.join("/");

             if (uRL.endsWith('//')){
              
              // newURL = uRL.slice(0, -1);
              console.log('after slicing page ',newURL)
             }else{
              newURL = uRL+'/';
             }
             
            
            console.log(newURL,' page value');
        
          
        }
           if ((currentURL.includes('price')) || (newURL.includes("price"))) {
              // If the URL contains "price," do something
              const urlParts = currentURL.split("/");
              const newUrlParts = urlParts.filter(part => !part.includes('price'));
              uRL = newUrlParts.join("/");
            // Reconstruct the modified URL
            if (uRL.endsWith('//')){
              //console.log('vannu')
              newURL = uRL.slice(0, -1);

              //console.log('after slicing price ',newURL)
             }else{
              newURL = uRL+'';
              //console.log(' not after slicing price ',newURL)
             }
             
            console.log(newURL,' price value');
          } 
          if (newURL !== ''){
            url = newURL+selectedValue;
          }else{
            url = currentURL+selectedValue;
          }
         

          console.log(url,'last url')

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


//========================================================================================


//form handling frontend user sign up


//funtion to empty the div for errors when user give value in a field and then again gives another value the existing p element will remain, to remove that using this

if (window.location.pathname === '/user_sign_up/'){

  //console.log('in sign up form page')

function clear_div(name){

  if (name.charAt(0) === '#'){
      element = document.querySelector(name+"-error")
      element.textContent=''
  }else{
      element = document.querySelectorAll(name)
      elements.forEach(element => {
      // Set the text content to an empty string
      element.textContent = '';
  });
  }
  
}

//empty the form errors before submitting then only if again occurs the div will be empty
sign_up_form=document.getElementById('signup_form')

if (sign_up_form){

  //console.log('gets the form')

  addEventListener('submit', (e) => {
    if ((document.getElementById('username-error').textContent === '') &&
(document.getElementById('phone-error').textContent === '') &&
(document.getElementById('email-error').textContent === '') &&
(document.getElementById('password-error').textContent === '') &&
(document.getElementById('password2-error').textContent === '') &&
(document.getElementById('password21-error').textContent === '') &&
(document.getElementById('phone1-error').textContent === '') &&
(document.getElementById('password-2-error').textContent === '') &&
(document.getElementById('password-3-error').textContent === '') 
){
  clear_div('.error-container');
      console.log('No error');

}else{
  e.preventDefault();
  console.log('Error');
}
    // const elements = document.querySelectorAll('.error-container')
    // // Loop through the selected elements
    // clear_div('.error-container')

    
  })
}



//form handling
document.addEventListener('DOMContentLoaded', function () {
  // Function to check if value and some another validation  in the database


  async function checkExists(fieldName, fieldValue) {

      const response = await fetch(`/user_sign_up_value/?field_name=${fieldName}&field_value=${fieldValue}`);
      const data = await response.json();

      if (data.exists) {

          // 'data.errors' is an object with the structure like { field_name: error_list (it is a string) }


          const errors = data.errors;
          // const fieldN = data.errors.field_name;
          // console.log(fieldN)



          for (const field_name in errors) {

              if (errors.hasOwnProperty(field_name)) {

                  const error_list = errors[field_name];
                  
                  //console.log("Field Name: " + field_name + "Error List: " + error_list);
                  
                  //getting the div element to display error
                  errorContainer = document.getElementById(fieldName + '-error')

                  //If error_list is an array, you can loop through its items
                  //checking if any element in list is ''
                  arr = error_list.split(',').filter(item => item !== '');
                  

                  if (arr) {

                      for (let i = 0; i < arr.length; i++) {

                          const errorLine = document.createElement('p');
                          //console.log(error_list[i])
                          errorLine.textContent = arr[i]
                          errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1');
                          errorContainer.appendChild(errorLine);
                          //console.log("Error " + (i + 1) + ": " + error_list[i]);
                      }
                  }
              }
          }





         
      } else {
          document.getElementById(fieldName + '-error').textContent = '';
      }
  }

//function to check if phone field contains any charecters
  function containsNonNumericChars(inputString) {
    //console.log(inputString)
    const result = parseInt(inputString)
    console.log(typeof result,result)
    return isNaN(result);  //return result=== Nan won't work nan special type 
  }

  const password2 =document.getElementById('id_password2')
const password =document.getElementById('id_password')
const username =document.getElementById('id_username')



//passwords comparing

function passwordCompare(){
  console.log('comparing passwords')
  if ((password) && (password2)){

    if ( password2.value !== '' && password.value !== password2.value ){
  
      errorContainer = document.getElementById('password21-error')
      console.log('password and password2 comparing')
      const errorLine = document.createElement('p');
      //console.log(error_list[i])
      errorLine.textContent = "Password's didn't match"
      //console.log(errorLine.value)
      errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1','never-erase');
      console.log(errorLine,errorContainer)
      errorContainer.appendChild(errorLine);
      
  
  
    }
  
  }
}





//console.log('passoword2 field ',password2)


//function checks the username and password value
function passwordUsernameCheck(){
  
  console.log('Username field ',username.value)
  console.log('password field ',password.value)
  if (username && password && username.value != ''){

    if (password.value.includes(username.value)){

     errorContainer = document.getElementById('password-2-error')
   //console.log('username and password are comparing','  ',password.value,' ',username.value,'getting the  error div ',errorContainer)
   const errorLine = document.createElement('p');
   //console.log(error_list[i])
   //console.log(errorLine)
   errorLine.textContent = "Password simillar to username"
   //alert('password simillar to usernaem')
   errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1');
   errorContainer.appendChild(errorLine);
   //check password contain any number
   var digitPattern = /\d/;

  // Use the test method of the regular expression to check if the inputString contains a digit
  if (! (digitPattern.test(password.value))){
    errorContainer = document.getElementById('password-3-error')
    const errorLine = document.createElement('p');
    errorLine.textContent = "Password want to contain a number "
    errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1');
    errorContainer.appendChild(errorLine);
  }


   
   console.log(errorLine,errorContainer)
   //console.log('error container :',errorContainer)
    }
 }
}



  // Event listeners for each input field
  //id of input ta
  id_username=document.getElementById('id_username')
  if (id_username){
    id_username.addEventListener('blur', function () {

      //clear the div element again focusing on input element
      
      clear_div('#username')

      //check the value 
      checkExists('username', this.value); //this.value or document.getElementById('id_username').value
  });
  }
 

  id_email=document.getElementById('id_email')
  if(  id_email){
    document.getElementById('id_email').addEventListener('blur', function () {
      clear_div('#email')
      checkExists('email', document.getElementById('id_email').value);
  });
  }

if(  document.getElementById('id_phone')){

  document.getElementById('id_phone').addEventListener('blur', function () {
    clear_div('#phone')
    document.getElementById('phone1-error').textContent=''
    checkExists('phone', document.getElementById('id_phone').value);
    containsNonNumericChars(document.getElementById('id_phone').value)
    const digits_check = containsNonNumericChars(phone.value)
      //console.log(digits_check)

      if (digits_check){

        errorContainer = document.getElementById('phone1-error')
          console.log('password and password2 comparing')
          const errorLine = document.createElement('p');
          //console.log(error_list[i])
          errorLine.textContent = "Phone number want to be numbers"
          errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1');
          errorContainer.appendChild(errorLine);

      }

});
}
if(document.getElementById('id_password')){
  document.getElementById('id_password').addEventListener('blur', function () {
    document.getElementById('password-2-error').textContent=''
    document.getElementById('password-3-error').textContent=''
    clear_div('#password')
    checkExists('password', document.getElementById('id_password').value);
    passwordUsernameCheck()
    
  });
}
  if(document.getElementById('id_password2')){
    document.getElementById('id_password2').addEventListener('blur', function () {
      document.getElementById('password21-error').textContent=''
      clear_div('#password2')
      checkExists('password2', document.getElementById('id_password2').value);
      passwordCompare()
    });
  }
  


});

}


//verify otp input value length limit and focus change

if ((window.location.pathname === '/user_sign_up/') || (window.location.pathname === '/verify_otp/')){


  document.addEventListener('DOMContentLoaded', function () {
    const otpInputs = document.querySelectorAll('.otp-input');

    if (otpInputs){
      otpInputs.forEach((input, index) => {
        input.addEventListener('input', function () {
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace' && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
    }
   
});

}


//password update field value check 

if (window.location.pathname.startsWith('/user_password_update/')){

  password=document.getElementById('id_password')
  password2 =document.getElementById('id_password2')
//passwords comparing

function passwordCompare(){
  console.log('comparing passwords')
  if ((password) && (password2)){

    if ( password2.value !== '' && password.value !== password2.value ){
  
      errorContainer = document.getElementById('password21-error')
      console.log('password and password2 comparing')
      const errorLine = document.createElement('p');
      //console.log(error_list[i])
      errorLine.textContent = "Password's didn't match"
      //console.log(errorLine.value)
      errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1','never-erase');
      console.log(errorLine,errorContainer)
      errorContainer.appendChild(errorLine);
      
  
  
    }
  
  }
}

if(password){
  document.getElementById('id_password').addEventListener('blur', function () {
    document.getElementById('password-2-error').textContent=''
    document.getElementById('password-3-error').textContent=''
    
    
    
    
  });
}

  if(password2 ){
    document.getElementById('id_password2').addEventListener('blur', function () {
      document.getElementById('password21-error').textContent=''
      
      
      passwordCompare()
    });
  }

}

//-----------------------------------------------------------------------------------------------------
//search bar fetch

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const suggestionsContainer = document.getElementById('suggestions');
 
  
  // Sample data for suggestions (replace with your own data)
  const suggestionsData = [];
  
  // Function to update the suggestions based on user input
  function updateSuggestions() {
    
    const userInput = searchInput.value.toLowerCase();
    suggestionsContainer.innerHTML = ''; // Clear previous suggestions
    suggestionsContainer.style.display='none';

    // Filter the suggestions based on user input
    const filteredSuggestions = suggestionsData.filter(item => item.toLowerCase().includes(userInput));
  

       // Fetch suggestions from the server using the user input
       fetch(`/search_variants/?search_value=${userInput}`)
       .then(response => response.json())
       .then(data => {
         const results = data.results; // Assuming the server returns a 'results' array
        
        // Create and display suggestion paragraphs
if (results.length > 0) {
  results.forEach(result => {

    
    const innerdiv = document.createElement('div')
    innerdiv.style.display='flex'
    // innerdiv.style.justifyContent='space-between'
    innerdiv.style.margin='2px'
    innerdiv.style.marginBottom='5px'
   
    
    const arrow = document.createElement('span')
    arrow.classList.add('glyphicon')
    arrow.innerHTML='&rarr;'
    arrow.style.fontSize='30px'
    

    const link = document.createElement('a');
    const paragraph = document.createElement('p');
    link.setAttribute('href', `/product/${result.id}/`); // Set the link URL based on your data
    paragraph.textContent = result.name; // Set the suggestion text based on your data
    paragraph.style.color = '#333333';
    paragraph.style.fontWeight = '400';
    innerdiv.style.border = '1px solid black';
    paragraph.style.padding = '3px';
    




    // Add a click event listener to populate the input field with the selected suggestion
    paragraph.addEventListener('click', () => {
      searchInput.value = result.name; // Set the input value based on your data
      suggestionsContainer.innerHTML = ''; // Clear suggestions
    });

    // Add a mouseover event listener to change background color on hover
    paragraph.addEventListener('mouseover', () => {
      paragraph.style.backgroundColor = '#333333 !important'; // Use !important
      paragraph.style.color = '#fff !important'; // Use !important
    });

    // Add a mouseout event listener to reset background color when not hovering
    paragraph.addEventListener('mouseout', () => {
      paragraph.style.backgroundColor = ''; // Reset background color
      paragraph.style.color = ''; // Reset text color
    });

    link.appendChild(paragraph);
    innerdiv.appendChild(link)
    innerdiv.appendChild(arrow)
    suggestionsContainer.appendChild(innerdiv);
    suggestionsContainer.style.display='block'
    suggestionsContainer.style.padding = '20px'
  });
} else {
  // Create a paragraph for "No results" message
  suggestionsContainer.textContent=""
  
  const noResultsParagraph = document.createElement('p');
  noResultsParagraph.textContent = 'No results found';
  noResultsParagraph.style.color = '#333333';
    noResultsParagraph.style.fontWeight = '400';
    noResultsParagraph.style.border = '1px solid black';
    noResultsParagraph.style.padding = '3px';
    noResultsParagraph.style.fontSize= '2rem';
    suggestionsContainer.style.background='white'
    
  suggestionsContainer.appendChild(noResultsParagraph);
}

suggestionsContainer.style.display = 'block';
suggestionsContainer.style.padding = '20px'
       })
       .catch(error => {
         console.error('Error fetching suggestions:', error);
       });


    
  }
  
  // Event listener for input changes
  searchInput.addEventListener('input', updateSuggestions);
  

  document.getElementById('searchInput').addEventListener('blur',()=>{
    if (document.getElementById('searchInput').value === ''){
      document.getElementById('suggestions').style.display='none';
    }
  })
  });