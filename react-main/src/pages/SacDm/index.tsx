import { useCallback, useEffect, useState } from "react";
import { SacDmProps } from "./types";
import { VehicleProps } from "../../types";
import { Container } from "./styles";
import vehicleService from "../../app/services/vehicle";
import sacDmService from "../../app/services/sac_dm";
import SacDmDevice from "./components/SacDmDevice";
import { formatTime } from "../../utils/formatTime";
import { CustomSelect } from "../../components/CustomSelect";

export const SacDm = () => {
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);
  const [selectedVehicleId, setSelectedVehicleId] = useState<number | null>(1);
  const [vehicles, setVehicles] = useState<VehicleProps[]>([]);
  const [dataCount] = useState(100);

  const loadVehicles = useCallback(async () => {
    try {
      const response = await vehicleService.getVehicles();
      setVehicles(response);
      const vehicleIds = response.map((vehicle: VehicleProps) => vehicle.id);
      if (!vehicleIds.includes(selectedVehicleId) && response.length > 0) {
        setSelectedVehicleId(response[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  }, [selectedVehicleId]);

  const loadSacDm = useCallback(async () => {
    if (selectedVehicleId === null) return;
    try {
      const response = await sacDmService.getSacDmByFilter({
        vehicleId: selectedVehicleId,
        limit: dataCount,
      });
      const formattedResponse = response.map((item: SacDmProps) => ({
        ...item,
        timestamp: formatTime(item.timestamp),
      }));

      if (JSON.stringify(sacDm) !== JSON.stringify(formattedResponse)) {
        setSacDm(formattedResponse);
      }
    } catch (error) {
      console.error(error);
    }
  }, [selectedVehicleId, dataCount, sacDm]);

  useEffect(() => {
    loadVehicles();
    loadSacDm();
  }, [loadVehicles, loadSacDm]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      loadSacDm();
    }, 5000);

    return () => clearInterval(intervalId);
  }, [loadSacDm]);

  return (
    <>
      <Container>
        <CustomSelect
          label="Selecionar Veículo"
          options={vehicles.map((vehicle) => ({
            id: vehicle.id,
            description: `${vehicle.manufacturer} ${vehicle.model}`,
          }))}
          selectedOption={selectedVehicleId}
          setSelectedOption={setSelectedVehicleId}
        />
      </Container>

      {/* <DataCountSelect dataCount={dataCount} setDataCount={setDataCount} /> */}
      {selectedVehicleId && (
        <SacDmDevice
          key={selectedVehicleId}
          deviceId={selectedVehicleId}
          sacDm={sacDm}
        />
      )}
    </>
  );
};
