import { Routes as AppRoutes, Navigate, Route } from "react-router-dom";
import { Home } from "../../pages/Home";
import { Devices } from "../../pages/Devices";
import { SacDm } from "../../pages/SacDm";

export const Routes = () => {
  return (
    <AppRoutes>
      <Route path="/" element={<Navigate replace to="/dashboard" />} />
      <Route path="/dashboard" element={<Home />} />
      <Route path="/devices" element={<Devices />} />
      <Route path="/sac_dm" element={<SacDm />} />
    </AppRoutes>
  );
};
