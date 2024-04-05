import styled from "styled-components";

export const Container = styled.div`
  position: relative;
  max-width: 156px;
  width: 100%;
`;

export const StyledSelect = styled.div`
  padding: 8px 16px;
  background-color: ${({ theme }) => theme.gray100};
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #e0e0e0;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  }
`;

export const StyledOptions = styled.div`
  width: 100%;
  position: absolute;
  background-color: ${({ theme }) => theme.gray100};
  display: flex;
  flex-direction: column;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 0 0 8px 8px;

  div {
    display: flex;
    align-items: center;
    padding: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: ${({ theme }) => theme.gray300};
      border-radius: 8px;
    }
  }
`;
