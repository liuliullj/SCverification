export interface GetEntryItemRequestData {
  id?: string
  entryItemName: string
  entryItemConditions: string
  entryItemAgreements: string
  demandId: string
  createTime: string
}

export interface CreateOrUpdateEntryItemRequestData{
  id?: string
  entryItemName: string
  entryItemConditions: string
  entryItemAgreements: string
  demandId: string
}