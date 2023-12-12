import React, { useState } from "react";
import './Header.css';
export default function Header() {
  const [productName, setProductName] = useState("");
  const [amazonData, setAmazonData] = useState({});
  const [flipkartData, setFlipkartData] = useState({});

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/mainapp/${productName}/`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Store Amazon and Flipkart data separately
      setAmazonData(data.amazon);
      setFlipkartData(data.flipkart);

    } catch (error) {
      console.error("API Error:", error);
      // Handle errors if any
    }
  };

  return (
    <header>
      <nav>
        <div className="headings">
          <h2 className="a">Amazon</h2>
          <h2 className="f">Flipkart</h2>
        </div>
        <h1>AvF</h1>
      </nav>
      <form onSubmit={handleFormSubmit}>
        <div className="searchbar">
          <input
            type="text"
            name="search"
            id="search"
            placeholder="Enter product name to compare"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
          />
          <button type="submit">Compare</button>
        </div>
      </form>

      {/* Display Amazon and Flipkart data */}
      <div className="split-container">
        <div className="left-half">
          <p>Title: {amazonData.title}</p>
          <p>Price: {amazonData.price}</p>
          <img src={amazonData.img} alt="Amazon Product" />
        </div>
        <div className="right-half">
          <p>Title: {flipkartData.title}</p>
          <p>Price: {flipkartData.price}</p>
          <img src={flipkartData.img} alt="Flipkart Product" />
        </div>
      </div>
    </header>
  );
}
