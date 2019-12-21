import React, { useState } from "react";
import Select from "react-select";
import Loading from "./loading.js";

const EventDropdown = props => {
  const [inputValue, setInputValue] = useState("");

  function handleChange(newSelection) {
    setInputValue(newSelection);
    props.setRegion(newSelection.value);
  }

  if (props.error) {
    return <div>Error: {props.error.message}</div>;
  } else if (props.loading) {
    return <Loading />;
  } else {
    return (
      <div style={{zIndex: 1000, position: 'relative'}}>
        <Select
          value={inputValue}
          options={props.regions.map(item => ({value: item.webname, label: item.name}))}
          onChange={handleChange}
          />
      </div>
    );
  }
};

export default EventDropdown;
