import React from "react";
import spinner from "./loading.svg";
class Loading extends React.Component {
  render() {
    return <img src={spinner} alt="Loading" />;
  }
}

export default Loading;
