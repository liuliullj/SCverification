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


export function getBasicDataDataApi(paras: Table.GetBasicDataRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getBasicData`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatBasicDataDataApi(data:Table.CreateOrUpdateBasicDataRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'basicDataName':data.basicDataName,
    'basicDataExpression':data.basicDataExpression
  }
  console.log("CreatBasicDataDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createBasicData`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateBasicDataDataApi(data:Table.CreateOrUpdateBasicDataRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'basicDataName':data.basicDataName,
    'basicDataExpression':data.basicDataExpression
  }
  console.log(param)
  // console.log("CreatBasicDataDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateBasicData, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateBasicData`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteBasicDataDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteBasicData`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
