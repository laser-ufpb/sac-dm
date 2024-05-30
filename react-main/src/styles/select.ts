import styled from "styled-components";

export const SelectContainer = styled.div`
  margin-bottom: 20px;

  label {
    margin-right: 10px;
  }

  select {
    padding: 8px 16px;
    border-radius: 8px;
    background-color: #616161;
    color: #e0e0e0;
    cursor: pointer;
    border: none;
    transition: background-color 0.3s;

    &:focus-visible {
      outline: none;
    }
  }
`;
