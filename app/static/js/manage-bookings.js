// Show modal with payment details
$("#booking_payment_modal").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var paymentId = button.data("payment-id"); // Get payment ID from button data attribute
  var paymentReferenceNo = button.data("payment-reference");
  var paymentDate = button.data("payment-date");
  var paymentMethod = button.data("payment-method");
  var paymentAmount = button.data("payment-amount");
  var paymentStatus = button.data("payment-status");

  // Set paymentId in modal data-* attribute
  $(this).data("payment-id", paymentId);

  // Populate modal fields
  $("#payment_reference_no").text(paymentReferenceNo);
  $("#payment_date").text(paymentDate);
  $("#payment_method").text(paymentMethod);
  $("#payment_amount").text(paymentAmount);
  $("#payment_status").text(paymentStatus);

  // Show edit fields
  $("#edit-section").hide();
  $("#save-changes-btn").hide();
  $("#edit-payment-btn").show();

  // Handle Edit button click
  $("#edit-payment-btn").click(function () {
    $("#edit-section").show();
    $("#save-changes-btn").show();
    $("#edit-payment-btn").hide();
  });
});

// Handle Save changes button click
$("#save-changes-btn").click(function () {
  var newAmount = $("#new_amount").val();
  var newPaymentMethod = $("#new_payment_method").val();
  var newPaymentStatus = $("#new_payment_status").val();

  // Retrieve paymentId from the modal's data-payment-id attribute
  var paymentId = $("#booking_payment_modal").data("payment-id");

  // Send the updated data to the backend via fetch
  fetch(`/edit_payment/${paymentId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      amount: newAmount,
      payment_method: newPaymentMethod,
      payment_status: newPaymentStatus,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Update the UI with the new values
        $("#payment_amount").text(newAmount);
        $("#payment_method").text(newPaymentMethod);
        $("#payment_status").text(newPaymentStatus);
        $("#booking_payment_modal").modal("hide");
        alert("Booking updated");
        window.location.reload();
      } else {
        alert("Failed to update payment");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to update payment");
    });
});

// Handle Delete Payment button click
$("#delete-payment-btn").click(function () {
  var paymentId = $("#booking_payment_modal").data("payment-id");

  if (confirm("Are you sure you want to delete this payment?")) {
    // AJAX request to delete payment
    fetch(`/delete_payment/${paymentId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Payment deleted successfully");
          $("#booking_payment_modal").modal("hide");
          window.location.reload();
        } else {
          alert("Failed to delete payment");
        }
      });
  }
});

function fetchPaymentDetails(paymentId) {
  $.ajax({
    url: `/get_payment_details/${paymentId}`,
    type: "GET",
    dataType: "json",
    success(data) {
      if (data.error) {
        showErrorMessage();
      } else {
        $("#payment_reference_no").text(data.reference_no);
        $("#payment_date").text(data.payment_date);
        $("#payment_method").text(data.payment_method);
        $("#payment_amount").text(data.amount);
        $("#payment_status").text(data.payment_status);
        $("#booking_payment_modal").attr("data-payment-id", paymentId);
        $('#booking_payment_modal').modal('show');
      }
    },
    error() {
      showErrorMessage("Failed to fetch payment details.");
    },
  });
}
function deleteBookingByAdmin(bookingId) {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        // Proceed with the API call to delete the booking
        fetch(`/delete-booking-by-admin/${bookingId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}',  // Include CSRF token if you're using Flask-WTF
          },
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              Swal.fire(
                'Deleted!',
                'The booking has been deleted.',
                'success'
              ).then(() => {
                // Optionally, reload the page or remove the booking row
                location.reload();  // Reload the page
              });
            } else {
              Swal.fire(
                'Error!',
                'There was a problem deleting the booking.',
                'error'
              );
            }
          })
          .catch(error => {
            Swal.fire(
              'Error!',
              'An unexpected error occurred.',
              'error'
            );
            console.error('Error:', error);
          });
      }
    });
  }
