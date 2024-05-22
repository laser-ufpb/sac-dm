import styled from "styled-components";
import { theme } from "../../styles/theme";

export const Description = styled.div`
  margin: 16px 0;

  svg {
    margin-right: 8px;
  }

  p {
    color: ${theme.text};
    font-size: 16px;
    margin-top: 8px;
  }
`;

export const ChartContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
`;
