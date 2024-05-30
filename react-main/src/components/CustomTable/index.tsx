import React, { useState } from "react";
import {
  StyledTable,
  StyledTableHead,
  StyledTableRow,
  StyledTableCell,
  StyledTableBody,
  HeaderCell,
  ArrowStyled,
} from "./styles";
import { CustomTableProps } from "./types";
import { CircularProgress } from "@mui/material";
export const CustomTable: React.FC<CustomTableProps> = ({
  columns,
  data,
  isLoading,
  onCellClick,
}) => {
  const [orderDirection, setOrderDirection] = useState<"asc" | "desc">("desc");
  const [orderBy, setOrderBy] = useState<string>("id");

  const handleSort = (columnId: string) => {
    const isAsc = orderBy === columnId && orderDirection === "asc";
    setOrderDirection(isAsc ? "desc" : "asc");
    setOrderBy(columnId);
  };

  const sortData = (data: any[]) => {
    if (!orderBy) return data;
    return [...data].sort((a, b) => {
      if (a[orderBy] < b[orderBy]) return orderDirection === "asc" ? -1 : 1;
      if (a[orderBy] > b[orderBy]) return orderDirection === "asc" ? 1 : -1;
      return 0;
    });
  };

  const sortedData = sortData(data);

  return (
    <StyledTable>
      <StyledTableHead>
        <StyledTableRow>
          {columns.map((column) => (
            <StyledTableCell
              key={column.id}
              onClick={() => handleSort(column.id)}
              style={{ cursor: "pointer", padding: "0" }}
            >
              <HeaderCell>
                {column.label}

                <div className="icons">
                  <ArrowStyled
                    active={orderBy === column.id}
                    orderDirection={orderDirection}
                  />
                </div>
              </HeaderCell>
            </StyledTableCell>
          ))}
        </StyledTableRow>
      </StyledTableHead>
      <StyledTableBody>
        {isLoading ? (
          <StyledTableRow>
            <StyledTableCell
              colSpan={columns.length}
              style={{ textAlign: "center" }}
            >
              <CircularProgress />
            </StyledTableCell>
          </StyledTableRow>
        ) : (
          sortedData.map((row, index) => (
            <StyledTableRow key={index} className="custom-row">
              {columns.map((column) => (
                <StyledTableCell
                  key={column.id}
                  onClick={() => onCellClick && onCellClick(row.id)}
                >
                  {row[column.id]}
                </StyledTableCell>
              ))}
            </StyledTableRow>
          ))
        )}
      </StyledTableBody>
    </StyledTable>
  );
};
