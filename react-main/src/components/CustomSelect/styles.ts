import styled from "styled-components";

export const SelectContainer = styled.div`
  position: relative;
  z-index: 1;
  width: 200px;
`;

export const StyledSelect = styled.div`
  padding: 8px 16px;
  background-color: ${({ theme }) => theme.gray700};
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: ${({ theme }) => theme.text};
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;

  &:hover {
    background-color: ${({ theme }) => theme.gray600};
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  }
`;

export const StyledOptions = styled.div`
  width: 100%;
  position: absolute;
  background-color: ${({ theme }) => theme.gray700};
  display: flex;
  flex-direction: column;
  color: ${({ theme }) => theme.text};
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 0 0 8px 8px;

  span {
    padding: 0;
    margin-right: 8px;
  }

  svg {
    color: ${({ theme }) => theme.text};
  }

  div {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    transition: background-color 0.2s;
    border-top: 1px solid ${({ theme }) => theme.gray600};

    &.selected {
      background-color: ${({ theme }) => theme.lighterBlue};
      color: ${({ theme }) => theme.text};
    }

    &:hover {
      background-color: ${({ theme }) => theme.primary};
    }

    &:last-child {
      border-radius: 0 0 8px 8px;
    }
  }
`;
