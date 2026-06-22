const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export const API_ENDPOINTS = {
  login: `${API_BASE}/auth/login/`,
  refreshToken: `${API_BASE}/auth/token/refresh/`,
  me: `${API_BASE}/auth/me/`,
  approvalRequests: `${API_BASE}/approval-requests/`,
  approvalActions: `${API_BASE}/approval-actions/`,
  complaints: `${API_BASE}/complaints/`,
  complaintResolve: (id) => `${API_BASE}/complaints/${id}/resolve/`,
  reports: `${API_BASE}/reports/`,
  reportGenerate: (id) => `${API_BASE}/reports/${id}/generate/`,
  transcripts: `${API_BASE}/transcripts/`,
  transcriptGenerate: (id) => `${API_BASE}/transcripts/${id}/generate/`,
  notifications: `${API_BASE}/notifications/`,
  notificationMarkRead: (id) => `${API_BASE}/notifications/${id}/mark-read/`,
}

