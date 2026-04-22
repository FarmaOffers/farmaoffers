import { EcomData, PaymentInfo, ValidatorParams } from "../types/common/main";
declare class YappyPayment {
    private merchantId;
    private secretKey;
    constructor(merchantId: string, secretKey: string);
    /**
     *
     * @param paymentInfo Object with payment info.
     * @param donation If your transaction to donation, by default is false.
     * @param sandbox Sets the transaction to sandbox mode, by default is false.
     */
    getPaymentUrl(paymentInfo: PaymentInfo, donation?: boolean, sandbox?: boolean): Promise<EcomData>;
    private decodeSecret;
    validateHash(params: ValidatorParams): boolean;
}
export default YappyPayment;
//# sourceMappingURL=YappyPayment.d.ts.map