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

  let calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    editable: false,
    selectable: true,
    events: function (fetchInfo, successCallback, failureCallback) {
      $.ajax({
        url: "/fetch_bookings",
        type: "GET",
        success: function (response) {
          successCallback(response);
        },
        error: function (xhr) {
          console.error("Error fetching bookings:", xhr.responseText);
          failureCallback(xhr);
        },
      });
    },
    dateClick: function (info) {
      let selectedDate = info.dateStr;

      $.ajax({
        url: "/block_date",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ date: selectedDate }),
        success: function (response) {
          toastr.success(response.success);
          calendar.refetchEvents();
          fetchBlockedDates();
        },
        error: function (xhr) {
          let errorMsg = xhr.responseJSON?.error || "Something went wrong!";
          toastr.error(errorMsg);
        },
      });
    },
    eventClick: function (info) {
      alert(
        "Booking ID: " +
          info.event.id +
          "\nStatus: " +
          info.event.extendedProps.status +
          "\nTotal Price: $" +
          info.event.extendedProps.total_price
      );
    },
    validRange: function (nowDate) {
      return {
        start: nowDate,
      };
    },
    datesSet: function () {
      fetchBlockedDates();
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
