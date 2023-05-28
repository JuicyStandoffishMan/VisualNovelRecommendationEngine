import './App.css';
import VNLookup from './vn';
import Autocomplete from './autosuggest';
import Recommendation from './rec'; // assuming Recommendation component is in the same directory
import { useState } from 'react';

import misaki1 from './misaki/1.png';
import misaki2 from './misaki/2.png';
import misaki3 from './misaki/3.png';
import misaki4 from './misaki/4.png';
import misaki5 from './misaki/5.png';
import misaki6 from './misaki/6.png';
import misaki7 from './misaki/7.png';
import misaki8 from './misaki/8.png';
import misaki9 from './misaki/9.png';
import misaki10 from './misaki/10.png';
import misaki11 from './misaki/11.png';
import misaki12 from './misaki/12.png';

const misakiImages =
[
  misaki1,
  misaki2,
  misaki3,
  misaki4,
  misaki5,
  misaki6,
  misaki7,
  misaki8,
  misaki9,
  misaki10,
  misaki11,
  misaki12
];

const randomIndex = Math.floor(Math.random() * misakiImages.length);
const logo = misakiImages[randomIndex];

function App() {
  const [selectedTitle, setSelectedTitle] = useState('');
  const [selectedId, setSelectedId] = useState(null);

  const select_vn = (option) => {
    // Handle the selected item if it's non-null
    if (option) {
      setSelectedTitle(option.title);
      setSelectedId(option.id);
    }
  };
  return (
    <div className="App">
      <header className="App-header">
        <div className="vn_title">
          {selectedTitle && <h1>{selectedTitle}</h1>}
        </div>
      <div className="logo-container">
        <img src={logo} className="App-logo" alt="logo" />
      </div>
        <Autocomplete onSelect={select_vn}/>
        {selectedId && <Recommendation id={selectedId} />}
      </header>
    </div>
  );
}

export default App;
