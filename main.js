var layout = {
  // title:'IPQ',
  height: 600,
  xaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    mirror: true,
    title: '実施日時',
  },
  yaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    mirror: true,
    title: '温度 (℃)'
  },
  yaxis2: {
    overlaying: 'y',
    side: 'right',
    autorange: 'reversed',
    }
  // width: 600
};


var layout2 = {
  xaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    mirror: true,
    title: '加熱時間 (s)',
  },
  yaxis: {
    tickmode: 'auto',
    ticks: 'inside',
    linewidth: 1,
    mirror: true,
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
    isPower: false,
    startSec: 10,
    endSec: 20,
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
      {text: 'IHヒータ直流電圧値', value: 'voltageDC'},
      {text: 'MV (電圧出力)', value: 'MV'}

    ],
    options: [
      {text: '2020/10', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202010/'},
      {text: '2021/1 GRT7101(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202101/'},
      {text: '2021/2', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202102/'},
      {text: '2021/3', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202103/'},
      {text: 'PID改善実験', value: 'Z:/01_研究テーマ/14_三重IH改善/03_PID改善/生データ/'},
      {text: '2021/4 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/05_量産時日光の影響/生データ/202104/'},
      {text: '2021/5 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/06_周辺温度測定/202106_GRW5102B0/'},
      {text: '2021/6 GRT7101(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/07_冷却水温度測定/202106_GRT7101C0/'},
      {text: '2021/6 GRW5102(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102C0/'},
      {text: '2021/6 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202106_GRW5102B0/'},
      {text: '2021/7 GRW5102(B0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202107_GRW5102B0/'},
      {text: '2021/7 GRW5102(C0)', value: 'Z:/01_研究テーマ/14_三重IH改善/08_生産チャート/202107_GRW5102C0/'}
    ],
    loading: false,
  },
  methods: {
    historyplot: function(refresh){
      //refresh: 0;再読み込みなし，1；CSVファイルを再読み込み
      this.loading = true;
      axios
        .get(`http://10.112.120.156:5000/getdata?path=${this.path}&character=${this.selectedCharacter}&startsec=${this.startSec}&endsec=${this.endSec}&refresh=${refresh}`)
        .then(response => {

          // オブジェクトの要素数を取得
          // 日時，id は必ず含まれており，それ以外が特性値
          // このため，特性値の数は num-2
          num = Object.keys(response.data).length;
          x = response.data.datetime;
          id = response.data.id;

          seriesname = ['外側', '内側']
          y = []
          series = []
          for(let i=0;i<num-2;i++) {
            y.push(response.data['data' + String(i)]);
            series.push({x:x, y:y[i], text:id, name:seriesname[i], mode: 'markers', type: 'scatter', marker: { size: 6 }})
          }
    
          this.loading = false;

          Plotly.newPlot('myDiv', series, layout, config);
          this.myPlot.on("plotly_click", function(data){
            console.log(data.points[0].text);
            app.id = parseInt(data.points[0].text);
          });
        })
      this.ambCheck()
    },
    ambCheck: function(){

      // ambファイルの選択をリセット
      this.ambforplot = null;
      axios
        .get(`http://10.112.120.156:5000/ambcheck?path=${this.path}`)
        .then(response => {
          this.ambfiles = response.data.file;
        })
    },
    amb: function(){
      this.loading = true;
      axios
        .get(`http://10.112.120.156:5000/ambtemp?path=${this.path}&filename=${this.ambforplot}`)
        .then(response => {
          x = response.data.time;
          yin = response.data.in;
          yout = response.data.out;
          traceIn = {x:x, y:yin, yaxis:'y2', name: 'in', mode:'lines', type:'scatter', line:{color:'blue'}, opacity: 0.5};
          traceOut = {x:x, y:yout, yaxis:'y2', name: 'out', mode:'lines', type:'scatter', line:{color:'red'}, opacity: 0.5};
          Plotly.addTraces('myDiv', [traceIn, traceOut]);
        })
      this.loading = false;
    },
    trigger: function(event) {
      if (event.keyCode === 13){
        this.historyplot(0)
      }

    },
    judgePower: function() {
      if (this.selectedCharacter === 'temperature' || this.selectedCharacter === 'carbide') {
        this.isPower = false;
      }
      else {
        this.isPower = true;
      }
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
        this.judgePower();
        
      }
    },
    id:{
      handler: function(){
        axios
          .get(`http://10.112.120.156:5000/singleplot?path=${this.path}&character=${this.selectedCharacter}&id=${this.id}`)
          .then(response => {

          // オブジェクトの要素数を取得
          // 日時，id は必ず含まれており，それ以外が特性値
          // このため，特性値の数は num-2
          num = Object.keys(response.data).length;
          x = response.data.time;
          mv = response.data.mv;

          if (num===4){
            seriesname = ['外側', '内側']
          }
          else{
            seriesname = [this.selectedCharacterl]
          }

          y = []
          series = []
          for(let i=0;i<num-2;i++) {
            y.push(response.data['data' + String(i)]);
            series.push({x:x, y:y[i], text:id, name:seriesname[i], mode: 'lines', type: 'scatter', marker: { size: 6 }})
          }

          if (this.drawMV) series.push({x:x, y:mv, text:id, name:'MV',yaxis: 'y2', mode: 'lines', type: 'scatter', marker: { size: 6 }});

          Plotly.newPlot('singlePlot', series, layout2, config)
          });
      }
    },
    ambforplot:{
      handler: function(){
        this.amb();
      }
    }
  }

});

