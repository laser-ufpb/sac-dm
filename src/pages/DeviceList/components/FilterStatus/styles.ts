import styled from "styled-components";

export const Container = styled.div`
  max-width: 156px;
  width: 100%;
`;

export const SelectContainer = styled.div`
  position: relative;
  z-index: 1;
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
  width: max-content;

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

  div {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    transition: background-color 0.2s;
    border-top: 1px solid ${({ theme }) => theme.gray600};

    &:hover {
      background-color: ${({ theme }) => theme.gray600};
    }

    &:last-child {
      border-radius: 0 0 8px 8px;
    }
  }
`;
