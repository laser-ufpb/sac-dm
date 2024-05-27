import styled from "styled-components";

export const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  gap: 24px;

  padding: 24px;

  .flex {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 8px;
  }

  @media (max-width: 768px) {
    padding: 16px;
  }
`;

export const HeaderContent = styled.div`
  margin-bottom: 8px;
  text-align: center;
  display: flex;
  align-items: center;
  flex-direction: column;

  h2 {
    font-size: 24px;
    color: ${({ theme }) => theme.text};
    margin-bottom: 8px;
  }

  @media (max-width: 768px) {
    img {
      width: 150px;
    }
  }
`;
