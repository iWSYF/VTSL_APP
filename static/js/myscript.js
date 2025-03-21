/*glopal $, alert, console*/

$(function () {
  "use strict";

  // menu for header for mobile screen
  $("header .container .row > div:nth-of-type(1) span").click(function () {
    $("header .container .row > div ul, header .btnheader").slideToggle(500);
  });

  // the links of navbar (try it now)
  $(".linkdown").click(function () {
    $("html, body").animate(
      {
        scrollTop: $("#speechrecord").offset().top,
      },
      200
    );
  });

  // Starting function of two button record and end recording
  $("#record").click(function () {
    $(this).hide();
    $("#stop").show();
  });

  $("#stop").click(function () {
    $(this).hide();
    $("#record").show();
  });
  // End function of two button record and end recording
});
