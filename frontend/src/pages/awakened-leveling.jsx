import React, { useState, useEffect } from "react";
import axios from "axios";

import "./awakened-leveling.css";

const Awakened_Leveling = ({ apiData }) => {
  console.log(apiData);
  const [divine, setDivine] = useState(apiData ? apiData.divine : 0);
  const [gem_data, setGemData] = useState(apiData ? apiData.gem_data : []);
  const [gem_margins, setGemMargins] = useState(
    apiData ? apiData.gem_margins : {}
  );
  const [gemcutter, setGemcutter] = useState(apiData ? apiData.gemcutter : 0);
  const [wild_brambleback, setWildBrambleback] = useState(
    apiData ? apiData.wild_brambleback : 0
  );

  // // Function to fetch data from the API
  // const fetchData = async () => {
  //   try {
  //     const response = await axios.get(
  //       "http://localhost:5000/api/awakened_leveling"
  //     );

  //     // populate all data from api
  //     setDivine(response.data.divine);
  //     setGemData(response.data.gem_data);
  //     setGemMargins(response.data.gem_margins);
  //     setGemcutter(response.data.gemcutter);
  //     setWildBrambleback(response.data.wild_brambleback);
  //   } catch (error) {
  //     console.error("Error fetching data:", error);
  //   }
  // };

  // // Fetch data on component mount
  // useEffect(() => {
  //   fetchData();
  // }, []);

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
          <tr>
            <th className="table-name">Name</th>
            <th className="table-profit">
              <span className="column-label">Profit</span>
              <br></br>
              <span className="chaos-label">chaos</span>
              <span className="price-separator">|</span>
              <span className="divine-label">divine</span>
            </th>
            <th className="table-buy">
              <span className="column-label">Buy</span> <br></br>
              <span className="chaos-label">chaos</span>
              <span className="price-separator">|</span>
              <span className="divine-label">divine</span>
            </th>
            <th className="table-sell">
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
    <div className="content">
      <div className="heading">
        <h1 className="content-title">Awakened Leveling</h1>
      </div>
      <div className="info">
        {/* Text field to display and edit the divine value */}
        <label>Divine:</label>
        <input type="number" value={gemcutter} onChange={handleInputChange} />
        {displayGemMargins(gem_margins)}
      </div>
    </div>
  );
};

export default Awakened_Leveling;
