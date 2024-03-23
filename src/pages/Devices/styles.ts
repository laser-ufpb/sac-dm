import styled from "styled-components";
import {
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
} from "@mui/material";
import { theme } from "../../styles/theme";

export const Container = styled.div`
  padding: 0 16px;
`;

export const TableBox = styled.div`
  margin-top: 16px;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
`;

export const StyledTable = styled(Table)`
  &&& {
    .MuiTableCell-root {
      border-bottom: none;
    }
  }
`;

export const StyledTableHead = styled(TableHead).attrs({
  style: {
    backgroundColor: theme.black,
    borderRadius: "8px",
  },
})``;

export const StyledTableRow = styled(TableRow)``;

export const StyledTableBody = styled(TableBody)`
  .custom-row:nth-child(odd) {
    background-color: ${theme.gray900};
  }
  .custom-row:nth-child(even) {
    background-color: ${theme.blackEerie};
  }
`;

export const StyledTableCell = styled(TableCell).attrs({
  style: { color: theme.text },
})``;
