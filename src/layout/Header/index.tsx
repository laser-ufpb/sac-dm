import { useNavigate } from "react-router-dom";
import { isMenuItemActive } from "../../app/utils/isMenuItemActive";
import { Container, NavigationButton } from "./styles";
import { useEffect, useState } from "react";
import { Dashboard, Devices, Equalizer } from "@mui/icons-material";

export const Header = () => {
  const [isDesktop, setIsDesktop] = useState(() => {
    return window.innerWidth > 768 ? true : false;
  });

  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setIsDesktop(true);
      } else {
        setIsDesktop(false);
      }
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return (
    <Container>
      {isDesktop ? (
        <>
          <NavigationButton
            isActive={isMenuItemActive("/dashboard")}
            onClick={() => navigate("/dashboard")}
          >
            <Dashboard />
          </NavigationButton>
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
        </>
      ) : (
        <div className="menu-mobile">MOBILE</div>
      )}
    </Container>
  );
};
