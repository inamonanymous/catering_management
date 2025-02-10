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
  console.log(menuLink);
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

  $(document).on("click", function (event) {
    if (
      event.target.id === "btn-sidebar-mobile" ||
      event.target.id === "btn-sidebar-close"
    ) {
      sidebar.toggleClass("active");
    }
  });

  $("#bookingTable").DataTable({
    paging: true,
    searching: true,
    ordering: false,
    info: true,
    lengthMenu: [10, 25, 50, 100],
    columnDefs: [{ orderable: false, targets: 6 }],
  });
});
