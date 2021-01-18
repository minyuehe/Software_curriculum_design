$(function () {
  function submit_form(e) {
    $.getJSON(
      $SCRIPT_ROOT + "/show_remove",
      {
        now: new Date().getTime(),
      },
      function (data) {
        var color_rgba= $("#colorpalettediv").attr("value");

        var myChart = echarts.init(document.getElementById("er_pic"));
        
        myjson=data.json_str;
        var fuc = {
          color: color_rgba
        }
        myjson.series[0].itemStyle = fuc;
        console.log(myjson.series[0].itemStyle.color);
        myChart.setOption(data.json_str);
        
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


        $('#avgdegree').text(data.avg_degree);
        $('#avgpath').text(data.avg_path==999? "无穷大" : data.avg_path);
        $('#avgcluster').text(data.avg_cluster);
      }
    );
  }
  // 绑定click事件
  $("#show_remove").bind("click", submit_form);
});
