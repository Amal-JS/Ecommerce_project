
//including the content wrapper div inside main div
var main_panel_div = document.getElementById('main_panel_div')
var content_wrapper_div= document.getElementById('content_wrapper_div')
main_panel_div.appendChild(content_wrapper_div)
var container_fluid_page_body_wrapper_id=document.getElementById('container_fluid_page_body_wrapper_id')
container_fluid_page_body_wrapper_id.appendChild(main_panel_div)
var nav_ul = document.getElementById('nav_ul')
nav_ul.style.background='white';


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
    if (currentUrl === '/admin/all_category/') {
      
        // DataTable initialization for the first scenario
        var table = $('#myTable1').DataTable({

            ajax: '/product/category/', // URL to your Django view  ,return json response
  
            columns: [   //which datas to show
                { data: 'name' },  //show category name
                { data: null, render: function (data, type, row) {       //update button ,data :null showing this column not realated to the data from response
                    return '<button class="btn btn-warning view-button-update" data-id="' + row.id + '">Update</button>';
                } },
                { data: null, render: function (data, type, row) {     // delete button
                    return '<button class="btn btn-danger view-button-delete" data-id="' + row.id + '">Delete</button>';
                } },
                
            ],
  
        });


        //functions to handle update and delete object
        $('#myTable1 tbody').on('click', '.view-button-delete', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/category_delete/' + data.id + '/'; //calling the category delete url
        });


        $('#myTable1 tbody').on('click', '.view-button-update', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/category_update/' + data.id + '/';
        });
  
  
    } else if (currentUrl === '/admin/all_products/') { //product page
  
         //console.log('vannu');
  
         var table = $('#myTable2').DataTable({
            ajax: '/product/product/', // URL to your Django view
  
            columns: [
                { data: 'name' },
                {data:'category_id'},
                {data:'brand'},
  
  // data: null tells DataTables that this column doesn't directly map to any data from the server. Instead, it's used to generate custom content for each cell in this column.
  
  // render: function (data, type, row) is a function that defines how the content for each cell in this column should be generated.
  
  // Inside the render function, it's creating an HTML button element with the class "btn btn-primary" and a custom data attribute "data-id" which stores the value of row.id. This button is created dynamically for each row in the DataTable.
  
  // The purpose of this configuration is to display a "Delete" button in each row of the DataTable. When the user clicks this button, the code you previously provided handles the click event and redirects the user to a URL for deleting the corresponding data item based on the data.id value.
  
  
                { data: null, render: function (data, type, row) {     
                    return '<button class="btn btn-warning view-button-update" data-id="' + row.id + '">Update</button>';
                } },
                { data: null, render: function (data, type, row) {     
                    return '<button class="btn btn-danger view-button-delete" data-id="' + row.id + '">Delete</button>';
                } },
                
            ],
  
        });
    
  
  
  $('#myTable2 tbody').on('click', '.view-button-delete', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/product_delete/' + data.id + '/';
        });


        $('#myTable2 tbody').on('click', '.view-button-update', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/product_update/' + data.id + '/';
        });
  
    
    } else if ( currentUrl === '/admin/all_variants/'){ //variant function

        //check root url there is a button to delete the object
  
         console.log('vannu');
  
         var table = $('#myTable3').DataTable({
            ajax: '/product/variant/', // URL to your Django view
  
            columns: [
                { data: 'name' },
                {data:'product_id'},
                {data:'ram'},
                {data:'storage'},
                {data:'color'},
                {data:'mr_price'},
                {data:'selling_price'},
  

                { data: null, render: function (data, type, row) {     
                    return '<button class="btn btn-warning view-button-update" data-id="' + row.id + '">Update</button>';
                } },
                { data: null, render: function (data, type, row) {     
                    return '<button class="btn btn-danger view-button-delete" data-id="' + row.id + '">Delete</button>';
                } },
                
            ],
  
        });
    
  
  
  $('#myTable3 tbody').on('click', '.view-button-delete', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/variant_delete/' + data.id + '/';
        });


        $('#myTable3 tbody').on('click', '.view-button-update', function () {
            var data = table.row($(this).parents('tr')).data();
            // Redirect to the URL with the object ID (data.id)
            window.location.href = '/admin/variant_update/' + data.id + '/';
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
  var customClassName = 'table_custom';
  
  // List of div IDs
  var tableIds = ['myTable1', 'myTable2', 'myTable3'];
  
  // Wait for the document to fully load before applying the class
  document.addEventListener('DOMContentLoaded', function () {
    // Apply the .table_custom class to each div
    for (var i = 0; i < tableIds.length; i++) {
      applyCustomStyleToDiv(tableIds[i], customClassName);
    }
  });
  


    
