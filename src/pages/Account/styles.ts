import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
`;

export const InfoCard = styled.div`
  width: 50%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  gap: 10px;

  h1 {
    font-size: 24px;
  }

  h2 {
    font-size: 20px;
  }

  p {
    font-size: 16px;
  }
`;
