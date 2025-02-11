$(document).ready(() => {
  const html = $("html"),
    themeIcon = $("#themeIcon"),
    theme = localStorage.getItem("theme");

  theme == "dark" ? enableDarkMode() : disableDarkMode();

  $(document).on("click", ".changeTheme", () =>
    html.attr("data-theme") == "dark" ? disableDarkMode() : enableDarkMode()
  );

  function enableDarkMode() {
    html.attr("data-theme", "dark");
    themeIcon.removeClass("bi-moon").addClass("bi-sun");
    localStorage.setItem("theme", "dark");
  }

  function disableDarkMode() {
    html.attr("data-theme", "light");
    themeIcon.removeClass("bi-sun").addClass("bi-moon");
    localStorage.setItem("theme", "light");
  }

  const sidebar = $(".sidebar"),
    activeLink = window.location.href.split("?")[0],
    menuLink = $(".menu-link").filter(function () {
      return $(this).attr("href") == activeLink;
    });

  if (menuLink.length) {
    menuLink.addClass("active-link");
    const subMenu = menuLink.closest(".sub-menu");

    if (subMenu.length)
      subMenu
        .addClass("active")
        .prev(".sub-btn")
        .find(".dropdown")
        .addClass("rotate");
  }

  $(window).resize(() => {
    if (!$("#btn-sidebar-mobile").is(":visible")) sidebar.removeClass("active");
  });

  $.ajax({
    url: "/get_user_details",
    type: "GET",
    success(response) {
      $(".sidebar .details-content p").text(response.username);
  
      // Check if the role is admin and add admin-specific navigation items
      if (response.user_role === 'admin') {
        // Add admin-specific items to the navigation
        $(".sidebar .nav_list").append(`
          <div class="navigation-item">
            <a href="/manage_bookings" class="menu-link">
              <i class="bi bi-list-check"></i>
              <span class="links_name">Manage bookings</span>
            </a>
          </div>
          <div class="navigation-item">
            <a href="{{ url_for('main.settings') }}" class="menu-link">
              <i class="bi bi-gear-fill"></i>
              <span class="links_name">Settings</span>
            </a>
          </div>
        `);
      }
  
      // Add the Logout button after all the items to ensure it's last
      $(".sidebar .nav_list").append(`
        <div class="navigation-item">
          <a href="/logout" class="menu-link">
            <i class="bi bi-door-open"></i>
            <span class="links_name">Logout</span>
          </a>
        </div>
      `);
    },
    error() {
      $(".sidebar .details-content p").text("Guest");
    },
  });
  
  

  $(document).on("click", function (event) {
    if (
      event.target.id === "btn-sidebar-mobile" ||
      event.target.id === "btn-sidebar-close"
    ) {
      sidebar.toggleClass("active");
    }
  });
let calendarEl = $("#calendar-view")[0];
let bookedDates = new Set(); // Store booked dates to prevent unblocking
let calendar = new FullCalendar.Calendar(calendarEl, {
  initialView: "dayGridMonth",
  editable: false,
  selectable: true,
  events: function (fetchInfo, successCallback, failureCallback) {
    $.ajax({
      url: "/fetch_bookings",
      type: "GET",
      success: function (response) {
        // Populate booked dates and event data
        bookedDates.clear(); // Reset stored booked dates
        response.forEach(event => {
          bookedDates.add(event.start.split("T")[0]); // Store only YYYY-MM-DD
        });
        successCallback(response); // Return events for the calendar
      },
      error: function (xhr) {
        console.error("Error fetching bookings:", xhr.responseText);
        failureCallback(xhr);
      },
    });
  },
  dateClick: function (info) {
    let selectedDate = info.dateStr;

    if (bookedDates.has(selectedDate)) {
      toastr.error("This date is already booked and cannot be blocked.");
      return; // Stop the function here
    }

    // If not booked, confirm before blocking
    Swal.fire({
      title: "Are you sure?",
      text: "Do you want to block this date?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, block it!",
      cancelButtonText: "Cancel"
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: "/block_date",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify({ date: selectedDate }),
          success: function (response) {
            toastr.success(response.success);
            calendar.refetchEvents(); // Manually refetch events after blocking
            fetchBookings();
          },
          error: function (xhr) {
            let errorMsg = xhr.responseJSON?.error || "Something went wrong!";
            toastr.error(errorMsg);
          },
        });
      }
    });
  },
  
  eventClick: function (info) {
    let eventId = info.event.extendedProps.event_id; // Get the event_id from extendedProps
    console.log(eventId);
    if (eventId) {
      window.location.href = `/booking-confirmation/${eventId}`;
    } else {
      alert("Event ID not found!");
    }
  },

  validRange: function (nowDate) {
    return {
      start: nowDate,
    };
  },

  datesSet: function () {
    fetchBlockedDates(); // Refetch blocked dates, if necessary
  },
});

calendar.render();

  function fetchBlockedDates() {
    $.ajax({
      url: "/fetch_blocked_dates",
      type: "GET",
      success: function (blockedDates) {
        $(".fc-daygrid-day").removeClass("blocked-date");
        blockedDates.forEach((blockedDate) => {
          $("td[data-date='" + blockedDate + "']").addClass("blocked-date");
        });
      },
    });
  }

  fetchBlockedDates();

  $("#bookingTable").DataTable({
    paging: true,
    searching: true,
    ordering: false,
    info: true,
    lengthMenu: [10, 25, 50, 100],
    columnDefs: [{ orderable: false, targets: 6 }],
  });

});


