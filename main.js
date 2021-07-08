var layout = {
  // title:'IPQ',
  height: 600,
  xaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    title: '実施日時'},
    yaxis: {
      tickmode: 'auto',
      ticks: 'inside',
      linewidth: 1,
      title: '温度 (℃)'}
  
  // width: 600
};


var layout2 = {
  xaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    title: '加熱時間 (s)'},
  yaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    title: '温度 (℃)'},
  // title: 'single graph',

  yaxis2: {
    title: 'MV',
    overlaying: 'y',
    side: 'right'
  },
  height: 600,
  // width: 600
};

var config = {
  responsive: true,
  scrollZoom: true,
  autosizable: true,
  }


var app = new Vue({
  el: '#app',
  data: {
    myPlot: document.getElementById("myDiv"),
    doadd: false,
    id: null,
    path: null,
    options: [
      {text: '2020/10', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202010/'},
      {text: '2021/1 GRT7101(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202101/'},
      {text: '2021/2', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202102/'},
      {text: '2021/3', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202103/'},
      {text: '2021/4 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202104/'},
      {text: '2021/5 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/06_周辺温度測定/202106_GRW5102B0/'},
      {text: '2021/6 GRT7101(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/'},
      {text: '2021/6 GRW5102(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102C0/'},
      {text: '2021/6 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102B0/'},
      {text: '2021/7 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202107_GRW5102B0/'}

    ],
    loading: false,
    outer: {
      x: null,
      y: null,
      text : null,
      name: 'outer',
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    },
    inner: {
      x: null,
      y: null,
      text : null,
      name: 'inner',
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    },
    single1: {
      x: null,
      y: null,
      name: 'outer',
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    },
    single2: {
      x: null,
      y: null,
      name: 'inner',
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    },
    single3: {
      x: null,
      y: null,
      name: 'MV',
      yaxis: 'y2',
      mode: 'lines',
      type: 'scatter',
      marker: { size: 6 }
    }
  },
  methods: {
    dorefresh: function(){
        this.loading = true;
        axios
          .get(`http://10.112.120.156:5000/getdata?path=${this.path}&refresh=1`)
          .then(response => {
            this.outer.x = response.data.datetime,
            this.outer.y = response.data.data1,
            this.inner.y = response.data.data2,
            this.inner.x = this.outer.x,
            this.outer.text = response.data.id,
            this.inner.text = this.outer.text,

            this.loading = false
            this.refresh = false,
  
            Plotly.newPlot('myDiv', [this.outer, this.inner], layout, config)
            this.myPlot.on("plotly_click", function(data){
              console.log(data.points[0].text);
              app.id = parseInt(data.points[0].text);
            });
          })
        }
    },

  // methods: {
  //   historyGraph: function(){
  //     axios
  //       .get(`http://10.112.120.156:5000/getdata?path=${this.path}`)
  //       .then(response => {
  //         this.outer.x = response.data.datetime,
  //         this.outer.y = response.data.data1,
  //         this.inner.y = response.data.data2,
  //         this.inner.x = this.outer.x,
  //         this.outer.text = response.data.id,
  //         this.inner.text = this.outer.text,

  //         Plotly.newPlot('myDiv', [this.outer, this.inner], layout)
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
        this.loading = true;
        axios
          .get(`http://10.112.120.156:5000/getdata?path=${this.path}&refresh=0`)
          .then(response => {
            this.outer.x = response.data.datetime,
            this.outer.y = response.data.data1,
            this.inner.y = response.data.data2,
            this.inner.x = this.outer.x,
            this.outer.text = response.data.id,
            this.inner.text = this.outer.text,

            this.loading = false
  
            Plotly.newPlot('myDiv', [this.outer, this.inner], layout, config)
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
            this.single1.x = response.data.time,
            this.single1.y = response.data.data1,
            this.single2.y = response.data.data2,
            this.single2.x = this.single1.x,
            this.single3.x = this.single1.x,
            this.single3.y = response.data.mv,
            // Plotly.newPlot('singlePlot', [this.single1, this.single2, this.single3], layout2)

            this.doadd ? Plotly.addTraces('singlePlot', [this.single1, this.single2]) : Plotly.newPlot('singlePlot', [this.single1, this.single2], layout2)
          });
      }
    }
  }

});

