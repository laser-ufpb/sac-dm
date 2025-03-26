import { useState, useEffect } from "react";
import { CustomModal } from "../../../../components/CustomModal";
import {
  ModalContent,
  ModalHeader,
} from "../../../../components/CustomModal/styles";

import { LogsVehicleProps } from "./types";

export const LogsVehicle = ({ open, onClose, logs }: LogsVehicleProps) => {
  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Logs do Veículo</h2>
      </ModalHeader>
      <ModalContent>
        <div style={{ maxHeight: "300px", overflowY: "auto", color: "white" }}>
          {logs.length > 0 ? (
            logs.map((log, index) => (
              <div key={index} style={{ padding: "8px 0", borderBottom: "1px solid #ddd" }}>
                {log}
              </div>
            ))
          ) : (
            <p>Nenhum log disponível.</p>
          )}
        </div>
      </ModalContent>
    </CustomModal>
  );
};
