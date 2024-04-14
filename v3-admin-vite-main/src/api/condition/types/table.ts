export interface GetConditionRequestData {
  id?: string
  conditionName: string
  conditionBasicDataOne: string
  conditionBasicDataTwo: string
  conditionOperator: string
  demandId: string
  createTime: string
}

export interface CreateOrUpdateConditionRequestData{
  id?: string
  conditionName: string
  conditionBasicDataOne: string
  conditionBasicDataTwo: string
  conditionOperator: string
  demandId: string
}