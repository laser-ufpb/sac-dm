import styled from "styled-components";

export const ModalContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  background-color: ${({ theme }) => theme.background};
  border-radius: 8px;
  border: 1px solid ${({ theme }) => `${theme.gray700}`};
  padding: 16px;
`;

export const ModalHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;

  padding-bottom: 8px;
  border-bottom: 1px solid ${({ theme }) => theme.gray700};

  h2 {
    font-size: 20px;
    font-weight: 500;
    color: ${({ theme }) => theme.lighterBlue};
  }
`;

export const ModalContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  margin-top: 16px;

  .small-message {
    color: ${({ theme }) => theme.gray300};
  }
`;

export const ModalFooter = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-top: 16px;
  gap: 8px;
`;
