// var trace1 = {
//     x:  [896.3, 895.4, 896.7, 897.0], 
//     y:  [878.5, 877.8, 885.5, 883.7], 
//     mode: 'markers',
//     type: 'scatter',
//     name: 'Team A',
//     text: ['A-1', 'A-2', 'A-3', 'A-4'],
//     marker: { size: 12 }
//   };
  
  
var layout = {
  // xaxis: {
  //   range: [ 0.75, 5.25 ]
  // },
  // yaxis: {
  //   range: [0, 8]
  // },
  title:'IPQ',
  height: 600,
  width: 1000
};

//   data = [trace1, trace2]

  // Plotly.newPlot('myDiv', data, layout);


var app = new Vue({
  el: '#app',
  data: {
    id: null,
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
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    },
    single2: {
      x: null,
      y: null,
      mode: 'markers',
      type: 'scatter',
      marker: { size: 6 }
    }
  },
  methods: {
      historyGraph: function(){
          axios
              .get("http://10.112.120.156:5000/getdata")
              .then(response => (this.trace1.x = response.data.datetime,
                                this.trace1.y = response.data.data1,
                                this.trace2.y = response.data.data2,
                                this.trace2.x = this.trace1.x,
                                this.trace1.text = response.data.id,
                                this.trace2.text = this.trace1.text));
      },
      singleGraph: function(){
        axios
          .get(`http://10.112.120.156:5000/singleplot?id=${this.id}`)
          .then(response => (this.single1.x = response.data.time,
                            this.single1.y = response.data.data1,
                            this.single2.y = response.data.data2,
                            this.single2.x = this.single1.x));
      }
  },

  //データ読み込みに少し時間がかかるので，データが更新されたらグラフを表示する
  //https://qiita.com/smkhkc/items/d5e1bc5580a62d060516
  watch: {
    trace1: {
      handler: function(newVal, oldVal){
      Plotly.newPlot('myDiv', [this.trace1, this.trace2], layout);
      },
    deep: true,
    immediate: false
    },
    single2: {
      handler: function(newVal, oldVal){
      Plotly.newPlot('singlePlot', [this.single1, this.signle2], layout);
      },
    deep: true,
    immediate: false
    },
  }

});



