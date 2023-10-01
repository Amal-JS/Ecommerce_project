//functions that want to work most of the times


// Function to show a simple notification
function showNotification(message,color){
 
        const liveToast = new bootstrap.Toast(document.getElementById("liveToast"));
        const toast_body = document.getElementById('toast_body')
        toast_body.textContent = message
      // Remove existing color classes
    toast_body.classList.remove('text-success', 'text-danger');

    // Add the specified color class
    if (color === 'text-success') {
        toast_body.classList.add('text-success');
    } else if (color === 'text-danger') {
        toast_body.classList.add('text-danger');
       
            
    }
    liveToast.show();
      }

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
          ramValueAnchor.style.color = '#333333';          // Set text color to #333333
          ramValueAnchor.style.textDecoration = 'none'; 

          const storageLabel = document.createElement('label');
          storageLabel.textContent = 'Storage:';
          const storageValue = document.createElement('div');
          const storageValueAnchor = document.createElement('a');
         storageValueAnchor.href = `/product/${variant.id}/`; // Replace with the actual URL
         storageValueAnchor.textContent = variant.storage;
         storageValueAnchor.style.color = '#333333';          // Set text color to #333333
          storageValueAnchor.style.textDecoration = 'none'; 

          

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

//====================================================================================================

  //---------------------------------------------------------------------------------------------------
  //shopping cart icon

  const cart_icon = document.getElementById('shopping_cart_icon')
  document.getElementById('shopping_cart_icon').addEventListener('click',()=>{

    window.location.href = '/cart/'
  })

  //----------------------------------------------------------------------------------------------------
//user account details update

if (window.location.pathname === '/account_details'){

  // console.log('in sign up form page')

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
sign_up_form=document.getElementById('user_account_update_form')

if (sign_up_form){

  //console.log('gets the form')

  addEventListener('submit', (e) => {
    if ((document.getElementById('username-error').textContent === '') &&
(document.getElementById('phone-error').textContent === '') &&
(document.getElementById('email-error').textContent === '') &&
(document.getElementById('phone1-error').textContent === '') 
){
  clear_div('.error-container');
      console.log('No error');
      showNotification('Account Details update successfully' ,'text-success')

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

  user_id = document.getElementById('id_bs')
  // console.log(user_id.textContent)

  async function checkExists(fieldName, fieldValue) {

      const response = await fetch(`/user_account_details_update_value/?user_id=${user_id.textContent}&field_name=${fieldName}&field_value=${fieldValue}`);
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
    // console.log(typeof result,result)
    return isNaN(result);  //return result=== Nan won't work nan special type 
  }




//console.log('passoword2 field ',password2)

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

    const digits_check = containsNonNumericChars(document.getElementById('id_phone').value)
      //console.log(digits_check)

      if (digits_check){

        errorContainer = document.getElementById('phone1-error')
         
          const errorLine = document.createElement('p');
          //console.log(error_list[i])
          errorLine.textContent = "Phone number want to be numbers"
          errorLine.classList.add('text-danger','m-0', 'ml-5', 'mt-1');
          errorContainer.appendChild(errorLine);

      }

});
}
});

}

//user profile password update
//otp focus change

if ((window.location.pathname === '/profile_password_update/') || (window.location.pathname === '/verify_otp/')){

  document.addEventListener("DOMContentLoaded", function () {
    const otpInputs = document.querySelectorAll(".otp-input");
    
    otpInputs.forEach(function (input, index) {
        input.addEventListener("input", function (e) {
            const currentValue = e.target.value;

            if (currentValue.length === 1) {
                // Move focus to the next input if a character is entered
                if (index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            } else if (currentValue.length === 0) {
                // Move focus to the previous input if Backspace is pressed
                if (index > 0) {
                    otpInputs[index - 1].focus();
                }
            }
        });

        input.addEventListener("keydown", function (e) {
            // Prevent default Backspace behavior when the input is empty
            if (e.key === "Backspace" && !input.value) {
                e.preventDefault();
            }
        });
    });
});


}
  
//=========================================================================================================================
//get wishlist product count

const wishlist_count = document.getElementById('wishlist_count_badge')
if (wishlist_count){

  fetch('/wishlist_product_count/')
  .then(response=>response.json())
  .then((data)=>{
    wishlist_count.textContent=data.wishlist_product_count
  })
  .catch(error=>console.log('wishlist count error'))
}

//get cart product count
const cart_count = document.getElementById('cart_count_badge')
if (cart_count){

  fetch('/cart_product_count/')
  .then(response=>response.json())
  .then((data)=>{
    cart_count.textContent=data.cart_product_count
    
  })
  .catch(error=>console.log('cart count error'))
}

//=====================================================================================
//events for handling wishlist and add to cart click event

//wishlist
document.addEventListener("DOMContentLoaded", function() {

  // Find all elements with the class "btn-cart"
  var cartButtons = document.querySelectorAll(".btn-cart");

  // Add a click event listener to "btn-cart" buttons

  cartButtons.forEach(function(button) {
      button.addEventListener("click", function(event) {
          // Prevent the default behavior of the anchor tag
         
         
          // Prevent the default behavior of the anchor tag
          event.preventDefault();

          // Retrieve the value of the "data-variant" attribute
          var dataVariant = button.getAttribute("data-variant");

          fetch('/user_logged_in_status/')

          .then(response => response.json())

          .then(async (data) => {

            

            if (!data.user_authenticated) {

              showNotification('User should be logged in', 'text-danger');

            } else {

              const response = await fetch(`/variant_in_cart_status/?variant_id=${dataVariant}`);
              const cartData = await response.json();
        
              if (cartData.variant_in_cart) {

                showNotification('Product already in cart', 'text-danger');

              }else if ( parseInt(button.getAttribute("data-value")) === 0 ) {

                showNotification('Product not in stock', 'text-danger');

              }
              else {
                try {
                  const response = await fetch(`/add_to_cart/${dataVariant}/`);
                  const data = await response.json();
              
                  if (data.added) {
                    showNotification('Product added to cart', 'text-success');
                    const cart_count = document.getElementById('cart_count_badge')
                    if (cart_count){

                      fetch('/cart_product_count/')
                      .then(response=>response.json())
                      .then((data)=>{
                        cart_count.textContent=data.cart_product_count
                        console.log(cart_count)
                      })
                      .catch(error=>console.log('cart count error'))
                    }
                  }
                  else{
                    showNotification("Product couldn't be added in cart",'text-danger')
                  }
                } catch (error) {
                  console.log('add to cart error: ', error);
                }
                  }

                }


              })
              .catch(error=>console.log('variant in cart error  :',error))

            }
          
          
          )
          

          
      });
 

  // Find all elements with the class "btn-wishlist"
  var wishlistButtons = document.querySelectorAll(".btn-wishlist");

  // Add a click event listener to "btn-wishlist" buttons
  wishlistButtons.forEach(function(button) {


      button.addEventListener("click", function(event) {


        
          // Prevent the default behavior of the anchor tag
          event.preventDefault();

          // Retrieve the value of the "data-variant" attribute
          var dataVariant = button.getAttribute("data-variant");

          fetch('/user_logged_in_status/')

          .then(response => response.json())

          .then(async (data) => {

            

            if (!data.user_authenticated) {

              showNotification('User should be logged in', 'text-danger');

            } else {

              const response = await fetch(`/variant_in_wishlist_status/?variant_id=${dataVariant}`);
              const wishlistData = await response.json();
        
              if (wishlistData.variant_in_wishlist) {

                showNotification('Product already in wishlist', 'text-danger');

              }  else {
                try {
                  const response = await fetch(`/add_to_wishlist/${dataVariant}/`);
                  const data = await response.json();
              
                  if (data.added) {
                    showNotification('Product added to wishlist', 'text-success');
                    const wishlist_count = document.getElementById('wishlist_count_badge')
                    if (wishlist_count){

                      fetch('/wishlist_product_count/')
                      .then(response=>response.json())
                      .then((data)=>{
                        wishlist_count.textContent=data.wishlist_product_count
                      })
                      .catch(error=>console.log('wishlist count error'))
                    }
                  }
                  else{
                    showNotification("Product couldn't be added",'text-danger')
                  }
                } catch (error) {
                  console.log('add to wishlist error: ', error);
                }
                  }

                }


              })
              .catch(error=>console.log('variant in wishlist error  :',error))

            }
          
          
          )
          

          
      });
  });

  //---------------------==============================================================================================
  //-------------------------------------------------CART Page --------------------------------------------------------


//show product qty and increment decrement management


if (window.location.pathname.startsWith('/cart/')){

  document.addEventListener("DOMContentLoaded", function () {

  const minusIcons = document.querySelectorAll(".minus_icon");
    const plusIcons = document.querySelectorAll(".plus_icon");
    const qtyInputs = document.querySelectorAll(".show_qty");
    const variantTotalPrices = document.querySelectorAll('.variant-total-price');
    const variantPrices = document.querySelectorAll('.variant-price');
    const subtotal = document.getElementById('subtotal')
    
      //function to set subtotal in cart

      function setSubTotal(){
        
        let total = 0;
        for (let index=0 ;index<variantTotalPrices.length;index++){
          const price = parseFloat(variantTotalPrices[index].innerText.replace(/[^\d.]+/g, '')); // Clean and parse price
          total += price ;
          console.log(variantTotalPrices[index].innerText,parseFloat(variantTotalPrices[index].innerText.replace(/[^\d.]+/g, '')))
        }
        // console.log('total :',total)
        subtotal.innerHTML = total.toFixed(2); // Update subtotal
      }
      
  
      // Function to calculate and set initial total prices
      function setInitialTotalPrices() {
        for (let index = 0; index < variantTotalPrices.length; index++) {
            const quantity = parseInt(qtyInputs[index].value);
            const price = parseFloat(variantPrices[index].innerText.replace(/[^\d.]+/g, '')); // Clean and parse price
            const total = quantity * price;
            
            variantTotalPrices[index].innerHTML = total.toFixed(2); // Set total with two decimal places
            
        }
        
    }

    setInitialTotalPrices()
    setSubTotal()

//hide '-' icon if 1 item
// Check show_qty value and hide minus icon at the start
qtyInputs.forEach((qtyInput, index) => {
  if (parseInt(qtyInput.value) === 1) {
      minusIcons[index].style.display = 'none';
  }
});

   // Event listener for the minus icon

   if (minusIcons && plusIcons && qtyInputs ){
    

      // Add event listeners for each variant
      minusIcons.forEach((minusIcon, index) => {

        minusIcon.addEventListener("click", function () {
          
            let currentValue = parseInt(qtyInputs[index].value);
            
            if (!isNaN(currentValue) && currentValue > 1) {
              
                qtyInputs[index].value = (currentValue - 1).toString();
                variant_id =parseInt(qtyInputs[index].getAttribute('data-var'))

                fetch(`/cart_variant_qty_update/${variant_id}/${qtyInputs[index].value}`)
                .then(response=>response.json())
                .then(response=>console.log(response.response))
                .catch(error=>console.log('error in variant qty update in cart ',error))
                
                // console.log('parseInt(qtyInputs[index].value) :',parseInt(qtyInputs[index].value),'-----','parseInt(variantPrices[index].innerHTML)) :',variantPrices[index].innerText)
                const cleanedPriceText = variantPrices[index].innerText.replace(/[^\d.]+/g, '') + '.00'; 
                const final_price =parseInt(qtyInputs[index].value) * parseInt(cleanedPriceText);
                variantTotalPrices[index].innerHTML = String(final_price)+'.00'
                setSubTotal();
            }
            // Hide the corresponding minus icon if show_qty is 1
            if (parseInt(qtyInputs[index].value) === 1) {
              minusIcon.style.display = 'none';
          } else {
              minusIcon.style.display = 'block';
          }
        });
    });

    plusIcons.forEach((plusIcon, index) => {
        plusIcon.addEventListener("click", function () {
            let currentValue = parseInt(qtyInputs[index].value);

            if (!isNaN(currentValue) && currentValue < parseInt(qtyInputs[index].getAttribute("max_stock"))) {
              
                qtyInputs[index].value = (currentValue + 1).toString();

                variant_id =parseInt(qtyInputs[index].getAttribute('data-var'))
                
                fetch(`/cart_variant_qty_update/${variant_id}/${qtyInputs[index].value}`)
                .then(response=>response.json())
                .then(response=>console.log(response.response))
                .catch(error=>console.log('error in variant qty update in cart ',error))
                
                // console.log('parseInt(qtyInputs[index].value) :',parseInt(qtyInputs[index].value),'-----','parseInt(variantPrices[index].innerHTML)) :',variantPrices[index].innerText)
                const cleanedPriceText = variantPrices[index].innerText.replace(/[^\d.]+/g, '') + '.00'; 
                const final_price =parseInt(qtyInputs[index].value) * parseInt(cleanedPriceText);
                variantTotalPrices[index].innerHTML = String(final_price)+'.00'
                setSubTotal()
            }
           // Show the corresponding minus icon
           minusIcons[index].style.display = 'block';
            
        });
    });

   } 




//variant qty update in cart

  }

  )};
  
 //======================================================================================================================

//place order variant quantity check
//getting the place order btn
placeOrderBtn = document.getElementById('placeOrderBtn')


if (placeOrderBtn){
  
  placeOrderBtn.addEventListener('click', placeOrder);
}

    //calls when click the place order btn
    function placeOrder() {


      fetch('/user_cart_status/')  // Replace with the correct URL for your view
      .then(response => response.json())
      .then(data => {
          if (data.cart_empty) {
              showNotification('Your cart is empty !','text-danger')
              return
          } 
      })
      .catch(error => {
          console.error('Error on cart status:', error);
  });

  const subtotal = document.getElementById('subtotal_cart').innerHTML
   
  if (subtotal === ''){
    
    showNotification('No item in cart','text-danger');
    return; // Prevent order placement if no address is selected
  }

// Check if a shipping address is selected
var selectedAddress = document.querySelector('input[name="selected_address"]:checked');
if (!selectedAddress) {
    showNotification('Please select an address','text-danger');
    return; // Prevent order placement if no address is selected
}

//get address id 
const address_id = selectedAddress.value;
//address selection is working
// console.log(selectedAddress.value,selectedAddress)

var razorPayAnchor = document.querySelector('[href="#collapse-2"]');
var cashOnDeliveryAnchor = document.querySelector('[href="#collapse-3"]');
let payment_method = null;

//payment selection works
if (razorPayAnchor.classList.contains('collapsed') && cashOnDeliveryAnchor.classList.contains('collapsed')) {

  // Neither "Razor Pay" nor "Cash on Delivery" is selected
  showNotification('Please select a payment method','text-danger');
  return; // Prevent order placement if no payment method is selected
}

//which means razor pay or the online payment method is selected
if (!razorPayAnchor.classList.contains('collapsed')) {

    payment_method = 'online_payment';
  // console.log('Selected payment method: Razor Pay , address id ',selectedAddress.value);

} else {
  payment_method = 'cash_on_delivery';
  // console.log('Selected payment method: Cash on Delivery , address id ',selectedAddress.value);
}

//getting the cart items 

c_element= document.getElementById('item_qty')
c__items= c_element.getAttribute('data-t')
//parse to js object
cartItems=JSON.parse(c__items);



//array which is gonna hold which products are outof stock
let outOfStockVariants = [];

 
  // Function to check stock for a variant


  function checkStockForVariant(variant_id,variant_name, quantityInCart) {
      // Send a fetch request to fetch the current stock quantity
      
     
      fetch('/get_variant_stock/' + variant_id + '/')

          .then(response => response.json())

          .then(data => {

              var stockQuantity = data.stock_quantity;

              // console.log(variant_name,' name ',quantity,'varinat cart qty ---------- response qty',stockQuantity)
              // Check if quantity in cart is greater than available stock

              if (quantityInCart <= stockQuantity) {
                  
                  //stock is enough
              }
              else{
                //console.log('Not enough stock available for ' + variant_name,)
                
                outOfStockVariants.push(variant_name); // Add variant to the list of out of stock variants
       
              }


              // Check if this is the last iteration of the loop
              //due to fetch check in normal flow won't work
        if (variant_id === cartItems[cartItems.length - 1].variant_id) {

          // Proceed with order placement only if there is sufficient stock
          function redirectToOrderSuccess(orderNum) {
            if (orderNum) {
                console.log(orderNum);
                // If the order_confirm request is successful, redirect to the order success page
                window.location.href = `/order_success/${orderNum}/`;
            }
        }


        async function fetchRazorPayData() {
          try {
              const razorPayResponse = await fetch('/razor_pay_instance/');
              if (!razorPayResponse.ok) {
                  throw new Error('Network response was not ok');
              }
              return await razorPayResponse.json();
          } catch (error) {
              console.log('Error fetching Razorpay data:', error);
              throw error;
          }
      }
      
      async function makePayment(razorPayData) {
          // Define your Razorpay options
          var options = {
              "key": "rzp_test_JVNu2LgSFIq4MX",
              "amount": `${razorPayData.payment.amount}`,
              "currency": "INR",
              "name": "Digix Store",
              "description": "Product Purchase",
              "image": "https://example.com/your_logo",
              "order_id": `${razorPayData.payment.id}`,
              "theme": {
                  "color": "#333333",
             

              },

              // Specify the callback URL for redirect after successful payment
        "handler": function (response) {
          console.log('comes into the instance', response);

          // Handle successful payment

          // Instead of using 'window.location.href', you can use a fetch request
          const successUrl = '/order_confirm/?selected_address=' + address_id + '&payment_method=' + payment_method;
          fetch(successUrl, {
              method: 'GET'
          })
          .then(response => response.json())
          .then(data => {
              // Call the order confirmation function
              redirectToOrderSuccess(data.order_num);
          })
          .catch(error => {
              console.log('Error fetching order num:', error);
          });
      }
          };
          console.log(options);
      
          var rzp1 = new Razorpay(options);
          console.log('instance ==========================',rzp1)
      
          rzp1.on('payment.success', function (response) {
            console.log('comes into the instance',response)
              // Handle successful payment
              const url = `/order_confirm/?selected_address=${address_id}&payment_method=${payment_method}`;
              fetch(url, {
                  method: 'GET'
              })
              .then(response => response.json())
              .then(data => {
                  // Call the order confirmation function
                  redirectToOrderSuccess(data.order_num);
              })
              .catch(error => {
                  console.log('Error fetching order num:', error);
              });
          });
      
          rzp1.on('payment.failed', function (response) {
              // Handle payment failure
              alert(response.error.code);
              alert(response.error.description);
              alert(response.error.source);
              alert(response.error.step);
              alert(response.error.reason);
              alert(response.error.metadata.order_id);
              alert(response.error.metadata.payment_id);
          });
      
          // Open the Razorpay payment dialog
          rzp1.open();
      }
        
        if (!outOfStockVariants.length) {



          
            // Check if the payment method is 'online_payment'
            if (payment_method === 'online_payment') {

              async function main(){
                try {
                  const razorPayData = await fetchRazorPayData();
                  makePayment(razorPayData);
              } catch (error) {
                  console.log('An error occurred during online payment:', error);
              }
              }
              main()
             
          } else {
                // If payment method is not 'online_payment', directly proceed to order confirmation
                const url = `/order_confirm/?selected_address=${address_id}&payment_method=${payment_method}`;
                fetch(url, {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(data => {
                    // Call the order confirmation function
                    redirectToOrderSuccess(data.order_num);
                })
                .catch(error => {
                    console.log('Error fetching order num on cash on delivery');
                });
            }
        } else {
            // Display the out-of-stock variants in a modal
            displayOutOfStockVariants(outOfStockVariants);
        }
        }
          })
          .catch(error => {
              console.log('Error fetching variant stock for ' + variant.name);
          });
  }

  // Iterate through cart items and check stock for each variant
  for (var i = 0; i < cartItems.length; i++) {

      var cartItem = cartItems[i];
      
      //variant name
      var variant_id = cartItem.variant_id;
      //variant name
      var variant_name = cartItem.variant_name;
      //quantity
      var quantity = cartItem.quantity;
 
      //check quantity for each variant exist in  inventory
      checkStockForVariant(variant_id, variant_name,quantity);
  }


//function to display the variants which are out of stock
function displayOutOfStockVariants(variants) {

  var modalBody = document.getElementById('details');
  modalBody.innerHTML = ''; // Clear any previous content

  for (var i = 0; i < variants.length; i++) {
    var variantName = variants[i];
    var variantElement = document.createElement('div');
    const para = document.createElement('p')
    para.classList.add('fs-3','m-2','text-dark')
    para.textContent = variantName + ' is out of stock.';
    variantElement.appendChild(para)
    modalBody.appendChild(variantElement);
  }

  // Show the modal
  var modal = new bootstrap.Modal(document.getElementById('exampleModal'));
  modal.show();
}
    }


//----------------------------------------------------------------------------------------------------
//wishlist cart page delete product modal confirm delete
if (window.location.pathname.startsWith('/wishlist') || (window.location.pathname.startsWith('/cart'))){


    document.addEventListener('DOMContentLoaded', function () {
        
       
        
        
        // Handle click event on "Remove" buttons
        var removeButtons = document.querySelectorAll('.btn-remove');

        removeButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent the default behavior of the anchor element
                var deleteLink = this.getAttribute('data-remove-url'); // Get the delete link
                const deletebtn = document.querySelector('#deleteLink')
                deletebtn.setAttribute('href',deleteLink)
                
            });

         });
    });








}

//=====================================================================================================
//return reason modal 
// if (window.location.pathname.startsWith('/order_detail/')){

//   document.addEventListener("DOMContentLoaded", function () {
//     // Get references to the elements
//     var returnBtn = document.getElementById("returnBtn");
//     var returnModal = document.getElementById("returnModal");
//     var sendReasonBtn = document.getElementById("sendReasonBtn");
//     var returnReasonInput = document.getElementById("returnReasonInput");
  
//     if (returnBtn){
//  // When the "Return" button is clicked, show the modal
//  returnBtn.addEventListener("click", function () {
//   returnModal.style.display = "block";
// });
//     }
   
  
//     // When the "Send" button inside the modal is clicked
//     sendReasonBtn.addEventListener("click", function () {
//       // Get the return reason entered by the user
//       var returnReason = returnReasonInput.value;
  
//       // You can now send the return reason to your server or perform any necessary action with it
//       // For demonstration, we'll just display an alert
//       alert("Return Reason: " + returnReason);
  
//       // Close the modal by hiding it
//       returnModal.style.display = "none";
//       // Now, navigate to the specified URL
//     window.location.href = sendReasonBtn.href;
//     });
//   });
// }


//=====================================================================================================
//star rating in product page
if (window.location.pathname.startsWith('/product/')) {

  const starRating = document.getElementById("starRating");
  const starRatingValue = document.getElementById("starRatingValue");

  let review_id = null;
  let variant_id=null;

  if (starRating && starRatingValue) { // Check if both elements exist
    starRating.addEventListener("input", function () {
      const ratingValue = (this.value - 1) * 30; // Convert to percentage
      starRatingValue.style.width = ratingValue + "%";
    });
  }

  const reviewForm = document.getElementById("reviewForm");
  if (reviewForm) {
    reviewForm.addEventListener("submit", function (e) {
      // Append the star rating value as a hidden input field before submitting
      const starRatingInput = document.createElement("input");
      starRatingInput.type = "hidden";
      starRatingInput.name = "star_rating";
      starRatingInput.value = starRating.value;
      this.appendChild(starRatingInput);
    });
  }

  
    
    
  // ...

const updateReviewButtons = document.querySelectorAll('.update-review-btn');

if (updateReviewButtons) {
  // Check if updateReviewButtons exist
  updateReviewButtons.forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault();

      const variantid = this.getAttribute('data-variant-id');
      const reviewId = this.getAttribute('data-review-id');

      // Get the star rating from the review container
      const ratingsValElement = this.closest('.review').querySelector('.ratings-val');
      const starRatingWidth = ratingsValElement.style.width;
      const starRating = parseInt(starRatingWidth) / 20; // Assuming each star represents 20% width

      // Get the review text from the review container
      const reviewTextElement = this.closest('.review').querySelector('.text-dark.fs-4');
      const reviewText = reviewTextElement.textContent;

      const reviewUpdateContainer = document.getElementById('review-container');

      // Create the review update form dynamically
      const reviewUpdateForm = document.createElement('form');
      reviewUpdateForm.id = 'reviewUpdateForm';

      // Create input elements for star rating and review text
      const starRatingInput = document.createElement('input');
      starRatingInput.type = 'range';
      starRatingInput.min = '1';
      starRatingInput.max = '5';
      starRatingInput.step = '1';
      starRatingInput.value = starRating;
      starRatingInput.id = `star_rating`;
      starRatingInput.name = 'star_rating';

      const reviewTextInput = document.createElement('textarea');
      reviewTextInput.className = 'form-control';
      reviewTextInput.name = 'review';
      reviewTextInput.id = `review_update`;
      reviewTextInput.textContent = reviewText;

      // Create a submit button
      const submitButton = document.createElement('button');
      submitButton.type = 'submit';
      submitButton.className = 'btn btn-dark';
      submitButton.textContent = 'Update Review';

      // Append input elements and submit button to the form
      reviewUpdateForm.appendChild(starRatingInput);
      reviewUpdateForm.appendChild(reviewTextInput);
      reviewUpdateForm.appendChild(submitButton);

      reviewUpdateContainer.innerHTML = '';
      reviewUpdateContainer.appendChild(reviewUpdateForm);

      // Update the scope of these variables for the reviewUForm event listener
      const reviewIdForForm = reviewId;
      const variantIdForForm = variantid;
      const reviewTextForForm = reviewText;

      const reviewUForm = document.getElementById("reviewUpdateForm");
      if (reviewUForm) {
        reviewUForm.addEventListener("submit", function (e) {
          e.preventDefault(); // Prevent the default form submission
        // Get the star rating and review text from the form elements
          const starRating = document.getElementById('star_rating').value;
          const reviewText = encodeURIComponent(document.getElementById('review_update').value);
          const decodedReviewText = decodeURIComponent(reviewText);
          const url = `/update_review/${reviewIdForForm}/${variantIdForForm}/?star_rating=${starRating}&review=${encodeURIComponent(decodedReviewText)}`;

          // Send a POST request using fetch
          fetch(url, {
            method: 'GET', // Use GET for the URL with query parameters
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json(); // Assuming the server returns JSON
            })
            .then(data => {
              window.location.href=`/product/${variantIdForForm}/`
            })
            .catch(error => {
              // Handle errors (e.g., display an error message)
              const errorDiv = document.getElementById('error-div');
              errorDiv.textContent = 'An error occurred: ' + error.message;
            });
        });
      }
    });
  });
}

// ...


  


}

//==========================================================================================================================
//order page 
//return reason 


if (window.location.pathname.startsWith('/order_detail/')){

  document.addEventListener("DOMContentLoaded", function () {
   
    // Get references to the elements
    var returnBtn = document.getElementById("sendReasonBtn");
    var returnReasonInput = document.getElementById("returnReasonInput");
    var returnSelect = document.getElementById("returnSelect");
    var orderDetailId = returnBtn.getAttribute('data-id')

    // Add a click event listener to the "returnBtn" button
    returnBtn.addEventListener("click", function () {
      // Get the input value
      var inputReason = returnReasonInput.value.trim();

      // Get the selected option from the dropdown
      var selectedOption = returnSelect.value;

      // Check if the input has a value
      if (inputReason.length > 0 || selectedOption !== "Select a choice") {
        // Make a fetch request to your Django view
        fetch(`/return_order/${orderDetailId}/${inputReason || selectedOption}/`)
          .then(function (response) {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Network response was not ok");
            }
          })
          .then(function (data) {
            // Display the response in a notification
            showNotification(data.response, 'text-success');
             // Reload the page after a short delay (e.g., 1 second)
      setTimeout(function () {
        window.location.reload();
      }, 1000); // Adjust the delay as needed
  
          })
          .catch(function (error) {
            // Handle any errors
            showNotification("An error occurred", 'text-danger');
          });
      } else {
        // Log a message to the console
        showNotification("Select any option to continue",'text-danger');
      }
    });
  });

}

//---------------------------------------order detail product tracking--------------------------------
//----------------------------------------------------------------------------------------------------

if (window.location.pathname.startsWith('/order_detail/')) {
  document.addEventListener("DOMContentLoaded", function () {
    const progress = document.querySelector(".progress");
    const stepCircles = document.querySelector(".step-circles");
    const statusDiv = document.querySelector(".status-message");
    const progressBar = document.querySelector(".progress-bar");
  const dot = document.querySelector(".dot");

    // Define a mapping of statuses to steps (percentages)
    const statusToStep = {
      "order_pending": 20,
      "order_confirmed": 40,
      "shipped": 75,
      "delivered": 100,
      "cancelled": -1, // Use a negative value for canceled
      "returned": -2,  // Use another negative value for returned
      "waiting_for_approval": 100, // Set "Waiting For Approval" as delivered
    };

    // Simulate an order status change (replace with actual status from your data)
    async function updateProgress() {
      const orderId = document.getElementById("sendReasonBtn").getAttribute('data-id');
      try {
        const response = await fetch(`/current_order_status/${orderId}/`);
        
        if (!response.ok) {
          // Handle HTTP error responses here, e.g., display an error message.
          console.error(`Error: ${response.status} - ${response.statusText}`);
          return;
        }else{
          
        }
    
        // Read the response body as text
        const responseBody = await response.json(); // Parse the JSON response
        
    const trimmedStatus = responseBody;
       
        
    let currentStep = statusToStep[trimmedStatus] || 0;
    
    

        let progressBarColor = 'green';
       
        let dotLeft = "0%"; // Initialize dotLeft to 0% by default

  if (
    trimmedStatus === 'delivered' ||
    trimmedStatus === 'cancelled' ||
    trimmedStatus === 'waiting_for_approval' ||
    trimmedStatus === 'returned'
  ) {
    // For specific statuses, set dotLeft to 100%
    dotLeft = "96%";
  } else if (trimmedStatus === 'shipped') {
    // For "shipped" status, set dotLeft to 75%
    dotLeft = "75%";
    console.log(dotLeft)
  } else if (trimmedStatus === 'order_confirmed') {
    // For "shipped" status, set dotLeft to 75%
    dotLeft = "40%";
  } else {
    // Calculate the dotLeft based on currentStep for other statuses
    dotLeft = currentStep + "%";
  }

  // Set the left position of the dot
  dot.style.left = dotLeft;


        if (currentStep < 0) {
         
         
          progressBarColor = trimmedStatus === 'cancelled' ? 'orange' : 'red';
          dot.style.display = "block"; 
          dot.backgroundColor=progressBarColor;
          statusDiv.innerHTML = `<div><p class='fs-3 text-center text-dark fw-bold'>${trimmedStatus.charAt(0).toUpperCase() + trimmedStatus.slice(1)}</p></div>`;
          document.getElementById('orderStatusContiner').style.border=`1px solid ${progressBarColor}`;
        } else {
          stepCircles.style.display = 'flex';
          statusDiv.innerHTML = '';
          dot.style.display = "block"; 
          
        }
    
        progress.style.width = currentStep + "%";
        
        progress.style.backgroundColor = progressBarColor;
      } catch (error) {
        // Handle any fetch or processing errors here.
        console.error('An error occurred:', error);
      }

    }

    // Initial update when the page loads
    updateProgress();

  });
}
