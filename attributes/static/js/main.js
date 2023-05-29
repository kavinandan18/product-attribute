import product_attributes  from "./attributes.js"

$(document).ready(function() {
  // Clear filters button
  $('#clear-filters-btn').click(function() {
    // Reset all select boxes
    $('#family-select').prop('selectedIndex', 0);
    $('#category-select').prop('selectedIndex', 0);
    $('#brand-select').prop('selectedIndex', 0);

    // Reload all products
    $.ajax({
      url: '/api/products/',
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        // clear the product-list
        $('.product-list').empty();
        // loop through the data and add each product to the product-list
        $.each(data.data, function(index, product) {
          // add product to the list
          var li = $('<li>');
          var a = $('<a>').attr('href', 'api/products/' + product.id + '/').text(product.name);
          a.css({
            'text-decoration': 'none',
            'color': '#000'
          });
          a.click(function() {
            $(this).css('color', '#4287f5');
          });
          li.append(a);
          $('.product-list').append(li);
        });
      }
    });
  });
});

const icon = document.querySelector('.mode-icon');

icon.addEventListener('click', function() {
  document.body.classList.toggle('dark-mode');
  icon.classList.toggle('bi-toggle2-off');
  icon.classList.toggle('bi-toggle2-on');
});



$(document).ready(function() {

    // Reload all products
          $.ajax({
            url: '/api/products/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
              // clear the product-list
              $('.product-list').empty();
              // loop through the data and add each product to the product-list
              $.each(data.data, function(index, product) {
                // add product to the list
                var li = $('<li>');
                var a = $('<a>').attr('href', 'api/products/' + product.id + '/').text(product.name);
                a.css({
                  'text-decoration': 'none',
                  'color': '#000'
                });
                a.click(function() {
                  $(this).css('color', '#4287f5');
                });
                li.append(a);
                $('.product-list').append(li);
              });
            }
          });

        // search products by name and ID
        $('#search-input').on('input', function() {
          var searchQuery = $(this).val().toLowerCase();
          let input = searchQuery.toLowerCase();
          let productList = $('.product-list');

          // hide all products by default
          productList.find('li').hide();

          // loop through each product and show/hide based on search query
          productList.find('li').each(function() {
            let productName = $(this).text().toLowerCase();
            let productId = $(this).find('a').attr('href').match(/\d+/)[0];
            if (productName.includes(input) || productId.includes(input)) {
              $(this).show();
            }
          });
        });
    // listen to the change event of the family-select dropdown
    $('#family-select').on('change', function() {
      // get the selected family id
      var family_id = $(this).val();
      // make an AJAX request to get the categories that belong to the selected family
      $.ajax({
        url: '/api/categories/?family=' + family_id,
        type: 'GET',
        success: function(data) {
          // clear the options of the category-select dropdown
          $('#category-select').empty();
          // add the default option
          $('#category-select').append($('<option>').text('Select Category').attr('value', ''));
          // loop through the data and add each category option to the category-select dropdown
          $.each(data.data, function(index, category) {
            $('#category-select').append($('<option>').text(category.name).attr('value', category.id));
          });
        }
      });
    });

    $('#category-select').on('change', function(){
        // get the value of the selected category from the category-select dropdown
        var category_id = $(this).val();
        // get the value of the selected family from the family-select dropdown
        var family_id = $('#family-select').val();
        // make an AJAX request to get the brands
        $.ajax({
            url: '/api/brands/?family=' + family_id + '&category=' + category_id,
            type: 'GET',
            success: function(data) {
                // clear the options of the brand-select dropdown
                $('#brand-select').empty();
                // add the default option
                $('#brand-select').append($('<option>').text('Select Brand').attr('value', ''));
                // loop through the data and add each brand option to the brand-select dropdown
                $.each(data.data, function(index, brand) {
                    $('#brand-select').append($('<option>').text(brand.name).attr('value', brand.id));
                });
            }
        });
    });
    
    
  
    // listen to the change event of the brand-select dropdown
    $('#brand-select').on('change', function() {
        // get the selected brand id
        var brand_id = $(this).val();
        // make an AJAX request to get the products that belong to the selected brand
        $.ajax({
          url: '/api/products/?brand=' + brand_id,
          type: 'GET',
          dataType: 'json',
          success: function(data) {
            // clear the product-list
            $('.product-list').empty();
            // loop through the data and add each product to the product-list
            $.each(data.data, function(index, product) {
                  var li = $('<li>');
                  var a = $('<a>').attr('href', 'api/products/' + product.id + '/').text(product.name);
                  a.css({
                    'text-decoration': 'none',
                    'color': '#000'
                  });
                  a.click(function() {
                    $(this).css('color', '#4287f5');
                  });
                  li.append(a);
                  $('.product-list').append(li);
                //}
              }); 
      
            // filter products by name and ID
            $('#search-input').on('input', function() {
              var searchQuery = $(this).val().toLowerCase();
              let input = searchQuery.toLowerCase();
              let productList = $('.product-list');
              
              // hide all products by default
              productList.find('li').hide();
              
              // loop through each product and show/hide based on search query
              productList.find('li').each(function() {
                let productName = $(this).text().toLowerCase();
                let productId = $(this).find('a').attr('href').match(/\d+/)[0];
                if (productName.includes(input) || productId.includes(input)) {
                  $(this).show();
                }
              });
            });
          }
        });
      });

        $(document).on('click', '.product-list li a', function(e) {
            e.preventDefault();
            // hide the attributes form
            $('.product-attributes-form').hide();
            var product_url = $(this).attr('href');
            // make an AJAX request to get the selected product's details
            $.ajax({
                url: product_url,
                type: 'GET',
                success: function(data) {
                    var product = data.data;
                    // set the selected product name
                    $('.selected-product-name').text(product.id + ' . '+product.name);
                    // populate the attributes form with the product's attributes
                   
                    // Get the selected product family and attributes
                    var family = product.family;
                    // console.log(family);
                    const attributes = product_attributes.filter(item => item.hasOwnProperty(family))[0];
                    console.log(attributes);
                    // Check if the family exists in the attributes list
                    var attributesForm = $('.product-attributes-form form');
                    attributesForm.empty();
                    if (attributes) {
                      // Loop through the attributes and create form fields for each
                      $.each(attributes, function(index, attribute) {
                          const formGroup = $('<div>', { 'class': 'form-group row mt-4 no-gutters' });
                  
                          // loop through subkeys of attribute
                          $.each(attribute, function(name, value) {
                              const label = $('<label>', { 'for': name, 'class': 'col-md-4 col-form-label text-md-left ms-5' }).text(name + ' ');
                              const asterisk = $('<span>', { 'class': 'required', 'style': 'color: red' }).text('*');
                              label.append(asterisk);
                              const inputCol = $('<div>', { 'class': 'col-md-6 mb-3' }); 
                              const select = $('<select>', { 'id': name, 'name': name, 'class': 'form-select category-select', 'required': 'required', 'aria-label': 'Select ' + name });
                              select.append($('<option>').text('Select ' + name).attr('value', ''));
                              $.each(value, function(index, option) {
                                  const optionElem = $('<option>', { 'value': option }).text(option);
                                  select.append(optionElem);
                              });
                              select.addClass('caret');
                              inputCol.append(select);
                              

                  
                              const deleteCol = $('<div>', { 'class': 'col-md-1 col-2' });
                              const deleteButton = $('<span>', { 'class': 'delete-btn bi bi-trash', 'style': 'color: red; font-weight: bold; cursor: pointer;' });
                              inputCol.append(select);
                              formGroup.append(label);
                              formGroup.append(inputCol);
                              deleteCol.append(deleteButton);
                              formGroup.append(deleteCol);
                              deleteButton.on('click', function() {
                                  const confirmed = confirm('Are you sure you want to delete?');
                                  if (confirmed) {
                                      // Add data-id attribute to the formGroup element
                                      formGroup.attr('data-id', attribute.id);
                  
                                      // Retrieve the id value from the clicked formGroup element
                                      var attributeId = $(this).closest('.form-group').data('id');
                                      console.log(attributeId)
                  
                                      // Send the AJAX request with the correct attributeId value in the URL
                                      $.ajax({
                                          type: 'DELETE',
                                          url: '/api/product-attributes/' + attributeId + '/',
                                          dataType: 'json',
                                          success: function(response) {
                                              var alertClass = 'alert-success';
                                              var message = response && response.message ? response.message : 'Product attribute deleted successfully.';
                                              $('.product-attributes-box').prepend('<div class="alert ' + alertClass + ' alert-dismissible" role="alert">' +
                                                  message + '</div>');
                                              setTimeout(function() {
                                                  $('.product-attributes-box .alert').remove();
                                              }, 5000); // remove after 5 seconds
                                              formGroup.remove();
                                          },
                                          error: function(xhr, status, error) {
                                              var message = xhr.responseJSON.message;
                                              var alertClass = 'alert-danger';
                                              $('.product-attributes-box').prepend('<div class="alert ' + alertClass + ' alert-dismissible" role="alert">' +
                                                  message + '</div>');
                                              setTimeout(function() {
                                                  $('.product-attributes-box .alert').remove();
                                              }, 10000); // remove after 10 seconds
                                          }
                                      });
                                  }
                              });
                          });            
                          attributesForm.append(formGroup);
                      });
                  }
                  
                    else {
                      console.log('Family does not match attributes');
                    }  
                    // show the attributes form
                    $('.product-attributes-form').show();

                    // scroll to the attributes form
                    $('html, body').animate({
                    scrollTop: $(".product-attributes-form").offset().top
                    }, 500);
        
                    // set the product ID
                    var productId = product.id;
                    // Event listener for save button
                    $('#save-button').off('click').on('click', function() {
                      var updatedAttributes = [];
                      // Loop through form inputs and add values to updatedAttributes array
                      $('.product-attributes-form form :input').each(function() {
                          var attrName = $(this).attr('name');
                          var attrValue = $(this).val();
                          updatedAttributes.push({'name': attrName, 'value': attrValue});
                      });

                      // Send AJAX request to update product attributes
                      $.ajax({
                          url: '/api/products/' + productId + '/',
                          type: 'PATCH',
                          data: JSON.stringify({ 'attributes': updatedAttributes }),
                          contentType: 'application/json',
                          dataType: 'json',
                          success: function(response) {
                              var message = response.message;
                              var alertClass = 'alert-success';
                              $('.product-attributes-box').prepend('<div class="alert ' + alertClass + ' alert-dismissible" role="alert">' +
                                  message + '</div>');
                              setTimeout(function() {
                                  $('.product-attributes-box .alert').remove();
                              }, 5000); // remove after 5 seconds
                          },
                          error: function(xhr, status, error) {
                              var message = xhr.responseJSON.message;
                              var alertClass = 'alert-danger';
                              $('.product-attributes-box').prepend('<div class="alert ' + alertClass + ' alert-dismissible" role="alert">' +
                                  message + '</div>');
                              setTimeout(function() {
                                  $('.product-attributes-box .alert').remove();
                              }, 10000); // remove after 10 seconds
                          }
                      });   
                    });

                    
                    $('#add-button').off('click').on('click', function() {
                        $('#staticBackdrop1').modal('show');
                      });
                      
                      // Event listener for save button
                      $('#AddAtt').off('click').on('click', function(e) {
                        e.preventDefault();
                        var message = "Product attribute added successfully.";
                                var alertClass = 'alert-success';
                                $('.product-attributes-box').prepend('<div class="alert ' + alertClass + ' alert-dismissible" role="alert">' +
                                    message + '</div>');
                                setTimeout(function() {
                                    $('.product-attributes-box .alert').remove();
                                }, 5000); // remove after 5 seconds
                      
                        var name = $('#name').val();
                        var value = $('#value').val();
                      
                        // Populate the fields of the other form with the values entered
                        const formGroup = $('<div>', { 'class': 'form-group row mt-4 no-gutters' });
                        const label = $('<label>', { 'for': name, 'class': 'col-md-3 col-form-label text-md-left ms-5' }).text(name + ' ');
                        const inputCol = $('<div>', { 'class': 'col-md-7' });
                        const input = $('<input>', { 'type': 'text', 'id': name, 'name': name, 'value': value, 'class': 'form-control', 'autocomplete': 'off', 'required': 'required' });
                        const deleteCol = $('<div>', { 'class': 'col-md-1' });
                        const deleteButton = $('<span>', { 'class': 'delete-btn bi bi-trash', 'style': 'color: red; font-weight: bold; cursor: pointer;' });

                        deleteButton.on('click', function() {
                        const confirmed = confirm('Are you sure you want to delete?');
                        if (confirmed) {
                            formGroup.remove();
                        }
                        });

                        inputCol.append(input);
                        deleteCol.append(deleteButton);

                        formGroup.append(label);
                        formGroup.append(inputCol);
                        formGroup.append(deleteCol);
                        $('.product-attributes-form form').append(formGroup);
                        // Clear the modal form
                        $('#name').val('');
                        $('#value').val('');
                        // Hide the modal form
                        $('#staticBackdrop1').modal('hide');
                      });             
                }.bind(this)
                
            });  
        });
  });
  
  
  