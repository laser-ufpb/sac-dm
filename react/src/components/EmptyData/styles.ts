import styled from "styled-components";

export const Container = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  padding: 32px;
  transform: translate(-50%, -50%);
  width: max-content;
  border-radius: 8px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.5);
  background-color: ${({ theme }) => theme.gray800};

  p {
    font-size: 20px;
    color: #fff;
  }
`;
