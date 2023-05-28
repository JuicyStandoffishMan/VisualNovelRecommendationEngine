import React from 'react';
import AsyncSelect from 'react-select/async';

class DropdownSearch extends React.Component {
  loadOptions = (inputValue, callback) => {
    fetch(`http://localhost:80/php/auto_title.php?q=${inputValue}`)
      .then(response => response.json())
      .then(data => {
        const options = data.map(item => ({
          value: item.value, // Replace 'value' and 'label' with actual keys of your JSON data
          label: item.label,
        }));
        callback(options);
      })
      .catch(error => {
        console.error('Error:', error);
        callback([]);
      });
  };

  render() {
    return (
      <AsyncSelect 
        cacheOptions
        loadOptions={this.loadOptions}
        defaultOptions
      />
    );
  }
}

export default DropdownSearch;
