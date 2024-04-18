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


export function getConditionDataApi(paras: Table.GetConditionRequestData){
  console.log(paras)
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/getCondition`,
        data: qs.stringify(paras)
    }).then(function (response) {
        console.log(response);
        return response.data;
    }).catch(function (error) {
        console.log(error);
  });
}


export function CreatConditionDataApi(data:Table.CreateOrUpdateConditionRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'conditionName':data.conditionName,
    'conditionBasicDataOne':data.conditionBasicDataOne,
    'conditionBasicDataTwo':data.conditionBasicDataTwo,
    'conditionOperator':data.conditionOperator,
    'demandId':data.demandId
  }
  console.log("CreatConditionDateApi"+qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/createCondition`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}


export function updateConditionDataApi(data:Table.CreateOrUpdateConditionRequestData, projectname:string){
  var param = {
    'projectname':projectname,
    'id':data.id,
    'conditionName':data.conditionName,
    'conditionBasicDataOne':data.conditionBasicDataOne,
    'conditionBasicDataTwo':data.conditionBasicDataTwo,
    'conditionOperator':data.conditionOperator,
    'demandId':data.demandId
  }
  console.log(param)
  // console.log("CreatConditionDateApi"+qs.stringify(param))
  //return axios.post(`${BASE_URL}/myapi/updateCondition, param);
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/updateCondition`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}

export function deleteConditionDataApi(id:string, projectname:string){
  var param = {
    'projectname': projectname,
    'id': id
  }
  console.log(qs.stringify(param))
  return axios({
    method: 'post',
    url: `${BASE_URL}/myapi/deleteCondition`,
        data: qs.stringify(param)
    }).then(function (response) {
        console.log(response);
    }).catch(function (error) {
        console.log(error);
  });
}
