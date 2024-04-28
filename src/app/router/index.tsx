import { Routes as AppRoutes, Navigate, Route } from "react-router-dom";
import { Home } from "../../pages/Home";
import { DeviceList } from "../../pages/DeviceList";
import { SacDm } from "../../pages/SacDm";
import { Device } from "../../pages/Device";
import AuthGuard from "./guards/authGuard";

export const Routes = () => {
  return (
    <AppRoutes>
      <Route element={<AuthGuard />}>
        <Route path="/" element={<Navigate replace to="/dashboard" />} />
        <Route path="/dashboard" element={<Home />} />
        <Route path="/devices" element={<DeviceList />} />
        <Route path="/device/:id" element={<Device />} />
        <Route path="/sac_dm" element={<SacDm />} />
      </Route>
    </AppRoutes>
  );
};
