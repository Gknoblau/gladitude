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
      })
  };

  componentDidMount(){
    this.getData();
  };

  render() {
    if (!this.state.data) {
      return (<div> Loading data </div>);
    }

    const width = 960;
    const height = 600;

    // Createing the map
    const dataStates = topojson.mesh(topodata, topodata.objects.states, (a, b) => a !== b);
    const dataCounties = topojson.feature(topodata, topodata.objects.counties).features;


    const domain = {
      scale: 'quantize',
      domain: [-1, 1],
      range: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17].map(i => "q" + i + "-9") // Defines how many steps as well as css classes for them
    };
    const domainValue = d => d.rate;
    const domainKey = d => d.id;

    return (
      <div className="App">
        <MapChoropleth
          width={width}
          height={height}
          dataPolygon={dataCounties}
          dataMesh={dataStates}
          scale={1000}
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
      </div>
    );
  }
}

export default App;
