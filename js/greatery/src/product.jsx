import Websocket from 'react-websocket';

class ProductDetail extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      count: 90
    };
  };

  handleData(data) {
    let result = JSON.parse(data);
    console.log("handled data", data);
    this.setState({count: this.state.count + result.movement});
    console.log("this.state", this.state);
  };

  render() {
    console.log("ahhh react-websocket render");
    return (
      <div>
        Count: <strong>{this.state.count}</strong>

        <Websocket url="ws://localhost:8765"
                   onMessage={this.handleData} />
      </div>
    );
  }
}

export default ProductDetail;
