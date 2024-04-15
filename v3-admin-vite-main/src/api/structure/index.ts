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


export function getStructureDataApi(paras: Table.GetStructureRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getStructure`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function verifyStructureDataApi(data:Table.VerifyStructureRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'expectedExpression':data.expectedExpression,
    'demandId':data.demandId,
    'demandName':data.demandName
  }
  console.log("verifyStructureDataApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/verifyStructure`,
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
    'demandList':data
  }
  console.log("verifyAllDataApi     "+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/verifyAll`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

