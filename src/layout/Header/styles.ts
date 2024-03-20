import styled from "styled-components";

export const Container = styled.header`
  width: 100%;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1.5px solid ${({ theme }) => theme.border};
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  padding: 0 8px;
  position: fixed;
  top: 0;
  z-index: 9;
  background-color: ${({ theme }) => theme.headerBackground};
  backdrop-filter: blur(10px);

  @media (max-width: 768px) {
    padding: 4px;
  }

  .mobile-menu {
    display: none;
    align-items: center;
    justify-content: center;

    a {
      display: none;
    }

    @media (max-width: 768px) {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;

      a {
        display: flex;

        .mobile-logo {
          display: flex;
          width: 100px;
          max-height: 30px;
          margin-bottom: 4px;
        }
      }
    }
  }

  .menu-desktop {
    height: 100%;
    display: block;

    @media (max-width: 768px) {
      display: none;
      margin-left: 8px;
    }
  }
`;

export const MenuIconBox = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
`;

export const HeaderLink = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;
