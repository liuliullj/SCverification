export interface CreateOrUpdateTableRequestData {
  id?: string
  name: string
  description: string
}

export interface GetTableRequestData {
  /** 当前页码 */
  currentPage: number
  /** 查询条数 */
  size: number
  /** 查询参数：用户名 */
  name?: string
  /** 查询参数：手机号 */
  description?: string
}

export interface GetDemandRequestData{
  projectname:string
  currentPage: number
  size: number
}

export interface GetTableData {
  createTime: string
  id: string
  description: string
  status: boolean
  name: string
}


export type GetTableResponseData = ApiResponseData<{
  list: GetTableData[]
  total: number
}>

export interface CreateOrUpdateDemandRequestData{
  id?: string
  demandname: string
  category: string
  demanddescription: string
  parentD: string
}

export interface GetPathRequestData{
  projectname: string
  currentPage: number
  size: number
}

export interface CreateOrUpdateDesignRequestData{
  id?:string
  pathname:string
  expression:string
}
