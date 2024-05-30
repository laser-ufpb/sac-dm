import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 16px;
  gap: 16px;
  padding: 16px;
`;

export const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 32px;

  h1 {
    font-size: 24px;
  }

  button {
    position: absolute;
    left: 0;
  }
`;

export const AccountDetails = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  gap: 16px;

  img {
    width: 64px;
    height: 64px;
    border-radius: 50%;
  }

  h2 {
    font-size: 24px;
  }
`;

export const InfoCard = styled.div`
  display: flex;
  flex-direction: column;
  background-color: ${({ theme }) => theme.gray800};
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 8px;
  padding: 24px;
  gap: 16px;
  width: 100%;
  margin-top: 16px;

  h3 {
    margin-bottom: 8px;
  }

  div {
    display: flex;
    gap: 4px;
    padding: 8px;
    border-radius: 4px;

    strong {
      color: ${({ theme }) => theme.white};
      font-weight: 600;
    }

    p {
      color: ${({ theme }) => theme.lightGray};
      margin: 0;
    }
  }
`;

export const ExitButton = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;

  button {
    width: max-content;
    transition: background-color 0.2s;

    &:hover {
      opacity: 0.8;
    }
  }
`;
