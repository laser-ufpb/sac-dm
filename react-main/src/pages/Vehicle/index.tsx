import { useParams } from "react-router-dom";
import { useEffect, useState, useCallback } from "react";
import { SacDmProps } from "../SacDm/types";
import { Description } from "./styles";
import { SacDmDevice } from "../SacDm/components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";
import { BackPage } from "../../components/BackPage";
import { DirectionsCarFilled } from "@mui/icons-material";
import { StatusProps, VehicleProps } from "../../types";
import sacDmService from "../../app/services/sac_dm";
import vehicleService from "../../app/services/vehicle";
import { getStatusColor } from "../../utils/getStatusColor";
import statusService from "../../app/services/status";

export const Vehicle = () => {
  const { id } = useParams();
  const numericId = Number(id);
  const [dataCount] = useState(100);

  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [vehicle, setVehicle] = useState<VehicleProps>();
  const [statusOptions, setStatusOptions] = useState<StatusProps[]>([]);

  const loadSacDm = useCallback(async () => {
    if (!numericId) return;
    try {
      const response = await sacDmService.getSacDmByFilter({
        vehicleId: numericId,
        limit: dataCount,
      });
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));

      setSacDm(formattedResponse);
    } catch (error) {
      console.error(error);
    }
  }, [numericId, dataCount]);

  const loadVehicles = useCallback(async () => {
    try {
      const response = await vehicleService.getVehicleById(numericId);
      setVehicle(response);
    } catch (error) {
      console.error(error);
    }
  }, [numericId]);

  const loadStatusOptions = async () => {
    try {
      const response = await statusService.getStatus();
      setStatusOptions(response);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadSacDm();
    loadVehicles();
    loadStatusOptions();
  }, [loadSacDm, loadVehicles]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [loadSacDm]);

  return (
    <>
      <BackPage />
      {vehicle && (
        <Description>
          <h1>
            <DirectionsCarFilled
              sx={{
                color: getStatusColor(vehicle.status_id, statusOptions),
              }}
            />
            {vehicle.model} - {vehicle.manufacturer}
          </h1>
          <p>
            Última atualização:{" "}
            {sacDm.length > 0 ? sacDm[sacDm.length - 1].timestamp : "N/A"}
          </p>
          <p>
            Ano de fabricação: {vehicle.manufacture_year} / Tipo de motor:{" "}
            {vehicle.engine_type} / Número de motores:{" "}
            {vehicle.number_of_engines}
          </p>
        </Description>
      )}

      {/* <DataCountSelect dataCount={dataCount} setDataCount={setDataCount} /> */}
      <SacDmDevice deviceId={numericId} sacDm={sacDm} />
    </>
  );
};
