import apiClient from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const createReportRequest = (payload) => apiClient.post(API_ENDPOINTS.reports, payload)
export const generateReport = (id) => apiClient.post(API_ENDPOINTS.reportGenerate(id))
export const listReportRequests = (params = {}) => apiClient.get(API_ENDPOINTS.reports, { params })

