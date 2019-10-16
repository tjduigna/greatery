import React from 'react';
import logo from './logo.svg';
import './App.css';
import ProductDetail from 'react-websocket';
import Button from '@material-ui/core/Button';
// import Websocket from 'react-websocket';

class App extends React.Component {

  doThing(data) {
      let result = JSON.parse(data);
      console.log(result);
  };

  onClick() {
      console.log("button clicked!!!");
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Button variant="contained" onClick={this.onClick}> Hello World </Button>
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        Hello world!!
        <ProductDetail url="ws://localhost:8765"
                       onMessage={this.doThing} />
        </header>
      </div>
    );
  }
}

export default App;
