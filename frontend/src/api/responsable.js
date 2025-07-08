import axios from 'axios';

const BASE_URL = 'http://localhost:8000/responsable';

// Consulter le stock central
export const consulterStockCentral = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/stock`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la consultation du stock central :", error);
    return [];
  }
};

// Mettre à jour un produit (nom, prix, etc.)
export const mettreAJourProduit = async (produitId, champ, valeur) => {
  try {
    const response = await axios.put(`${BASE_URL}/produits/${produitId}`, {
      champ,
      valeur
    });
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la mise à jour du produit :", error);
    return null;
  }
};

// Obtenir toutes les demandes de réapprovisionnement
export const getDemandesReapprovisionnement = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/reapprovisionnements`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des demandes :", error);
    return [];
  }
};

// Approuver une demande
export const approuverReapprovisionnement = async (reapproId) => {
  try {
    const response = await axios.post(`${BASE_URL}/reapprovisionner/${reapproId}/approuver`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de l'approbation :", error);
    return null;
  }
};

// Refuser une demande
export const refuserReapprovisionnement = async (reapproId) => {
  try {
    const response = await axios.post(`${BASE_URL}/reapprovisionner/${reapproId}/refuser`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors du refus de la demande :", error);
    return null;
  }
};

// Supprimer une demande
export const supprimerReapprovisionnement = async (reapproId) => {
  try {
    const response = await axios.delete(`${BASE_URL}/reapprovisionner/${reapproId}`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la suppression de la demande :", error);
    return null;
  }
};

// Récupérer les produits d’un magasin spécifique
export const getProduitsParMagasin = async (magasinId) => {
  try {
    const response = await axios.get(`${BASE_URL}/magasin/${magasinId}/produits`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des produits du magasin :", error);
    return [];
  }
};

// Obtenir les alertes de rupture
export const getAlertesRupture = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/alertes-rupture`);
    return response.data;
  } catch (error) {
    console.error("Erreur lors de la récupération des alertes :", error);
    return [];
  }
};
