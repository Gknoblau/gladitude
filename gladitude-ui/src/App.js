import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import topodata from "./us.json"
var topojson = require('topojson');
var MapChoropleth = require('react-d3-map-choropleth').MapChoropleth;
import unemploy from "./unemployment.json"

class App extends Component {
  render() {
    const width = 960;
    const height = 600;

    // data should be a MultiLineString
    const dataStates = topojson.mesh(topodata, topodata.objects.states, function(a, b) { return a !== b; });
    const dataCounties = topojson.feature(topodata, topodata.objects.counties).features;

    // domain
  const domain = {
    scale: 'quantize',
    domain: [0, .15],
    range: [0, 1, 2, 3, 4, 5, 6, 7, 8].map(function(i) { return "q" + i + "-9"; })
  };
  const domainValue = function(d) { return +d.rate; };
  const domainKey = function(d) {return +d.id};
  const mapKey = function(d) {return +d.id};

  const scale = 1280;
  const translate = [width / 2, height / 2];
  const projection = 'albersUsa';

    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <MapChoropleth
          width= {width}
          height= {height}
          dataPolygon= {dataCounties}
          dataMesh= {dataStates}
          scale= {scale}
          domain= {domain}
          domainData= {unemploy}
          domainValue= {domainValue}
          domainKey= {domainKey}
          mapKey = {mapKey}
          translate= {translate}
          projection= {projection}
          showGraticule= {true}
        />
      </div>
    );
  }
}

export default App;
