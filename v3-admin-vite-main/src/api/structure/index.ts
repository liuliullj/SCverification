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


export function verifyStructureDataApi(data:Table.VerifyStructureRequestData[], projectname:string){

  var ids = ""
  var expectedExpressions = ""
  var demandIds = ""
  var demandNames = ""

  data.forEach(item => {
    ids = ids + item.id + ";"
    expectedExpressions = expectedExpressions + item.expectedExpression + ";"
    demandIds = demandIds + item.demandId + ";"
    demandNames = demandNames + item.demandName + ";"
  });

  var param = {
    'projectname':projectname,
    'id':ids,
    'expectedExpression':expectedExpressions,
    'demandId':demandIds,
    'demandName':demandNames
  }

  console.log("verifyStructureDataApidata:"+qs.stringify(param))

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
    url: `${BASE_URL}/myapi/verifyAllStructure`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}

