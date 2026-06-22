import apiClient from '../api/axios.js'
import { API_ENDPOINTS } from '../api/endpoints.js'

export const requestTranscript = (payload) => apiClient.post(API_ENDPOINTS.transcripts, payload)
export const generateTranscript = (id) => apiClient.post(API_ENDPOINTS.transcriptGenerate(id))
export const listTranscripts = (params = {}) => apiClient.get(API_ENDPOINTS.transcripts, { params })

