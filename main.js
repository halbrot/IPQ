var layout = {
  title:'IPQ',
  height: 500,
  width: 1000
};

var layout2 = {
  // xaxis: {
  //   range: [ 0.75, 5.25 ]
  // },
  // yaxis: {
  //   range: [0, 8]
  // },
  // title: 'single graph',
  yaxis: {title: 'temperature'},
  yaxis2: {
    title: 'MV',
    overlaying: 'y',
    side: 'right'
  },
  height: 500,
  width: 800
};

var app = new Vue({
  el: '#app',
  data: {
    myPlot: document.getElementById("myDiv"),
    id: null,
    path: null,
    options: [
      {text: '2020/10', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202010/'},
      {text: '2021/1', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202101/'},
      {text: '2021/2', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202102/'},
      {text: '2021/3', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202103/'},
      {text: '2021/4', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202104/'},
      {text: '2021/6 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/06_周辺温度測定/202106_GRW5102B0/'},
      {text: '2021/6 GRT7101(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/'}
    ],
    trace1: {
      x: null,
      y: null,
      text : null,
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    },
    trace2: {
      x: null,
      y: null,
      text : null,
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    },
    single1: {
      x: null,
      y: null,
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    },
    single2: {
      x: null,
      y: null,
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    },
    single3: {
      x: null,
      y: null,
      yaxis: 'y2',
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    }
  },
  // methods: {
  //   historyGraph: function(){
  //     axios
  //       .get(`http://10.112.120.156:5000/getdata?path=${this.path}`)
  //       .then(response => {
  //         this.trace1.x = response.data.datetime,
  //         this.trace1.y = response.data.data1,
  //         this.trace2.y = response.data.data2,
  //         this.trace2.x = this.trace1.x,
  //         this.trace1.text = response.data.id,
  //         this.trace2.text = this.trace1.text,

  //         Plotly.newPlot('myDiv', [this.trace1, this.trace2], layout)
  //         this.myPlot.on("plotly_click", function(data){
  //           console.log(data.points[0].text);
  //           app.id = parseInt(data.points[0].text);
  //         });
  //       })
  //   }
    // singleGraph: function(){
    //   axios
    //     .get(`http://10.112.120.156:5000/singleplot?id=${this.id}`)
    //     .then(response => {
    //       this.single1.x = parseFloat(response.data.time),
    //       this.single1.y = response.data.data1,
    //       this.single2.y = response.data.data2,
    //       this.single2.x = this.single1.x,
    //       this.single3.x = this.single1.x,
    //       this.single3.y = response.data.mv,
    //       Plotly.newPlot('singlePlot', [this.single1, this.single2, this.single3], layout2)
    //     });
    // }
  // },
  watch: {
    path:{
      handler: function(){
        axios
          .get(`http://10.112.120.156:5000/getdata?path=${this.path}`)
          .then(response => {
            this.trace1.x = response.data.datetime,
            this.trace1.y = response.data.data1,
            this.trace2.y = response.data.data2,
            this.trace2.x = this.trace1.x,
            this.trace1.text = response.data.id,
            this.trace2.text = this.trace1.text,
  
            Plotly.newPlot('myDiv', [this.trace1, this.trace2], layout)
            this.myPlot.on("plotly_click", function(data){
              console.log(data.points[0].text);
              app.id = parseInt(data.points[0].text);
            });
          })
        }

    },
    id:{
      handler: function(){
        axios
          .get(`http://10.112.120.156:5000/singleplot?path=${this.path}&id=${this.id}`)
          .then(response => {
            this.single1.x = parseFloat(response.data.time),
            this.single1.y = response.data.data1,
            this.single2.y = response.data.data2,
            this.single2.x = this.single1.x,
            this.single3.x = this.single1.x,
            this.single3.y = response.data.mv,
            Plotly.newPlot('singlePlot', [this.single1, this.single2, this.single3], layout2)
          });
      }
    }
  }

});

