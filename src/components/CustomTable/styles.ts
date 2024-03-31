import styled from "styled-components";
import {
  Table,
  TableHead,
  TableBody,
  TableCell,
  TableRow,
} from "@mui/material";
import { theme } from "../../styles/theme";
import { ArrowUpward } from "@mui/icons-material";

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

export const StyledTableCellHeader = styled(TableCell).attrs({
  style: {
    color: theme.text,
    fontWeight: 600,
  },
})`
  cursor: pointer;
`;

export const HeaderCell = styled.div`
  display: flex;
  padding: 16px;
  gap: 8px;

  .icons {
    display: flex;
    align-items: center;

    svg {
      width: 20px;
      height: 20px;
    }
  }

  &:hover {
    background-color: ${theme.blackEerie};
  }
`;

export const StyledTableRow = styled(TableRow)``;

export const StyledTableBody = styled(TableBody)`
  .custom-row:nth-child(odd) {
    background-color: ${theme.gray900};
    transition: background-color 0.2s;

    &:hover {
      background-color: ${theme.gray600};
    }
  }
  .custom-row:nth-child(even) {
    background-color: ${theme.blackEerie};
    transition: background-color 0.2s;

    &:hover {
      background-color: ${theme.gray600};
    }
  }
`;

export const StyledTableCell = styled(TableCell).attrs({
  style: {
    color: theme.text,
    fontWeight: 600,
    cursor: "pointer",
  },
})``;

interface ArrowProps {
  active: boolean;
  orderDirection: "asc" | "desc";
}

export const ArrowStyled = styled(ArrowUpward)<ArrowProps>`
  color: ${({ active }) => (active ? theme.primary : theme.gray800)};
  transform: ${({ active, orderDirection }) =>
    active && orderDirection === "asc" ? "rotate(180deg)" : "rotate(0deg)"};
`;
