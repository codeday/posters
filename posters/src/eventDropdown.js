import React from 'react';
import Loading from './loading.js'
class EventDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      events: [],
      region: ''
    };
    this.handleChange = this.handleChange.bind(this);
  }
  handleChange(event){
    this.setState({region: event.target.value})
    this.props.setRegion(event.target.value)
  }
  componentDidMount() {
    fetch("https://clear.codeday.org/api/regions/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            events: result
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }
  render() {
    const { error, isLoaded, events } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <Loading />;
    } else {
      return (
          <div>
            <form>
          <datalist id="eventList">
            {events.filter(event => event.current_event != null).map(item => (
                      <option key={item.webname}>
                          {item.name}
                      </option>
                  ))}
          </datalist>
              <input autoComplete="on"  value={this.state.region} list="eventList" onChange={this.handleChange}/>
            </form>
          </div>
      );
    }
  }

}

export default EventDropdown