import { Routes as AppRoutes, Navigate, Route } from "react-router-dom";
import { Home } from "../../pages/Home";
import { Devices } from "../../pages/Devices";

export const Routes = () => {
  return (
    <AppRoutes>
      <Route path="/" element={<Navigate replace to="/dashboard" />} />
      <Route path="/dashboard" element={<Home />} />
      <Route path="/devices" element={<Devices />} />
    </AppRoutes>
  );
};
