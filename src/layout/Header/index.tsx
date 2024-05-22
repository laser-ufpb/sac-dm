import { useNavigate } from "react-router-dom";
import { isMenuItemActive } from "../../app/utils/isMenuItemActive";
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
        isActive={isMenuItemActive("/devices")}
        onClick={() => navigate("/devices")}
      >
        <Devices />
      </NavigationButton>
      <NavigationButton
        isActive={isMenuItemActive("/sac_dm")}
        onClick={() => navigate("/sac_dm")}
      >
        <Equalizer />
      </NavigationButton>

      <NavigationButton
        isActive={isMenuItemActive("/account")}
        onClick={() => navigate("/account")}
        style={{
          position: "absolute",
          right: "8px",
        }}
      >
        <Person />
      </NavigationButton>
    </Container>
  );
};
