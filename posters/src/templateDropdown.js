import React from 'react';
import Loading from './loading.js'
class TemplateDropdown extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      templates: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:5000/listTemplates/", {mode:'no-cors'})
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            templates: result
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
    const { error, isLoaded, templates } = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <Loading />;
    } else {
      return (
          <div>
          <datalist id="templateList">
              {templates.map(item => (
                      <option key={item}>
                          {item}
                      </option>
                  ))}
          </datalist>
            <input autoComplete="on" list="templateList"/>
          </div>
      );
    }
  }
}

export default TemplateDropdown