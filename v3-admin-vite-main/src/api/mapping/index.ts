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

export function getBasicDataInputApi(paras){
  console.log("getBasicDataInputApi")
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getBasicDataInput`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function getMappingDataApi(paras){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getMapping`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatMappingDataApi(data:Table.CreateOrUpdateMappingRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'mappingName':data.mappingName,
    'mappingInputBasicData':data.mappingInputBasicData,
    'mappingOutputBasicData':data.mappingOutputBasicData,
    'demandId':data.demandId
  }
  console.log("CreatMappingDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createMapping`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateMappingDataApi(data:Table.CreateOrUpdateMappingRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'mappingName':data.mappingName,
    'mappingInputBasicData':data.mappingInputBasicData,
    'mappingOutputBasicData':data.mappingOutputBasicData,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatMappingDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateMapping, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateMapping`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteMappingDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteMapping`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
