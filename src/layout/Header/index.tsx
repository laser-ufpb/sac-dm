import { NavigationMenuDesktop } from "./components/NavigationMenuDesktop";
import { Container, MenuIconBox } from "./styles";
import { useEffect, useState } from "react";

export const Header = () => {
  const [isDesktop, setIsDesktop] = useState(() => {
    return window.innerWidth > 768 ? true : false;
  });

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
        <div className="menu-desktop">
          <MenuIconBox>
            <NavigationMenuDesktop />
          </MenuIconBox>
        </div>
      ) : (
        <div className="menu-mobile">MOBILE</div>
      )}
    </Container>
  );
};
