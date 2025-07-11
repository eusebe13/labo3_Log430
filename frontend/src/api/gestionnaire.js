import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api/v1/gestionnaire';

// Obtenir un rapport consolidé des ventes
export const getRapportConsolide = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/rapports/consolide`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération du rapport consolidé :", error.response?.data || error);
    return null;
  }
};

// Tableau de bord des performances des magasins
export const getDashboard = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/dashboard`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération du tableau de bord :", error.response?.data || error);
    return null;
  }
};

// Voir tous les rapports de tendance existants
export const getRapports = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/rapports`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des rapports :", error.response?.data || error);
    return [];
  }
};

// Générer un rapport pour une région
export const creerRapportPourRegion = async (region) => {
  try {
    const response = await axios.post(`${BASE_URL}/rapports`, { region });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la création du rapport :", error.response?.data || error);
    return null;
  }
};
