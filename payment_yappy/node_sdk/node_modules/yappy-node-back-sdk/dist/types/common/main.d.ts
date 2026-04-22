export interface PaymentInfo {
  total: number | string;
  currency?: string;
  subtotal: number | string;
  shipping?: number | string;
  discount?: number | string;
  taxes: number | string;
  sandbox?: boolean;
  donation?: boolean;
  orderId: string;
  successUrl: string;
  failUrl: string;
  tel?: string;
  domain: string;
}

export interface PagosBgUrlBody {
  total: string;
  currency?: string;
  subtotal: string;
  shipping?: string;
  discount?: string;
  taxes: string;
  orderId: string;
  successUrl: string;
  failUrl: string;
  tel?: string;
  domain: string;
}

export interface EcomProperties {
  merchantId: string;
  total: string;
  subtotal: string;
  taxes: string;
  shipping: string;
  discount: string;
  donation: YappyDonation;
  paymentDate: number;
  paymentMethod: string;
  transactionType: string;
  orderId: string;
  successUrl: string;
  failUrl: string;
  domain: string;
  jwtToken: string;
  cancelUrl: string;
  platform: string;
  signature: string;
  sbx: BgSbx;
  tel: string;
}

export interface EcomData {
  success: boolean;
  url?: string;
  error?: EcomError;
}

export interface EcomHeaders {
  "x-api-key": string;
  "Content-Type": string;
  version: string;
}

export interface PagosBgxResponse {
  success: boolean;
  accessToken?: string;
  unixTimestamp?: number;
  error?: EcomError;
}

export interface EcomError {
  code: string;
  message: string;
}

export interface ValidatorParams {
  orderId: string | undefined;
  status: YappyStatus | undefined;
  hash: string | undefined;
  domain: string | undefined;
}

export type YappyStatus = "A" | "P" | "R" | "E" | "X" | "C";
export type BgSbx = "no" | "yes";
export type YappyDonation = "no" | "yes";
