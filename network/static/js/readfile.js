$(function () {
    function submit_file(e) {
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
        $SCRIPT_ROOT + "/readFile",
        {
          a: $('input[id="files"]').attr("name"),
          now: new Date().getTime(),
        },
        function (data) {
          $("#ico").attr("src","../static/image/user.png")

          var myChart = echarts.init(document.getElementById("er_pic"));
          myjson=data.json_str;
        //   var newjson; 
        //   var fuck;
        //   fuck[0]=myjson
        //   newjson.series=fuck;

          myChart.setOption(myjson);
          //myChart.setOption(newjson);

          var myChart2 = echarts.init(document.getElementById("er_degree"));
          var xdata = data.histogramtostr.slice(
            1,
            data.histogramtostr.length - 1
          );
  
          xdata = xdata.split(", ");
          var data2 = JSON.parse(JSON.stringify(xdata));
          //xdata.forEach((value,index)=>{value=index});
          for (let i = 0; i < xdata.length; i++) {
            xdata[i] = i;
          }
  
          option = {
            xAxis: {
              type: "category",
              nameLocation: "end",
              name: "度",
              data: xdata,
              nameTextStyle: {
                color: "#000",
                fontWeight: "bolder",
                fontSize: 16,
              },
              axisLabel: {
                fontWeight: "bold",
                fontSize: 12,
              },
            },
            yAxis: {
              type: "value",
              nameLocation: "end",
              name: "节点个数",
              nameTextStyle: {
                color: "#000",
                fontWeight: "bolder",
                fontSize: 16,
              },
              axisLabel: {
                fontWeight: "bold",
                fontSize: 12,
              },
            },
            series: [
              {
                data: data2,
                type: "bar",
              },
            ],
          };
  
          myChart2.setOption(option);
  
  
          $('#avgdegree').text(parseFloat(data.avg_degree).toFixed(4));
          $('#avgpath').text(data.avg_path==999? "无穷大" : parseFloat(data.avg_path).toFixed(4));
          $('#avgcluster').text(parseFloat(data.avg_cluster).toFixed(4));

          recoverIcon();
          
        }
      );
    }
    // 绑定click事件
    $("#submit").bind("click", submit_file);
  });
  