import styled from "styled-components";

export const Container = styled.div`
  padding: 0 16px;
  margin-bottom: 40px;
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

export const DevicesList = styled.ul`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 0;
  list-style: none;
`;

export const DeviceItem = styled.li`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  border-radius: 8px;
  background-color: ${({ theme }) => theme.gray800};
  cursor: pointer;
  gap: 8px;
  transition: background-color 0.2s;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);

  &:hover {
    background-color: ${({ theme }) => theme.gray700};
  }

  > svg {
    font-size: 48px;
  }

  > h3 {
    margin-top: 8px;
    font-size: 16px;
    color: ${({ theme }) => theme.text};
  }
`;

export const NoDevicesMessage = styled.div`
  text-align: center;
  color: ${({ theme }) => theme.text};
  font-size: 24px;
  font-weight: normal;
  margin-top: 48px;
  opacity: 0.5;
`;
