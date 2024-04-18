import { request } from "@/utils/service"
import type * as Table from "./types/table"
import axios from 'axios'
import qs from 'qs'
import { Tracing } from "trace_events";

const BASE_URL = 'http://127.0.0.1:5000';

export function getProjectNameApi(){
  console.log("getnames")
  return axios.get(`${BASE_URL}/myapi/getProjectName`)
}


export function getInterfaceDataApi(paras: Table.GetInterfaceRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getInterface`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatInterfaceDataApi(data:Table.CreateOrUpdateInterfaceRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'interfaceName':data.interfaceName,
    'interfaceMember':data.interfaceMember,
    'interfaceMethods':data.interfaceMethods,
    'demandId':data.demandId
  }
  console.log("CreatInterfaceDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createInterface`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateInterfaceDataApi(data:Table.CreateOrUpdateInterfaceRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'interfaceName':data.interfaceName,
    'interfaceMember':data.interfaceMember,
    'interfaceMethods':data.interfaceMethods,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatInterfaceDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateInterface, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateInterface`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteInterfaceDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteInterface`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
