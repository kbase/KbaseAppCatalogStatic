// I'm no fan of global namespacing like this ... but requirejs in 
// wordpress is no fun.
(function($) {
  $(document).ready(function () {
    // 'use strict';
      function adjustRowHeight(el) {
          var row = $(el);
          var maxHeight = 0;
          row.children().each(function () {
              var panel = $(this).children('.panel');
              panel.css('height', '');
              maxHeight = Math.max(maxHeight, $(panel).height());
          });
          console.log(maxHeight);
          row.children().each(function () {
              var panel = $(this).children('.panel');
              panel.height(maxHeight);
          });
      }
  
      $('.row.same-height').each(function() {adjustRowHeight($(this))});
  });
})(jQuery);