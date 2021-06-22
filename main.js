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
  title: 'single graph',
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
  methods: {
    historyGraph: function(){
      axios
        .get("http://10.112.120.156:5000/getdata")
        .then(response => {
          this.trace1.x = response.data.datetime,
          this.trace1.y = response.data.data1,
          this.trace2.y = response.data.data2,
          this.trace2.x = this.trace1.x,
          this.trace1.text = response.data.id,
          this.trace2.text = this.trace1.text,
          Plotly.newPlot('myDiv', [this.trace1, this.trace2], layout)
        });
    },
    singleGraph: function(){
      axios
        .get(`http://10.112.120.156:5000/singleplot?id=${this.id}`)
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
});
