import { useNavigate } from "react-router-dom";
import { isMenuItemActive } from "../../utils/isMenuItemActive";
import { Container, NavigationButton } from "./styles";
import { Devices, Equalizer, Person } from "@mui/icons-material";

export const Header = () => {
  const navigate = useNavigate();
  return (
    <Container>
      {/* <NavigationButton
            isActive={isMenuItemActive("/dashboard")}
            onClick={() => navigate("/dashboard")}
          >
            <Dashboard />
          </NavigationButton> */}
      <NavigationButton
        className={isMenuItemActive("/devices") || isMenuItemActive("/device") ? "active" : ""}
        onClick={() => navigate("/devices")}
      >
        <Devices />
      </NavigationButton>
      <NavigationButton
        className={isMenuItemActive("/sac_dm") ? "active" : ""}
        onClick={() => navigate("/sac_dm")}
      >
        <Equalizer />
      </NavigationButton>

      <NavigationButton
        className={isMenuItemActive("/account") ? "active" : ""}
        onClick={() => navigate("/account")}
        style={{
          position: "absolute",
          right: "16px",
        }}
      >
        <Person />
      </NavigationButton>
    </Container>
  );
};
