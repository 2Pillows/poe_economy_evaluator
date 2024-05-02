// App.js

import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import Navigation from "./components/Navigation";
import Home from "./pages/home";
import Awakened_Leveling from "./pages/awakened-leveling";
import Chaos_Res_Crafting from "./pages/chaos-res-crafting";
import Harvest_Rolling from "./pages/harvest-rolling";
import Reforge_Influence from "./pages/reforge-influence";
import Sanctum_Rewards from "./pages/sanctum-rewards";
import Six_Linking from "./pages/six-linking";
import T17_Maps from "./pages/t17-maps";
import "./App.css";

function App({ routes }) {
  const [apiData, setApiData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/awakened_leveling"
        );
        setApiData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  if (!apiData) {
    return <div>Loading...</div>;
  } else {
    const router = createBrowserRouter(
      createRoutesFromElements(
        <Route exact path="/" element={<Navigation />}>
          <Route index element={<Home />} />
          <Route
            path="awakened-leveling"
            element={<Awakened_Leveling apiData={apiData} />}
          />
          <Route path="chaos-res-crafting" element={<Chaos_Res_Crafting />} />
          <Route path="harvest-rolling" element={<Harvest_Rolling />} />
          <Route path="reforge-influence" element={<Reforge_Influence />} />
          <Route path="sanctum-rewards" element={<Sanctum_Rewards />} />
          <Route path="six-linking" element={<Six_Linking />} />
          <Route path="t17-maps" element={<T17_Maps />} />
        </Route>
      )
    );

    return <RouterProvider router={router}>{router}</RouterProvider>;
  }
}

export default App;
