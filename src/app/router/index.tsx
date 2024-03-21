import { Routes as AppRoutes, Route } from "react-router-dom";
import { Home } from "../../pages/Home";

export const Routes = () => {
  return (
    <AppRoutes>
      <Route path="/dashboard" element={<Home />} />
    </AppRoutes>
  );
};
