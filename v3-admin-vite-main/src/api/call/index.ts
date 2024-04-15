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


export function getCallDataApi(paras: Table.GetCallRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getCall`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function verifyCallDataApi(data:Table.VerifyCallRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'pathExpression':data.pathExpression,
    'pathId':data.pathId,
    'pathName':data.pathName
  }
  console.log("verifyCallDataApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/verifyCall`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

export function verifyAllDataApi(data:string, projectname:string){
  var param = {
    'projectname':projectname,
    'pathList':data
  }
  console.log("verifyAllDataApi     "+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/verifyAllCall`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

