import { request } from "@/utils/service"
import type * as Table from "./types/table"
import axios from 'axios'
import qs from 'qs'
import { Tracing } from "trace_events";

const BASE_URL = 'http://127.0.0.1:5000';
/** 增 */
export function createTableDataApi(data: Table.CreateOrUpdateTableRequestData) {

  var param = {
    'name': data.name,
    'description': data.description
  }
  console.log(qs.stringify(param))
  // return axios.post(`${BASE_URL}/myapi/createProject`, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createProject`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
  // return request({
  //   url: "table",
  //   method: "post",
  //   data
  // })
}

/** 删 */
export function deleteTableDataApi(id: string) {
  var param = {
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteProject`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
  // return request({

  //   url: `table/${id}`,
  //   method: "delete"
  // })
}

/** 改 */
export function updateTableDataApi(data: Table.CreateOrUpdateTableRequestData) {
  var param = {
    'id': data.id,
    'name': data.name,
    'description': data.description
  }
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateProject`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
  // return request({
  //   url: "table",
  //   method: "put",
  //   data
  // })
}

/** 查 */
export function getTableDataApi(params: Table.GetTableRequestData) {
  // axios.get(`${BASE_URL}/myapi/getTableData`, { params })
  // .then(({ data }) => {
  //   console.error('yesyes');
  // })
  // .catch((error) => {
  //   // 打印错误信息
  //   console.error('请求失败lo:', error);
  // });
  console.log("show")
  console.log(params)
  var httpRequest = axios.get(`${BASE_URL}/myapi/getTableData`, { params });
  return httpRequest.then((response) => {
    console.log("###### table data api", response);
    return response.data;
  });
  // return request<Table.GetTableResponseData>({
  //   url: "table",
  //   method: "get",
  //   params
  // })
}

export function getProjectNameApi(){
  console.log("getnames")
  return axios.get(`${BASE_URL}/myapi/getProjectName`)
}


export function getDemandDataApi(paras: Table.GetDemandRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getDemandData`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatDemandDateApi(data:Table.CreateOrUpdateDemandRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'demandname':data.demandname,
    'category':data.category,
    'demanddescription':data.demanddescription,
    'parentD':data.parentD
  }
  console.log("CreatDemandDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createDemand`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function updateDemandDateApi(data:Table.CreateOrUpdateDemandRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'demandname':data.demandname,
    'category':data.category,
    'demanddescription':data.demanddescription,
    'parentD':data.parentD
  }
  console.log(param)
  // console.log("CreatDemandDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateDemand, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateDemand`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteDemandDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteDemand`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function getDesignDataApi(paras: Table.GetDemandRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getDesignData`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

export function getPathDataApi(paras:Table.GetPathRequestData){
  console.log("getpathdataapi")
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getPathData`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

export function CreatDesignDateApi(data:Table.CreateOrUpdateDesignRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'pathname':data.pathname,
    'expression':data.expression,
  }
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createDesign`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });

}


export function updateDesignDateApi(data:Table.CreateOrUpdateDesignRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'pathname':data.pathname,
    'expression':data.expression,
  }
  console.log("update!!!")
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateDesign`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });

}


export function deleteDesignDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteDesign`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
