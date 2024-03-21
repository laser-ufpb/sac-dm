import { Button } from "@mui/material";
import styled, { css } from "styled-components";

export const Container = styled.header`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1.5px solid ${({ theme }) => theme.border};
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.25);
  padding: 4px 8px;
  z-index: 9;
  background-color: ${({ theme }) => theme.headerBackground};
  backdrop-filter: blur(10px);
  margin-bottom: 16px;
  height: 100%;
`;

interface NavigationButtonProps {
  isActive?: boolean;
}

export const NavigationButton = styled(Button)<NavigationButtonProps>`
  &.MuiButtonBase-root {
    color: ${({ theme }) => theme.text};
  }

  ${({ isActive }) =>
    isActive &&
    css`
      &.MuiButtonBase-root {
        color: ${({ theme }) => theme.primary};
        background-color: ${({ theme }) => `${theme.information}23`};
      }
    `}

  svg {
    width: 32px;
    height: 32px;
  }
`;
