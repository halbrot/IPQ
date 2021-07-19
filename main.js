var layout = {
  // title:'IPQ',
  height: 600,
  xaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    title: '実施日時'
  },
  yaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    title: '温度 (℃)'
  },
  yaxis2: {
    overlaying: 'y',
    side: 'right',
    autorange: 'reversed'
    }
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
};

var labelDic = {
  carbide: '炭化物面積率 (%)',
  temperature: '最高到達温度 (℃)',
  frequency: '周波数 (Hz)',
  power: '電力 (W)',
  voltageAC: '高周波電圧 (Vrms)',
  voltageDC: '直流電圧 (V)'
};

var app = new Vue({
  el: '#app',
  data: {
    myPlot: document.getElementById("myDiv"),
    doadd: false,
    id: null,
    drawMV: null,
    path: null,
    ambfiles: null,
    ambforplot: null,
    selectedCharacter: 'temperature',
    characterList: [
      {text: '炭化物面積率', value: 'carbide'},
      {text: '最高到達温度', value: 'temperature'},
      {text: '周波数', value: 'frequency'},
      {text: 'IHヒータ出力電力値', value: 'power'},
      {text: 'IHヒータ電圧値', value: 'voltageAC'},
      {text: 'IHヒータ直流電圧値', value: 'voltageDC'}

    ],
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
      {text: '2021/7 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202107_GRW5102B0/'},
      {text: '2021/7 GRW5102(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202107_GRW5102C0/'}
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
    historyplot: function(refresh){
      //refresh: 0;再読み込みなし，1；CSVファイルを再読み込み
      this.loading = true;
      axios
        .get(`http://10.112.120.156:5000/getdata?path=${this.path}&character=${this.selectedCharacter}&refresh=${refresh}`)
        .then(response => {
          this.outer.x = response.data.datetime,
          this.outer.y = response.data.data1,
          this.inner.y = response.data.data2,
          this.inner.x = this.outer.x,
          this.outer.text = response.data.id,
          this.inner.text = this.outer.text,

          this.loading = false
          this.refresh = false,

          Plotly.newPlot('myDiv', [this.outer, this.inner], layout, config);
          this.myPlot.on("plotly_click", function(data){
            console.log(data.points[0].text);
            app.id = parseInt(data.points[0].text);
          });
        })
      axios
        .get(`http://10.112.120.156:5000/ambcheck?path=${this.path}`)
        .then(response => {
          this.ambfiles = response.data.file
        })
      },
    amb: function(){
      axios
        .get(`http://10.112.120.156:5000/ambtemp?path=${this.path}&filename=${this.ambforplot}`)
        .then(response => {
          x = response.data.time,
          yin = response.data.in,
          yout = response.data.out,
          trace1 = {x:x, y:yin, yaxis:'y2', name: 'in', mode:'lines', type:'scatter'},
          trace2 = {x:x, y:yout, yaxis:'y2', name: 'out', mode:'lines', type:'scatter'}
          Plotly.addTraces('myDiv', [trace1, trace2])
        })
      }
    },
  watch: {
    path:{
      handler: function() {
        this.historyplot(0)
      }
    },
    selectedCharacter:{
      handler: function(){
        layout.yaxis.title = labelDic[this.selectedCharacter];
        layout2.yaxis.title = labelDic[this.selectedCharacter];
        this.historyplot(0);
        
      }
    },
    id:{
      handler: function(){
        axios
          .get(`http://10.112.120.156:5000/singleplot?path=${this.path}&character=${this.selectedCharacter}&id=${this.id}`)
          .then(response => {
            this.single1.x = response.data.time,
            this.single1.y = response.data.data1,
            this.single2.y = response.data.data2,
            this.single2.x = this.single1.x,
            this.single3.x = this.single1.x,
            this.single3.y = response.data.mv,
            this.drawMV ? series = [this.single1, this.single2, this.single3] : series = [this.single1, this.single2],
            Plotly.newPlot('singlePlot', series, layout2, config)

          });
      }
    }
  }

});

