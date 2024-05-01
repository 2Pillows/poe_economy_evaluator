import React, { useState, useEffect } from "react";
import axios from "axios";

import "./awakened-leveling.css";

const Awakened_Leveling = () => {
  const [divine, setDivine] = useState(0);
  const [gem_data, setGemData] = useState([]);
  const [gem_margins, setGemMargins] = useState({});
  const [gemcutter, setGemcutter] = useState(0);
  const [wild_brambleback, setWildBrambleback] = useState(0);

  // Function to fetch data from the API
  const fetchData = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/awakened_leveling"
      );

      // populate all data from api
      setDivine(response.data.divine);
      setGemData(response.data.gem_data);
      setGemMargins(response.data.gem_margins);
      setGemcutter(response.data.gemcutter);
      setWildBrambleback(response.data.wild_brambleback);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // Function to handle input change and update divine state
  const handleInputChange = (event) => {
    const value = parseFloat(event.target.value); // Parsing input value to integer
    setGemcutter(isNaN(value) ? 0 : value); // Set to 0 if NaN
    createPost(value); // Trigger createPost function on input change
  };

  // Function to create a new post
  const createPost = async (divineValue) => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/awakened_leveling",
        {
          gemcutter: divineValue, // Send the updated divine value
        }
      );
      setGemMargins(response.data.gem_margins);
    } catch (error) {
      console.error("Error creating post:", error);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchData();
  }, []);

  const gemValueChange = (event) => {};

  const displayGemMargins = (gem_margins) => {
    // Convert gem_margins object to an array of [key, value] pairs
    const gemMarginsArray = Object.entries(gem_margins);

    // Sort the gem margins array based on profit in descending order
    gemMarginsArray.sort(([keyA, valueA], [keyB, valueB]) => {
      return valueB.profit - valueA.profit;
    });

    let buyLink = "buy";
    let sellLink = "sell";

    const gemTable = gemMarginsArray
      .filter(([key, value]) => value.profit > 0)
      .map(([key, value]) => (
        <tr key={key}>
          <td className="gem-id">
            <span className="gem-name">{key}</span>
            <span className="gem-links">
              ({buyLink}, {sellLink})
            </span>
          </td>

          <td className="gem-profit">
            <span className="gem-chaos">{value.profit.toFixed(0)}</span>
            <span className="price-separator">|</span>
            <span className="gem-divine">
              {(value.profit / divine).toFixed(1)}
            </span>
          </td>

          <td className="gem-buy">
            <input
              className="gem-chaos"
              type="number"
              value={value.buy.toFixed(0)}
              onChange={gemValueChange}
            ></input>
            <span className="price-separator">|</span>
            <input
              className="gem-divine"
              type="number"
              value={(value.buy / divine).toFixed(1)}
              onChange={gemValueChange}
            ></input>
          </td>

          <td className="gem-sell">
            <input
              className="gem-chaos"
              type="number"
              value={value.sell.toFixed(0)}
              onChange={gemValueChange}
            ></input>
            <span className="price-separator">|</span>
            <input
              className="gem-divine"
              type="number"
              value={(value.sell / divine).toFixed(1)}
              onChange={gemValueChange}
            ></input>
          </td>
        </tr>
      ));

    return (
      <table className="gem-table">
        <thead>
          {" "}
          <tr>
            <th class="table-name">Name</th>
            <th class="table-profit">
              <span className="column-label">Profit</span>
              <br></br>
              <span className="chaos-label">chaos</span>
              <span className="price-separator">|</span>
              <span className="divine-label">divine</span>
            </th>
            <th class="table-buy">
              <span className="column-label">Buy</span> <br></br>
              <span className="chaos-label">chaos</span>
              <span className="price-separator">|</span>
              <span className="divine-label">divine</span>
            </th>
            <th class="table-sell">
              <span className="column-label">Sell</span>
              <br></br>
              <span className="chaos-label">chaos</span>
              <span className="price-separator">|</span>
              <span className="divine-label">divine</span>
            </th>
          </tr>
        </thead>
        <tbody>{gemTable}</tbody>
      </table>
    );
  };

  return (
    <div class="content">
      <div class="heading">
        <h1 class="content-title">Awakened Leveling</h1>
      </div>
      <div class="info">
        {/* Text field to display and edit the divine value */}
        <label>Divine:</label>
        <input type="number" value={gemcutter} onChange={handleInputChange} />
        {displayGemMargins(gem_margins)}
      </div>
    </div>
  );
};

export default Awakened_Leveling;
