
document.addEventListener('DOMContentLoaded', function() {
    // Select all delete buttons
    const deleteButtons = document.querySelectorAll(".delete-button");
  
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default action (navigating to the URL)
  
        const deleteUrl = this.href; // Get the URL from the href attribute
  
        const swalWithBootstrapButtons = Swal.mixin({
          customClass: {
            confirmButton: "btn btn-success",
            cancelButton: "btn btn-danger"
          },
          buttonsStyling: false
        });
  
        swalWithBootstrapButtons.fire({
          title: "Are you sure?",
          text: "You won't be able to revert this!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, delete it!",
          cancelButtonText: "No, cancel!",
          reverseButtons: true
        }).then((result) => {
          if (result.isConfirmed) {
            // Redirect to the URL if confirmed
            window.location.href = deleteUrl;
          } else if (
            result.dismiss === Swal.DismissReason.cancel
          ) {
            swalWithBootstrapButtons.fire({
              title: "Cancelled",
              icon: "error",
              timer: 3000,
            });
          }
        });
      });
    });
  });
  