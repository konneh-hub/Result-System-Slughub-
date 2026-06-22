import apiClient from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const createComplaint = (payload) => apiClient.post(API_ENDPOINTS.complaints, payload)
export const resolveComplaint = (id, payload) => apiClient.post(API_ENDPOINTS.complaintResolve(id), payload)
export const listComplaints = (params = {}) => apiClient.get(API_ENDPOINTS.complaints, { params })

