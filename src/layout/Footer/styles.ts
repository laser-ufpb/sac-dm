import styled from "styled-components";

export const Container = styled.footer`
  width: 100%;
  background-color: ${({ theme }) => `${theme.headerBackground}dd`};
  backdrop-filter: blur(10px);

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  color: #d9d9d9;
  z-index: 999;
  position: fixed;
  bottom: 0;
  border-top: 1.5px solid ${({ theme }) => theme.border};

  small {
    font-size: 12px;
  }

  img {
    width: 100px;
  }

  a {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #d9d9d9;
    text-decoration: none;
    gap: 8px;
  }

  @media (max-width: 768px) {
    margin-top: 40px;

    small {
      font-size: 8px;
    }
  }
`;
