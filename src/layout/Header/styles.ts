import { Button } from "@mui/material";
import styled, { css } from "styled-components";

export const Container = styled.header`
  width: 100%;
  display: flex;
  align-items: center;
  border-bottom: 1.5px solid ${({ theme }) => theme.border};
  box-shadow: 0px 2px 4px ${({ theme }) => theme.blackEerie};
  padding: 4px 16px;
  z-index: 9;
  background-color: ${({ theme }) => theme.headerBackground};
  backdrop-filter: blur(10px);
  margin-bottom: 24px;
  height: 80px;
  gap: 8px;
`;

interface NavigationButtonProps {
  isActive?: boolean;
}

export const NavigationButton = styled(Button) <NavigationButtonProps>`

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
    height: 36px;
    width: 36px;
    margin: 8px;
  }
`;
