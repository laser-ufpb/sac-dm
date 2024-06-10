import styled from "styled-components";

export const FormGroup = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  margin-bottom: 16px;

  label {
    color: ${({ theme }) => theme.text};
    margin-bottom: 8px;

    @media (max-width: 768px) {
      font-size: 14px;
    }
  }

  small {
    color: ${({ theme }) => theme.negative};
    margin-top: 8px;
    font-size: 12px;
    font-weight: 500;
  }

  .MuiCheckbox-root {
    color: ${({ theme }) => theme.lighterBlue};
  }

  .MuiCheckbox-root.Mui-checked {
    color: ${({ theme }) => theme.lighterBlue};
  }
`;
