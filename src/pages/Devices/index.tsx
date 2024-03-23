import { useEffect, useState } from "react";
import DeviceService from "../../app/services/devices";
import { DeviceProps } from "./types";
import {
  Container,
  StyledTable,
  StyledTableBody,
  StyledTableCell,
  StyledTableHead,
  StyledTableRow,
  TableBox,
} from "./styles";
import { CircularProgress } from "@mui/material";
import formatDate from "../../app/utils/formatDate";

export const Devices = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [devices, setDevices] = useState<DeviceProps[]>([]);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setIsLoading(true);
    try {
      const response = await DeviceService.getDevices();
      setDevices(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <h1>Dispositivos</h1>
      <TableBox>
        <StyledTable>
          <StyledTableHead>
            <StyledTableRow>
              <StyledTableCell>ID</StyledTableCell>
              <StyledTableCell>Código do Dispositivo</StyledTableCell>
              <StyledTableCell>Última Atualização</StyledTableCell>
            </StyledTableRow>
          </StyledTableHead>
          <StyledTableBody>
            {isLoading ? (
              <CircularProgress />
            ) : (
              devices.map((device) => (
                <StyledTableRow key={device.id} className="custom-row">
                  <StyledTableCell>{device.id}</StyledTableCell>
                  <StyledTableCell>{device.device_code}</StyledTableCell>
                  <StyledTableCell>
                    {formatDate(device.timestamp)}
                  </StyledTableCell>
                </StyledTableRow>
              ))
            )}
          </StyledTableBody>
        </StyledTable>
      </TableBox>
    </Container>
  );
};
