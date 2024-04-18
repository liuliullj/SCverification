export interface GetAgreementRequestData {
  id: string
  agreementName: string
  agreementInterfaces: string
  demandId: string
  createTime: string
}

export interface CreateOrUpdateAgreementRequestData{
  id?: string
  agreementName: string
  agreementInterfaces: string
  demandId: string
}