import React from "react";
import {
  StyledTable,
  StyledTableHead,
  StyledTableRow,
  StyledTableCell,
  StyledTableBody,
} from "./styles";
import { CustomTableProps } from "./types";
import { CircularProgress } from "@mui/material";

export const CustomTable: React.FC<CustomTableProps> = ({
  columns,
  data,
  isLoading,
}) => {
  return (
    <StyledTable>
      <StyledTableHead>
        <StyledTableRow>
          {columns.map((column) => (
            <StyledTableCell key={column.id}>{column.label}</StyledTableCell>
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
          (() => {
            const reversedData = [...data].reverse();
            return reversedData.map((row, index) => (
              <StyledTableRow key={index} className="custom-row">
                {columns.map((column) => (
                  <StyledTableCell key={column.id}>
                    {row[column.id]}
                  </StyledTableCell>
                ))}
              </StyledTableRow>
            ));
          })()
        )}
      </StyledTableBody>
    </StyledTable>
  );
};
