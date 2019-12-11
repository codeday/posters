import React, { useState } from 'react';
import Loading from './loading.js'
const EventDropdown = (props) => {
  const [inputValue, setInputValue] = useState('')

  function handleChange(event) {
    setInputValue(event.target.value)
    props.setRegion(event.target.value)
  }

  if (props.error) {
    return <div>Error: {props.error.message}</div>;
  } else if (props.loading) {
    return <Loading />;
  } else {
    return (
        <div>
          <form>
        <datalist id="eventList">
          {props.regions.map(item => (
            <option value={item.webname} key={item.name}>
                {item.name}
            </option>
          ))}
        </datalist>
            <input autoComplete="on"  value={inputValue} list="eventList" onChange={handleChange}/>
          </form>
        </div>
    );
  }
}

export default EventDropdown