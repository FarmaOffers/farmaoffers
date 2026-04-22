import { PaymentInfo, EcomData, PagosBgxResponse } from "../types/common/main";
declare class BgFirma {
    private total;
    private merchantId;
    private currency;
    private subtotal;
    private taxes;
    private shipping;
    private discount;
    private donation;
    private paymentDate;
    private paymentMethod;
    private transactionType;
    private orderId;
    private successUrl;
    private failUrl;
    private domain;
    private secretToken;
    private sandbox;
    private ssl;
    private jwtToken;
    private tel;
    constructor(data: PaymentInfo, merchantId: string, secretToken: string, jwt: string, timeStamp: number);
    /**
     *
     * @param merchantId Client merchant ID
     * @param secretKey Client secretKey aka secretToken
     * @param domain  The domain of your shop.
     * @returns asynchronously if the checking was succesfull.
     * @description Check if the shop (client) meets the requirements to execute this sdk.
     */
    static checkCredentials(merchantId: string, secretKey: string, domain: string): Promise<PagosBgxResponse>;
    /**
     *
     * @param secretKey  Your Secret Key (base64).
     * @description Decodes the secretToken into a readable string.
     * @returns An array with secret strings.
     */
    private static decodeSecret;
    private validateNumbers;
    private parseNumericValues;
    /**
     * @description Creates the signature
     * @returns url to redirect to minisitio and complete the order
     */
    createHash(): EcomData;
    /**
     * @description Validates if the domain is secure or not
     */
    private isSecure;
    /**
     * @description Create the string for the signature
     * @returns  string for the signature
     */
    private concatElements;
    /**
     *@abstract Validates the phone number before sending it to "minisitio".
     * @param tel Phone number.
     * @returns phone number without especial character | empty string.
     */
    static validatePhone(tel: string): string;
}
export default BgFirma;
//# sourceMappingURL=BgFirma.d.ts.map