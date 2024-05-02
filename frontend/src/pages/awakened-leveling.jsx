import React, { useState, useEffect } from "react";
import axios from "axios";

import "./awakened-leveling.css";

const Awakened_Leveling = ({ apiData }) => {
  // console.log(apiData);
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

  const gemValueChange = (event, gemName, priceType, currencyType) => {
    console.log("Gem Value Change - Event:", event.target.value);
    console.log("Gem Value Change - Gem Name:", gemName);
    console.log("Gem Value Change - Price Type:", priceType);
    console.log("Gem Value Change - Currency Type:", currencyType);

    // Copy the current gem margins to avoid mutating state directly
    const updatedGemMargins = { ...gem_margins };

    let newValue = parseFloat(event.target.value); // udpated input value
    if (currencyType == "divine") {
      newValue *= divine;
    }

    let oldValue = updatedGemMargins[gemName]["old" + priceType]
      ? updatedGemMargins[gemName]["old" + priceType]
      : newValue;
    delete updatedGemMargins[gemName]["old" + priceType];

    console.log("Gem Value Change - Event:", newValue);
    console.log("Gem Value Change - Old Price:", oldValue);
    updatedGemMargins[gemName][priceType] = newValue;

    // make ngative if buying price
    if (priceType == "buy") {
      newValue *= -1;
      oldValue *= -1;
    }

    updatedGemMargins[gemName]["profit"] -= oldValue;
    updatedGemMargins[gemName]["profit"] += newValue;

    setGemMargins(updatedGemMargins);
  };

  const handleGemInputChange = (event, gemName, priceType, currencyType) => {
    const updatedGemMargins = { ...gem_margins };

    let value = parseFloat(event.target.value); // Parsing input value to integer
    if (currencyType == "divine") {
      value *= divine;
    }
    let oldValue = updatedGemMargins[gemName][priceType];

    updatedGemMargins[gemName][priceType] = value;

    if (!updatedGemMargins[gemName]["old" + priceType]) {
      updatedGemMargins[gemName]["old" + priceType] = oldValue;
    }

    setGemMargins(updatedGemMargins);
  };

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
              value={parseFloat(value.buy.toFixed(0))}
              onChange={(event) =>
                handleGemInputChange(event, key, "buy", "chaos")
              }
              onBlur={(event) => gemValueChange(event, key, "buy", "chaos")}
            ></input>
            <span className="price-separator">|</span>
            <input
              className="gem-divine"
              type="number"
              value={parseFloat((value.buy / divine).toFixed(1))}
              onChange={(event) =>
                handleGemInputChange(event, key, "buy", "divine")
              }
              onBlur={(event) => gemValueChange(event, key, "buy", "divine")}
            ></input>
          </td>

          <td className="gem-sell">
            <input
              className="gem-chaos"
              type="number"
              value={parseFloat(value.sell.toFixed(0))}
              onChange={(event) =>
                handleGemInputChange(event, key, "sell", "chaos")
              }
              onBlur={(event) => gemValueChange(event, key, "sell", "chaos")}
            ></input>
            <span className="price-separator">|</span>
            <input
              className="gem-divine"
              type="number"
              value={parseFloat((value.sell / divine).toFixed(1))}
              onChange={(event) =>
                handleGemInputChange(event, key, "sell", "divine")
              }
              onBlur={(event) => gemValueChange(event, key, "sell", "divine")}
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

  // Function to handle input change and update divine state
  const handleOptionInputChange = (event, setter, key) => {
    const value = parseFloat(event.target.value);
    setter(isNaN(value) ? 0 : value);
    createPost(key, value);
  };

  // Function to create a new post
  const createPost = async (key, value) => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/awakened_leveling",
        {
          [key]: value,
        }
      );
      setGemMargins(response.data.gem_margins);
    } catch (error) {
      console.error("Error creating post:", error);
    }
  };

  // Define your options as an array of objects
  const options = [
    {
      label: "Divine: ",
      key: "divine",
      value: divine,
      setter: setDivine,
      onChange: handleOptionInputChange,
    },
    {
      label: "Gemcutter: ",
      key: "gemcutter",
      value: gemcutter,
      setter: setGemcutter,
      onChange: handleOptionInputChange,
    },
    {
      label: "Wild Brambeback: ",
      key: "wild_brambleback",
      value: wild_brambleback,
      setter: setWildBrambleback,

      onChange: handleOptionInputChange,
    },

    // Add more options as needed
  ];

  const displayOptions = () => {
    return (
      <div className="options-grid">
        {options.map((option, index) => (
          <div className="options" key={index}>
            <label>{option.label}</label>
            <input
              className="options-input"
              type="number"
              value={option.value}
              onChange={(event) =>
                option.onChange(event, option.setter, option.key)
              }
            />
          </div>
        ))}
      </div>
    );
  };

  // Render the options grid dynamically
  return (
    <div className="content">
      <div className="heading">
        <h1 className="content-title">Awakened Leveling</h1>
        {displayOptions()}
      </div>
      <div className="info">{displayGemMargins(gem_margins)}</div>
    </div>
  );
};

export default Awakened_Leveling;
