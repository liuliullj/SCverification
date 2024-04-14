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


export function getEntryItemDataApi(paras: Table.GetEntryItemRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getEntryItem`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatEntryItemDataApi(data:Table.CreateOrUpdateEntryItemRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'entryItemName':data.entryItemName,
    'entryItemConditions':data.entryItemConditions,
    'entryItemAgreements':data.entryItemAgreements,
    'demandId':data.demandId
  }
  console.log("CreatEntryItemDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createEntryItem`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateEntryItemDataApi(data:Table.CreateOrUpdateEntryItemRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'entryItemName':data.entryItemName,
    'entryItemConditions':data.entryItemConditions,
    'entryItemAgreements':data.entryItemAgreements,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatEntryItemDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateEntryItem, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateEntryItem`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteEntryItemDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteEntryItem`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
