import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Recommendation = (id) => {
  const [data, setData] = useState([]);
  
const handleFetchData = async () => {
    let url = "";
    console.log(id.id);
    if(process.env.NODE_ENV === 'development')
      url = "http://localhost:80/php/recs.php?q=" + id.id;
    else
      url = "https://vnlike.org/php/recs.php?q=" + id.id;
    
    const response = await fetch(url);
    const json = await response.json();
    setData(JSON.parse(json));
}

  useEffect(() => {
    handleFetchData();
  }, [id]);

  const renderRecommendations = async (category) => {
    if(data && data.length > 0)
    {
      let rec = data[category];
      let elements = [];
      for (let i = 0; i < 25; i++) {
        const recKey = `rec_${i}`;
        if (rec[recKey]) {
          try {
            const response = await fetch(`http://localhost:80/php/fetch_title.php?q=${rec[recKey]}`);
            if(!response.ok) throw new Error('Network response was not ok');
            const title = await response.text();
            elements.push(
              <div key={i}>
                {title}
              </div>
            );
          } catch(error) {
            console.error('Error:', error);
          }
        }
      }
  
      return elements;
    }
  };
  

  return (
    <div>
      <h1>Recommendations</h1>
      <div>
        <h2>Category 0</h2>
        {renderRecommendations(0)}
      </div>
      <div>
        <h2>Category 1</h2>
        {renderRecommendations(1)}
      </div>
      <div>
        <h2>Category 2</h2>
        {renderRecommendations(2)}
      </div>
    </div>
  );
};

export default Recommendation;
