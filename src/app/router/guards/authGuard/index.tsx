import { useContext } from "react";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../../../contexts/AuthContext";

export default function AuthGuard() {
  const { user, showLoginModal } = useContext(AuthContext);

  if (!user) {
    showLoginModal();
    return null;
  }

  return <Outlet />;
}
