import axios from "axios";

const BASE_URL = "http://localhost:8000/api/chatbot";

const chatbotApi = {
  openAiChat: (data) => axios.post(`${BASE_URL}/openai`, data),
  lammaChat: (data) => axios.post(`${BASE_URL}/lamma`, data),
  gemmniChat: (data) => axios.post(`${BASE_URL}/gemmni`, data),
  databaseChat: (data) => axios.post(`${BASE_URL}/db`, data),
};

export default chatbotApi;
