import React from "react";
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

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route exact path="/" element={<Navigation />}>
      <Route index element={<Home />} />
      <Route path="awakened-leveling" element={<Awakened_Leveling />} />
      <Route path="chaos-res-crafting" element={<Chaos_Res_Crafting />} />
      <Route path="harvest-rolling" element={<Harvest_Rolling />} />
      <Route path="reforge-influence" element={<Reforge_Influence />} />
      <Route path="sanctum-rewards" element={<Sanctum_Rewards />} />
      <Route path="six-linking" element={<Six_Linking />} />
      <Route path="t17-maps" element={<T17_Maps />} />
    </Route>
  )
);

function App({ routes }) {
  return <RouterProvider router={router} />;
}

export default App;
