import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FetchRecommendations = ({category, name, data}) => {
  const [titles, setTitles] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTitles = async () => {
      setLoading(true);
      if(data && data.length > 0) {
        let rec = data[category];
        let tempTitles = [];
        for (let i = 0; i < 25; i++) {
          const recKey = `rec_${i}`;
          if (rec[recKey]) {
            try {
              let url = "";
              if(process.env.NODE_ENV === 'development')
                url = `http://localhost:80/php/fetch_title.php?q=${rec[recKey]}`;
              else
                url = `https://vnlike.org/php/fetch_title.php?q=${rec[recKey]}`;
              const response = await fetch(url);
              if(!response.ok) throw new Error('Network response was not ok');
              const title = await response.text();
              tempTitles.push({id: i, title, vnid:rec[recKey]});
            } catch(error) {
              console.error('Error:', error);
            }
          }
        }
        setTitles(tempTitles);
      }
      setLoading(false); // when the fetching is done, set loading to false
    };

    fetchTitles();
  }, [category, data]);

  // show a loading spinner if loading is true
  if (loading) return <div className="loader"></div>

  return titles.map(({id, title, vnid}) => (
    <div key={id}>
      <a href={`https://vndb.org/v${vnid}`} target="_blank" rel="noopener noreferrer">
        {title}
      </a>
    </div>
  ));
  
};

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
  

  return (
    <div className="recommendations-container">
      <div className="recommendations-column">
        <h2>High Votes</h2>
        {data && <FetchRecommendations category={0} data={data} />}
      </div>
      <div className="recommendations-column">
        <h2>Similar Tags</h2>
        {data && <FetchRecommendations category={1} data={data} />}
      </div>
      <div className="recommendations-column">
        <h2>Combination</h2>
        {data && <FetchRecommendations category={2} data={data} />}
      </div>
    </div>


  );
};

export default Recommendation;
