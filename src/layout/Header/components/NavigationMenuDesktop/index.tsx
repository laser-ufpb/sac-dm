import { Home } from "@mui/icons-material";
import { MenuItem } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { HeaderLink } from "../../styles";

export const NavigationMenuDesktop = () => {
  const navigate = useNavigate();

  return (
    <HeaderLink>
      <MenuItem onClick={() => navigate("/")}>
        <Home fontSize="large" />
      </MenuItem>
    </HeaderLink>
  );
};
