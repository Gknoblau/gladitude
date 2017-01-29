/**
 * Created by anjueappen on 1/28/17.
 */
import React, {Component} from "react"
import logo from './logo.svg';

var SearchBar = require('react-search-bar').SearchBar;

class HeaderBar extends Component{

    render(){

        return (<div>
            <div className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <h2>Welcome to React</h2>
                {/*<SearchBar  onChange={(input, resolve) => {*/}
                    {/*// get suggestions based on `input`, then pass them to `resolve()`*/}
                {/*}} />*/}
            </div>
            <p className="App-intro">
                To get started, edit <code>src/App.js</code> and save to reload.
            </p>
        </div>);
    }
}

export default HeaderBar;