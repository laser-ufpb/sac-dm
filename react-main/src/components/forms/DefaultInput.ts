import styled from "styled-components";

export const DefaultInput = styled.input`
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: ${({ theme }) => theme.background};
  border: 1px solid ${({ theme }) => theme.gray700};
  color: #fff;
  font-size: 14px;
  transition: colors 0.2s ease-in-out, border-color 0.2s ease-in-out;

  &:disabled {
    cursor: not-allowed;
    opacity: 0.4;
  }

  &:focus {
    border: 1px solid ${({ theme }) => theme.lighterBlue};
    outline: 1px solid ${({ theme }) => theme.lighterBlue};
  }
`;

export const DefaultSelect = styled.select`
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: ${({ theme }) => theme.background};
  border: 1px solid ${({ theme }) => theme.gray700};
  color: #fff;
  font-size: 14px;
  transition: colors 0.2s ease-in-out, border-color 0.2s ease-in-out;

  &:disabled {
    cursor: not-allowed;
    opacity: 0.4;
  }

  &:focus {
    border: 1px solid ${({ theme }) => theme.lighterBlue};
    outline: 1px solid ${({ theme }) => theme.lighterBlue};
  }

  option {
    background-color: ${({ theme }) => theme.background};
    color: #fff;
  }
`;
