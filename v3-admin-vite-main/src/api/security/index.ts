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


export function getSecurityDataApi(paras: Table.GetSecurityRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getSecurity`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function verifySecurityDataApi(data:Table.VerifySecurityRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'pathExpression':data.pathExpression,
    'pathId':data.pathId,
    'pathName':data.pathName
  }
  console.log("verifySecurityDataApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/verifySecurity`,
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
    url: `${BASE_URL}/myapi/verifyAllSecurity`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function uploadFileApi(data:string[], projectname:string){

  var keyvalues = ""


  data.forEach(item => {
    keyvalues = keyvalues + item + "#"
  });
  var param = {
    'projectname':projectname,
    'keyvalues':keyvalues,
  }
  console.log(keyvalues)
  console.log("uploadFileApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/uploadFileApi`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

