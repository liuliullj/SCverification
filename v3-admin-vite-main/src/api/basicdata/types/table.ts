export interface GetBasicDataRequestData {
  id: string
  basicDataName: string
  basicDataExpression: string
  createTime: string
}

export interface CreateOrUpdateBasicDataRequestData{
  id?: string
  basicDataName: string
  basicDataExpression: string
}