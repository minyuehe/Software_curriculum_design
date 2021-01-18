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
      $SCRIPT_ROOT + "/ws_submit",
      {
        a: $('input[name="ws_nodes"]').val(),
        b: $('input[name="ws_nodes2"]').val(),
        c: $('input[name="ws_p"]').val(),
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
  $("#ws_submit").bind("click", submit_form);
});
