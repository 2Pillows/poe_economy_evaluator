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
  const [apiLevelingData, setApiLevelingData] = useState(null);
  const [apiCraftingData, setApiCraftingData] = useState(null);
  const [apiHarvestData, setApiHarvestData] = useState(null);
  const [apiInfluenceData, setApiInfluenceData] = useState(null);
  const [apiSanctumData, setApiSanctumData] = useState(null);
  const [apiLinkingData, setApiLinkingData] = useState(null);
  const [apiT17Data, setApiT17Data] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const routeData = {
          "/awakened-leveling": {
            endpoint: "http://localhost:5000/api/awakened_leveling",
            setter: setApiLevelingData,
          },
          "/chaos-res-crafting": {
            endpoint: "http://localhost:5000/api/chaos_res_crafting",
            setter: setApiCraftingData,
          },
          "/harvest-rolling": {
            endpoint: "http://localhost:5000/api/harvest_rolling",
            setter: setApiHarvestData,
          },
          "/reforge-influence": {
            endpoint: "http://localhost:5000/api/reforge_influence",
            setter: setApiInfluenceData,
          },
          "/sanctum-rewards": {
            endpoint: "http://localhost:5000/api/sanctum_rewards",
            setter: setApiSanctumData,
          },
          "/six-linking": {
            endpoint: "http://localhost:5000/api/six_linking",
            setter: setApiLinkingData,
          },
          "/t17-maps": {
            endpoint: "http://localhost:5000/api/t17_maps",
            setter: setApiT17Data,
          },
        };

        for (const [route, data] of Object.entries(routeData)) {
          const response = await axios.get(data.endpoint);
          data.setter(response.data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route exact path="/" element={<Navigation />}>
        <Route index element={<Home />} />
        <Route
          path="awakened-leveling"
          element={<Awakened_Leveling apiData={apiLevelingData} />}
        />
        <Route
          path="chaos-res-crafting"
          element={<Chaos_Res_Crafting apiData={apiCraftingData} />}
        />
        <Route
          path="harvest-rolling"
          element={<Harvest_Rolling apiData={apiHarvestData} />}
        />
        <Route
          path="reforge-influence"
          element={<Reforge_Influence apiData={apiInfluenceData} />}
        />
        <Route
          path="sanctum-rewards"
          element={<Sanctum_Rewards apiData={apiSanctumData} />}
        />
        <Route
          path="six-linking"
          element={<Six_Linking apiData={apiLinkingData} />}
        />
        <Route path="t17-maps" element={<T17_Maps apiData={apiT17Data} />} />
      </Route>
    )
  );

  if (
    !apiLevelingData ||
    !apiCraftingData ||
    !apiHarvestData ||
    !apiInfluenceData ||
    !apiSanctumData ||
    !apiLinkingData ||
    !apiT17Data
  ) {
    return <div>Loading...</div>;
  } else {
    return <RouterProvider router={router}>{router}</RouterProvider>;
  }
}

export default App;
