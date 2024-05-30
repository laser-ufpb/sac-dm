import styled from "styled-components";

export const DefaultForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;

  label {
    color: ${({ theme }) => theme.text};
  }

  .flex {
    width: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;

    @media (max-width: 768px) {
      flex-direction: column;
    }
  }

  strong {
    font-size: 16px;
    color: ${({ theme }) => theme.lighterBlue};
    font-weight: 500;
    margin: 16px 0;
  }
`;
