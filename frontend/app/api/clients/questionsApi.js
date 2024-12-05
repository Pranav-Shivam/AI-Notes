import axios from "axios";

const BASE_URL = "http://localhost:8000/api/question";

const chatbotApi = {
  updateQnA: (questionId, data) => axios.put(`${BASE_URL}/qna/update/${questionId}`, data),
  getQnA: (questionId) => axios.get(`${BASE_URL}/qna/get/${questionId}`),
  getAllQnA: () => axios.get(`${BASE_URL}/qna/get/all`),
  deleteQnA: (questionId) => axios.delete(`${BASE_URL}/qna/delete/${questionId}`),
};

export default chatbotApi;
