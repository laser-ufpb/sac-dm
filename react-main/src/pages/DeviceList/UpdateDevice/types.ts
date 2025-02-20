export interface UpdateDeviceProps {
    open: boolean;
    onClose: () => void;
    onSubmitted: () => void;
    deviceCode: string | null;
  }
  