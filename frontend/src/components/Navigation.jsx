import React from "react";
import { Outlet, Link } from "react-router-dom";

const Navigation = () => {
  return (
    <div className="app">
      <div className="navigation">
        <Link to="/" className="navigation-button">
          Home
        </Link>
        <Link to="/awakened-leveling" className="navigation-button">
          Awakened Leveling
        </Link>
        <Link to="/chaos-res-crafting" className="navigation-button">
          Chaos Res Crafting
        </Link>
        <Link to="/harvest-rolling" className="navigation-button">
          Harvest Rolling
        </Link>
        <Link to="/reforge-influence" className="navigation-button">
          Reforge Influence
        </Link>
        <Link to="/sanctum-rewards" className="navigation-button">
          Sanctum Rewards
        </Link>
        <Link to="/six-linking" className="navigation-button">
          Six Linking
        </Link>
        <Link to="/t17-maps" className="navigation-button">
          T17 Maps
        </Link>
      </div>
      <Outlet />
    </div>
  );
};

export default Navigation;
