export interface DeviceProps {
    open: boolean;
    onClose: () => void;
    onSubmitted: () => void;
    deviceCode: string | null;
  }
  