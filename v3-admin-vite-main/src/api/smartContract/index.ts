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


export function getSmartContractDataApi(paras: Table.GetSmartContractRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getSmartContract`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatSmartContractDataApi(data:Table.CreateOrUpdateSmartContractRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'smartContractName':data.smartContractName,
    'smartContractEntryItems':data.smartContractEntryItems,
    'demandId':data.demandId
  }
  console.log("CreatSmartContractDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createSmartContract`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateSmartContractDataApi(data:Table.CreateOrUpdateSmartContractRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'smartContractName':data.smartContractName,
    'smartContractEntryItems':data.smartContractEntryItems,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatSmartContractDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateSmartContract, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateSmartContract`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteSmartContractDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteSmartContract`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
