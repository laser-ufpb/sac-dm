import styled from "styled-components";

export const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: calc(100vh - 200px);
`;

export const FormContainer = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 12px;
  gap: 24px;

  background-color: 
  backdrop-filter: blur(10px);
  border: 1px solid ${({ theme }) => theme.gray500};
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0px 10px 15px -3px rgba(0, 0, 0, 0.9);

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
