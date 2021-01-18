$(function () {
    function submit_form(e) {
      var changeIcon = function () {    
        var link = document.head.querySelector("link");
        link.href = "../static/waiting.gif";
      };
      var recoverIcon = function () {    
        var link = document.head.querySelector("link");
        link.href = "../static/ig.ico";
      };
      changeIcon();
      $("#ico").attr("src","../static/waiting.gif")
      $.getJSON(
        $SCRIPT_ROOT + "/ba_submit",
        {
          a: $('input[name="ba_nodes"]').val(),
          b: $('input[name="ba_p"]').val(),
          now: new Date().getTime(),
        },
        function (data) {
          $("#ico").attr("src","../static/image/user.png")
          recoverIcon();
          alert(data);
        }
      );
    }
    // 绑定click事件
    $("#ba_submit").bind("click", submit_form);
  });
  