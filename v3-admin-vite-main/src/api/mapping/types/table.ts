export interface GetMappingRequestData {
  id?: string
  mappingName: string
  mappingInputBasicData: string
  mappingOutputBasicData: string
  demandId: string
  createTime: string
}

export interface CreateOrUpdateMappingRequestData{
  id?: string
  mappingName: string
  mappingInputBasicData: string
  mappingOutputBasicData: string
  demandId: string
}