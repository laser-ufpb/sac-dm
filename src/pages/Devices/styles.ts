import styled from "styled-components";

export const Container = styled.div`
  padding: 0 16px;
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  > button {
    background-color: ${({ theme }) => theme.lighterBlue};
  }
`;

export const TableBox = styled.div`
  border-radius: 8px;
  overflow: hidden;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
`;
