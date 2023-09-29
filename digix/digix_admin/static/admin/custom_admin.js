//including the content wrapper div inside main div
var main_panel_div = document.getElementById("main_panel_div");
var content_wrapper_div = document.getElementById("content_wrapper_div");
main_panel_div.appendChild(content_wrapper_div);
var container_fluid_page_body_wrapper_id = document.getElementById(
  "container_fluid_page_body_wrapper_id"
);
container_fluid_page_body_wrapper_id.appendChild(main_panel_div);
var nav_ul = document.getElementById("nav_ul");
nav_ul.style.background = "white";




//used for showing product , category , variant data
//data table admin

//starts when document is loaded
$(document).ready(function () {
  // Check the URL to determine which scenario you are in
  var currentUrl = window.location.pathname;

  // so this condition checks which url is visited now in the browser
  //when it knows we are trying to access the page with product or category or variant
  //it will create a datatable with data got from the view function as a json response
  //the view function which return the json data is written in views.py file in products app
  //using ajax and you have to specify which datas to show in columns

  //accessing category page
  if (currentUrl === "/admin/all_category/") {
    // DataTable initialization for the first scenario
    var table = $("#myTable1").DataTable({
      ajax: "/product/category/", // URL to your Django view  ,return json response

      columns: [
        //which datas to show
        { data: "name" }, //show category name
        {data :"is_availble"},
        {
          data: null,
          render: function (data, type, row) {
            //update button ,data :null showing this column not realated to the data from response
            return (
              '<button class="btn btn-warning view-button-update" data-id="' +
              row.id +
              '">Update</button>'
            );
          },
        },
        {
          data: null,
          render: function (data, type, row) {
            // delete button
            return (
              '<button class="btn btn-danger view-button-delete" data-id="' +
              row.id +
              '">Delete</button>'
            );
          },
        },
      ],
    });

    //functions to handle update and delete object
    $("#myTable1 tbody").on("click", ".view-button-delete", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/category_delete/" + data.id + "/"; //calling the category delete url
    });

    $("#myTable1 tbody").on("click", ".view-button-update", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/category_update/" + data.id + "/";
    });
  } else if (currentUrl === "/admin/all_products/") {
    //product page

    //console.log('vannu');

    var table = $("#myTable2").DataTable({
      ajax: "/product/product/", // URL to your Django view

      columns: [
        { data: "name" },
        { data: "category__name" },
        { data: "brand" },

        // data: null tells DataTables that this column doesn't directly map to any data from the server. Instead, it's used to generate custom content for each cell in this column.

        // render: function (data, type, row) is a function that defines how the content for each cell in this column should be generated.

        // Inside the render function, it's creating an HTML button element with the class "btn btn-primary" and a custom data attribute "data-id" which stores the value of row.id. This button is created dynamically for each row in the DataTable.

        // The purpose of this configuration is to display a "Delete" button in each row of the DataTable. When the user clicks this button, the code you previously provided handles the click event and redirects the user to a URL for deleting the corresponding data item based on the data.id value.

        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-warning view-button-update" data-id="' +
              row.id +
              '">Update</button>'
            );
          },
        },
        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-danger view-button-delete" data-id="' +
              row.id +
              '">Delete</button>'
            );
          },
        },
      ],
    });

    $("#myTable2 tbody").on("click", ".view-button-delete", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/product_delete/" + data.id + "/";
    });

    $("#myTable2 tbody").on("click", ".view-button-update", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/product_update/" + data.id + "/";
    });
  } else if (currentUrl === "/admin/all_variants/") {
    //variant function

    //check root url there is a button to delete the object

    //console.log("vannu");

    var table = $("#myTable3").DataTable({
      ajax: "/product/variant_with_image/", // URL to your Django view
      columns: [
        { data: "name" },
        { data: "product_name" },
        { data: "ram" },
        { data: "storage" },
        { data: "color" },
        { data: "mr_price" },
        { data: "selling_price" },
        { data: "stock" },
        { data: "is_available" },

        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-warning view-button-update" data-id="' +
              row.id +
              '">Update</button>'
            );
          },
        },
        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-danger view-button-delete" data-id="' +
              row.id +
              '">Delete</button>'
            );
          },
        },
        // { data :null ,render :function (data,type,row){
        //     return '<p>' + row.images + '</p>'
        // }},
        {
          data: null,
          render: function (data, type, row) {
            if (Array.isArray(data.images) && data.images.length > 0) {
              return (
                '<button class="btn btn-info view-images " data-images="' +
                data.images.join(",") +
                '" style="width:100px";>View Images</button>'
              );
            } else {
              return ""; // Return an empty string if no images are available
            }
          },
        },
        // Other columns (Update and Delete buttons)
      ],
      createdRow: function (row, data, dataIndex) {
        // Handle rendering of images
        var images = data.images;
        var imagesButton = $(row).find(".view-images");

        imagesButton.click(function () {
          var imageUrls = images;
          var currentUrl = "";
          console.log(images);

          // Add the last URL (after the last comma)
          imageUrls[imageUrls.length] = currentUrl;

          var modal = $("#imageModal");
          var currentIndex = 0;
          var imageWidth = 200; // Replace with your desired width in pixels
          var imageHeight = 200;

          modal.on("show.bs.modal", function () {
            currentIndex = 0;
            var imageContainer = $("#imageContainer"); // Select the image container

            // Clear any existing content in the container
            imageContainer.empty();

            // Populate the container with images
            console.log(imageUrls.length)
            for (var i = 0; i < imageUrls.length-1; i++) {
              var img = $("<img>");
              img.attr("src", imageUrls[i]);
              img.attr(
                "style",
                "width: " + imageWidth + "px; height: " + imageHeight + "px;;margin-left:10px;margin-right:10px;margin-bottom:10px;"
              );
              imageContainer.append(img);
            }
          });

          modal.find(".modal-body").on("click", function () {
            currentIndex = (currentIndex + 1) % imageUrls.length;
            var nextImage = imageUrls[currentIndex];
            imagePreview.attr("src", nextImage);
            imagePreview.attr(
              "style",
              "width: " + imageWidth + "px; height: " + imageHeight + "px"
            );
          });

          modal.modal("show");
        });
      },
    });

    $("#myTable3 tbody").on("click", ".view-button-delete", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/variant_delete/" + data.id + "/";
    });

    $("#myTable3 tbody").on("click", ".view-button-update", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/admin/variant_update/" + data.id + "/";
    });
  }else if (currentUrl === "/admin/all_users/") {
    //product page

    //console.log('vannu');

    var table = $("#myTable4").DataTable({
      ajax: "/user/get_all_users/", // URL to your Django view

      columns: [
        { data: "username" },
        { data: "phone" },
        { data: "email" },
        { data : "is_active"},

        
        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-success view-button-unblock" data-id="' +
              row.id +
              '">Unblock</button>'
            );
          },
        },
        {
          data: null,
          render: function (data, type, row) {
            return (
              '<button class="btn btn-danger view-button-block" data-id="' +
              row.id +
              '">Block</button>'
            );
          },
        },
      ],
    });

    $("#myTable4 tbody").on("click", ".view-button-block", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/user/block/" + data.id + "/";
    });

    $("#myTable4 tbody").on("click", ".view-button-unblock", function () {
      var data = table.row($(this).parents("tr")).data();
      // Redirect to the URL with the object ID (data.id)
      window.location.href = "/user/unblock/" + data.id + "/";
    });
  }
});

//styling table// Function to apply the .table_custom class to a div if it exists
function applyCustomStyleToDiv(divId, className) {
  var div = document.getElementById(divId);
  if (div) {
    div.classList.add(className); // Add the CSS class to the div
  }
}

// Define the CSS class name you want to apply
var customClassName = "table_custom";

// List of div IDs
var tableIds = ["myTable1", "myTable2", "myTable3"];

// Wait for the document to fully load before applying the class
document.addEventListener("DOMContentLoaded", function () {
  // Apply the .table_custom class to each div
  for (var i = 0; i < tableIds.length; i++) {
    applyCustomStyleToDiv(tableIds[i], customClassName);
  }
});

//styling the modal  body variant
var ad_modal_body=document.querySelector('#imageContainer')
if(ad_modal_body){
    ad_modal_body.style.borderRadius='25px';
    ad_modal_body.style.border='10px solid #333333';
    ad_modal_body.style.background='white';
}
//styling the modal  content variant

var ad_modal_content=document.querySelector('#ad_modal_content')
if(ad_modal_content){
    ad_modal_content.style.borderRadius='25px';}


//-------------------------------------------------------------------------------------------------------
//add form image croping  and update form image crop

if ( (window.location.pathname.startsWith('/admin/add')) || ( (window.location.pathname.includes('update'))  &&  (window.location.pathname.includes('admin'))))  { 

     //document fully loaded

     document.addEventListener("DOMContentLoaded", function () {
      // Function to handle image upload and cropping for a specific image input
      function handleImageUpload(
        inputId,
        imageId,
        modalId,
        cropBtnId,
        closeBtnId // Add close button ID argument
      ) {
        const input = document.getElementById(inputId);
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        const cropBtn = document.getElementById(cropBtnId);
        const closeBtn = document.getElementById(closeBtnId); // Get close button element
      
        let cropper = null; // Declare cropper variable outside of the event listener
      
        input.addEventListener("change", () => {
          const img_data = input.files[0];
          const url = URL.createObjectURL(img_data);
      
          let image = null;
      
          // Create a new image element
          image = new Image();
          image.id = imageId; // Set the ID for the image element
          image.style.maxWidth = "600px";
          image.style.maxHeight = "350px";
      
          image.src = url;
      
          modal.show(); // Show the modal
      
          image.onload = function () {
            const imageBoxModal = document.getElementById("image-box-modal");
      
            // Clear modal content before opening it for a new image
            imageBoxModal.innerHTML = "";
            imageBoxModal.appendChild(image);
      
            // Initialize Cropper after the image has loaded
            // Delay the Cropper initialization by a short time (e.g., 100 milliseconds)
            setTimeout(function () {
              cropper = new Cropper(image, {
                aspectRatio: 1, // Set the aspect ratio to 1:1 (square)
                autoCropArea: 1,
                viewMode: 1,
                scalable: true,
                zoomable: true,
                movable: true,
                minCropBoxWidth: 200,
                minCropBoxHeight: 200,
              });
            }, 1000); // Adjust the delay time as needed
          };
      
          cropBtn.addEventListener("click", () => {
            cropper.getCroppedCanvas().toBlob((blob) => {
              let fileInputElement = document.getElementById(inputId);
              let file = new File([blob], img_data.name, {
                type: "image/*",
                lastModified: new Date().getTime(),
              });
              let container = new DataTransfer();
              container.items.add(file);
              fileInputElement.files = container.files;
      
              modal.hide(); // Hide the modal after cropping
              updateInputField(inputId, blob); // Update the input field with the cropped image
            });
          });
      
          closeBtn.addEventListener("click", () => {
            modal.hide(); // Hide the modal when the close button is clicked
          });
      
          // JavaScript to close the modal when clicking the icon
          document.getElementById("closeModalIcon").addEventListener("click", function () {
            // Assuming you have a reference to the modal element by its ID
            modal.hide(); // Hide the modal when the close button is clicked
          });
        });
      
        // Function to update the input field with a Blob object
        function updateInputField(inputId, blob) {
          let fileInputElement = document.getElementById(inputId);
          let file = new File([blob], "cropped_image.png", {
            type: "image/png",
            lastModified: new Date().getTime(),
          });
          let container = new DataTransfer();
          container.items.add(file);
          fileInputElement.files = container.files;
        }
      }
      
      // Call the function for each image input
      handleImageUpload("id_image1", "image", "imageModal", "crop-btn", "close-btn");
      handleImageUpload("id_image2", "image2", "imageModal", "crop-btn", "close-btn");
      handleImageUpload("id_image3", "image3", "imageModal", "crop-btn", "close-btn");
      handleImageUpload("id_image4", "image4", "imageModal", "crop-btn", "close-btn");
      handleImageUpload("id_image5", "image5", "imageModal", "crop-btn", "close-btn");

      
            });




}

//--------------------------------------------------------------------------------------------------------

//order status change
if (window.location.pathname.startsWith('/admin/all_orders/')) {
  document.addEventListener("DOMContentLoaded", function () {
      // Initialize the DataTable
      var table = $('#example').DataTable(); // Replace 'yourDataTable' with your table's ID or other selector

      // Function to update option availability based on the current status
function updateOptionAvailability(selectElement, currentStatus) {
  // Loop through the options and set the 'selected' attribute for the matching option
  selectElement.querySelectorAll("option").forEach(function (option) {
      // Enable all options
      option.removeAttribute("disabled");
    
      // If the option's innerText matches the currentStatus, select it
      if (option.innerText === currentStatus) {
          option.setAttribute("selected", "selected");
      }
  });

  
 // Disable options based on the current status and order
let disableOptions = true; // Flag to indicate when to start disabling options
let start = 0;

selectElement.querySelectorAll("option").forEach(function (option, index) {

    if (option.innerText === currentStatus) {
        start = index;
        disableOptions = false; // Allow options after the current status to be enabled
    }

    if (disableOptions) {
        // Set the 'disabled' attribute to true for options before the current status
        option.setAttribute("disabled", "disabled");
    }
});
}
      // Function to add event listeners to select elements
      function addEventListenersToSelects() {
          var selectElements = document.querySelectorAll(".status_select");


          
          selectElements.forEach(function (selectElement,index) {
              var orderId = selectElement.getAttribute("data-order-id");
              var statusTd = document.querySelector(`.changed_status[data-order-id="${orderId}"]`);
              var currentStatus = statusTd.getAttribute("data-status");
              
               // Loop through the options and set the 'selected' attribute for the matching option
        selectElement.querySelectorAll("option").forEach(function (option) {
          if (option.innerHTML === currentStatus) {
              option.setAttribute("selected", "selected");


          }
      });
      
      
              updateOptionAvailability(selectElement,currentStatus);

              
              selectElement.addEventListener("change", function () {
                  var selectedValue = selectElement.value;
                  var orderId = selectElement.getAttribute("data-order-id");
              var statusTd = document.querySelector(`.changed_status[data-order-id="${orderId}"]`);
            
                  var url = "/admin/change_order_status/" + orderId + "/" + selectedValue + "/";

                  fetch(url, {
                      method: "GET",
                      headers: {
                          "Accept": "application/json",
                      },
                  })
                  .then(function (response) {
                      if (response.ok) {
                          return response.json();
                      } else {
                          console.log("Error updating order status:", response.statusText);
                          throw new Error("Failed to update order status");
                      }
                  })
                  .then(function (data) {
                      if (data.order_status_changed) {
                          //working perfectly
                          // Convert to first letter uppercase and remove underscores
                          var formattedValue = data.new_status.toString().replace(/_/g, ' ').replace(/\w\S*/g, function (text) {
                              return text.charAt(0).toUpperCase() + text.slice(1);
                          });
                          statusTd.innerHTML = formattedValue;
                          
                        updateOptionAvailability(selectElement,formattedValue)
                      //     console.log("Order status updated successfully");
                      
                    } else {
                          console.log("Error updating order status:", data.response_error);
                      }
                  })
                  .catch(function (error) {
                      console.error("Fetch error:", error);
                  });
              });
          });
      }

      // Call the function to add event listeners after DataTable initialization
      addEventListenersToSelects();

      // Add event listener to DataTable's 'draw.dt' event
      table.on('draw.dt', function () {
          // Call the function again to add event listeners to any newly added <select> elements
          addEventListenersToSelects();
      });
  });
}



//--------------------------------------------------------------------------------------------------------

// return order status change
if (window.location.pathname.startsWith('/admin/returns/')) {
  document.addEventListener("DOMContentLoaded", function () {
      // Initialize the DataTable
      var table = $('#example').DataTable(); // Replace 'yourDataTable' with your table's ID or other selector

      // Function to update option availability based on the current status
function updateOptionAvailability(selectElement, currentStatus) {
  // Loop through the options and set the 'selected' attribute for the matching option
  selectElement.querySelectorAll("option").forEach(function (option) {
      // Enable all options
      option.removeAttribute("disabled");
    
      // If the option's innerText matches the currentStatus, select it
      if (option.innerText === currentStatus) {
          option.setAttribute("selected", "selected");
      }
  });

  
 // Disable options based on the current status and order
let disableOptions = true; // Flag to indicate when to start disabling options
let start = 0;

selectElement.querySelectorAll("option").forEach(function (option, index) {

    if (option.innerText === currentStatus) {
        start = index;
        disableOptions = false; // Allow options after the current status to be enabled
    }

    if (disableOptions) {
        // Set the 'disabled' attribute to true for options before the current status
        option.setAttribute("disabled", "disabled");
    }
});
}
      // Function to add event listeners to select elements
      function addEventListenersToSelects() {
          var selectElements = document.querySelectorAll(".status_select");


          
          selectElements.forEach(function (selectElement,index) {
              var orderId = selectElement.getAttribute("data-order-id");
              var statusTd = document.querySelector(`.changed_status[data-order-id="${orderId}"]`);
              var currentStatus = statusTd.getAttribute("data-status");
              
               // Loop through the options and set the 'selected' attribute for the matching option
        selectElement.querySelectorAll("option").forEach(function (option) {
          if (option.innerHTML === currentStatus) {
              option.setAttribute("selected", "selected");


          }
      });
      
      
              updateOptionAvailability(selectElement,currentStatus);

              
              selectElement.addEventListener("change", function () {
                  var selectedValue = selectElement.value;
                  var orderId = selectElement.getAttribute("data-order-id");
              var statusTd = document.querySelector(`.changed_status[data-order-id="${orderId}"]`);
            
                  var url = "/admin/change_order_status/" + orderId + "/" + selectedValue + "/";

                  fetch(url, {
                      method: "GET",
                      headers: {
                          "Accept": "application/json",
                      },
                  })
                  .then(function (response) {
                      if (response.ok) {
                          return response.json();
                      } else {
                          console.log("Error updating order status:", response.statusText);
                          throw new Error("Failed to update order status");
                      }
                  })
                  .then(function (data) {
                      if (data.order_status_changed) {
                          //working perfectly
                          // Convert to first letter uppercase and remove underscores
                          var formattedValue = data.new_status.toString().replace(/_/g, ' ').replace(/\w\S*/g, function (text) {
                              return text.charAt(0).toUpperCase() + text.slice(1);
                          });
                          statusTd.innerHTML = formattedValue;
                          
                        updateOptionAvailability(selectElement,formattedValue)
                      //     console.log("Order status updated successfully");
                      
                    } else {
                          console.log("Error updating order status:", data.response_error);
                      }
                  })
                  .catch(function (error) {
                      console.error("Fetch error:", error);
                  });
              });
          });
      }

      // Call the function to add event listeners after DataTable initialization
      addEventListenersToSelects();

      // Add event listener to DataTable's 'draw.dt' event
      table.on('draw.dt', function () {
          // Call the function again to add event listeners to any newly added <select> elements
          addEventListenersToSelects();
      });
  });
}
