// Based on code from https://github.com/react-d3/react-d3-map-choropleth/blob/master/example/src/choropleth.jsx react-d3
// This file as well as us.json are also licenced under Apache 2.0
import React, {Component} from 'react';
import './App.css';
import topodata from "./us.json"
import * as topojson from 'topojson';
import {MapChoropleth} from 'react-d3-map-choropleth';

class App extends Component {

  constructor() {
    super();

    this.state = {
      data: null
    }
  }

  getData(){
      fetch(new Request('http://gladitude.net/data'))
      .then(response => response.json())
      .then(response => {
        this.setState({
          data: response.items
        })
      });
  };

  componentDidMount(){
    this.getData();
  };

  render() {
    if (!this.state.data) {
      return (<div className="loader"></div>);
    }

    const width = 960;
    const height = 600;

    // Creating the map
    const dataStates = topojson.mesh(topodata, topodata.objects.states, (a, b) => a !== b);
    const dataCounties = topojson.feature(topodata, topodata.objects.counties).features;


    const domain = {
      scale: 'quantize',
      domain: [-1, 1],
      range: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(i => "q" + i + "-9") // Defines how many steps as well as css classes for them
    };
    const domainValue = d => d.rate;
    const domainKey = d => d.id;

    const legend = <div className="legend">
        <div>Polarity of Tweets</div>
        <div className="rates">
            <span className="negative">Negative</span>
                {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(i => <div className={`legend-box q${i}-9`}/>)}
            <span className="positive">Positive</span>
        </div>
    </div>;

    return (
      <div className="App">
        <h1>Gladitude</h1>
        <h2>Analyzing the polarity of tweets by US district</h2>
        <MapChoropleth
          width={width}
          height={height}
          dataPolygon={dataCounties}
          dataMesh={dataStates}
          scale={1200}
          domain={domain}
          domainData={this.state.data}
          domainValue={domainValue}
          domainKey={domainKey}
          mapKey={domainKey}
          translate={[width/2, height/2]}
          tooltipContent={() => {}}
          projection='albersUsa'
          legend={true}
        />
        {legend}
        <p>Colors from www.ColorBrewer.org by Cynthia A. Brewer, Geography, Pennsylvania State University.</p>
      </div>
    );
  }
}

export default App;
