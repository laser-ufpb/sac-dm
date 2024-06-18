import { useNavigate } from "react-router-dom";
import { isMenuItemActive } from "../../utils/isMenuItemActive";
import { Container, NavigationButton } from "./styles";
import { AirplanemodeActive, Equalizer, Person } from "@mui/icons-material";
import { Tooltip } from "@mui/material";

export const Header = () => {
  const navigate = useNavigate();
  return (
    <Container>
      <Tooltip title="Dispositivos e Veículos">
        {/* <NavigationButton
            isActive={isMenuItemActive("/dashboard")}
            onClick={() => navigate("/dashboard")}
          >
            <Dashboard />
          </NavigationButton> */}
        <NavigationButton
          className={
            isMenuItemActive("/devices") ||
            isMenuItemActive("/device") ||
            isMenuItemActive("/vehicle")
              ? "active"
              : ""
          }
          onClick={() => navigate("/devices")}
        >
          <AirplanemodeActive />
        </NavigationButton>
      </Tooltip>
      <Tooltip title="Métricas">
        <NavigationButton
          className={isMenuItemActive("/sac_dm") ? "active" : ""}
          onClick={() => navigate("/sac_dm")}
        >
          <Equalizer />
        </NavigationButton>
      </Tooltip>
      <Tooltip title="Conta">
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
      </Tooltip>
    </Container>
  );
};
