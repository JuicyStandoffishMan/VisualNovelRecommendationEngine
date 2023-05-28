import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const Autocomplete = ({ onSelect }) => {
  const [inputValue, setInputValue] = useState('');
  const [dropdownOptions, setDropdownOptions] = useState([]);
  const [isDropdownVisible, setIsDropdownVisible] = useState(false);
  const [activeOptionIndex, setActiveOptionIndex] = useState(-1);
  const [isChangeEnabled, setChangeEnabled] = useState(true);
  const optionRefs = useRef([]);
  const inputRef = useRef(null); // Create reference to the input element
  const [delayedQuery, setDelayedQuery] = useState(''); // State to handle delayed queries
  const timeoutId = useRef(null); // Reference to store timeout ID

  useEffect(() => {
    if (delayedQuery && isChangeEnabled) {
      let url = "";
      if(process.env.NODE_ENV === 'development')
        url = `http://localhost:80/php/auto_title.php?q=${delayedQuery}`;
      else
        url = `https://vnlike.org/php/auto_title.php?q=${delayedQuery}`;
      axios.get(url)
        .then((response) => {
          setDropdownOptions(response.data);
          setIsDropdownVisible(true);
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    } else if (isChangeEnabled) {
      setDropdownOptions([]);
      setIsDropdownVisible(false);
    }
    setChangeEnabled(true);
  }, [delayedQuery]);

  const handleInputChange = (event) => {
    if(isChangeEnabled)
    {
      setInputValue(event.target.value);
      setActiveOptionIndex(-1);

      // Cancel old timeout
      clearTimeout(timeoutId.current);

      // Start new timeout
      timeoutId.current = setTimeout(() => {
        setDelayedQuery(event.target.value);
      }, 500);
    }
    setChangeEnabled(true);
  };

  const handleOptionClick = (option) => {
    setInputValue(option.title + " (" + option.id + ")");
    setIsDropdownVisible(false);
    // Call onSelect if it's not null
    if (onSelect) {
      onSelect(option);
    }
  };

  const selectOption = (option) => {
    setInputValue(option.title + " (" + option.id + ")");
    setIsDropdownVisible(false);
    // Call onSelect if it's not null
    if (onSelect) {
      onSelect(option);
    }
  };

  useEffect(() => {
    if (optionRefs.current[activeOptionIndex]) {
      optionRefs.current[activeOptionIndex].scrollIntoView({
        behavior: "instant",
        block: "nearest"
      });
    }
  }, [activeOptionIndex]);

  const handleKeyDown = (event) => {
    let index = 0;
    switch(event.key) {
      case 'ArrowDown':
        index = Math.max(0, Math.min(activeOptionIndex + 1, dropdownOptions.length - 1));
        if(dropdownOptions.length > 0)
        {
          setChangeEnabled(false);
          setActiveOptionIndex(index);
          setInputValue(dropdownOptions[index].title + " (" + dropdownOptions[index].id + ")");
        }
        break;
      case 'ArrowUp':
        index = Math.max(0, Math.min(activeOptionIndex - 1, dropdownOptions.length - 1));
        if(dropdownOptions.length > 0)
        {
          setChangeEnabled(false);
          setActiveOptionIndex(index);
          setInputValue(dropdownOptions[index].title + " (" + dropdownOptions[index].id + ")");
        }
        break;
      case 'Enter':
        index = Math.max(0, Math.min(activeOptionIndex, dropdownOptions.length - 1));
        if (isDropdownVisible && index < dropdownOptions.length && dropdownOptions[index]) {
          selectOption(dropdownOptions[index]);
          inputRef.current.blur(); // Lose focus when enter is pressed
        }
        break;
      default:
        break;
    }
  };

  return (
    <div style={{position: 'relative'}}>
      <input 
        ref={inputRef}
        type="text" 
        placeholder='Enter a VN name or ID' 
        value={inputValue} 
        className="search-class" 
        onChange={handleInputChange} 
        onKeyDown={handleKeyDown}
        autoFocus
      />
      {isDropdownVisible && dropdownOptions.length > 0 && (
        <div className='search-container'>
          {dropdownOptions.map((option, index) => (
            <div 
            ref={(el) => optionRefs.current[index] = el}
            className={`search-option ${index === activeOptionIndex ? 'active' : ''}`}
              key={index} 
              onClick={() => handleOptionClick(option)}
            >
              {option.title + " (" + option.id + ")"}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Autocomplete;
