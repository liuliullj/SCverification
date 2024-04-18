export interface GetSmartContractRequestData {
  id: string
  smartContractName: string
  smartContractEntryItems: string
  demandId: string
  createTime: string
}

export interface CreateOrUpdateSmartContractRequestData{
  id?: string
  smartContractName: string
  smartContractEntryItems: string
  demandId: string
}