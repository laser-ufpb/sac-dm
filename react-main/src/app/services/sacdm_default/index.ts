import { api } from "..";

class SacDmDefault {
  async getSacDmDefault(vehicleId: number) {
    try {
      const response = await api.get("/sacdm_default", {
        params: {
          vehicle_id: vehicleId,
        },
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const sacDmDefault = new SacDmDefault();
export default sacDmDefault;
