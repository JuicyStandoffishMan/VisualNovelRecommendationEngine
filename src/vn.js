import React, { useState } from "react";

function VNLookup() {
    const [id, setId] = useState("");
    const [title, setTitle] = useState("");
  
    const handleSubmit = async (event) => {
      event.preventDefault();
  
      // Send a POST request to your PHP script
      const response = await fetch("http://localhost:80/php/fetch_title.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `id=${id}`,
      });
  
      // Parse the response as text
      const title = await response.text();
  
      setTitle(title);
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={id}
          onChange={(event) => setId(event.target.value)}
        />
        <button type="submit">Look up VN</button>
        <p>{title}</p>
      </form>
    );
  }
  
  export default VNLookup;