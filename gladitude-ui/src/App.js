// Based on code from https://github.com/react-d3/react-d3-map-choropleth/blob/master/example/src/choropleth.jsx react-d3
// This file as well as us.json are also licenced under Apache 2.0
import React, {Component} from 'react';
import './App.css';
import topodata from "./us.json"
import * as topojson from 'topojson';
import {MapChoropleth} from 'react-d3-map-choropleth';
import unemploy from "./unemployment.json"

class App extends Component {
  render() {
    const width = 960;
    const height = 600;

    const dataStates = topojson.mesh(topodata, topodata.objects.states, (a, b) => a !== b);
    const dataCounties = topojson.feature(topodata, topodata.objects.counties).features;

    const domain = {
      scale: 'quantize',
      domain: [0, 0.15],
      range: [0, 1, 2, 3, 4, 5, 6, 7, 8].map(i => "q" + i + "-9")
    };
    const domainValue = d => d.rate;
    const domainKey = d => d.id;

    return (
      <div className='App'>
        <MapChoropleth
          width={width}
          height={height}
          dataPolygon={dataCounties}
          dataMesh={dataStates}
          scale={1000}
          domain={domain}
          domainData={unemploy}
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
